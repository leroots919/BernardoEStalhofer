import { createClient } from '@/lib/supabase/server'
import {
  ArrowLeft,
  FileText,
  Calendar,
  User,
  ShieldCheck,
  Phone,
  ExternalLink,
  ChevronRight,
  FolderOpen,
  AlertCircle
} from 'lucide-react'
import Link from 'next/link'
import { redirect } from 'next/navigation'

export default async function CaseDetailsPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const supabase = await createClient()

  const { data: caseData, error } = await supabase
    .from('client_cases')
    .select(`
      *,
      profiles (name, email, phone),
      services (name, description)
    `)
    .eq('id', id)
    .single()

  if (error || !caseData) {
    redirect('/dashboard/cases')
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
          <h1 className="text-2xl font-bold text-brand-dark">{caseData.title}</h1>
          <p className="text-slate-500 text-sm">ID do Processo: {id}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Main Info */}
        <div className="lg:col-span-2 space-y-8">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/50">
              <h2 className="font-bold text-brand-dark flex items-center gap-2">
                <FileText className="w-5 h-5 text-brand-primary" />
                Informações do Caso
              </h2>
            </div>
            <div className="p-6 space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="space-y-1">
                  <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Serviço Contratado</label>
                  <p className="text-slate-900 font-medium">{caseData.services?.name || 'N/A'}</p>
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Status Atual</label>
                  <div>
                    <StatusBadge status={caseData.status} />
                  </div>
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Data de Criação</label>
                  <p className="text-slate-900">{new Date(caseData.created_at).toLocaleDateString('pt-BR')}</p>
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Última Atualização</label>
                  <p className="text-slate-900">{new Date(caseData.updated_at).toLocaleDateString('pt-BR')}</p>
                </div>
              </div>

              <div className="space-y-1 pt-4 border-t border-slate-100">
                <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Descrição do Caso</label>
                <p className="text-slate-600 leading-relaxed whitespace-pre-wrap">
                  {caseData.description || 'Nenhuma descrição fornecida para este processo.'}
                </p>
              </div>
            </div>
          </div>

          {/* Files Section Quick Link */}
          <div className="bg-brand-primary rounded-2xl p-6 text-white shadow-lg shadow-brand-primary/20 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 rounded-xl">
                <FolderOpen className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg">Documentos do Processo</h3>
                <p className="text-brand-primary/80 text-sm">Envie ou visualize arquivos vinculados a este caso.</p>
              </div>
            </div>
            <Link
              href={`/dashboard/cases/${id}/files`}
              className="bg-white text-brand-primary px-4 py-2 rounded-lg font-bold text-sm hover:bg-brand-primary/10 transition-all flex items-center gap-2"
            >
              Abrir Repositório
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Right Column: Client Details */}
        <div className="space-y-8">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/50">
              <h2 className="font-bold text-brand-dark flex items-center gap-2">
                <User className="w-5 h-5 text-brand-primary" />
                Dados do Cliente
              </h2>
            </div>
            <div className="p-6 space-y-6">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-full bg-brand-primary/10 text-brand-primary flex items-center justify-center font-bold text-lg">
                  {caseData.profiles?.name?.[0].toUpperCase() || 'C'}
                </div>
                <div>
                  <div className="font-bold text-slate-900">{caseData.profiles?.name}</div>
                  <div className="text-xs text-slate-500">{caseData.profiles?.email}</div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-start gap-3 text-sm">
                  <Phone className="w-4 h-4 text-slate-400 mt-0.5" />
                  <span className="text-slate-600">{caseData.profiles?.phone || 'Não informado'}</span>
                </div>
                <div className="flex items-start gap-3 text-sm">
                  <ShieldCheck className="w-4 h-4 text-slate-400 mt-0.5" />
                  <span className="text-slate-600">Cliente Verificado</span>
                </div>
              </div>

              <div className="pt-6 border-t border-slate-100">
                <button className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg border border-slate-200 text-slate-600 text-sm font-medium hover:bg-slate-50 transition-all">
                  <ExternalLink className="w-4 h-4" />
                  Ver Perfil Completo
                </button>
              </div>
            </div>
          </div>

          <div className="bg-amber-50 rounded-2xl p-6 border border-amber-200">
            <div className="flex items-center gap-3 text-amber-800 font-bold mb-3">
              <AlertCircle className="w-5 h-5" />
              Lembrete de Prazo
            </div>
            <p className="text-sm text-amber-700 leading-relaxed">
              Lembre-se de verificar a validade dos prazos recursais para este processo conforme o calendário do tribunal.
            </p>
          </div>
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
