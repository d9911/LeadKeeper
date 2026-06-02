"""
Email notification service for LeadKeeper
Sends notifications to owner when new leads are submitted
"""
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import smtplib

logger = logging.getLogger(__name__)

# Email templates
OWNER_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #eeefe9; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #bfc1b7; overflow: hidden; }}
        .header {{ background: #23251d; color: #ffffff; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 20px; font-weight: 700; }}
        .content {{ padding: 24px; }}
        .field {{ margin-bottom: 16px; }}
        .field-label {{ font-size: 12px; text-transform: uppercase; color: #6c6e63; letter-spacing: 0.5px; margin-bottom: 4px; }}
        .field-value {{ font-size: 16px; color: #23251d; }}
        .comment-block {{ background: #eeefe9; border-left: 4px solid #f7a501; padding: 16px; margin-top: 8px; border-radius: 0 6px 6px 0; }}
        .footer {{ background: #f5f4f0; padding: 16px; text-align: center; font-size: 12px; color: #6c6e63; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 Новый лид</h1>
        </div>
        <div class="content">
            <div class="field">
                <div class="field-label">Имя</div>
                <div class="field-value"><strong>{name}</strong></div>
            </div>
            {phone_block}
            {email_block}
            {company_block}
            <div class="field">
                <div class="field-label">Комментарий</div>
                <div class="comment-block">{comment}</div>
            </div>
        </div>
        <div class="footer">
            LeadKeeper • {created_at}
        </div>
    </div>
</body>
</html>
"""

USER_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #eeefe9; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #bfc1b7; overflow: hidden; }}
        .header {{ background: #2c8c66; color: #ffffff; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 20px; font-weight: 700; }}
        .content {{ padding: 24px; }}
        .message {{ font-size: 16px; color: #23251d; margin-bottom: 20px; }}
        .highlight {{ background: #eeefe9; border-left: 4px solid #2c8c66; padding: 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }}
        .footer {{ background: #f5f4f0; padding: 16px; text-align: center; font-size: 12px; color: #6c6e63; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✓ Заявка принята</h1>
        </div>
        <div class="content">
            <div class="message">
                <p>Здравствуйте, <strong>{name}</strong>!</p>
                <p>Ваше сообщение успешно доставлено. Мы свяжемся с вами в ближайшее время.</p>
            </div>
            <div class="highlight">
                <strong>Ваша заявка:</strong><br>
                {comment}
            </div>
            <p style="color: #6c6e63; font-size: 14px;">С уважением,<br>Команда LeadKeeper</p>
        </div>
        <div class="footer">
            Отправлено: {created_at}
        </div>
    </div>
</body>
</html>
"""


class EmailConfig:
    """Email configuration from environment variables"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', '')
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_pass = os.getenv('SMTP_PASS', '')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_secure = os.getenv('SMTP_SECURE', 'false').lower() == 'true'
        
        self.smtp_host_2 = os.getenv('SMTP_HOST_2', '')
        self.smtp_user_2 = os.getenv('SMTP_USER_2', '')
        self.smtp_pass_2 = os.getenv('SMTP_PASS_2', '')
        self.smtp_port_2 = int(os.getenv('SMTP_PORT_2', '587'))
        self.smtp_secure_2 = os.getenv('SMTP_SECURE_2', 'false').lower() == 'true'
        
        self.owner_email = os.getenv('OWNER_EMAIL', '')
        self.smtp_method = int(os.getenv('SMTP_METHOD', '0'))  # 0 = disabled, 1 = primary, 2 = secondary
        
        self.from_name = os.getenv('SMTP_FROM_NAME', 'LeadKeeper')
        self.from_email = os.getenv('SMTP_FROM_EMAIL', '')
    
    @property
    def is_enabled(self) -> bool:
        return bool(self.smtp_method > 0 and self.owner_email)
    
    def get_smtp_config(self) -> Optional[dict]:
        """Get active SMTP configuration"""
        if self.smtp_method == 1:
            return {
                'host': self.smtp_host,
                'user': self.smtp_user,
                'pass': self.smtp_pass,
                'port': self.smtp_port,
                'secure': self.smtp_secure,
                'from_email': self.from_email or self.smtp_user,
                'from_name': self.from_name
            } if self.smtp_host and self.smtp_user and self.smtp_secure else None
        elif self.smtp_method == 2:
            return {
                'host': self.smtp_host_2,
                'user': self.smtp_user_2,
                'pass': self.smtp_pass_2,
                'port': self.smtp_port_2,
                'secure': self.smtp_secure_2,
                'from_email': self.from_email or self.smtp_user_2,
                'from_name': self.from_name
            } if self.smtp_host_2 and self.smtp_user_2 else None
        return None


def send_email(to: str, subject: str, html_content: str, config: dict) -> bool:
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f'"{config["from_name"]}" <{config["from_email"]}>'
        msg['To'] = to
        
        # Attach both plain text and HTML
        part1 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        
        # Connect to SMTP server
        if config['secure']:
            server = smtplib.SMTP_SSL(config['host'], config['port'])
        else:
            server = smtplib.SMTP(config['host'], config['port'])
            server.starttls()
        
        server.login(config['user'], config['pass'])
        server.sendmail(config['from_email'], to, msg.as_string())
        server.quit()
        
        logger.info(f"Email sent to {to}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        return False


def notify_owner(lead: dict, created_at: str) -> bool:
    """Send notification to owner about new lead"""
    config = EmailConfig()
    
    if not config.is_enabled:
        logger.info("Email notifications disabled (SMTP_METHOD=0 or no owner email)")
        return False
    
    smtp_config = config.get_smtp_config()
    if not smtp_config:
        logger.warning("No valid SMTP configuration found")
        return False
    
    # Build phone/email/company blocks
    phone_block = ""
    if lead.get('phone'):
        phone_block = f"""
            <div class="field">
                <div class="field-label">Телефон</div>
                <div class="field-value">{lead['phone']}</div>
            </div>
        """
    
    email_block = ""
    if lead.get('email'):
        email_block = f"""
            <div class="field">
                <div class="field-label">Email</div>
                <div class="field-value">{lead['email']}</div>
            </div>
        """
    
    company_block = ""
    if lead.get('company'):
        company_block = f"""
            <div class="field">
                <div class="field-label">Компания</div>
                <div class="field-value">{lead['company']}</div>
            </div>
        """
    
    comment_text = lead.get('comment') or '—'
    
    html = OWNER_EMAIL_TEMPLATE.format(
        name=lead['name'],
        phone_block=phone_block,
        email_block=email_block,
        company_block=company_block,
        comment=comment_text,
        created_at=created_at
    )
    
    subject = f"🔥 Новая заявка от {lead['name']}"
    
    return send_email(config.owner_email, subject, html, smtp_config)


def notify_user(email: str, name: str, comment: str, created_at: str) -> bool:
    """Send confirmation email to user"""
    config = EmailConfig()
    
    if not config.is_enabled:
        return False
    
    smtp_config = config.get_smtp_config()
    if not smtp_config:
        return False
    
    comment_text = comment or '—'
    
    html = USER_EMAIL_TEMPLATE.format(
        name=name,
        comment=comment_text,
        created_at=created_at
    )
    
    subject = "✓ Заявка принята"
    
    return send_email(email, subject, html, smtp_config)