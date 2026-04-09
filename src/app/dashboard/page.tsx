'use client'

import React, { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import {
  FileText,
  Folder,
  User,
  LogOut,
  ChevronRight,
  Clock,
  AlertCircle
} from 'lucide-react'

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
  case_documents: CaseDocument[]
}

interface Profile {
  full_name: string
  email: string
}

interface SupabaseUser {
  id: string
}

export default function Dashboard() {
  const [user, setUser] = useState<SupabaseUser | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [cases, setCases] = useState<Case[]>([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    async function loadDashboardData() {
      try {
        // 1. Check Auth
        const { data: { user }, error: authError } = await supabase.auth.getUser()

        if (authError || !user) {
          router.push('/login')
          return
        }

        setUser(user)

        // 2. Fetch Profile
        const { data: profileData, error: profileError } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', user.id)
          .single()

        if (profileError) console.error('Profile fetch error:', profileError)
        setProfile(profileData as Profile)

        // 3. Fetch Cases
        const { data: casesData, error: casesError } = await supabase
          .from('cases')
          .select('*, case_documents(*)')
          .eq('client_id', user.id)

        if (casesError) console.error('Cases fetch error:', casesError)
        setCases(casesData as Case[] || [])

      } catch (error) {
        console.error('Dashboard load error:', error)
      } finally {
        setLoading(false)
      }
    }

    loadDashboardData()
  }, [router])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/login')
    router.refresh()
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-brand-primary border-t-transparent rounded-full animate-spin" />
          <p className="text-slate-500 font-medium">Carregando seu portal...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-brand-dark text-white hidden md:flex flex-col">
        <div className="p-6 border-b border-white/10">
          <img src="/bs-logo.png" alt="Logo" className="h-10 w-auto object-contain" />
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <a href="#" className="flex items-center gap-3 px-4 py-3 rounded-xl bg-brand-primary text-white font-bold transition-all">
            <Folder className="w-5 h-5" />
            Meus Processos
          </a>
        </nav>
        <div className="p-4 border-t border-white/10">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-all font-medium"
          >
            <LogOut className="w-5 h-5" />
            Sair do Portal
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        <header className="h-20 bg-white border-b border-slate-200 px-8 flex items-center justify-between shrink-0">
          <h1 className="text-2xl font-serif font-bold text-slate-900">Painel do Cliente</h1>
          <div className="flex items-center gap-4">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-bold text-slate-900">{profile?.full_name || 'Cliente'}</p>
              <p className="text-xs text-slate-500"> Bem-vindo ao seu portal seguro</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-brand-primary/10 flex items-center justify-center text-brand-primary ring-2 ring-brand-primary/20">
              <User className="w-6 h-6" />
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto space-y-8">
            {/* Welcome Banner */}
            <div className="p-8 rounded-[32px] bg-gradient-to-r from-brand-dark to-blue-900 text-white shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-brand-primary/20 rounded-full blur-3xl -mr-32 -mt-32" />
              <div className="relative z-10">
                <h2 className="text-3xl font-serif font-bold mb-2">Olá, {profile?.full_name || 'Cliente'}!</h2>
                <p className="text-blue-100 text-lg max-w-2xl">
                  Acompanhe aqui a evolução de seus processos, visualize documentos e verifique as atualizações mais recentes de forma segura.
                </p>
              </div>
            </div>

            {/* Cases Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {cases.length > 0 ? (
                cases.map((caseItem) => (
                  <div key={caseItem.id} className="bg-white p-8 rounded-[32px] border border-slate-200 shadow-sm hover:shadow-md transition-all group">
                    <div className="flex justify-between items-start mb-6">
                      <div className="flex items-center gap-3">
                        <div className="p-3 bg-brand-primary/10 rounded-2xl text-brand-primary">
                          <FileText className="w-6 h-6" />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-slate-900">{caseItem.case_number}</h3>
                          <p className="text-sm text-slate-500 flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            Iniciado em {new Date(caseItem.created_at).toLocaleDateString('pt-BR')}
                          </p>
                        </div>
                      </div>
                      <span className={`px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider ${
                        caseItem.status === 'Concluído' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
                      }`}>
                        {caseItem.status}
                      </span>
                    </div>

                    <p className="text-slate-600 mb-8 leading-relaxed">
                      {caseItem.description}
                    </p>

                    <div className="space-y-4">
                      <h4 className="text-sm font-bold text-slate-900 uppercase tracking-widest flex items-center gap-2">
                        <Folder className="w-4 h-4" />
                        Documentos do Caso
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {caseItem.case_documents && caseItem.case_documents.length > 0 ? (
                          caseItem.case_documents.map((doc) => (
                            <a
                              key={doc.id}
                              href={`https://vasmwzwrqtjksnipiitd.supabase.co/storage/v1/object/public/case-documents/${doc.file_path}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 border border-slate-100 hover:bg-white hover:border-brand-primary/50 transition-all group/doc"
                            >
                              <FileText className="w-4 h-4 text-slate-400 group-hover/doc:text-brand-primary transition-colors" />
                              <span className="text-sm text-slate-600 truncate">{doc.file_name}</span>
                              <ChevronRight className="w-4 h-4 ml-auto text-slate-300 group-hover/doc:text-brand-primary transition-colors" />
                            </a>
                          ))
                        ) : (
                          <p className="text-sm text-slate-400 italic">Nenhum documento disponível para este caso.</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="col-span-full py-20 text-center bg-white rounded-[32px] border-2 border-dashed border-slate-200">
                  <div className="mx-auto w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4 text-slate-400">
                    <AlertCircle className="w-8 h-8" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">Nenhum processo encontrado</h3>
                  <p className="text-slate-500">Você ainda não possui processos vinculados ao seu perfil.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
