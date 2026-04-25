import { createClient } from '@/lib/supabase/server'
import {
  Briefcase,
} from 'lucide-react'
import Link from 'next/link'
import CaseTable from './CaseTable'
import CreateCaseModal from './CreateCaseModal'

interface CaseItem {


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
        <CreateCaseModal />
      </div>
      </div>

      <div className="grid grid-cols-1 gap-8">
        <CaseTable initialCases={filteredCases || []} />
      </div>
    </div>
  )
}
