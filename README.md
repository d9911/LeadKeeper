# LeadKeeper — Lead Capture Module

> Мини-прототип модуля сбора заявок (lead-capture) для Alakris Platform.
> Форма с валидацией, локальное хранение, админ-просмотр заявок.

---

- Lead form: `http://localhost:5173/`
- Admin page: `http://localhost:5173/admin`
- API docs: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/api/health`

<div style="display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; gap: 20px; width: 100%; margin: 24px 0;">
  <div style="flex: 2; text-align: center;">
    <img src="./screenshots/1389.jpg" alt="desktop preview" sstyle="width: 100%; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08);" />
    <p><strong>Desktop</strong></p>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="./screenshots/428.jpg" alt="mobile preview" style="width: 100%; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08);" />
    <p><strong>Mobile</strong></p>
  </div>
</div>

## Возможности

- 📝 Форма заявки с полями: имя, контакт (email/телефон), компания, комментарий
- ✅ Валидация обязательных полей на клиенте и сервере
- 💾 Сохранение заявок в SQLite
- 📋 Служебная страница для просмотра заявок
- 📱 Адаптивный дизайн

## Стек

- **Frontend**: React 18 + TypeScript + Vite + React Router
- **Backend**: Python + FastAPI + SQLAlchemy
- **База данных**: SQLite
- Tooling: Makefile

## Быстрый старт

### 1. Установка зависимостей

```bash
make install
```

Или вручную:

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Запуск

```bash
make dev
```



## Чек-лист проверки

- [ ] `make install` успешно устанавливает зависимости
- [ ] `make dev` запускает приложение без ошибок
- [ ] Форма открывается и отображается корректно
- [ ] Валидация работает: пустая форма показывает ошибки
- [ ] После заполнения формы и отправки показывается сообщение об успехе
- [ ] Заявка появляется на странице `/admin`
- [ ] Таблица заявок отображает все поля корректно

### Ручная проверка

```bash
# Проверка health endpoint
curl http://localhost:8000/api/health

# Проверка создания заявки
curl -X POST http://localhost:8000/api/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"Тест","contact":"test@example.com","consent":true}'

# Просмотр всех заявок
curl http://localhost:8000/api/leads
```

## Допущения

1. **Хранение**: Используется SQLite для простоты. Для production рекомендуется PostgreSQL.
2. **Без авторизации**: Служебная страница `/admin` доступна без авторизации (указано в requirements).
3. **Валидация контакта**: Простая проверка на наличие `@` (email) или цифр (телефон).
4. **Без защиты от спама**: В production нужно добавить rate limiting или captcha.

## Production-риски

1. **Безопасность**: `/admin` должен быть защищён авторизацией (JWT, session) или закрыт VPN/паролем
2. **Спам**: Добавить rate limiting и/или CAPTCHA
3. **Масштабирование**: SQLite не подходит для high load; мигрировать на PostgreSQL
4. **Миграции**: Добавить Alembic для управления схемой БД
5. **Логирование**: Добавить structured logging и мониторинг
6. **Юридическое**: Продумать хранение согласия на обработку данных (GDPR, 152-ФЗ)

## Структура проекта

```
leadkeeper/
├── backend/
│   ├── app/
│   │   ├── main.py      # FastAPI app
│   │   ├── database.py  # DB config
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── crud.py      # CRUD operations
│   ├── requirements.txt
│   └── leadkeeper.db    # SQLite database
├── frontend/
│   ├── src/
│   │   ├── api/leads.ts
│   │   ├── components/
│   │   │   ├── LeadForm.tsx
│   │   │   └── LeadsTable.tsx
│   │   ├── pages/
│   │   │   ├── LeadPage.tsx
│   │   │   └── AdminPage.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── Makefile
├── README.md
└── screenshots/
```

## AI usage

- Планирование структуры проекта
- Генерация boilerplate кода
- Проверка README на полноту

---

**Время выполнения**: ~3 часа