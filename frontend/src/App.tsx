import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { Footer } from './components/Footer'
import { LeadPage } from './pages/LeadPage'
import { AdminPage } from './pages/AdminPage'

function Navigation() {
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

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <div className="container">
        <Routes>
          <Route path="/" element={<LeadPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </div>
      <Footer />
    </BrowserRouter>
  )
}

export default App
