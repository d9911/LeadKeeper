import { useState, FormEvent } from 'react'
import { createLead, LeadFormData } from '../api/leads'

interface FormErrors {
  name?: string
  phone?: string
  email?: string
  consent?: string
  general?: string
}

type FormState = 'idle' | 'loading' | 'success' | 'error'

// Email validation (RFC 5322 compliant)
const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/

// Phone validation: + followed by country code and digits
const PHONE_REGEX = /^\+?[1-9]\d{0,2}[\s\-]?\(?\d{1,4}\)?[\s\-\.]?\d{1,4}[\s\-\.]?\d{1,4}[\s\-\.]?\d{0,6}$/

function validatePhone(phone: string): { valid: boolean; message?: string } {
  if (!phone.trim()) {
    return { valid: true } // Phone is optional
  }

  // Remove formatting characters
  const cleanPhone = phone.replace(/[\s\-\.\(\)]/g, '')

  // Extract digits only
  const digits = cleanPhone.replace(/\D/g, '')

  // Check digit count (max 16)
  if (digits.length > 16) {
    return { valid: false, message: 'Номер слишком длинный (максимум 16 цифр)' }
  }

  if (digits.length > 0 && digits.length < 7) {
    return { valid: false, message: 'Номер слишком короткий (минимум 7 цифр)' }
  }

  if (!PHONE_REGEX.test(phone)) {
    return { valid: false, message: 'Некорректный формат номера' }
  }

  return { valid: true }
}

function validateEmail(email: string): { valid: boolean; message?: string } {
  if (!email.trim()) {
    return { valid: true } // Email is optional
  }

  // RFC 5322 compliant email validation
  if (!EMAIL_REGEX.test(email)) {
    return { valid: false, message: 'Некорректный формат email' }
  }

  // Check local part rules
  const localPart = email.split('@')[0]

  // No disallowed characters
  const disallowedChars = /[<>()\[\]\\,"\s]/
  if (disallowedChars.test(localPart)) {
    return { valid: false, message: 'Email содержит недопустимые символы' }
  }

  // Cannot start or end with dot
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
    cleaned = '+' + cleaned.replace(/\+/g, '')
  }

  // Limit total digits to 16
  const digits = cleaned.replace(/\D/g, '')
  if (digits.length > 16) {
    const trimmedDigits = digits.substring(0, 16)
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

    // Phone validation (only if filled)
    if (formData.phone.trim()) {
      const phoneResult = validatePhone(formData.phone)
      if (!phoneResult.valid) {
        newErrors.phone = phoneResult.message
      }
    }

    // Email validation (only if filled)
    if (formData.email.trim()) {
      const emailResult = validateEmail(formData.email)
      if (!emailResult.valid) {
        newErrors.email = emailResult.message
      }
    }

    // At least one contact method required
    if (!formData.phone.trim() && !formData.email.trim()) {
      newErrors.phone = 'Укажите телефон или email для связи'
      newErrors.email = 'Укажите телефон или email для связи'
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

    // Clear field-specific error on change
    if (field === 'phone' && errors.phone) {
      // Don't clear if it's the "at least one contact" error
      if (!formData.email.trim()) {
        // Keep error until other contact is filled
      }
    }
    if (field === 'email' && errors.email) {
      // Don't clear if it's the "at least one contact" error
    }
  }

  // Handle blur - validate individual field when user leaves it
  const handleBlur = (field: keyof LeadFormData) => () => {
    if (field === 'phone' && formData.phone.trim()) {
      const result = validatePhone(formData.phone)
      if (!result.valid) {
        setErrors((prev) => ({ ...prev, phone: result.message }))
      }
    }
    if (field === 'email' && formData.email.trim()) {
      const result = validateEmail(formData.email)
      if (!result.valid) {
        setErrors((prev) => ({ ...prev, email: result.message }))
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

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">
            Имя <span className="required">*</span>
          </label>
          <input type="text" id="name" value={formData.name} onChange={handleChange('name')} className={errors.name ? 'error' : ''} placeholder="Иван Петров" disabled={formState === 'loading'} />
          {errors.name && <div className="error-message">{errors.name}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="phone">Телефон {!formData.email.trim() && <span className="required">*</span>}</label>
          <input
            type="tel"
            id="phone"
            value={formData.phone}
            onChange={handleChange('phone')}
            onBlur={handleBlur('phone')}
            className={errors.phone ? 'error' : ''}
            placeholder="+7 999 123-45-67"
            disabled={formState === 'loading'}
          />
          {formData.phone && <div className="field-hint">Формат: +КодСтраны Номер (макс 16 цифр)</div>}
          {errors.phone && <div className="error-message">{errors.phone}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="email">Email {!formData.phone.trim() && <span className="required">*</span>}</label>
          <input
            type="email"
            id="email"
            value={formData.email}
            onChange={handleChange('email')}
            onBlur={handleBlur('email')}
            className={errors.email ? 'error' : ''}
            placeholder="ivan@company.com"
            disabled={formState === 'loading'}
          />
          {formData.email && <div className="field-hint">Латинские буквы, цифры, точки, дефис, @</div>}
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
