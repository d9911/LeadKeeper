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

# Email templates - PostHog-inspired design
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
        .comment-block {{ background: #eeefe9; border-left: 4px solid #f7a501; padding: 16px; margin-top: 8px; border-radius: 0 6px 6px 0; font-style: italic; }}
        .footer {{ background: #f5f4f0; padding: 16px; text-align: center; font-size: 12px; color: #6c6e63; }}
        .badge {{ background: #f7a501; color: #23251d; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">🔥 НОВЫЙ ЛИД</span>
            <h1 style="margin-top: 12px;">LeadKeeper</h1>
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
            <div class="field" style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #dcdfd2;">
                <div class="field-label">Время заявки</div>
                <div class="field-value" style="color: #6c6e63;">{created_at}</div>
            </div>
        </div>
        <div class="footer">
            Автоматическое уведомление от LeadKeeper
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
        .message {{ font-size: 16px; color: #23251d; line-height: 1.6; }}
        .highlight {{ background: #eeefe9; border-left: 4px solid #2c8c66; padding: 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }}
        .highlight-text {{ font-style: italic; color: #4d4f46; }}
        .footer {{ background: #f5f4f0; padding: 16px; text-align: center; font-size: 12px; color: #6c6e63; }}
        .signature {{ margin-top: 20px; color: #4d4f46; }}
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
                <p>Ваше обращение успешно получено. Наш менеджер свяжется с вами в ближайшее время.</p>
            </div>
            {has_comment}
            <div class="signature">
                <p>С уважением,<br><strong>Команда LeadKeeper</strong></p>
            </div>
        </div>
        <div class="footer">
            Отправлено: {created_at}
        </div>
    </div>
</body>
</html>
"""

USER_EMAIL_TEMPLATE_WITH_COMMENT = USER_EMAIL_TEMPLATE.replace(
    '{has_comment}',
    '<div class="highlight"><div class="field-label">Ваше обращение:</div><div class="highlight-text">{comment}</div></div>'
).replace(
    '{has_comment}',
    '<div class="highlight"><div class="field-label">Ваше обращение:</div><div class="highlight-text">{comment}</div></div>'
)

USER_EMAIL_TEMPLATE_NO_COMMENT = USER_EMAIL_TEMPLATE.replace('{has_comment}', '')


class EmailConfig:
    """Email configuration from environment variables"""
    
    def __init__(self):
        self.owner_email = os.getenv('OWNER_EMAIL', '')
        self.smtp_host = os.getenv('SMTP_HOST', '')
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_pass = os.getenv('SMTP_PASS', '')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587') or '587')
        self.smtp_secure = os.getenv('SMTP_SECURE', 'false').lower() == 'true'
        
        self.smtp_host_2 = os.getenv('SMTP_HOST_2', '')
        self.smtp_user_2 = os.getenv('SMTP_USER_2', '')
        self.smtp_pass_2 = os.getenv('SMTP_PASS_2', '')
        self.smtp_port_2 = int(os.getenv('SMTP_PORT_2', '587') or '587')
        self.smtp_secure_2 = os.getenv('SMTP_SECURE_2', 'false').lower() == 'true'
        
        self.smtp_method = int(os.getenv('SMTP_METHOD', '0') or '0')
        
        self.from_name = os.getenv('SMTP_FROM_NAME', 'LeadKeeper')
        self.from_email = os.getenv('SMTP_FROM_EMAIL', '')
    
    @property
    def is_enabled(self) -> bool:
        """Check if email is configured and enabled"""
        return bool(
            self.smtp_method > 0 and 
            self.owner_email and 
            (self.smtp_host if self.smtp_method == 1 else self.smtp_host_2)
        )
    
    def get_smtp_config(self) -> Optional[dict]:
        """Get active SMTP configuration"""
        if self.smtp_method == 1:
            if not self.smtp_host or not self.smtp_user:
                logger.warning("Primary SMTP not configured")
                return None
            return {
                'host': self.smtp_host,
                'user': self.smtp_user,
                'pass': self.smtp_pass,
                'port': self.smtp_port,
                'secure': self.smtp_secure,
                'ssl': self.smtp_port == 465,  # Port 465 uses implicit SSL
                'from_email': self.from_email or self.smtp_user,
                'from_name': self.from_name
            }
        elif self.smtp_method == 2:
            if not self.smtp_host_2 or not self.smtp_user_2:
                logger.warning("Secondary SMTP not configured")
                return None
            return {
                'host': self.smtp_host_2,
                'user': self.smtp_user_2,
                'pass': self.smtp_pass_2,
                'port': self.smtp_port_2,
                'secure': self.smtp_secure_2,
                'ssl': self.smtp_port_2 == 465,
                'from_email': self.from_email or self.smtp_user_2,
                'from_name': self.from_name
            }
        return None


def send_email(to: str, subject: str, html_content: str, config: dict) -> bool:
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f'"{config["from_name"]}" <{config["from_email"]}>'
        msg['To'] = to
        
        # Attach HTML content
        part1 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        
        logger.info(f"Connecting to SMTP {config['host']}:{config['port']} (SSL={config.get('ssl', False)})")
        
        # Connect to SMTP server
        if config.get('ssl', False):
            # Port 465 typically uses implicit SSL
            server = smtplib.SMTP_SSL(config['host'], config['port'], timeout=30)
        else:
            # Other ports use STARTTLS
            server = smtplib.SMTP(config['host'], config['port'], timeout=30)
            if config.get('secure', False):
                server.starttls()
        
        # Login
        logger.info(f"Logging in as {config['user']}")
        server.login(config['user'], config['pass'])
        
        # Send
        logger.info(f"Sending email to {to}")
        server.sendmail(config['from_email'], to, msg.as_string())
        server.quit()
        
        logger.info(f"Email sent successfully to {to}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed: {e}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {e}")
        return False


def notify_owner(lead: dict, created_at: str) -> bool:
    """Send notification to owner about new lead"""
    config = EmailConfig()
    
    logger.info(f"Checking email config: method={config.smtp_method}, owner={config.owner_email}")
    
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
    
    if comment and comment.strip():
        template = USER_EMAIL_TEMPLATE_WITH_COMMENT
        html = template.format(
            name=name,
            comment=comment,
            created_at=created_at
        )
    else:
        template = USER_EMAIL_TEMPLATE_NO_COMMENT
        html = template.format(
            name=name,
            created_at=created_at
        )
    
    subject = "✓ Заявка принята"
    
    return send_email(email, subject, html, smtp_config)