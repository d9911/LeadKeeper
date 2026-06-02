import { Link, useLocation } from 'react-router-dom'
import { LeadForm } from '../components/LeadForm'

export function LeadPage() {
  const location = useLocation()

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
        <h1>Свяжитесь с нами</h1>
        <p className="subtitle">Оставьте заявку и наш менеджер свяжется с вами в ближайшее время</p>

        <div className="tip-banner">Заполните форму — это займёт всего пару минут</div>

        <LeadForm />
      </div>
    </div>
  )
}
