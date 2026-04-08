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

export async function updateCaseStatus(id: string, status: string): Promise<ActionResponse> {
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

  // 3. Trigger WhatsApp Notification
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

  return { success: true, message: 'Status atualizado e cliente notificado!' }
}
