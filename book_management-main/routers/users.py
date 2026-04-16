import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.news import UserCreate, UserLogin, User, UserResponse, UserStats
from database import get_db_connection
from auth.security import (
    hash_password, verify_password, create_session_token, 
    get_current_user, invalidate_session, api_key_header
)

router = APIRouter()


@router.post("/register", response_model=dict)
def register(user: UserCreate):
    """Register a new user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(user.password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (user.username, user.email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        
        # Create session token
        token = create_session_token(user_id)
        conn.close()
        
        return {
            "message": "Registration successful",
            "user_id": user_id,
            "username": user.username,
            "token": token
        }
    except sqlite3.IntegrityError as e:
        conn.close()
        if 'username' in str(e):
            raise HTTPException(status_code=409, detail="Username already exists")
        elif 'email' in str(e):
            raise HTTPException(status_code=409, detail="Email already exists")
        raise HTTPException(status_code=409, detail="User already exists")


@router.post("/login", response_model=dict)
def login(credentials: UserLogin):
    """Login a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, password_hash, is_admin 
        FROM users WHERE username = ?
    ''', (credentials.username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(credentials.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_session_token(user['id'])
    
    return {
        "message": "Login successful",
        "user_id": user['id'],
        "username": user['username'],
        "email": user['email'],
        "is_admin": user['is_admin'],
        "token": token
    }


@router.post("/logout")
def logout(token: str = Depends(api_key_header)):
    """Logout the current user"""
    if token:
        if token.startswith('Bearer '):
            token = token[7:]
        invalidate_session(token)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(user_id: int = Depends(get_current_user)):
    """Get current user information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, is_admin 
        FROM users WHERE id = ?
    ''', (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return dict(user)


@router.get("/stats", response_model=UserStats)
def get_user_stats(user_id: int = Depends(get_current_user)):
    """Get statistics for the current user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total articles
    cursor.execute("SELECT COUNT(*) FROM articles WHERE author_id = ?", (user_id,))
    total_articles = cursor.fetchone()[0]
    
    # Total likes received
    cursor.execute('''
        SELECT COUNT(*) FROM likes l
        JOIN articles a ON l.article_id = a.id
        WHERE a.author_id = ?
    ''', (user_id,))
    total_likes = cursor.fetchone()[0]
    
    # Total comments received
    cursor.execute('''
        SELECT COUNT(*) FROM comments c
        JOIN articles a ON c.article_id = a.id
        WHERE a.author_id = ?
    ''', (user_id,))
    total_comments = cursor.fetchone()[0]
    
    # Total views
    cursor.execute("SELECT COALESCE(SUM(views), 0) FROM articles WHERE author_id = ?", (user_id,))
    total_views = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_articles": total_articles,
        "total_likes_received": total_likes,
        "total_comments_received": total_comments,
        "total_views": total_views
    }


@router.get("/{username}", response_model=UserResponse)
def get_user_by_username(username: str):
    """Get user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, is_admin 
        FROM users WHERE username = ?
    ''', (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return dict(user)
