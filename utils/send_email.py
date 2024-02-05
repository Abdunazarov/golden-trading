# stdlib
from email.message import EmailMessage

# thirdparty
import aiosmtplib
from fastapi.exceptions import HTTPException

# project
import settings


async def send_email_async(to: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            message=msg,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
        )
    except Exception:
        raise HTTPException(status_code=409, detail="Error while sending email")
