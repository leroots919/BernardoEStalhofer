import { createClient } from '@/lib/supabase/server'
import {
  Briefcase,
  Search,
  Plus,
  Filter,
  MoreVertical,
  ArrowUpRight,
  Clock,
  CheckCircle,
  AlertCircle,
  Archive
} from 'lucide-react'
import Link from 'next/link'

export default async function CasesPage({
  searchParams,
}: {
  searchParams: { status?: string }
}) {
  const supabase = await createClient()
  const currentStatus = searchParams.status

  // Fetch cases with joined data
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

  // Filter locally for simplicity in this demo, or we could do it via Supabase
  const filteredCases = currentStatus
    ? cases?.filter(c => c.status === currentStatus)
    : cases

  const statusOptions = [
    { value: 'pendente', label: 'Pendentes', icon: Clock, color: 'text-amber-600 bg-amber-50 border-amber-200' },
    { value: 'em_andamento', label: 'Em Andamento', icon: AlertCircle, color: 'text-brand-primary bg-brand-primary/10 border-brand-primary/20' },
    { value: 'concluido', label: 'Concluídos', icon: CheckCircle, color: 'text-green-600 bg-green-50 border-green-200' },
    { value: 'arquivado', label: 'Arquivados', icon: Archive, color: 'text-slate-600 bg-slate-50 border-slate-200' },
  ]

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-brand-dark">Gestão de Processos</h1>
          <p className="text-slate-500">Controle e acompanhe todos os casos jurídicos.</p>
        </div>
        <Link
          href="/dashboard/cases/new"
          className="flex items-center justify-center gap-2 bg-brand-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-primary/90 transition-all shadow-sm"
        >
          <Plus className="w-4 h-4" />
          Novo Processo
        </Link>
      </div>

      {/* Status Filters */}
      <div className="flex flex-wrap items-center gap-3">
        <Link
          href="/dashboard/cases"
          className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium border transition-all ${
            !currentStatus
              ? 'bg-brand-primary text-white border-brand-primary'
              : 'bg-white text-slate-600 border-slate-200 hover:border-brand-primary/30'
          }`}
        >
          Todos
        </Link>
        {statusOptions.map((opt) => (
          <Link
            key={opt.value}
            href={`/dashboard/cases?status=${opt.value}`}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium border transition-all ${
              currentStatus === opt.value
                ? 'bg-brand-primary text-white border-brand-primary'
                : 'bg-white text-slate-600 border-slate-200 hover:border-brand-primary/30'
            }`}
          >
            <opt.icon className="w-3.5 h-3.5" />
            {opt.label}
          </Link>
        ))}
      </div>

      {/* Cases Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider font-medium">
              <tr>
                <th className="px-6 py-4">Processo</th>
                <th className="px-6 py-4">Cliente</th>
                <th className="px-6 py-4">Serviço</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Última Atualização</th>
                <th className="px-6 py-4 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredCases && filteredCases.length > 0 ? (
                filteredCases.map((caseItem) => (
                  <tr key={caseItem.id} className="hover:bg-slate-50 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-slate-900">
                        {caseItem.title}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-slate-600">
                        {caseItem.profiles?.name || 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs font-medium px-2 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                        {caseItem.services?.name || 'N/A'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={caseItem.status} />
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-500">
                      {new Date(caseItem.updated_at).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          href={`/dashboard/cases/${caseItem.id}`}
                          className="p-2 text-slate-400 hover:text-brand-primary transition-colors"
                          title="Gerenciar Processo"
                        >
                          <ArrowUpRight className="w-4 h-4" />
                        </Link>
                        <button className="p-2 text-slate-400 hover:text-slate-600 transition-colors">
                          <MoreVertical className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500 italic">
                    Nenhum processo encontrado para este filtro.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    pendente: 'bg-amber-50 text-amber-700 border-amber-200',
    em_andamento: 'bg-brand-primary/10 text-brand-primary border-brand-primary/20',
    concluido: 'bg-green-50 text-green-700 border-green-200',
    arquivado: 'bg-slate-50 text-slate-700 border-slate-200',
  }

  return (
    <span className={`text-xs font-medium px-2.5 py-0.5 rounded-full border ${styles[status] || styles.pendente}`}>
      {status.replace('_', ' ').toUpperCase()}
    </span>
  )
}
