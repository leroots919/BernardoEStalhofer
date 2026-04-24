'use client'

import React, { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import {
  FileText,
  Upload,
  CheckCircle2,
  XCircle,
  Clock,
  AlertCircle,
  ChevronRight,
  Loader2
} from 'lucide-react'
import { uploadCaseDocument } from '@/app/dashboard/actions'

interface DocumentRequest {
  id: string
  case_id: string
  document_name: string
  status: 'pending' | 'uploaded' | 'approved' | 'rejected'
  lawyer_feedback: string | null
  created_at: string
}

interface Case {
  id: string
  case_number: string
}

export default function DocumentsPage() {
  const [requests, setRequests] = useState<DocumentRequest[]>([])
  const [cases, setCases] = useState<Case[]>([])
  const [loading, setLoading] = useState(true)
  const [uploadingId, setUploadingId] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    async function loadDocuments() {
      try {
        const { data: { user }, error: authError } = await supabase.auth.getUser()
        if (authError || !user) {
          router.push('/login')
          return
        }

        // 1. Fetch all cases for this user
        const { data: casesData, error: casesError } = await supabase
          .from('client_cases')
          .select('id, case_number')
          .eq('user_id', user.id)

        if (casesError) throw casesError
        setCases(casesData || [])

        const caseIds = casesData?.map(c => c.id) || []

        // 2. Fetch document requests for these cases
        if (caseIds.length > 0) {
          const { data: requestsData, error: requestsError } = await supabase
            .from('document_requests')
            .select('*')
            .in('case_id', caseIds)
            .order('created_at', { ascending: false })

          if (requestsError) throw requestsError
          setRequests(requestsData || [])
        }
      } catch (error) {
        console.error('Error loading documents:', error)
      } finally {
        setLoading(false)
      }
    }

    loadDocuments()
  }, [router])

  const handleFileUpload = async (requestId: string, caseId: string, event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setUploadingId(requestId)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('caseId', caseId)
    formData.append('requestId', requestId)

    try {
      const result = await uploadCaseDocument(formData)
      if (result.success) {
        // Refresh data
        const { data: updatedRequests, error } = await supabase
          .from('document_requests')
          .select('*')
          .in('case_id', cases.map(c => c.id))
          .order('created_at', { ascending: false })

        if (!error) setRequests(updatedRequests || [])
      } else {
        alert(result.message)
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('Ocorreu um erro ao enviar o documento.')
    } finally {
      setUploadingId(null)
    }
  }

  const getCaseNumber = (caseId: string) => {
    return cases.find(c => c.id === caseId)?.case_number || 'Desconhecido'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-10 h-10 animate-spin text-brand-primary" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Central de Documentos</h1>
        <p className="text-slate-500">Envie os documentos solicitados pelo escritório para agilizar seu processo.</p>
      </div>

      {requests.length === 0 ? (
        <div className="bg-white p-12 rounded-[32px] border border-slate-200 shadow-sm text-center">
          <div className="mx-auto w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4 text-slate-400">
            <FileText className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 mb-2">Nenhuma solicitação encontrada</h3>
          <p className="text-slate-500">No momento, não há documentos pendentes para seus processos.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {requests.map((req) => (
            <div key={req.id} className="bg-white p-6 rounded-[32px] border border-slate-200 shadow-sm hover:shadow-md transition-all">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div className="space-y-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                      Processo {getCaseNumber(req.case_id)}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                      req.status === 'approved' ? 'bg-green-100 text-green-700' :
                      req.status === 'rejected' ? 'bg-red-100 text-red-700' :
                      req.status === 'uploaded' ? 'bg-blue-100 text-blue-700' :
                      'bg-amber-100 text-amber-700'
                    }`}>
                      {req.status === 'pending' ? 'Pendente' :
                       req.status === 'uploaded' ? 'Em Análise' :
                       req.status === 'approved' ? 'Aprovado' : 'Recusado'}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900">{req.document_name}</h3>
                  <p className="text-sm text-slate-500 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    Solicitado em {new Date(req.created_at).toLocaleDateString('pt-BR')}
                  </p>
                </div>

                <div className="flex items-center gap-4">
                  {req.status === 'pending' || req.status === 'rejected' ? (
                    <label className={`
                      flex items-center gap-2 px-6 py-3 rounded-2xl font-bold transition-all cursor-pointer
                      ${uploadingId === req.id
                        ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                        : 'bg-brand-primary text-white hover:bg-brand-dark'}
                    `}>
                      {uploadingId === req.id ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Enviando...
                        </>
                      ) : (
                        <>
                          <Upload className="w-4 h-4" />
                          {req.status === 'rejected' ? 'Reenviar' : 'Enviar Documento'}
                        </>
                      )}
                      <input
                        type="file"
                        className="hidden"
                        onChange={(e) => handleFileUpload(req.id, req.case_id, e)}
                        disabled={uploadingId !== null}
                      />
                    </label>
                  ) : req.status === 'uploaded' ? (
                    <div className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-blue-50 text-blue-700 font-bold text-sm">
                      <Clock className="w-4 h-4 animate-pulse" />
                      Aguardando análise
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-green-50 text-green-700 font-bold text-sm">
                      <CheckCircle2 className="w-4 h-4" />
                      Documento OK
                    </div>
                  )}
                </div>
              </div>

              {req.lawyer_feedback && (
                <div className={`mt-4 p-4 rounded-2xl flex items-start gap-3 ${
                  req.status === 'approved' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
                }`}>
                  {req.status === 'approved' ? (
                    <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5" />
                  ) : (
                    <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                  )}
                  <div className="text-sm">
                    <span className="font-bold block mb-1">
                      {req.status === 'approved' ? 'Feedback do Advogado:' : 'Motivo da Recusa:'}
                    </span>
                    {req.lawyer_feedback}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
