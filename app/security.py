from fastapi import Header, HTTPException, status

from app.config import settings


async def verify_api_key(x_api_key: str | None = Header(default=None)):
    
    """Dependency that protects an endpoint behind a required X-API-Key
    header. Health checks are deliberately left unprotected elsewhere,
    since monitoring systems typically need to reach /health without
    authenticating.
    """
    if x_api_key is None or x_api_key != settings.API_KEY:
        
        raise HTTPException(
            
            status_code=status.HTTP_401_UNAUTHORIZED,
            
            detail="Invalid or missing API key",
            
        ) 
        