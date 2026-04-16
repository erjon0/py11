import sqlite3
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from models.news import Article, ArticleCreate, ArticleUpdate, ArticleWithDetails
from database import get_db_connection
from auth.security import get_current_user, get_optional_user

router = APIRouter()


@router.get("/", response_model=List[ArticleWithDetails])
def get_articles(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: Optional[int] = Depends(get_optional_user)
):
    """Get all published articles with optional filtering"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            a.id, a.title, a.content, a.summary, a.author_id, a.category_id,
            a.image_url, a.views, a.created_at, a.updated_at, a.is_published,
            u.username as author_name,
            c.name as category_name, c.color as category_color,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.is_published = 1
    '''
    params = []
    
    if category_id:
        query += " AND a.category_id = ?"
        params.append(category_id)
    
    if search:
        query += " AND (a.title LIKE ? OR a.content LIKE ?)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += " ORDER BY a.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    articles = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in articles]


@router.get("/trending", response_model=List[ArticleWithDetails])
def get_trending_articles(limit: int = Query(10, ge=1, le=50)):
    """Get trending articles based on views and engagement"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            a.id, a.title, a.content, a.summary, a.author_id, a.category_id,
            a.image_url, a.views, a.created_at, a.updated_at, a.is_published,
            u.username as author_name,
            c.name as category_name, c.color as category_color,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count,
            (a.views + (SELECT COUNT(*) FROM likes WHERE article_id = a.id) * 5 + 
             (SELECT COUNT(*) FROM comments WHERE article_id = a.id) * 3) as engagement_score
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.is_published = 1
        ORDER BY engagement_score DESC
        LIMIT ?
    ''', (limit,))
    
    articles = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in articles]


@router.get("/my-articles", response_model=List[ArticleWithDetails])
def get_my_articles(user_id: int = Depends(get_current_user)):
    """Get all articles by the current user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            a.id, a.title, a.content, a.summary, a.author_id, a.category_id,
            a.image_url, a.views, a.created_at, a.updated_at, a.is_published,
            u.username as author_name,
            c.name as category_name, c.color as category_color,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.author_id = ?
        ORDER BY a.created_at DESC
    ''', (user_id,))
    
    articles = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in articles]


@router.get("/{article_id}", response_model=ArticleWithDetails)
def get_article(article_id: int, user_id: Optional[int] = Depends(get_optional_user)):
    """Get a single article by ID and increment views"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Increment view count
    cursor.execute("UPDATE articles SET views = views + 1 WHERE id = ?", (article_id,))
    conn.commit()
    
    cursor.execute('''
        SELECT 
            a.id, a.title, a.content, a.summary, a.author_id, a.category_id,
            a.image_url, a.views, a.created_at, a.updated_at, a.is_published,
            u.username as author_name,
            c.name as category_name, c.color as category_color,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.id = ?
    ''', (article_id,))
    
    article = cursor.fetchone()
    conn.close()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return dict(article)


@router.post("/", response_model=Article)
def create_article(article: ArticleCreate, user_id: int = Depends(get_current_user)):
    """Create a new article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO articles (title, content, summary, author_id, category_id, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (article.title, article.content, article.summary, user_id, 
              article.category_id, article.image_url))
        conn.commit()
        article_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        new_article = cursor.fetchone()
        conn.close()
        
        return dict(new_article)
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{article_id}", response_model=Article)
def update_article(article_id: int, article: ArticleUpdate, user_id: int = Depends(get_current_user)):
    """Update an existing article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user owns the article
    cursor.execute("SELECT author_id FROM articles WHERE id = ?", (article_id,))
    existing = cursor.fetchone()
    
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Article not found")
    
    if existing['author_id'] != user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="Not authorized to edit this article")
    
    # Build update query dynamically
    updates = []
    params = []
    
    if article.title is not None:
        updates.append("title = ?")
        params.append(article.title)
    if article.content is not None:
        updates.append("content = ?")
        params.append(article.content)
    if article.summary is not None:
        updates.append("summary = ?")
        params.append(article.summary)
    if article.category_id is not None:
        updates.append("category_id = ?")
        params.append(article.category_id)
    if article.image_url is not None:
        updates.append("image_url = ?")
        params.append(article.image_url)
    if article.is_published is not None:
        updates.append("is_published = ?")
        params.append(article.is_published)
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    
    query = f"UPDATE articles SET {', '.join(updates)} WHERE id = ?"
    params.append(article_id)
    
    cursor.execute(query, params)
    conn.commit()
    
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    updated_article = cursor.fetchone()
    conn.close()
    
    return dict(updated_article)


@router.delete("/{article_id}")
def delete_article(article_id: int, user_id: int = Depends(get_current_user)):
    """Delete an article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user owns the article
    cursor.execute("SELECT author_id FROM articles WHERE id = ?", (article_id,))
    existing = cursor.fetchone()
    
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Article not found")
    
    if existing['author_id'] != user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="Not authorized to delete this article")
    
    cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()
    
    return {"detail": "Article deleted successfully"}
