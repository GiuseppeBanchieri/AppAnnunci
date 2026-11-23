from pathlib import Path

from send_noreply_emails import send_noreply_email
from config import settings


async def send_forgotten_pw_emails(mail_recipient: str, token: str, nome_user: str | None = None) -> None:
  pw_reset_url = f'{settings.password_reset_frontend_url}/reset_password?token={token}'
  if nome_user is None:
    nome_user= ''
  plain_text_content = f"""Buongiorno {nome_user},
clicca il seguente link per impostare una nuova password:
  {pw_reset_url}
Il link non sarà più valido tra un'ora.
Se non hai richiesto di impostare una nuova password ignora questa mail.
Cordiali saluti,
AnnunciApp"""

  html_content = Path('forgotten_pw_mail.html').read_text(encoding='utf-8')
  html_content = html_content.replace('{{nome_user}}', nome_user).replace('{{pw_reset_url}}', pw_reset_url)

  await send_noreply_email(recipient=mail_recipient,
                           subject='Reset password AppAnnunci',
                           plain_text=plain_text_content,
                           html_content=html_content)