import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { getLeads, Lead } from '../api/leads';
import { LeadsTable } from '../components/LeadsTable';

export function AdminPage() {
  const location = useLocation();
  const isActive = location.pathname === '/admin';

  const [leads, setLeads] = useState<Lead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadLeads();
  }, []);

  const loadLeads = async () => {
    setIsLoading(true);
    setError(null);

    const result = await getLeads();

    if (result.error) {
      setError(result.error);
    } else if (result.data) {
      setLeads(result.data);
    }

    setIsLoading(false);
  };

  return (
    <div className="container">
      <nav className="nav">
        <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
          📝 Оставить заявку
        </Link>
        <Link to="/admin" className={`nav-link ${isActive ? 'active' : ''}`}>
          📋 Заявки
        </Link>
      </nav>

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
        <button 
          onClick={loadLeads} 
          style={{ marginTop: '1rem', background: 'transparent', color: 'var(--color-primary)', border: '1px solid var(--color-primary)' }}
        >
          🔄 Обновить список
        </button>
      )}
    </div>
  );
}