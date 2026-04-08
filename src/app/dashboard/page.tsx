export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <h1 className="text-3xl font-serif font-bold text-slate-900">Lawyer Dashboard</h1>
      <p className="mt-4 text-slate-600">Welcome to your secure portal.</p>
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded-xl shadow-sm border border-slate-200">
          <h3 className="text-lg font-medium text-slate-900">Active Cases</h3>
          <p className="text-3xl font-bold text-indigo-600">12</p>
        </div>
        <div className="p-6 bg-white rounded-xl shadow-sm border border-slate-200">
          <h3 className="text-lg font-medium text-slate-900">Pending Consultations</h3>
          <p className="text-3xl font-bold text-indigo-600">5</p>
        </div>
        <div className="p-6 bg-white rounded-xl shadow-sm border border-slate-200">
          <h3 className="text-lg font-medium text-slate-900">Documents to Review</h3>
          <p className="text-3xl font-bold text-indigo-600">8</p>
        </div>
      </div>
    </div>
  )
}
