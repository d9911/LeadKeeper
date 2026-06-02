# LeadKeeper — Отчёт о выполнении

## Что сделано

1. **Fullstack-приложение** с React + TypeScript (frontend) и FastAPI + SQLite (backend)
2. **Форма заявки** с отдельными полями: имя, телефон, email, компания, комментарий, согласие
3. **Строгая валидация** на клиенте и сервере:
   - Телефон: `+КодСтраны Номер` (максимум 16 цифр после +)
   - Email: RFC 5322 compliant
   - Хотя бы один контакт обязателен
4. **SQLite база данных**: заявки сохраняются локально
5. **Email-уведомления** через SMTP:
   - Красивый HTML-шаблон для владельца
   - Подтверждение пользователю
   - Настройка через `.env` файл
6. **Служебная страница `/admin`**: таблица с phone/email колонками
7. **PostHog-inspired дизайн**: кремовый фон, жёлто-оранжевый акцент, минимализм
8. **Makefile** для Linux/macOS + **make.bat** для Windows
9. **README.md**: полная документация, чек-лист, валидация, email

## Дизайн-система

| Элемент | Значение                    |
| ------- | --------------------------- |
| Фон     | `#eeefe9` — тёплый кремовый |
| Primary | `#f7a501` — жёлто-оранжевый |
| Ink     | `#23251d` — олив-чаркоал    |
| Body    | `#4d4f46` — олив-серый      |
| Cards   | белые с 1px границей        |
| Radius  | 4–8px                       |

## Строгая валидация

### Телефон

```
+7 999 123-45-67  ✓
+44 20 7946 0958  ✓
+1 (555) 123-4567 ✓
1234567890        ✓ (без +)
+12345678901234567 ✗ (слишком длинный)
```

### Email

```
ivan@example.com        ✓
user.name@company.co.uk ✓
user_name@mail.ru       ✓
user..name@mail.ru      ✗ (две точки)
.user@mail.ru           ✗ (начинается с точки)
user.@mail.ru           ✗ (заканчивается точкой)
```

## Не делал намеренно

- Авторизация `/admin` — указано в requirements
- Интеграция с CRM, Telegram
- Docker / сложная инфраструктура
- Сложный дизайн (только аккуратный PostHog-inspired UI)
- Production-миграции, логирование, мониторинг
- Защита от спама (rate limiting / CAPTCHA)
## Допущения

1. **SQLite** — подходит для прототипа, для production нужен PostgreSQL
2. **Валидация контакта** — простая (email с @ или телефон с цифрами)
3. **Без защиты от спама** — в production нужны rate limiting или captcha
4. **Согласие** — чекбокс, в production нужна юридически корректная форма
## Production-риски

- `/admin` открыт → добавить JWT или VPN
- Нет защиты от спама → CAPTCHA
- SQLite → PostgreSQL для масштабирования
- Нет миграций → Alembic
- Email через SMTP → SendGrid / SES

## AI usage

- Планирование структуры проекта
- Генерация boilerplate (FastAPI, React)
- Дизайн-система (PostHog-inspired)
- Email-шаблоны (HTML/CSS)
- Валидация (RFC 5322, phone format)

## Проверка

```bash
make install
make dev

# Открыть http://localhost:5173
# Заполнить форму и отправить
# Проверить http://localhost:5173/admin
```

## Время

~4 часа (в рамках оценки 2-4 часа + доп. функционал)

## Технический стек

- **Frontend**: React 18, TypeScript, Vite 5, React Router 6
- **Backend**: Python 3.13, FastAPI 0.115, SQLAlchemy 2.0
- **База**: SQLite
- **Email**: SMTP + python-dotenv
- **Запуск**: Makefile (Linux) + make.bat (Windows)
- **Дизайн**: PostHog-inspired CSS (cream canvas, yellow-orange accent, minimal style)
