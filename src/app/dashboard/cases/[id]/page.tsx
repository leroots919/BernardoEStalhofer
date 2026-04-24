'use client'

import React, { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import {
  ArrowLeft,
  FileText,
  CheckCircle2,
  Clock,
  AlertCircle,
  ChevronRight,
  Loader2,
  Calendar,
  Scale
} from 'lucide-react'

interface CaseEvent {
  id: string
  event_description: string
  status_label: string
  created_at: string
}

interface CaseDocument {
  id: string
  file_name: string
  file_path: string
}

interface Case {
  id: string
  case_number: string
  description: string
  status: string
  created_at: string
}

interface DocumentRequest {
  id: string
  document_name: string
  status: string
  created_at: string
}

export default function CaseDetailPage({ params }: { params: { id: string } }) {
  const [caseData, setCaseData] = useState<Case | null>(null)
  const [events, setEvents] = useState<CaseEvent[]>([])
  const [documents, setDocuments] = useState<CaseDocument[]>([])
  const [requests, setRequests] = useState<DocumentRequest[]>([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    async function loadCaseDetails() {
      try {
        const { data: { user }, error: authError } = await supabase.auth.getUser()
        if (authError || !user) {
          router.push('/login')
          return
        }

        const caseId = params.id

        const { data: caseInfo, error: caseError } = await supabase
          .from('client_cases')
          .select('*')
          .eq('id', caseId)
          .eq('user_id', user.id)
          .single()

        if (caseError || !caseInfo) {
          console.error('Case not found or unauthorized:', caseError)
          return
        }
        setCaseData(caseInfo as Case)

        const { data: eventsData, error: eventsError } = await supabase
          .from('case_events')
          .select('*')
          .eq('case_id', caseId)
          .order('created_at', { ascending: false })

        if (!eventsError) setEvents(eventsData || [])

        const { data: docsData, error: docsError } = await supabase
          .from('case_documents')
          .select('*')
          .eq('case_id', caseId)
          .order('created_at', { ascending: false })

        if (!docsError) setDocuments(docsData || [])

        const { data: reqsData, error: reqsError } = await supabase
          .from('document_requests')
          .select('*')
          .eq('case_id', caseId)
          .in('status', ['pending', 'uploaded'])
          .order('created_at', { ascending: false })

        if (!reqsError) setRequests(reqsData || [])

      } catch (error) {
        console.error('Error loading case details:', error)
      } finally {
        setLoading(false)
      }
    }

    loadCaseDetails()
  }, [params.id, router])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-12 h-12 animate-spin text-brand-primary" />
          <p className="text-slate-500 font-serif italic">Consultando arquivos do processo...</p>
        </div>
      </div>
    )
  }

  if (!caseData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-8">
        <div className="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-6 text-slate-300">
          <AlertCircle className="w-10 h-10" />
        </div>
        <h2 className="text-2xl font-serif font-bold text-slate-900 mb-2">Processo não localizado</h2>
        <p className="text-slate-500 max-w-md mb-8">
          Não conseguimos encontrar as informações deste processo ou você não tem permissão para acessá-lo.
        </p>
        <button
          onClick={() => router.push('/dashboard')}
          className="px-8 py-3 bg-brand-dark text-white rounded-2xl font-bold hover:bg-brand-primary transition-all shadow-lg"
        >
          Voltar ao Painel Principal
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-10 pb-20">
      {/* Navigation */}
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-slate-500 hover:text-brand-primary transition-all font-medium group w-fit"
      >
        <ArrowLeft className="w-4 h-4 transition-transform group-hover:-translate-x-1" />
        Voltar ao Painel
      </button>

      {/* Case Header Card */}
      <div className="relative overflow-hidden bg-white p-8 md:p-12 rounded-[40px] border border-slate-200 shadow-sm">
        <div className="absolute top-0 right-0 w-96 h-96 bg-slate-50 rounded-full blur-3xl -mr-48 -mt-48 opacity-50" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-brand-dark text-white rounded-2xl shadow-lg">
                <Scale className="w-6 h-6" />
              </div>
              <h1 className="text-4xl font-serif font-bold text-slate-900 tracking-tight">
                {caseData.case_number}
              </h1>
            </div>

            <div className="flex items-center gap-3">
              <span className={`px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-widest shadow-sm ${
                caseData.status === 'Concluído' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
              }`}>
                {caseData.status}
              </span>
              <span className="text-slate-300">•</span>
              <span className="text-sm text-slate-500 flex items-center gap-1.5">
                <Calendar className="w-4 h-4" />
                Iniciado em {new Date(caseData.created_at).toLocaleDateString('pt-BR')}
              </span>
            </div>

            <p className="text-slate-600 text-lg leading-relaxed max-w-3xl font-light">
              {caseData.description}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        {/* Timeline Section */}
        <div className="lg:col-span-2 space-y-8">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-serif font-bold text-slate-900 flex items-center gap-3">
              <Clock className="w-6 h-6 text-brand-primary" />
              Histórico do Processo
            </h2>
          </div>

          <div className="relative space-y-10 before:absolute before:inset-0 before:ml-6 before:-translate-x-px before:h-full before:w-px before:bg-slate-200">
            {events.length > 0 ? (
              events.map((event, index) => (
                <div key={event.id} className="relative pl-16 group">
                  <div className={`absolute left-0 top-1 w-12 h-12 rounded-full border-4 border-white shadow-md flex items-center justify-center transition-all group-hover:scale-110 ${
                    index === 0 ? 'bg-brand-dark text-white ring-4 ring-brand-dark/10' : 'bg-slate-100 text-slate-400'
                  }`}>
                    {index === 0 ? <CheckCircle2 className="w-6 h-6" /> : <Clock className="w-6 h-6" />}
                  </div>

                  <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm hover:shadow-md transition-all hover:border-brand-primary/30">
                    <div className="flex justify-between items-center mb-3">
                      <span className={`text-[10px] font-bold uppercase tracking-tighter px-2 py-1 rounded-md ${
                        index === 0 ? 'bg-brand-primary/10 text-brand-primary' : 'bg-slate-100 text-slate-500'
                      }`}>
                        {event.status_label}
                      </span>
                      <span className="text-xs font-medium text-slate-400 italic">
                        {new Date(event.created_at).toLocaleDateString('pt-BR')}
                      </span>
                    </div>
                    <p className="text-slate-700 leading-relaxed font-medium">
                      {event.event_description}
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <div className="bg-white p-12 rounded-3xl border border-slate-200 text-center">
                <p className="text-slate-400 italic font-serif">Ainda não há atualizações disponíveis para este processo.</p>
              </div>
            )}
          </div>
        </div>

        {/* Side panel: Documents & Requests */}
        <div className="space-y-10">
          {/* Documents Archive */}
          <div className="space-y-6">
            <h3 className="text-xl font-serif font-bold text-slate-900 flex items-center gap-3">
              <FileText className="w-6 h-6 text-brand-primary" />
              Arquivo Digital
            </h3>
            <div className="bg-white rounded-[32px] border border-slate-200 shadow-sm overflow-hidden">
              {documents.length > 0 ? (
                <div className="divide-y divide-slate-100">
                  {documents.map((doc) => (
                    <a
                      key={doc.id}
                      href={`https://vasmwzwrqtjksnipiitd.supabase.co/storage/v1/object/public/case-documents/${doc.file_path}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between p-5 hover:bg-slate-50 transition-all group"
                    >
                      <div className="flex items-center gap-3 overflow-hidden">
                        <div className="p-2 bg-slate-100 rounded-lg group-hover:bg-brand-primary/10 group-hover:text-brand-primary transition-all">
                          <FileText className="w-4 h-4 text-slate-400 transition-colors" />
                        </div>
                        <span className="text-sm text-slate-600 truncate font-medium">{doc.file_name}</span>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-brand-primary transition-all" />
                    </a>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center text-slate-400 text-sm italic">
                  Nenhum documento anexado a este caso.
                </div>
              )}
            </div>
          </div>

          {/* Actionable Requests */}
          <div className="space-y-6">
            <h3 className="text-xl font-serif font-bold text-slate-900 flex items-center gap-3">
              <AlertCircle className="w-6 h-6 text-amber-500" />
              Ações Necessárias
            </h3>
            <div className="space-y-4">
              {requests.length > 0 ? (
                requests.map((req) => (
                  <div key={req.id} className="bg-amber-50 p-5 rounded-3xl border border-amber-200 shadow-sm group hover:shadow-md transition-all">
                    <div className="flex items-start justify-between gap-3 mb-4">
                      <div>
                        <p className="text-sm font-bold text-amber-900 leading-tight">{req.document_name}</p>
                        <p className="text-[10px] text-amber-600 uppercase font-bold mt-1 tracking-wider">
                          {req.status === 'uploaded' ? 'Em Análise' : 'Aguardando Envio'}
                        </p>
                      </div>
                      <span className={`w-2 h-2 rounded-full animate-pulse ${
                        req.status === 'uploaded' ? 'bg-blue-500' : 'bg-amber-500'
                      }`} />
                    </div>
                    <button
                      onClick={() => router.push('/dashboard/documents')}
                      className="w-full py-2.5 bg-white border border-amber-200 text-amber-700 rounded-xl text-xs font-bold hover:bg-amber-100 transition-all flex items-center justify-center gap-2"
                    >
                      {req.status === 'uploaded' ? 'Ver detalhes' : 'Enviar Documento'}
                      <ChevronRight className="w-3 h-3" />
                    </button>
                  </div>
                ))
              ) : (
                <div className="bg-white p-6 rounded-3xl border border-slate-200 text-center">
                  <div className="inline-flex p-3 bg-green-50 text-green-600 rounded-full mb-3">
                    <CheckCircle2 className="w-5 h-5" />
                  </div>
                  <p className="text-slate-500 text-sm italic">Tudo em ordem! Nenhuma pendência para este processo.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
