export function FooterMain() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-grid">
          <div>
            <div className="footer-brand">
              <div className="footer-brand-icon">📋</div>
              <span className="footer-brand-name">LeadKeeper</span>
            </div>
            <p className="footer-description">Модуль для сбора и управления заявками с клиентских сайтов. Разработка сайтов под ключ — быстро, качественно, с гарантией результата.</p>
            <div className="footer-author">
              <span className="footer-author-name">Denis Gutsuliak</span>
              <a href="mailto:admin@d9911.org" className="footer-author-link">
                📧 admin@d9911.org
              </a>
              <a href="https://t.me/d9911/" target="_blank" rel="noopener noreferrer" className="footer-author-link">
                💬 Telegram: @d9911
              </a>
            </div>
          </div>

          <div>
            <h4 className="footer-section-title">Навигация</h4>
            <ul className="footer-links">
              <li>
                <a href="/">Форма заявки</a>
              </li>
              <li>
                <a href="/admin">Просмотр заявок</a>
              </li>
              <li>
                <a href="/api/health">API</a>
              </li>
              <li>
                <a href="/docs">Документация</a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="footer-section-title">Услуги</h4>
            <ul className="footer-links">
              <li>
                <a href="https://t.me/d9911/" target="_blank" rel="noopener noreferrer">
                  Разработка сайтов
                </a>
              </li>
              <li>
                <a href="https://t.me/d9911/" target="_blank" rel="noopener noreferrer">
                  Frontend разработка
                </a>
              </li>
              <li>
                <a href="https://t.me/d9911/" target="_blank" rel="noopener noreferrer">
                  Backend разработка
                </a>
              </li>
              <li>
                <a href="https://t.me/d9911/" target="_blank" rel="noopener noreferrer">
                  Интеграции
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <span className="footer-copyright">© {new Date().getFullYear()} LeadKeeper. Все права защищены.</span>
          <div className="footer-privacy">
            <a href="#">Политика конфиденциальности</a>
            <a href="#">Условия использования</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
