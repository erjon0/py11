from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import hashlib
import secrets
from datetime import datetime, timedelta

# Simple token storage (in production, use Redis or database)
active_sessions = {}

API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def hash_password(password: str) -> str:
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash"""
    return hash_password(password) == hashed


def create_session_token(user_id: int) -> str:
    """Create a session token for a user"""
    token = secrets.token_hex(32)
    active_sessions[token] = {
        'user_id': user_id,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(days=7)
    }
    return token


def get_user_from_token(token: str) -> int:
    """Get user ID from a session token"""
    session = active_sessions.get(token)
    if not session:
        return None
    if datetime.now() > session['expires_at']:
        del active_sessions[token]
        return None
    return session['user_id']


def invalidate_session(token: str):
    """Invalidate a session token"""
    if token in active_sessions:
        del active_sessions[token]


def get_current_user(token: str = Depends(api_key_header)):
    """Get the current user from the Authorization header"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = get_user_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user_id


def get_optional_user(token: str = Depends(api_key_header)):
    """Get the current user if authenticated, None otherwise"""
    if not token:
        return None
    
    if token.startswith('Bearer '):
        token = token[7:]
    
    return get_user_from_token(token)
