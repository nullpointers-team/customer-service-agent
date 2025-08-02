import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SUPPORT_TEAM_EMAIL = os.getenv("SUPPORT_TEAM_EMAIL", SMTP_EMAIL)  # default to same email

def send_support_email(user_message: str, user_email: str = "anonymous@user.com") -> str:
    subject = "Customer Support Request"
    body = f"""
This is an automated support request from the customer service system.

User Message:
-------------
{user_message}

User Contact (if known): {user_email}
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = SUPPORT_TEAM_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, SUPPORT_TEAM_EMAIL, msg.as_string())
        return "✅ Your request has been sent to our support team."
    except Exception as e:
        return f"❌ Failed to send email: {e}"
