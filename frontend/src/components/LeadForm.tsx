import { useState, FormEvent } from 'react'
import { createLead, LeadFormData } from '../api/leads'

interface FormErrors {
  name?: string
  phone?: string
  email?: string
  contact?: string
  consent?: string
  general?: string
}

type FormState = 'idle' | 'loading' | 'success' | 'error'

// Email validation (RFC 5322 compliant)
const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/

// Phone validation: + followed by country code and digits
// Accepts formats like: +7 999 123-45-67, +44 20 7946 0958, +1 (555) 123-4567
const PHONE_REGEX = /^\+?[1-9]\d{0,2}[\s\-]?\(?\d{1,4}\)?[\s\-\.]?\d{1,4}[\s\-\.]?\d{1,4}[\s\-\.]?\d{0,6}$/

function validatePhone(phone: string): { valid: boolean; message?: string } {
  if (!phone.trim()) {
    return { valid: true } // Phone is optional
  }

  // Remove all spaces for digit count
  const cleanPhone = phone.replace(/[\s\-\.\(\)]/g, '')

  // Must have only digits and one +
  const digitsOnly = cleanPhone.replace(/\D/g, '')

  // Check digit count
  if (digitsOnly.length > 16) {
    return { valid: false, message: 'Номер слишком длинный (максимум 16 цифр)' }
  }

  if (digitsOnly.length < 7) {
    return { valid: false, message: 'Номер слишком короткий (минимум 7 цифр)' }
  }

  // Must start with + if international format
  if (phone.includes('+') && !phone.startsWith('+')) {
    return { valid: false, message: 'Знак + должен быть только в начале номера' }
  }

  if (!PHONE_REGEX.test(phone)) {
    return { valid: false, message: 'Некорректный формат номера' }
  }

  return { valid: true }
}

