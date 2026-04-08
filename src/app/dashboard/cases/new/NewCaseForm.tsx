'use client'

import React, { useState } from 'react'
import { useActionState } from 'react'
import { createCase, ActionResponse } from '@/app/dashboard/actions'
import { useRouter } from 'next/navigation'
import { Loader2, CheckCircle } from 'lucide-react'

interface Client {
  id: string
  name: string
  email: string
}

interface Service {
  id: string
  name: string
}

export default function NewCaseForm({ clients, services }: { clients: Client[], services: Service[] }) {
  const router = useRouter()
  const [state, formAction, isPending] = useActionState(createCase, {
    success: false,
    message: '',
  })

  return (
    <form action={formAction} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Client Selection */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700">Cliente</label>
          <select
            name="userId"
            required
            className="w-full px-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-brand-primary outline-none transition-all text-sm"
          >
            <option value="">Selecione o Cliente</option>
            {clients.map(client => (
              <option key={client.id} value={client.id}>
                {client.name} ({client.email})
              </option>
            ))}
          </select>
        </div>

        {/* Service Selection */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700">Serviço</label>
          <select
            name="serviceId"
            required
            className="w-full px-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-brand-primary outline-none transition-all text-sm"
          >
            <option value="">Selecione o Serviço</option>
            {services.map(service => (
              <option key={service.id} value={service.id}>
                {service.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Case Title */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-700">Título do Processo</label>
        <input
          name="title"
          type="text"
          required
          placeholder="Ex: Recurso Multa Velocidade - Cliente X"
          className="w-full px-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-brand-primary outline-none transition-all text-sm"
        />
      </div>

      {/* Case Description */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-700">Descrição Detalhada</label>
        <textarea
          name="description"
          rows={4}
          placeholder="Descreva os detalhes do caso, prazos e observações importantes..."
          className="w-full px-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-brand-primary outline-none transition-all text-sm"
        />
      </div>

      {/* Status Selection */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-700">Status Inicial</label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {['pendente', 'em_andamento', 'concluido', 'arquivado'].map((status) => (
            <label key={status} className="relative flex items-center gap-2 p-3 rounded-lg border border-slate-200 bg-white cursor-pointer hover:bg-slate-50 transition-all group">
              <input
                type="radio"
                name="status"
                value={status}
                defaultChecked={status === 'pendente'}
                className="w-4 h-4 text-brand-primary border-slate-300 focus:ring-brand-primary"
              />
              <span className="text-xs font-medium text-slate-600 capitalize">
                {status.replace('_', ' ')}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Feedback Message */}
      {state.message && (
        <div className={`p-4 rounded-lg text-sm font-medium border ${
          state.success
            ? 'bg-green-50 text-green-700 border-green-200'
            : 'bg-red-50 text-red-700 border-red-200'
        }`}>
          {state.message}
        </div>
      )}

      <div className="flex justify-end gap-4 pt-4">
        <button
          type="button"
          onClick={() => router.push('/dashboard/cases')}
          className="px-6 py-2 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-100 transition-all"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isPending}
          className="flex items-center justify-center gap-2 bg-brand-primary text-white px-6 py-2 rounded-lg font-bold text-sm hover:bg-brand-primary/90 transition-all disabled:opacity-50 shadow-lg shadow-brand-primary/20"
        >
          {isPending ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Criando Processo...
            </>
          ) : (
            <>
              <CheckCircle className="w-4 h-4" />
              Criar Processo
            </>
          )}
        </button>
      </div>
    </form>
  )
}
