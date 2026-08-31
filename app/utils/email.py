import io
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from app.core.config import settings

def _send_smtp_message(msg: MIMEMultipart)->None:
    smtp_host = str(getattr(settings, "SMTP_HOST", "smtp.gmail.com"))
    smtp_port = int(getattr(settings, "SMTP_PORT", 587))
    smtp_user = getattr(settings, "SMTP_USER", "")
    smtp_pass = getattr(settings, "SMTP_PASSWORD", "")

    use_ssl = (smtp_port==465) or getattr(settings, "SMTP_SSL", False)

    if use_ssl:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as server:
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.send_message(msg)

    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            if getattr(settings, "SMTP_TLS", True):
                server.starttls()

            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.send_message(msg)



def send_verification_email_task(recipient_email:str, verify_url:str)-> None:

    if not verify_url.startswith(("http://", "https://")):
        verify_url = f"https://{verify_url}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify Your Account - Event Ticketing"
    sender_email = getattr(settings, "EMAILS_FROM_EMAIL", settings.SMTP_USER) or settings.SMTP_USER
    msg["From"] = f"{getattr(settings, 'EMAILS_FROM_NAME','Event Ticketing')}<{sender_email}>"
    msg["To"] = recipient_email

    text_content = f"Welcome to Event Ticketing!\n\nPlease verify your email address by opening this link in your browser:\n{verify_url}\n\nIf you did not create this account, please ignore this email"

    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    </head>

    <body style="font-family:Arial, sans-serif; line-height:1.6; color: #333333; margin:0; padding:20px;">
    <h2>Welcome to Event Ticketing</h2>
    <p>Thank you for registering. Please verify your email address to complete your account setup and unlock ticket purchasing</p>
    <p style = "margin:25px 0;">
    <a href="{verify_url}" target="_blank" style="background-color:#007bff; color: #ffffff; padding:12px 24px; text-decoration:none; border-radius:5px; display:inline-block; font-weight:bold;">
    Verify Email Address
    </a>
    </p>

    <p>Or copy and paste this link into your browser</p>
    <p><a href="{verify_url}" target="_blank" style="color: #007bff;">{verify_url}</a></p>
    <hr style="border: none; border-top:1px solid #eeeeee; margin-top:30px;"/>
    <p style="font-size:12px; color:#777777;">if you did not create this account, please ignore this email.</p>
    </body>
    </html>

    """


    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        _send_smtp_message(msg)
    except Exception as e:
        print(f"[Email Error] Failed to send verification email to {recipient_email}:{e}")
        traceback.print_exc()