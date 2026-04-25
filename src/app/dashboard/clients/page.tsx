import { createClient } from '@/lib/supabase/server'
import ClientTable from './ClientTable'
import CreateClientModal from './CreateClientModal'

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
          <h1 className="text-3xl font-serif font-bold text-brand-dark tracking-tight">Gestão de Clientes</h1>
          <p className="text-slate-500">Gerencie todos os clientes cadastrados no sistema.</p>
        </div>
        <CreateClientModal />
      </div>

      <ClientTable initialClients={clients || []} />
    </div>
  )
}
