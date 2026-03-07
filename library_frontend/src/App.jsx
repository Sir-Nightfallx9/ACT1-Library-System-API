import { useResource } from './hooks/useResource'
import { authorsApi, booksApi, membersApi, loansApi } from './api'
import Authors from './components/Authors'
import Books from './components/Books'
import Members from './components/Members'
import Loans from './components/Loans'

function StatCard({ number, label, icon }) {
  return (
    <div className="rounded-2xl p-6 flex flex-col gap-2 transition-all duration-300 hover:-translate-y-1"
      style={{ background: 'var(--surface)', border: '1px solid var(--border)', boxShadow: '0 4px 20px rgba(0,0,0,0.3)' }}>
      <span className="text-3xl">{icon}</span>
      <div className="text-4xl font-bold glow" style={{ color: 'var(--accent)' }}>{number}</div>
      <div className="text-xs uppercase tracking-widest" style={{ color: 'var(--muted)' }}>{label}</div>
    </div>
  )
}

export default function App() {
  const authors = useResource(authorsApi)
  const books = useResource(booksApi)
  const members = useResource(membersApi)
  const loans = useResource(loansApi)

  const anyLoading = authors.loading || books.loading || members.loading || loans.loading
  const anyError = authors.error || books.error || members.error || loans.error

  return (
    <div className="min-h-screen grid-bg">
      <header className="sticky top-0 z-40 px-8 py-4 flex items-center justify-between"
        style={{ background: 'rgba(8,11,20,0.9)', borderBottom: '1px solid var(--border)', backdropFilter: 'blur(10px)' }}>
        <div className="flex items-center gap-3">
          <span className="text-2xl">🐺</span>
          <span className="text-lg font-bold" style={{ color: 'var(--accent)' }}>Library System</span>
        </div>
        <div className="flex items-center gap-4 text-xs" style={{ color: 'var(--muted)' }}>
          <a href="http://localhost:8000/admin/" target="_blank" rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-lg transition-all hover:bg-white/5" style={{ border: '1px solid var(--border)' }}>
            🔐 Django Admin
          </a>
          <a href="http://localhost:8000/api/" target="_blank" rel="noopener noreferrer"
            className="px-3 py-1.5 rounded-lg transition-all hover:bg-white/5" style={{ border: '1px solid var(--border)' }}>
            ⚙️ API Browser
          </a>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full" style={{ background: anyError ? '#f43f5e' : anyLoading ? '#f59e0b' : 'var(--success)' }} />
            <span>{anyError ? 'API Error' : anyLoading ? 'Loading…' : 'Connected'}</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-8 py-10">
        <div className="mb-10">
          <h1 className="text-5xl font-extrabold mb-2 glow">
            Library <span style={{ color: 'var(--accent)' }}>Dashboard</span>
          </h1>
          <p className="text-sm" style={{ color: 'var(--muted)' }}>Full CRUD — Authors · Books · Members · Loans</p>
        </div>

        {anyError && (
          <div className="mb-8 px-5 py-4 rounded-xl text-sm" style={{ background: 'rgba(244,63,94,0.1)', border: '1px solid rgba(244,63,94,0.3)', color: '#fda4af' }}>
            ⚠️ Could not connect to Django API. Make sure your Django server is running with <code className="mx-1">python manage.py runserver</code>.
          </div>
        )}

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
          <StatCard number={authors.data.length} label="Authors" icon="✍️" />
          <StatCard number={books.data.length} label="Books" icon="📖" />
          <StatCard number={members.data.length} label="Members" icon="👥" />
          <StatCard number={loans.data.length} label="Loans" icon="📋" />
        </div>

        <Authors data={authors.data} onCreate={authors.create} onUpdate={authors.update} onDelete={authors.remove} />
        <Books data={books.data} authors={authors.data} onCreate={books.create} onUpdate={books.update} onDelete={books.remove} />
        <Members data={members.data} onCreate={members.create} onUpdate={members.update} onDelete={members.remove} />
        <Loans data={loans.data} members={members.data} books={books.data} onCreate={loans.create} onUpdate={loans.update} onDelete={loans.remove} />
      </main>
    </div>
  )
}