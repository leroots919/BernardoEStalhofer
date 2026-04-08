'use client'

import { useActionState } from 'react'
import { register, AuthState } from '@/app/(auth)/actions'

const initialState: AuthState = {
  success: false,
  message: '',
}

export default function RegisterPage() {
  const [state, formAction, isPending] = useActionState(register, initialState)

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg border border-slate-200">
        <div className="text-center">
          <h2 className="text-3xl font-serif font-bold text-slate-900">Criar Conta</h2>
          <p className="mt-2 text-sm text-slate-600">Cadastre-se para gerir seus processos</p>
        </div>

        <form action={formAction} className="mt-8 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Nome Completo</label>
              <input
                name="name"
                type="text"
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                placeholder="Nome do Advogado"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input
                name="email"
                type="email"
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                placeholder="seu@email.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Senha</label>
              <input
                name="password"
                type="password"
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                placeholder="••••••••"
              />
            </div>
          </div>

          {state.message && (
            <div className={`p-3 rounded-md text-sm ${state.success ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'}`}>
              {state.message}
            </div>
          )}

          <button
            type="submit"
            disabled={isPending}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors"
          >
            {isPending ? 'Cadastrando...' : 'Criar Conta'}
          </button>
        </form>

        <div className="text-center text-sm text-slate-500">
          Já possui uma conta? <a href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">Faça login aqui</a>
        </div>
      </div>
    </div>
  )
}