function validateEmail(email: string): { valid: boolean; message?: string } {
  if (!email.trim()) {
    return { valid: true } // Email is optional if phone provided
  }

  // RFC 5322 compliant email validation
  if (!EMAIL_REGEX.test(email)) {
    return { valid: false, message: 'Некорректный формат email' }
  }

  // Check for disallowed characters in local part
  const localPart = email.split('@')[0]
  const disallowedChars = /[<>()\[\]\\,"\s]/
  if (disallowedChars.test(localPart)) {
    return { valid: false, message: 'Email содержит недопустимые символы' }
  }

  // Local part cannot start or end with dot
  if (localPart.startsWith('.') || localPart.endsWith('.')) {
    return { valid: false, message: 'Email не может начинаться или заканчиваться точкой' }
  }

  // No consecutive dots
  if (localPart.includes('..')) {
    return { valid: false, message: 'Email не может содержать две точки подряд' }
  }

  return { valid: true }
}

function formatPhone(value: string): string {
  // Remove invalid characters (keep only digits, +, spaces, -, (, ))
  let cleaned = value.replace(/[^\d+\s\-\(\)]/g, '')

  // Ensure only one +
  const plusCount = (cleaned.match(/\+/g) || []).length
  if (plusCount > 1) {
    // Keep only the first +
    cleaned = '+' + cleaned.replace(/\+/g, '')
  }

  // Limit total digits to 16 (excluding +)
  const digits = cleaned.replace(/\D/g, '')
  if (digits.length > 16) {
    // Trim excess digits
    const trimmedDigits = digits.substring(0, 16)
    // Reconstruct with the original format
    cleaned = '+' + trimmedDigits
  }

  return cleaned
}

export function LeadForm() {
  const [formState, setFormState] = useState<FormState>('idle')
  const [errors, setErrors] = useState<FormErrors>({})

  const [formData, setFormData] = useState<LeadFormData>({
    name: '',
    phone: '',
    email: '',
    company: '',
    comment: '',
    consent: false,
  })

  const validate = (): boolean => {
    const newErrors: FormErrors = {}

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = 'Введите ваше имя'
    } else if (formData.name.trim().length < 2) {
      newErrors.name = 'Имя слишком короткое'
    } else if (formData.name.trim().length > 100) {
      newErrors.name = 'Имя слишком длинное'
    }

    // Phone validation
    const phoneResult = validatePhone(formData.phone)
    if (!phoneResult.valid) {
      newErrors.phone = phoneResult.message
    }

    // Email validation
    const emailResult = validateEmail(formData.email)
    if (!emailResult.valid) {
      newErrors.email = emailResult.message
    }

    // At least one contact method required
    if (!formData.phone.trim() && !formData.email.trim()) {
      newErrors.contact = 'Укажите телефон или email для связи'
    }

    // Consent validation
    if (!formData.consent) {
      newErrors.consent = 'Необходимо принять согласие на обработку данных'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setErrors({})

    if (!validate()) {
      return
    }

    setFormState('loading')

    const result = await createLead(formData)

    if (result.error) {
      setFormState('error')
      setErrors({ general: result.error })
    } else {
      setFormState('success')
    }
  }

  const handleChange = (field: keyof LeadFormData) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    let value: string | boolean = e.target.value

    if (e.target.type === 'checkbox') {
      value = (e.target as HTMLInputElement).checked
    }

    // Format phone input
    if (field === 'phone') {
      value = formatPhone(value as string)
    }

    setFormData((prev) => ({ ...prev, [field]: value }))

    // Clear error when user starts typing
    const errorKey = field === 'phone' || field === 'email' ? field : field
    if (errors[errorKey as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [errorKey]: undefined }))
    }
    // Clear contact error if either field changes
    if (field === 'phone' || field === 'email') {
      if (errors.contact) {
        setErrors((prev) => ({ ...prev, contact: undefined }))
      }
    }
  }

  if (formState === 'success') {
    return (
      <div className="card success-card">
        <div className="success-icon">🎉</div>
        <h2>Заявка отправлена!</h2>
        <p>Спасибо за обращение. Менеджер свяжется с вами в ближайшее время.</p>
        <button
          className="btn btn-secondary"
          onClick={() => {
            setFormState('idle')
            setFormData({ name: '', phone: '', email: '', company: '', comment: '', consent: false })
          }}
        >
          Отправить ещё одну заявку
        </button>
      </div>
    )
  }

  return (
    <div className="card">
      {formState === 'error' && errors.general && <div className="alert alert-error">{errors.general}</div>}

      {errors.contact && (
        <div className="alert alert-error" style={{ marginBottom: '16px' }}>
          {errors.contact}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">
            Имя <span className="required">*</span>
          </label>
          <input type="text" id="name" value={formData.name} onChange={handleChange('name')} className={errors.name ? 'error' : ''} placeholder="Иван Петров" disabled={formState === 'loading'} />
          {errors.name && <div className="error-message">{errors.name}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="phone">Телефон</label>
          <input
            type="tel"
            id="phone"
            value={formData.phone}
            onChange={handleChange('phone')}
            className={errors.phone ? 'error' : ''}
            placeholder="+7 999 123-45-67"
            disabled={formState === 'loading'}
          />
          <div className="field-hint">Формат: +КодСтраны Номер (максимум 16 цифр)</div>
          {errors.phone && <div className="error-message">{errors.phone}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={formData.email}
            onChange={handleChange('email')}
            className={errors.email ? 'error' : ''}
            placeholder="ivan@company.com"
            disabled={formState === 'loading'}
          />
          <div className="field-hint">Латинские буквы, цифры, точки, дефис, @</div>
          {errors.email && <div className="error-message">{errors.email}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="company">Компания</label>
          <input type="text" id="company" value={formData.company} onChange={handleChange('company')} placeholder="Название компании" disabled={formState === 'loading'} />
        </div>

        <div className="form-group">
          <label htmlFor="comment">Комментарий</label>
          <textarea id="comment" value={formData.comment} onChange={handleChange('comment')} rows={3} placeholder="Расскажите подробнее о вашем проекте" disabled={formState === 'loading'} />
        </div>

        <div className="form-group">
          <div className="checkbox-group">
            <input type="checkbox" id="consent" checked={formData.consent} onChange={handleChange('consent')} disabled={formState === 'loading'} />
            <label htmlFor="consent">
              Я согласен на обработку персональных данных в соответствии с политикой конфиденциальности <span className="required">*</span>
            </label>
          </div>
          {errors.consent && <div className="error-message">{errors.consent}</div>}
        </div>

        <button type="submit" className="btn btn-primary" disabled={formState === 'loading'}>
          {formState === 'loading' ? (
            <>
              <span className="loading-spinner"></span>
              Отправка...
            </>
          ) : (
            'Отправить заявку'
          )}
        </button>
      </form>
    </div>
  )
}
