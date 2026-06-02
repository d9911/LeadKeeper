import { Lead } from '../api/leads';

interface LeadsTableProps {
  leads: Lead[];
  isLoading: boolean;
  error: string | null;
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function truncateText(text: string | null, maxLength: number = 50): string {
  if (!text) return '—';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

export function LeadsTable({ leads, isLoading, error }: LeadsTableProps) {
  if (isLoading) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">⏳</div>
        <p>Загрузка заявок...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">⚠️</div>
        <p>{error}</p>
      </div>
    );
  }

  if (leads.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📋</div>
        <p>Пока нет заявок</p>
        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
          Заявки появятся здесь после отправки формы
        </p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Дата</th>
            <th>Имя</th>
            <th>Контакт</th>
            <th>Компания</th>
            <th>Комментарий</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id}>
              <td>{formatDate(lead.created_at)}</td>
              <td>{lead.name}</td>
              <td>{lead.contact}</td>
              <td>{truncateText(lead.company)}</td>
              <td>{truncateText(lead.comment)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}