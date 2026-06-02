import { Link, useLocation } from 'react-router-dom';
import { LeadForm } from '../components/LeadForm';

export function LeadPage() {
  const location = useLocation();
  const isActive = location.pathname === '/';

  return (
    <div className="container">
      <nav className="nav">
        <Link to="/" className={`nav-link ${isActive ? 'active' : ''}`}>
          📝 Оставить заявку
        </Link>
        <Link to="/admin" className="nav-link">
          📋 Заявки
        </Link>
      </nav>

      <h1>Свяжитесь с нами</h1>
      <p className="subtitle">
        Оставьте заявку и наш менеджер свяжется с вами в ближайшее время
      </p>

      <LeadForm />
    </div>
  );
}