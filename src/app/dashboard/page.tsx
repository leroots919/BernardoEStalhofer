import { createClient } from '@/lib/supabase/server'
import {
  Briefcase,
  Clock,
  CheckCircle,
  AlertCircle,
  ArrowUpRight
} from 'lucide-react'
import Link from 'next/link'

export default async function DashboardPage() {
  const supabase = await createClient()

  // Fetch stats
  const { count: totalCases } = await supabase
    .from('client_cases')
    .select('*', { count: 'exact', head: true })

  const { count: pendingCases } = await supabase
    .from('client_cases')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'pendente')

  const { count: activeCases } = await supabase
    .from('client_cases')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'em_andamento')

  const { count: completedCases } = await supabase
    .from('client_cases')
    .select('*', { count: 'exact', head: true })
    .eq('status', 'concluido')

  // Fetch recent cases with profile info
  const { data: recentCases } = await supabase
    .from('client_cases')
    .select(`
      id,
      title,
      status,
      created_at,
      profiles (name, email),
      services (name)
    `)
    .order('created_at', { ascending: false })
    .limit(5)

  const stats = [
    {
      label: 'Total de Processos',
      value: totalCases || 0,
      icon: Briefcase,
      color: 'text-blue-600',
      bg: 'bg-blue-50',
    },
    {
      label: 'Pendentes',
      value: pendingCases || 0,
      icon: Clock,
      color: 'text-amber-600',
      bg: 'bg-amber-50',
    },
    {
      label: 'Em Andamento',
      value: activeCases || 0,
      icon: AlertCircle,
      color: 'text-brand-primary',
      bg: 'bg-brand-primary/10',
    },
    {
      label: 'Concluídos',
      value: completedCases || 0,
      icon: CheckCircle,
      color: 'text-green-600',
      bg: 'bg-green-50',
    },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-brand-dark">Visão Geral</h1>
        <p className="text-slate-500">Bem-vindo ao seu painel de gestão de processos.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div key={idx} className="p-6 bg-white rounded-2xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-2 rounded-lg ${stat.bg} ${stat.color}`}>
                <stat.icon className="w-6 h-6" />
              </div>
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Atual</span>
            </div>
            <div className="text-3xl font-bold text-brand-dark mb-1">{stat.value}</div>
            <div className="text-sm text-slate-500 font-medium">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Recent Activity Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-slate-200 flex items-center justify-between">
          <h2 className="text-lg font-bold text-brand-dark">Processos Recentes</h2>
          <Link
            href="/dashboard/cases"
            className="text-sm font-medium text-brand-primary hover:text-brand-primary/80 flex items-center gap-1 transition-colors"
          >
            Ver todos <ArrowUpRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider font-medium">
              <tr>
                <th className="px-6 py-4">Cliente</th>
                <th className="px-6 py-4">Processo</th>
                <th className="px-6 py-4">Serviço</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Data</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {recentCases && recentCases.length > 0 ? (
                recentCases.map((caseItem) => (
                  <tr key={caseItem.id} className="hover:bg-slate-50 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-brand-dark">
                        {(Array.isArray(caseItem.profiles) ? (caseItem.profiles[0] as {name: string})?.name : (caseItem.profiles as {name: string})?.name) || 'N/A'}
                      </div>
                      <div className="text-xs text-slate-500">
                        {(Array.isArray(caseItem.profiles) ? (caseItem.profiles[0] as {email: string})?.email : (caseItem.profiles as {email: string})?.email)}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600">
                      {caseItem.title}
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs font-medium px-2 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                        {(Array.isArray(caseItem.services) ? (caseItem.services[0] as {name: string})?.name : (caseItem.services as {name: string})?.name) || 'N/A'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={caseItem.status} />
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-500">
                      {new Date(caseItem.created_at).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        href={`/dashboard/cases/${caseItem.id}`}
                        className="p-2 text-slate-400 hover:text-brand-primary transition-colors"
                      >
                        <ArrowUpRight className="w-4 h-4" />
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500 italic">
                    Nenhum processo encontrado.
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
