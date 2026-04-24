'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { whatsappService } from '@/lib/notifications/whatsapp'

export type ActionResponse = {
  success: boolean
  message: string
}

export async function createCase(state: ActionResponse, formData: FormData): Promise<ActionResponse> {
  const supabase = await createClient()

  const title = formData.get('title') as string
  const description = formData.get('description') as string
  const userId = formData.get('userId') as string
  const serviceId = formData.get('serviceId') as string
  const status = formData.get('status') as string

  if (!title || !userId || !serviceId) {
    return { success: false, message: 'Título, cliente e serviço são obrigatórios.' }
  }

  const { error } = await supabase
    .from('client_cases')
    .insert({
      title,
      description,
      user_id: userId,
      service_id: serviceId,
      status: status || 'pendente',
    })

  if (error) {
    return { success: false, message: `Erro ao criar processo: ${error.message}` }
  }

  revalidatePath('/dashboard/cases')
  revalidatePath('/dashboard')

  return { success: true, message: 'Processo criado com sucesso!' }
}

export async function updateCaseStatus(id: string, status: string, eventDescription?: string): Promise<ActionResponse> {
  const supabase = await createClient()

  // 1. Get case and client info for notification
  const { data: caseData, error: fetchError } = await supabase
    .from('client_cases')
    .select('title, user_id, profiles(phone, name)')
    .eq('id', id)
    .single()

  if (fetchError || !caseData) {
    return { success: false, message: 'Não foi possível localizar o processo para atualização.' }
  }

  // 2. Update the status
  const { error: updateError } = await supabase
    .from('client_cases')
    .update({ status })
    .eq('id', id)

  if (updateError) {
    return { success: false, message: `Erro ao atualizar status: ${updateError.message}` }
  }

  // 3. Create the event in case_events for the timeline
  const description = eventDescription || `O status do processo foi atualizado para ${status}.`
  const { error: eventError } = await supabase
    .from('case_events')
    .insert({
      case_id: id,
      event_description: description,
      status_label: status,
    })

  if (eventError) {
    console.error('Erro ao criar evento na timeline:', eventError)
  }

  // 4. Trigger WhatsApp Notification
  const profile = Array.isArray(caseData.profiles) ? caseData.profiles[0] : caseData.profiles
  const phone = profile?.phone
  const clientName = profile?.name || 'cliente'
  const caseTitle = caseData.title

  if (phone) {
    const message = `Olá ${clientName}! O status do seu processo "${caseTitle}" foi atualizado para: ${status.replace('_', ' ').toUpperCase()}. Você pode acompanhar os detalhes no seu portal.`

    // We trigger this in the background
    whatsappService.sendNotification(phone, message).catch(err =>
      console.error('Background WhatsApp Notification Error:', err)
    )
  }

  revalidatePath('/dashboard/cases')
  revalidatePath(`/dashboard/cases/${id}`)

  return { success: true, message: 'Status atualizado e evento registrado na timeline!' }
}

export async function addCustomCaseEvent(caseId: string, description: string, statusLabel: string): Promise<ActionResponse> {
  const supabase = await createClient()

  const { error } = await supabase
    .from('case_events')
    .insert({
      case_id: caseId,
      event_description: description,
      status_label: statusLabel,
    })

  if (error) {
    return { success: false, message: `Erro ao adicionar evento: ${error.message}` }
  }

  revalidatePath('/dashboard/cases')
  revalidatePath(`/dashboard/cases/${caseId}`)

  return { success: true, message: 'Evento adicionado com sucesso!' }
}

