const API_BASE = '/api';

export interface Lead {
  id: number;
  name: string;
  phone: string | null;
  email: string | null;
  company: string | null;
  comment: string | null;
  consent: boolean;
  created_at: string;
}

export interface LeadFormData {
  name: string;
  phone: string;
  email: string;
  company?: string;
  comment?: string;
  consent: boolean;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export async function createLead(data: LeadFormData): Promise<ApiResponse<Lead>> {
  try {
    const response = await fetch(`${API_BASE}/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return { error: errorData.detail || 'Ошибка при отправке заявки' };
    }

    const lead = await response.json();
    return { data: lead };
  } catch (error) {
    console.error('Network error:', error);
    return { error: 'Ошибка сети. Проверьте подключение к серверу.' };
  }
}

export async function getLeads(): Promise<ApiResponse<Lead[]>> {
  try {
    const response = await fetch(`${API_BASE}/leads`);

    if (!response.ok) {
      return { error: 'Ошибка при загрузке заявок' };
    }

    const leads = await response.json();
    return { data: leads };
  } catch (error) {
    console.error('Network error:', error);
    return { error: 'Ошибка сети. Проверьте подключение к серверу.' };
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/health`);
    return response.ok;
  } catch {
    return false;
  }
}