from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from datetime import datetime
import os

# Create logs directory
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/api_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)

logger = logging.getLogger("API")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the API call
        logger.info(f"{request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        return response
    