export async function requestDocument(caseId: string, documentName: string): Promise<ActionResponse> {
  const supabase = await createClient()

  // 1. Create the document request
  const { error: requestError } = await supabase
    .from('document_requests')
    .insert({
      case_id: caseId,
      document_name: documentName,
      status: 'pending',
    })

  if (requestError) {
    return { success: false, message: `Erro ao solicitar documento: ${requestError.message}` }
  }

  // 2. Get case and client info for notification
  const { data: caseData, error: fetchError } = await supabase
    .from('client_cases')
    .select('title, user_id, profiles(phone, name)')
    .eq('id', caseId)
    .single()

  if (!fetchError && caseData) {
    const profile = Array.isArray(caseData.profiles) ? caseData.profiles[0] : caseData.profiles
    const phone = profile?.phone
    const clientName = profile?.name || 'cliente'
    const caseTitle = caseData.title

    if (phone) {
      const message = `Olá ${clientName}! O escritório solicitou um novo documento para o seu processo "${caseTitle}": ${documentName}. Você pode enviá-lo através do seu portal.`
      whatsappService.sendNotification(phone, message).catch(err =>
        console.error('Background WhatsApp Notification Error:', err)
      )
    }
  }

  revalidatePath('/dashboard/cases')
  revalidatePath(\`/dashboard/cases/\${caseId}\`)

}

export async function uploadCaseDocument(formData: FormData): Promise<ActionResponse> {
  const supabase = await createClient()

  const caseId = formData.get('caseId') as string
  const requestId = formData.get('requestId') as string | null
  const file = formData.get('file') as File

  if (!caseId || !file) {
    return { success: false, message: 'O caso e o arquivo são obrigatórios.' }
  }

  try {
    // 1. Upload file to Supabase Storage
    const fileExt = file.name.split('.').pop()
    const fileName = `${Math.random().toString(36).substring(2)}.${fileExt}`
    const filePath = `${caseId}/${fileName}`

    const { data: uploadData, error: uploadError } = await supabase.storage
      .from('case-documents')
      .upload(filePath, file)

    if (uploadError) {
      return { success: false, message: `Erro ao fazer upload do arquivo: ${uploadError.message}` }
    }

    // 2. Record document in the database
    const { error: docError } = await supabase
      .from('case_documents')
      .insert({
        case_id: caseId,
        file_name: file.name,
        file_path: filePath,
      })

    if (docError) {
      // Attempt to delete the uploaded file if DB record fails
      await supabase.storage.from('case-documents').remove([filePath])
      return { success: false, message: `Erro ao registrar documento: ${docError.message}` }
    }

    // 3. Update request status if this upload satisfies a request
    if (requestId) {
      const { error: requestError } = await supabase
        .from('document_requests')
        .update({ status: 'uploaded' })
        .eq('id', requestId)

      if (requestError) {
        console.error('Erro ao atualizar status da solicitação:', requestError)
        // We don't fail the whole action because the file was uploaded successfully
      }
    }

    revalidatePath('/dashboard/cases')
    revalidatePath(`/dashboard/cases/${caseId}`)

    return { success: true, message: 'Documento enviado com sucesso!' }
  } catch (error: any) {
    return { success: false, message: `Erro inesperado: ${error.message}` }
  }
}

export async function reviewDocument(requestId: string, status: 'approved' | 'rejected', feedback: string): Promise<ActionResponse> {
  const supabase = await createClient()

  // 1. Update the request status and feedback
  const { data: requestData, error: updateError } = await supabase
    .from('document_requests')
    .update({ status, lawyer_feedback: feedback })
    .eq('id', requestId)
    .select()
    .single()

  if (updateError || !requestData) {
    return { success: false, message: `Erro ao revisar documento: ${updateError?.message || 'Solicitação não encontrada.'}` }
  }

  const caseId = requestData.case_id
  const documentName = requestData.document_name

  // 2. Add event to the case timeline
  const statusText = status === 'approved' ? 'aprovado' : 'recusado'
  const eventDescription = `O documento "${documentName}" foi ${statusText}. ${feedback ? `Feedback: ${feedback}` : ''}`

  await supabase
    .from('case_events')
    .insert({
      case_id: caseId,
      event_description: eventDescription,
      status_label: statusText,
    })

  // 3. Notify the client via WhatsApp
  const { data: caseData, error: fetchError } = await supabase
    .from('client_cases')
    .select('title, user_id, profiles(phone, name)')
    .eq('id', caseId)
    .single()

  if (!fetchError && caseData) {
    const profile = Array.isArray(caseData.profiles) ? caseData.profiles[0] : caseData.profiles
    const phone = profile?.phone
    const clientName = profile?.name || 'cliente'
    const caseTitle = caseData.title

    if (phone) {
      const message = `Olá ${clientName}! O documento "${documentName}" do seu processo "${caseTitle}" foi ${statusText}. ${feedback ? `Observação: ${feedback}` : ''} Você pode conferir os detalhes no portal.`
      whatsappService.sendNotification(phone, message).catch(err =>
        console.error('Background WhatsApp Notification Error:', err)
      )
    }
  }

  revalidatePath('/dashboard/cases')
  revalidatePath(`/dashboard/cases/${caseId}`)

  return { success: true, message: `Documento ${statusText} com sucesso!` }
}

export async function updateCasesStatusBulk(ids: string[], status: string): Promise<ActionResponse> {
  const supabase = await createClient()

  const { error: updateError } = await supabase
    .from('client_cases')
    .update({ status })
    .in('id', ids)

  if (updateError) {
    return { success: false, message: `Erro ao atualizar processos: ${updateError.message}` }
  }

  for (const id of ids) {
    try {
      await createCaseStatusEventAndNotify(id, status)
    } catch (e) {
      console.error(`Error processing bulk event for case ${id}:`, e)
    }
  }

  revalidatePath('/dashboard/cases')
  return { success: true, message: `${ids.length} processos atualizados com sucesso!` }
}

async function createCaseStatusEventAndNotify(id: string, status: string) {
  const supabase = await createClient()

  const { data: caseData } = await supabase
    .from('client_cases')
    .select('title, user_id, profiles(phone, name)')
    .eq('id', id)
    .single()

  if (!caseData) return

  await supabase.from('case_events').insert({
    case_id: id,
    event_description: `O status do processo foi atualizado para ${status}.`,
    status_label: status,
  })

  const profile = Array.isArray(caseData.profiles) ? caseData.profiles[0] : caseData.profiles
  const phone = profile?.phone
  const clientName = profile?.name || 'cliente'
  const caseTitle = caseData.title

  if (phone) {
    const message = `Olá ${clientName}! O status do seu processo "${caseTitle}" foi atualizado para: ${status.replace('_', ' ').toUpperCase()}. Você pode acompanhar os detalhes no seu portal.`
    await whatsappService.sendNotification(phone, message).catch(err =>
      console.error('Background WhatsApp Notification Error:', err)
    )
  }
}
