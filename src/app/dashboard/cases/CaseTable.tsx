'use client'

import React, { useState, useMemo } from 'react'
import {
  ArrowUpRight,
  MoreVertical,
  Search,
  CheckCircle,
  Clock,
  AlertCircle,
  Archive,
  Filter,
  Trash2
} from 'lucide-react'
import Link from 'next/link'
import { updateCasesStatusBulk } from '@/app/dashboard/actions'

interface CaseItem {
  id: string
  title: string
  status: string
  created_at: string
  updated_at: string
  profiles: { name: string; email: string } | { name: string; email: string }[]
  services: { name: string } | { name: string }[]
}

interface CaseTableProps {
  initialCases: CaseItem[]
}

export default function CaseTable({ initialCases }: CaseTableProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())
  const [isUpdating, setIsUpdating] = useState(false)

  const filteredCases = useMemo(() => {
    return initialCases.filter(c =>
      c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (Array.isArray(c.profiles) ? c.profiles[0]?.name.toLowerCase() : c.profiles?.name?.toLowerCase()).includes(searchQuery.toLowerCase())
    )
  }, [initialCases, searchQuery])

  const toggleSelectAll = () => {
    if (selectedIds.size === filteredCases.length) {
      setSelectedIds(new Set())
    } else {
      setSelectedIds(new Set(filteredCases.map(c => c.id)))
    }
  }

  const toggleSelect = (id: string) => {
    const newSelected = new Set(selectedIds)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else {
      newSelected.add(id)
    }
    setSelectedIds(newSelected)
  }

  const handleBulkUpdate = async (status: string) => {
    if (selectedIds.size === 0) return

    setIsUpdating(true)
    const result = await updateCasesStatusBulk(Array.from(selectedIds), status)

    if (result.success) {
      setSelectedIds(new Set())
      // In a real app, we might use a state management library or refresh the page
      window.location.reload()
    } else {
      alert(result.message)
    }
    setIsUpdating(false)
  }

  const getClientName = (profiles: CaseItem['profiles']) => {
    return (Array.isArray(profiles) ? profiles[0]?.name : profiles?.name) || 'N/A'
  }

  const getServiceName = (services: CaseItem['services']) => {
    return (Array.isArray(services) ? services[0]?.name : services?.name) || 'N/A'
  }

  return (
    <div className="space-y-6">
      {/* Toolbar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Buscar processo ou cliente..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-brand-primary outline-none transition-all text-sm"
          />
        </div>

        <div className="flex items-center gap-3">
          {selectedIds.size > 0 && (
            <div className="flex items-center gap-2 animate-in fade-in slide-in-from-right-4 duration-300">
              <span className="text-xs font-bold text-slate-500 mr-2">
                {selectedIds.size} selecionados
              </span>
              <select
                onChange={(e) => handleBulkUpdate(e.target.value)}
                className="text-xs font-medium bg-brand-primary text-white rounded-lg px-3 py-2 outline-none cursor-pointer hover:bg-brand-dark transition-all"
                value=""
              >
                <option value="" disabled>Atualizar status...</option>
                <option value="pendente">Pendente</option>
                <option value="em_andamento">Em Andamento</option>
                <option value="concluido">Concluído</option>
                <option value="arquivado">Arquivado</option>
              </select>
            </div>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-[32px] border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50/50 text-slate-500 text-[11px] uppercase tracking-widest font-bold">
              <tr>
                <th className="px-6 py-4 w-10">
                  <input
                    type="checkbox"
                    checked={selectedIds.size === filteredCases.length && filteredCases.length > 0}
                    onChange={toggleSelectAll}
                    className="rounded border-slate-300 text-brand-primary focus:ring-brand-primary"
                  />
                </th>
                <th className="px-6 py-4">Processo</th>
                <th className="px-6 py-4">Cliente</th>
                <th className="px-6 py-4">Serviço</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Atualização</th>
                <th className="px-6 py-4 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredCases.length > 0 ? (
                filteredCases.map((caseItem) => (
                  <tr
                    key={caseItem.id}
                    className={`group transition-all ${selectedIds.has(caseItem.id) ? 'bg-brand-primary/5' : 'hover:bg-slate-50'}`}
                  >
                    <td className="px-6 py-4">
                      <input
                        type="checkbox"
                        checked={selectedIds.has(caseItem.id)}
                        onChange={() => toggleSelect(caseItem.id)}
                        className="rounded border-slate-300 text-brand-primary focus:ring-brand-primary"
                      />
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-bold text-slate-900">{caseItem.title}</div>
                      <div className="text-[10px] text-slate-400 font-medium uppercase">ID: {caseItem.id.substring(0, 8)}...</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-slate-600 font-medium">{getClientName(caseItem.profiles)}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                        {getServiceName(caseItem.services)}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={caseItem.status} />
                    </td>
                    <td className="px-6 py-4 text-xs text-slate-500 font-medium">
                      {new Date(caseItem.updated_at).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Link
                          href={`/dashboard/cases/${caseItem.id}`}
                          className="p-2 text-slate-400 hover:text-brand-primary transition-colors bg-slate-50 rounded-lg hover:bg-brand-primary/10"
                          title="Gerenciar Processo"
                        >
                          <ArrowUpRight className="w-4 h-4" />
                        </Link>
                        <button className="p-2 text-slate-400 hover:text-slate-600 transition-colors bg-slate-50 rounded-lg hover:bg-slate-100">
                          <MoreVertical className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="px-6 py-20 text-center">
                    <div className="flex flex-col items-center gap-3 text-slate-400">
                      <Search className="w-8 h-8 opacity-20" />
                      <p className="text-sm italic">Nenhum processo corresponde à sua busca.</p>
                    </div>
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
    <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full border uppercase tracking-wider ${styles[status] || styles.pendente}`}>
      {status.replace('_', ' ').toUpperCase()}
    </span>
  )
}
