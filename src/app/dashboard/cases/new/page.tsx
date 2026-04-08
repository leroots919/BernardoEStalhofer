import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { ArrowLeft, Briefcase, User, FileText, CheckCircle } from 'lucide-react'
import NewCaseForm from './NewCaseForm'

export default async function NewCasePage() {
  const supabase = await createClient()

  // Fetch clients
  const { data: clients, error: clientError } = await supabase
    .from('profiles')
    .select('id, name, email')
    .eq('type', 'cliente')
    .order('name', { ascending: true })

  // Fetch services
  const { data: services, error: serviceError } = await supabase
    .from('services')
    .select('id, name')
    .eq('active', true)
    .order('name', { ascending: true })

  if (clientError || serviceError) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700">
        Erro ao carregar dados necessários para criar o processo.
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-4">
        <Link
          href="/dashboard/cases"
          className="p-2 rounded-lg bg-white border border-slate-200 text-slate-600 hover:text-brand-primary transition-all shadow-sm"
        >
          <ArrowLeft className="w-5 h-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-brand-dark">Novo Processo</h1>
          <p className="text-slate-500 text-sm">Cadastre um novo caso jurídico no sistema.</p>
        </div>
      </div>

      <div className="max-w-2xl bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-200 bg-slate-50/50">
          <h2 className="font-bold text-brand-dark flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-brand-primary" />
            Detalhes do Processo
          </h2>
        </div>
        <div className="p-8">
          <NewCaseForm clients={clients || []} services={services || []} />
        </div>
      </div>
    </div>
  )
}

// Helper component for Link since I missed importing it
import Link from 'next/link'
