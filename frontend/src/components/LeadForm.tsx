import { useState, FormEvent } from 'react'
import { createLead, LeadFormData } from '../api/leads'

interface FormErrors {
  name?: string
  contact?: string
  consent?: string
  general?: string
}

type FormState = 'idle' | 'loading' | 'success' | 'error'

function validateContact(contact: string): boolean {
  const isEmail = contact.includes('@') && contact.includes('.')
  const isPhone = /\d/.test(contact)
  return isEmail || isPhone
}

export function LeadForm() {
  const [formState, setFormState] = useState<FormState>('idle')
  const [errors, setErrors] = useState<FormErrors>({})

  const [formData, setFormData] = useState<LeadFormData>({
    name: '',
    contact: '',
    company: '',
    comment: '',
    consent: false,
  })

  const validate = (): boolean => {
    const newErrors: FormErrors = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Введите ваше имя'
    }

    if (!formData.contact.trim()) {
      newErrors.contact = 'Введите телефон или email'
    } else if (!validateContact(formData.contact)) {
      newErrors.contact = 'Введите корректный телефон или email'
    }

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
    const value = e.target.type === 'checkbox' ? (e.target as HTMLInputElement).checked : e.target.value

    setFormData((prev) => ({ ...prev, [field]: value }))

    if (errors[field as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }))
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
            setFormData({ name: '', contact: '', company: '', comment: '', consent: false })
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
          <label htmlFor="contact">
            Телефон или Email <span className="required">*</span>
          </label>
          <input
            type="text"
            id="contact"
            value={formData.contact}
            onChange={handleChange('contact')}
            className={errors.contact ? 'error' : ''}
            placeholder="+7 999 123-45-67 или ivan@company.com"
            disabled={formState === 'loading'}
          />
          {errors.contact && <div className="error-message">{errors.contact}</div>}
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
