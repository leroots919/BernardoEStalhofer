import { createClient } from '@/lib/supabase/server'
import {
  Users,
  Search,
  Plus,
  Mail,
  Phone,
  MoreVertical,
  ExternalLink
} from 'lucide-react'
import Link from 'next/link'

export default async function ClientsPage() {
  const supabase = await createClient()

  const { data: clients, error } = await supabase
    .from('profiles')
    .select('*')
    .eq('type', 'cliente')
    .order('name', { ascending: true })

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700">
        Erro ao carregar clientes: {error.message}
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-brand-dark">Gestão de Clientes</h1>
          <p className="text-slate-500">Gerencie todos os clientes cadastrados no sistema.</p>
        </div>
        <button className="flex items-center justify-center gap-2 bg-brand-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-primary/90 transition-all shadow-sm">
          <Plus className="w-4 h-4" />
          Novo Cliente
        </button>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Buscar cliente por nome ou email..."
            className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-brand-primary outline-none transition-all text-sm"
          />
        </div>
      </div>

      {/* Clients Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider font-medium">
              <tr>
                <th className="px-6 py-4">Cliente</th>
                <th className="px-6 py-4">Contato</th>
                <th className="px-6 py-4">Localização</th>
                <th className="px-6 py-4">Data Cadastro</th>
                <th className="px-6 py-4 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {clients && clients.length > 0 ? (
                clients.map((client) => (
                  <tr key={client.id} className="hover:bg-slate-50 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-brand-primary/10 text-brand-primary flex items-center justify-center font-bold text-sm">
                          {client.name?.[0].toUpperCase() || 'C'}
                        </div>
                        <div>
                          <div className="text-sm font-medium text-brand-dark">
                            {client.name}
                          </div>
                          <div className="text-xs text-slate-500">{client.username || 'sem username'}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col gap-1">
                        <div className="flex items-center gap-2 text-xs text-slate-600">
                          <Mail className="w-3 h-3" />
                          {client.email}
                        </div>
                        <div className="flex items-center gap-2 text-xs text-slate-600">
                          <Phone className="w-3 h-3" />
                          {client.phone || 'Não informado'}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-xs text-slate-600">
                        {client.city}, {client.state}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-500">
                      {new Date(client.register_date).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          href={`/dashboard/clients/${client.id}`}
                          className="p-2 text-slate-400 hover:text-brand-primary transition-colors"
                          title="Ver Detalhes"
                        >
                          <ExternalLink className="w-4 h-4" />
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
                  <td colSpan={5} className="px-6 py-12 text-center text-slate-500 italic">
                    Nenhum cliente encontrado.
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
