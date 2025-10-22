import os
import random
import smtplib
from email.message import EmailMessage
from typing import Optional


def generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP of `length` digits as a zero-padded string.

    Args:
        length: number of digits (default 6)

    Returns:
        A string containing the OTP, e.g. '004321'
    """
    if length <= 0:
        raise ValueError("length must be > 0")
    # ensure leading zeros are possible by formatting
    max_val = 10**length - 1
    num = random.randint(0, max_val)
    return f"{num:0{length}d}"


def send_session_code_smtp(
    recipient_email: str,
    otp: str,
    subject: str = "your session code",
    sender_email: Optional[str] = None,
    smtp_user: Optional[str] = None,
    smtp_password: Optional[str] = None,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 587,
    use_tls: bool = True,
) -> bool:
    """Send the `otp` to `recipient_email` using Gmail's SMTP server.

    The function prefers environment variables when credentials are not provided:
      - SMTP_USER
      - SMTP_PASSWORD
      - SENDER_EMAIL (fallback for From header)

    It uses `email.message.EmailMessage` to build the message and `smtplib.SMTP` to send it.

    Returns True on success, False on failure.
    """
    # Resolve sender and credentials from args or environment
    sender = sender_email or os.environ.get("SENDER_EMAIL")
    smtp_user = smtp_user or os.environ.get("SMTP_USER")
    smtp_password = smtp_password or os.environ.get("SMTP_PASSWORD")

    if not sender:
        raise ValueError("sender_email must be provided or SENDER_EMAIL env var set")
    if not smtp_user or not smtp_password:
        raise ValueError("SMTP credentials required: provide smtp_user & smtp_password or set SMTP_USER and SMTP_PASSWORD env vars")

    # Build the email message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient_email

    plain_body = f"Hello,\n\nYour session code is: {otp}\n\nUse this code to join your session.\n\nRegards,\nQuiz Portal"
    html_body = f"<html><body><p>Hello,</p><p>Your session code is: <strong>{otp}</strong></p><p>Use this code to join your session.</p><p>Regards,<br>Quiz Portal</p></body></html>"

    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype="html")

    try:
        if use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=20)
            server.ehlo()
            server.starttls()
            server.ehlo()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20)

        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as exc:
        # Keep errors local — caller can log them as needed
        print("Failed to send session code via SMTP:", exc)
        return False
