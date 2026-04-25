import React from 'react'
import Link from 'next/link'
import {
  LayoutDashboard,
  Users,
  Briefcase,
  Settings,
  LogOut,
  FileText,
  ChevronRight
} from 'lucide-react'
import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/login')
  }

  const { data: profile } = await supabase
    .from('profiles')
    .select('type')
    .eq('id', user.id)
    .single()

  const isAdmin = profile?.type === 'admin'

  const navItems = [
    { name: 'Visão Geral', href: '/dashboard', icon: LayoutDashboard },
    ...(isAdmin ? [
      { name: 'Clientes', href: '/dashboard/clients', icon: Users },
      { name: 'Configurações', href: '/dashboard/settings', icon: Settings },
    ] : []),
    { name: 'Processos', href: '/dashboard/cases', icon: Briefcase },
    { name: 'Documentos', href: '/dashboard/documents', icon: FileText },
  ]

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-brand-dark text-slate-300 flex flex-col sticky top-0 h-screen transition-all">
        <div className="p-6 flex items-center gap-3 border-b border-slate-800">
          <div className="w-8 h-8 bg-brand-primary rounded flex items-center justify-center text-white font-bold">
            BS
          </div>
          <span className="font-serif font-bold text-lg text-white truncate">
            {isAdmin ? 'Painel Admin' : 'Meu Portal'}
          </span>
        </div>

        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center justify-between px-4 py-3 rounded-lg hover:bg-slate-800 hover:text-white transition-all group"
            >
              <div className="flex items-center gap-3">
                <item.icon className="w-5 h-5 group-hover:text-brand-primary transition-colors" />
                <span className="text-sm font-medium">{item.name}</span>
              </div>
              <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-all" />
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-800">
          <form action={async () => {
            'use server'
            const supabase = await createClient()
            await supabase.auth.signOut()
            redirect('/login')
          }}>
            <button className="flex items-center gap-3 w-full px-4 py-3 rounded-lg text-sm font-medium text-slate-400 hover:bg-red-900/20 hover:text-red-400 transition-all">
              <LogOut className="w-5 h-5" />
              Sair do Sistema
            </button>
          </form>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
          <h1 className="text-slate-900 font-semibold">
            {/* The title will be handled by the page components */}
          </h1>

          <div className="flex items-center gap-4">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium text-slate-900">{user.email}</p>
              <p className="text-xs text-slate-500">{isAdmin ? 'Administrador' : 'Cliente'}</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-brand-primary/10 text-brand-primary flex items-center justify-center font-bold border border-brand-primary/20">
              {user.email?.[0].toUpperCase()}
            </div>
          </div>
        </header>

        <div className="p-8 overflow-y-auto">
          {children}
        </div>
      </main>
    </div>
  )
}
