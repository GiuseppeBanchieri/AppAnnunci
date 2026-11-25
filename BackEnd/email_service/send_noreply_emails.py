import aiosmtplib
from email.message import EmailMessage

from config import settings

async def send_noreply_email(recipient: str, subject: str, plain_text: str, html_content: str) -> None:
  msg = EmailMessage()
  msg['From'] = settings.mail_from
  msg['To'] = recipient
  msg['Subject'] = subject

  msg.set_content(plain_text)

  msg.add_alternative(html_content, subtype='html')

  await aiosmtplib.send(msg,
    hostname=settings.mail_server,
    port=settings.mail_port,
    username=settings.mail_username,
    password=settings.mail_password.get_secret_value(),
    start_tls=settings.mail_use_tls
  )