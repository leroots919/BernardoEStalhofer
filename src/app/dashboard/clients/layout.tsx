import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'

export default async function ClientsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  const { data: profile } = await supabase
    .from('profiles')
    .select('type')
    .eq('id', user.id)
    .single()

  if (profile?.type !== 'admin') {
    redirect('/dashboard/cases')
  }

  return <>{children}</>
}
