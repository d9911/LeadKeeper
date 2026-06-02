import { NavLink } from "react-router-dom";

export function NavigationMain() {
  return (
    <nav className="nav">
      <div className="nav-brand">
        <div className="nav-brand-icon">📋</div>
        <span className="nav-brand-name">LeadKeeper</span>
      </div>
      <div className="nav-links">
        <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          📝 Оставить заявку
        </NavLink>
        <NavLink to="/admin" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          📋 Заявки
        </NavLink>
      </div>
    </nav>
  )
}