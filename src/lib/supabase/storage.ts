import { createClient } from '@/lib/supabase/client'

export async function uploadFile(file: File, caseId: string, userId: string) {
  const supabase = createClient()
  
  const fileExt = file.name.split('.').pop()
  const fileName = `${Math.random().toString(36).substring(2)}.${fileExt}`
  const filePath = `cases/${caseId}/${fileName}`

  const { data, error } = await supabase.storage
    .from('process-files')
    .upload(filePath, file)

  if (error) throw error

  // Sync metadata to the database
  const { error: dbError } = await supabase
    .from('process_files')
    .insert({
      user_id: userId,
      case_id: caseId,
      filename: file.name,
      original_filename: file.name,
      file_path: filePath,
    })

  if (dbError) {
    // Rollback file upload if DB insert fails
    await supabase.storage.from('process-files').remove([filePath])
    throw dbError
  }

  return data
}

export async function getFileUrl(filePath: string) {
  const supabase = createClient()
  const { data } = supabase.storage.from('process-files').getPublicUrl(filePath)
  return data.publicUrl
}

export async function deleteFile(filePath: string, fileId: string) {
  const supabase = createClient()
  
  const { error: storageError } = await supabase.storage
    .from('process-files')
    .remove([filePath])
    
  if (storageError) throw storageError

  const { error: dbError } = await supabase
    .from('process_files')
    .delete()
    .eq('id', fileId)

  if (dbError) throw dbError

  return { success: true }
}
