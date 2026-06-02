import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { FooterMain } from './components/FooterMain'
import { LeadPage } from './pages/LeadPage'
import { AdminPage } from './pages/AdminPage'
import { NavigationMain } from './components/NavigationMain'



function App() {
  return (
    <BrowserRouter>
      <NavigationMain />
      <div className="main-content">
        <div className="container">
          <Routes>
            <Route path="/" element={<LeadPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </div>
      </div>
      <FooterMain />
    </BrowserRouter>
  )
}

export default App
