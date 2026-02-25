from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..database.schema import User
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_verification_token():
    return secrets.token_urlsafe(32)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
       
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       
        email: str = payload.get("sub")
       
        if email is None:
            raise credentials_exception
            
    except JWTError:
       
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    
   
    if user is None:
        raise credentials_exception
    
    return user

def generate_reset_token():
    return secrets.token_urlsafe(32)

def send_password_reset_email(to_email: str, reset_token: str):
    from .email_service import send_verification_email
    import os
    
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    reset_link = f"{BASE_URL}/api/auth/reset-password?token={reset_token}"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Your Password - Todo App"
    message["From"] = os.getenv("FROM_EMAIL")
    message["To"] = to_email
    
    html = f"""
    <html>
      <body>
        <h2>Password Reset Request</h2>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        <p>Or copy this link: {reset_link}</p>
        <p>This link will expire in 1 hour.</p>
        <p>If you didn't request this, please ignore this email.</p>
      </body>
    </html>
    """
    
    part = MIMEText(html, "html")
    message.attach(part)
    
    try:
        import smtplib
        SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
        SMTP_USERNAME = os.getenv("SMTP_USERNAME")
        SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(os.getenv("FROM_EMAIL"), to_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False