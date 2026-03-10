import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
  
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def send_verification_email(to_email: str, verification_token: str):
    verification_link = f"{BASE_URL}/api/auth/verify-email?token={verification_token}"


    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email - Todo App"
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    
    html = f"""
    <html>
      <body>
        <h2>Welcome to Todo App!</h2>
        <p>Please click the link below to verify your email:</p>
        <a href="{verification_link}">Verify Email</a>
        <p>Or copy this link: {verification_link}</p>
      </body>
    </html>
    """
    
    part = MIMEText(html, "html")
    message.attach(part)
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False