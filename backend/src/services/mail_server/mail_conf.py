from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from backend.src.services.mail_server.schema import EmailBody
from backend.src.core.config import settings


async def send_mail(
        body: EmailBody
):
    try:
        msg = MIMEText(body.message, "html")
        msg['Subject'] = body.subject
        msg['From'] = (f'Accept active user or get bearer '
                       f'<{settings.MAIL_FROM}>')
        msg['To'] = body.to
        port = int(settings.MAIL_PORT)
        server = SMTP_SSL(settings.MAIL_SERVER, port)
        server.login(settings.MAIL_FROM, settings.MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False
