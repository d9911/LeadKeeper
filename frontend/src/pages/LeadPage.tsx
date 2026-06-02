import { LeadForm } from '../components/LeadForm'

export function LeadPage() {
  return (
    <div className="page-section">
      <h1>Свяжитесь с нами</h1>
      <p className="subtitle">Оставьте заявку и наш менеджер свяжется с вами в ближайшее время</p>

      <div className="tip-banner">Заполните форму — это займёт всего пару минут</div>

      <LeadForm />
    </div>
  )
}
