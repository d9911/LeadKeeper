import { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { getLeads, Lead } from '../api/leads'
import { LeadsTable } from '../components/LeadsTable'

export function AdminPage() {
  const location = useLocation()

  const [leads, setLeads] = useState<Lead[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadLeads()
  }, [])

  const loadLeads = async () => {
    setIsLoading(true)
    setError(null)

    const result = await getLeads()

    if (result.error) {
      setError(result.error)
    } else if (result.data) {
      setLeads(result.data)
    }

    setIsLoading(false)
  }

  return (
    <div className="container">
      <nav className="nav">
        <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
          📝 Оставить заявку
        </Link>
        <Link to="/admin" className={`nav-link ${location.pathname === '/admin' ? 'active' : ''}`}>
          📋 Заявки
        </Link>
      </nav>

      <div className="page-section">
        <div className="admin-header">
          <div>
            <h1>Заявки</h1>
            <p className="subtitle">Служебная страница для просмотра поступивших заявок</p>
          </div>
          <span className="badge">{leads.length} заявок</span>
        </div>

        <div className="card">
          <LeadsTable leads={leads} isLoading={isLoading} error={error} />
        </div>

        {!isLoading && !error && leads.length > 0 && (
          <div style={{ marginTop: '16px', textAlign: 'center' }}>
            <button className="btn btn-secondary" onClick={loadLeads} style={{ width: 'auto', display: 'inline-flex' }}>
              🔄 Обновить список
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
