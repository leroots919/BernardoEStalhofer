import React, { useState, useEffect, use } from 'react'
import { uploadFile, getFileUrl, deleteFile } from '@/lib/supabase/storage'
import { createClient } from '@/lib/supabase/client'
import {
  Upload,
  FileText,
  Trash2,
  ExternalLink,
  Loader2,
  AlertCircle,
  ArrowLeft
} from 'lucide-react'
import Link from 'next/link'

interface CaseFile {
  id: string
  filename: string
  file_path: string
  created_at: string
}

export default function CaseFilesPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params)
  const id = resolvedParams.id

  const [files, setFiles] = useState<CaseFile[]>([])
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const supabase = createClient()

  useEffect(() => {
    fetchFiles()
  }, [id])

  async function fetchFiles() {
    const { data, error: fetchError } = await supabase
      .from('process_files')
      .select('*')
      .eq('case_id', id)
      .order('created_at', { ascending: false })

    if (fetchError) {
      setError(fetchError.message)
    } else {
      setFiles((data as CaseFile[]) || [])
    }
  }

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setError(null)

    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) throw new Error('Você precisa estar autenticado para enviar arquivos')

      await uploadFile(file, id, user.id)
      await fetchFiles()
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Erro ao enviar arquivo'
      setError(message)
    } finally {
      setUploading(false)
    }
  }

  async function handleDelete(fileId: string, path: string) {
    if (!confirm('Tem certeza que deseja excluir este arquivo?')) return

    try {
      await deleteFile(path, fileId)
      await fetchFiles()
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Erro ao excluir arquivo'
      setError(message)
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-8 space-y-8">
      <div className="flex items-center gap-4">
        <Link
          href={`/dashboard/cases/${id}`}
          className="p-2 rounded-lg bg-white border border-slate-200 text-slate-600 hover:text-brand-primary transition-all shadow-sm"
        >
          <ArrowLeft className="w-5 h-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-brand-dark">Arquivos do Processo</h1>
          <p className="text-slate-500 text-sm">Envie e gerencie os documentos vinculados a este caso.</p>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-200 bg-slate-50/50 flex justify-between items-center">
          <h2 className="font-bold text-brand-dark flex items-center gap-2">
            <FileText className="w-5 h-5 text-brand-primary" />
            Documentos do Caso
          </h2>
          <label className="cursor-pointer flex items-center gap-2 bg-brand-primary text-white px-4 py-2 rounded-lg hover:bg-brand-primary/90 transition-all shadow-sm font-medium text-sm">
            {uploading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Upload className="w-4 h-4" />
            )}
            {uploading ? 'Enviando...' : 'Upload de Arquivo'}
            <input type="file" className="hidden" onChange={handleUpload} disabled={uploading} />
          </label>
        </div>

        {error && (
          <div className="m-6 p-4 bg-red-50 text-red-700 border border-red-200 rounded-xl flex items-start gap-3 text-sm">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p>{error}</p>
          </div>
        )}

        <div className="p-6">
          {files.length === 0 ? (
            <div className="text-center py-20 space-y-4">
              <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto text-slate-400">
                <FileText className="w-8 h-8" />
              </div>
              <div>
                <p className="text-slate-900 font-medium">Nenhum arquivo encontrado</p>
                <p className="text-slate-500 text-sm">Os arquivos enviados aparecerão aqui.</p>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {files.map(file => (
                <div key={file.id} className="p-4 bg-white border border-slate-200 rounded-xl flex flex-col justify-between shadow-sm hover:border-brand-primary/30 transition-all group">
                  <div className="flex items-start gap-3 mb-4">
                    <div className="p-2 bg-brand-primary/10 text-brand-primary rounded-lg">
                      <FileText className="w-5 h-5" />
                    </div>
                    <div className="overflow-hidden">
                      <p className="text-sm font-bold text-slate-900 truncate" title={file.filename}>
                        {file.filename}
                      </p>
                      <p className="text-xs text-slate-500">
                        {new Date(file.created_at).toLocaleDateString('pt-BR')}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <a
                      href={getFileUrl(file.file_path)}
                      target="_blank"
                      className="flex items-center gap-1 text-xs font-bold text-brand-primary hover:text-brand-primary/80 transition-colors"
                    >
                      <ExternalLink className="w-3 h-3" />
                      Visualizar
                    </a>
                    <button
                      onClick={() => handleDelete(file.id, file.file_path)}
                      className="p-2 text-slate-400 hover:text-red-600 transition-colors"
                      title="Excluir arquivo"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
