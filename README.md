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
## Что сделано

- Форма заявки с обязательными полями.
- Клиентская и серверная валидация.
- Сохранение заявок в SQLite.
- Служебная страница для просмотра заявок.
- Запуск через Makefile.
- Короткий чек-лист проверки.

## Стек

- Frontend: React, TypeScript, Vite
- Backend: Python, FastAPI
- Database: SQLite
- ORM: SQLAlchemy
- Tooling: Makefile

## Как запустить

make install
make dev

## Как проверить

1. Открыть форму.
2. Попробовать отправить пустую форму.
3. Заполнить имя, контакт и согласие.
4. Отправить заявку.
5. Открыть `/admin`.
6. Проверить, что заявка появилась в списке.

## Допущения

- Авторизация для админского экрана не реализована, так как она исключена из задания.
- SQLite используется как простой локальный storage для прототипа.
- В production админский экран нужно защитить авторизацией.
- В production SQLite лучше заменить на PostgreSQL.
- Внешние CRM, Telegram и email-интеграции не подключались.

## Production-риски

- Нужна авторизация и роли для служебного экрана.
- Нужна защита от спама: rate limit, captcha или honeypot.
- Нужна серверная проверка и нормализация телефона/email.
- Нужны миграции базы данных.
- Нужны логи ошибок и мониторинг.
- Нужно хранить согласие на обработку данных корректно с учётом политики клиента.

## AI usage

AI использовался как помощник для планирования структуры, проверки README и формулировки production-рисков. Код был проверен вручную через запуск приложения, отправку формы и просмотр созданной заявки.