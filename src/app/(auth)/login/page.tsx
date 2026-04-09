'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import { Loader2, Lock, Mail, ArrowLeft } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) throw error

      router.push('/dashboard')
      router.refresh()
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Erro ao realizar login. Verifique suas credenciais.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const quickLogin = (role: 'admin' | 'client') => {
    if (role === 'admin') {
      setEmail('admin@teste.com')
      setPassword('admin123')
    } else {
      setEmail('cliente@teste.com')
      setPassword('cliente123')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <Link href="/" className="flex items-center gap-2 text-slate-500 hover:text-brand-primary transition-colors mb-8 group">
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          Voltar para a página inicial
        </Link>
        <div className="text-center">
          <img src="/bs-logo.png" alt="Bernardo & Stahlhöfer Logo" className="mx-auto h-12 w-auto mb-6" />
          <h2 className="text-3xl font-serif font-bold text-slate-900">Área do Cliente</h2>
          <p className="mt-2 text-sm text-slate-600">
            Acesse seu portal para acompanhar seu processo e documentos.
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-xl border border-slate-200 sm:rounded-[32px] sm:px-10">
          <div className="mb-8 p-4 bg-slate-50 rounded-2xl border border-slate-100">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest text-center mb-4">Acesso Rápido (Testes)</p>
            <div className="flex gap-3">
              <button
                onClick={() => quickLogin('admin')}
                className="flex-1 py-2 px-3 rounded-xl bg-white border border-slate-200 text-slate-600 text-xs font-bold hover:border-brand-primary hover:text-brand-primary transition-all shadow-sm"
              >
                Admin
              </button>
              <button
                onClick={() => quickLogin('client')}
                className="flex-1 py-2 px-3 rounded-xl bg-white border border-slate-200 text-slate-600 text-xs font-bold hover:border-brand-primary hover:text-brand-primary transition-all shadow-sm"
              >
                Cliente
              </button>
            </div>
          </div>

          <form className="space-y-6" onSubmit={handleLogin}>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">E-mail</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-brand-primary/10 focus:border-brand-primary outline-none transition-all bg-slate-50/50"
                  placeholder="seu@email.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Senha</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-11 pr-4 py-3 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-brand-primary/10 focus:border-brand-primary outline-none transition-all bg-slate-50/50"
                  placeholder="••••••••"
                />
              </div>
            </div>

            {error && (
              <div className="p-4 rounded-2xl bg-red-50 text-red-600 text-sm font-medium border border-red-100">
                {error}
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-2xl shadow-sm text-sm font-bold text-white bg-brand-primary hover:bg-brand-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary transition-all disabled:opacity-70"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Entrar no Portal'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
