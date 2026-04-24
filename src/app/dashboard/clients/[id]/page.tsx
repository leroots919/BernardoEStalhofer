'use client'

import React, { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import {
  ArrowLeft,
  Plus,
  FileText,
  Clock,
  CheckCircle2,
  AlertCircle,
  Send,
  Upload,
  MoreVertical,
  Search,
  User,
  Phone,
  Mail,
  Loader2
} from 'lucide-react'
import {
  createCase,
  updateCaseStatus,
  addCustomCaseEvent,
  requestDocument,
  reviewDocument
} from '@/app/dashboard/actions'

interface Profile {
  id: string
  name: string
  email: string
  phone: string
}

interface Case {
  id: string
  case_number: string
  title: string
  description: string
  status: string
  created_at: string
}

interface DocumentRequest {
  id: string
  document_name: string
  status: 'pending' | 'uploaded' | 'approved' | 'rejected'
  lawyer_feedback: string | null
  created_at: string
}

export default function AdminClientDetailPage({ params }: { params: { id: string } }) {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [cases, setCases] = useState<Case[]>([])
  const [requests, setRequests] = useState<DocumentRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'cases' | 'documents'>('cases')
  const [isCaseModalOpen, setIsCaseModalOpen] = useState(false)
  const [isRequestModalOpen, setIsRequestModalOpen] = useState(false)
  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false)
  const [selectedRequest, setSelectedRequest] = useState<DocumentRequest | null>(null)

  const router = useRouter()

  useEffect(() => {
    loadAllData()
  }, [params.id])

  async function loadAllData() {
    setLoading(true)
    try {
      // 1. Fetch Profile
      const { data: profileData } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', params.id)
        .single()
      setProfile(profileData as Profile)

      // 2. Fetch Cases
      const { data: casesData } = await supabase
        .from('client_cases')
        .select('*')
        .eq('user_id', params.id)
        .order('created_at', { ascending: false })
      setCases(casesData || [])

      // 3. Fetch Document Requests
      const { data: requestsData } = await supabase
        .from('document_requests')
        .select('*')
        .in('case_id', casesData?.map(c => c.id) || [])
        .order('created_at', { ascending: false })
      setRequests(requestsData || [])

    } catch (error) {
      console.error('Error loading admin data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateCase = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const title = formData.get('title') as string
    const description = formData.get('description') as string
    const status = formData.get('status') as string

    formData.append('userId', params.id)
    formData.append('serviceId', 'default-service-id')

    const result = await createCase({ success: false, message: '' }, formData)

    if (result.success) {
      setIsCaseModalOpen(false)
      await loadAllData()
    } else {
      alert(result.message)
    }
  }

  const handleUpdateStatus = async (caseId: string, newStatus: string) => {
    const result = await updateCaseStatus(caseId, newStatus)
    if (result.success) {
      await loadAllData()
    } else {
      alert(result.message)
    }
  }

  const handleRequestDoc = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const caseId = formData.get('caseId') as string
    const documentName = formData.get('documentName') as string

    const result = await requestDocument(caseId, documentName)
    if (result.success) {
      setIsRequestModalOpen(false)
      await loadAllData()
    } else {
      alert(result.message)
    }
  }

  const handleReviewDoc = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const status = formData.get('status') as 'approved' | 'rejected'
    const feedback = formData.get('feedback') as string

    if (!selectedRequest) return

    const result = await reviewDocument(selectedRequest.id, status, feedback)
    if (result.success) {
      setIsReviewModalOpen(false)
      await loadAllData()
    } else {
      alert(result.message)
    }
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
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.back()}
            className="p-2 rounded-xl bg-white border border-slate-200 text-slate-500 hover:text-brand-primary transition-all shadow-sm"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-brand-dark">{profile?.name}</h1>
            <div className="flex items-center gap-3 text-sm text-slate-500">
              <span className="flex items-center gap-1"><Mail className="w-3 h-3" /> {profile?.email}</span>
              <span className="flex items-center gap-1"><Phone className="w-3 h-3" /> {profile?.phone || 'Não informado'}</span>
            </div>
          </div>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setIsCaseModalOpen(true)}
            className="flex items-center gap-2 bg-brand-primary text-white px-4 py-2 rounded-xl font-bold hover:bg-brand-dark transition-all shadow-sm"
          >
            <Plus className="w-4 h-4" />
            Novo Processo
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200 gap-8">
        <button
          onClick={() => setActiveTab('cases')}
          className={`pb-4 text-sm font-bold transition-all relative ${activeTab === 'cases' ? 'text-brand-primary' : 'text-slate-400 hover:text-slate-600'}`}
        >
          Processos
          {activeTab === 'cases' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-primary" />}
        </button>
        <button
          onClick={() => setActiveTab('documents')}
          className={`pb-4 text-sm font-bold transition-all relative ${activeTab === 'documents' ? 'text-brand-primary' : 'text-slate-400 hover:text-slate-600'}`}
        >
          Documentos
          {activeTab === 'documents' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-primary" />}
        </button>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'cases' ? (
          <div className="grid grid-cols-1 gap-6">
            {cases.length > 0 ? (
              cases.map(caseItem => (
                <div key={caseItem.id} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-bold text-slate-900">{caseItem.case_number} - {caseItem.title}</h3>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        caseItem.status === 'Concluído' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
                      }`}>
                        {caseItem.status}
                      </span>
                    </div>
                    <p className="text-sm text-slate-500 line-clamp-1">{caseItem.description}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <select
                      value={caseItem.status}
                      onChange={(e) => handleUpdateStatus(caseItem.id, e.target.value)}
                      className="text-xs font-medium bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-brand-primary transition-all"
                    >
                      <option value="Aguardando">Aguardando</option>
                      <option value="Em Andamento">Em Andamento</option>
                      <option value="Concluído">Concluído</option>
                      <option value="Suspenso">Suspenso</option>
                    </select>
                    <button
                      onClick={() => {
                        const desc = prompt('Digite o evento para a linha do tempo:')
                        if (desc) addCustomCaseEvent(caseItem.id, desc)
                      }}
                      className="p-2 text-slate-400 hover:text-brand-primary transition-colors"
                      title="Adicionar Evento"
                    >
                      <Clock className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-20 bg-white rounded-2xl border border-slate-200 text-slate-500 italic">
                Nenhum processo vinculado a este cliente.
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-bold text-slate-900">Solicitações de Documentos</h2>
              <button
                onClick={() => setIsRequestModalOpen(true)}
                className="flex items-center gap-2 bg-brand-primary text-white px-4 py-2 rounded-xl text-sm font-bold hover:bg-brand-dark transition-all"
              >
                <Send className="w-4 h-4" />
                Solicitar Documento
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {requests.length > 0 ? (
                requests.map(req => (
                  <div key={req.id} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between gap-4">
                    <div className="space-y-1">
                      <p className="font-bold text-slate-900">{req.document_name}</p>
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                          req.status === 'approved' ? 'bg-green-100 text-green-700' :
                          req.status === 'rejected' ? 'bg-red-100 text-red-700' :
                          req.status === 'uploaded' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'
                        }`}>
                          {req.status}
                        </span>
                        <span className="text-[10px] text-slate-400">{new Date(req.created_at).toLocaleDateString('pt-BR')}</span>
                      </div>
                    </div>
                    {req.status === 'uploaded' && (
                      <button
                        onClick={() => { setSelectedRequest(req); setIsReviewModalOpen(true); }}
                        className="p-2 bg-brand-primary/10 text-brand-primary rounded-lg hover:bg-brand-primary hover:text-white transition-all"
                        title="Revisar Documento"
                      >
                        <CheckCircle2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                ))
              ) : (
                <div className="col-span-full text-center py-20 bg-white rounded-2xl border border-slate-200 text-slate-500 italic">
                  Nenhuma solicitação de documento ativa.
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Modals */}
      {isCaseModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl">
            <h3 className="text-xl font-bold text-slate-900 mb-6">Criar Novo Processo</h3>
            <form onSubmit={handleCreateCase} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Título do Processo</label>
                <input name="title" required className="w-full px-4 py-2 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-primary transition-all" placeholder="Ex: Ação de Indenização" />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Descrição</label>
                <textarea name="description" rows={3} className="w-full px-4 py-2 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-primary transition-all" placeholder="Detalhes do caso..." />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Status Inicial</label>
                <select name="status" className="w-full px-4 py-2 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-primary transition-all">
                  <option value="Aguardando">Aguardando</option>
                  <option value="Em Andamento">Em Andamento</option>
                </select>
              </div>
              <div className="flex gap-3 pt-4">
                <button type="button" onClick={() => setIsCaseModalOpen(false)} className="flex-1 py-2 rounded-xl border border-slate-200 font-bold text-slate-600 hover:bg-slate-50 transition-all">Cancelar</button>
                <button type="submit" className="flex-1 py-2 rounded-xl bg-brand-primary text-white font-bold hover:bg-brand-dark transition-all">Criar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {isRequestModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl">
            <h3 className="text-xl font-bold text-slate-900 mb-6">Solicitar Documento</h3>
            <form onSubmit={handleRequestDoc} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Vincular ao Processo</label>
                <select name="caseId" required className="w-full px-4 py-2 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-primary transition-all">
                  {cases.map(c => <option key={c.id} value={c.id}>{c.case_number} - {c.title}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Nome do Documento</label>
                <input name="documentName" required className="w-full px-4 py-2 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-primary transition-all" placeholder="Ex: Comprovante de Residência" />
              </div>
              <div className="flex gap-3 pt-4">
                <button type="button" onClick={() => setIsRequestModalOpen(false)} className="flex-1 py-2 rounded-xl border border-slate-200 font-bold text-slate-600 hover:bg-slate-50 transition-all">Cancelar</button>
                <button type="submit" className="flex-1 py-2 rounded-xl bg-brand-primary text-white font-bold hover:bg-brand-dark transition-all">Solicitar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {isReviewModalOpen && selectedRequest && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl">
            <h3 className="text-xl font-bold text-slate-900 mb-2">Revisar Documento</h3>
            <p className="text-sm text-slate-500 mb-6">{selectedRequest.document_name}</p>
            <form onSubmit={handleReviewDoc} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Decisão</label>
                <div className="flex gap-3">
                  <label className="flex-1 flex items-center justify-center gap-2 p-3 rounded-xl border border-slate-200 cursor-pointer hover:bg-slate-50 transition-all has-[:checked]:bg-green-50 has-[:checked]:border-green-500 has-[:checked]:text-green-700">
                    <input type="radio" name="status" value="approved" defaultChecked className="hidden" />
                    <CheckCircle2 className="w-4 h-4" /> Aprovar
                  </label>
                  <label className="flex-1 flex items-center justify-center gap-2 p-3 rounded-xl border border-slate-200 cursor-pointer hover:bg-slate-50 transition-all has-[:checked]:bg-red-50 has-[:checked]:border-red-500 has-[:checked]:text-red-700">
                    <input type="radio" name="status" value="rejected" className="hidden" />
                    <XCircle className="w-4 h-4" /> Recusar
                  </label>
                </div>
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Feedback / Observações</label>
                <textarea name="feedback" rows={3} className="w-full px-4 py-2 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-primary transition-all" placeholder="Ex: Imagem ilegível, favor enviar novamente..." />
              </div>
              <div className="flex gap-3 pt-4">
                <button type="button" onClick={() => setIsReviewModalOpen(false)} className="flex-1 py-2 rounded-xl border border-slate-200 font-bold text-slate-600 hover:bg-slate-50 transition-all">Cancelar</button>
                <button type="submit" className="flex-1 py-2 rounded-xl bg-brand-primary text-white font-bold hover:bg-brand-dark transition-all">Confirmar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

function XCircle(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="m15 9-6 6" />
      <path d="m9 9 6 6" />
    </svg>
  )
}
