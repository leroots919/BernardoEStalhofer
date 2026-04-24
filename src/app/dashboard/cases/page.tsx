import { createClient } from '@/lib/supabase/server'
import {
  Briefcase,
  Plus,
  ArrowUpRight,
} from 'lucide-react'
import Link from 'next/link'
import CaseTable from './CaseTable'

interface CaseItem {
  id: string
  title: string
  status: string
  created_at: string
  updated_at: string
  profiles: { name: string; email: string } | { name: string; email: string }[]
  services: { name: string } | { name: string }[]
}

export default async function CasesPage({
  searchParams,
}: {
  searchParams: Promise<{ status?: string }>
}) {
  const supabase = await createClient()
  const resolvedSearchParams = await searchParams
  const currentStatus = resolvedSearchParams.status

  const { data: cases, error } = await supabase
    .from('client_cases')
    .select(`
      id,
      title,
      status,
      created_at,
      updated_at,
      profiles (name, email),
      services (name)
    `)
    .order('created_at', { ascending: false })

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700">
        Erro ao carregar processos: {error.message}
      </div>
    )
  }

  const filteredCases = (currentStatus
    ? cases?.filter(c => c.status === currentStatus)
    : cases) as CaseItem[] | null

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-serif font-bold text-brand-dark tracking-tight">Gestão de Processos</h1>
          <p className="text-slate-500">Controle e acompanhe todos os casos jurídicos do escritório.</p>
        </div>
        <Link
          href="/dashboard/cases/new"
          className="flex items-center justify-center gap-2 bg-brand-primary text-white px-6 py-3 rounded-2xl font-bold hover:bg-brand-dark transition-all shadow-lg active:scale-95"
        >
          <Plus className="w-5 h-5" />
          Novo Processo
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-8">
        <CaseTable initialCases={filteredCases || []} />
      </div>
    </div>
  )
}
