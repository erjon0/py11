import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.news import (
    Comment, CommentCreate, CommentWithUser,
    Like, LikeCreate, Bookmark, BookmarkCreate, ArticleWithDetails
)
from database import get_db_connection
from auth.security import get_current_user

router = APIRouter()


# ============ COMMENTS ============

@router.get("/comments/{article_id}", response_model=List[CommentWithUser])
def get_comments(article_id: int):
    """Get all comments for an article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, c.article_id, c.user_id, c.content, c.created_at, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.article_id = ?
        ORDER BY c.created_at DESC
    ''', (article_id,))
    
    comments = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in comments]


@router.post("/comments", response_model=Comment)
def create_comment(comment: CommentCreate, user_id: int = Depends(get_current_user)):
    """Create a new comment on an article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if article exists
    cursor.execute("SELECT id FROM articles WHERE id = ?", (comment.article_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Article not found")
    
    cursor.execute('''
        INSERT INTO comments (article_id, user_id, content)
        VALUES (?, ?, ?)
    ''', (comment.article_id, user_id, comment.content))
    conn.commit()
    
    comment_id = cursor.lastrowid
    cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
    new_comment = cursor.fetchone()
    conn.close()
    
    return dict(new_comment)


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, user_id: int = Depends(get_current_user)):
    """Delete a comment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user owns the comment
    cursor.execute("SELECT user_id FROM comments WHERE id = ?", (comment_id,))
    comment = cursor.fetchone()
    
    if not comment:
        conn.close()
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment['user_id'] != user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    
    return {"detail": "Comment deleted successfully"}


# ============ LIKES ============

@router.post("/likes", response_model=dict)
def toggle_like(like: LikeCreate, user_id: int = Depends(get_current_user)):
    """Toggle like on an article (like if not liked, unlike if already liked)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if article exists
    cursor.execute("SELECT id FROM articles WHERE id = ?", (like.article_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Check if already liked
    cursor.execute('''
        SELECT id FROM likes WHERE article_id = ? AND user_id = ?
    ''', (like.article_id, user_id))
    existing = cursor.fetchone()
    
    if existing:
        # Unlike
        cursor.execute("DELETE FROM likes WHERE id = ?", (existing['id'],))
        conn.commit()
        conn.close()
        return {"liked": False, "message": "Article unliked"}
    else:
        # Like
        cursor.execute('''
            INSERT INTO likes (article_id, user_id) VALUES (?, ?)
        ''', (like.article_id, user_id))
        conn.commit()
        conn.close()
        return {"liked": True, "message": "Article liked"}


@router.get("/likes/{article_id}/status")
def get_like_status(article_id: int, user_id: int = Depends(get_current_user)):
    """Check if user has liked an article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM likes WHERE article_id = ? AND user_id = ?
    ''', (article_id, user_id))
    
    liked = cursor.fetchone() is not None
    
    cursor.execute("SELECT COUNT(*) FROM likes WHERE article_id = ?", (article_id,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return {"liked": liked, "count": count}


# ============ BOOKMARKS ============

@router.post("/bookmarks", response_model=dict)
def toggle_bookmark(bookmark: BookmarkCreate, user_id: int = Depends(get_current_user)):
    """Toggle bookmark on an article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if article exists
    cursor.execute("SELECT id FROM articles WHERE id = ?", (bookmark.article_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Check if already bookmarked
    cursor.execute('''
        SELECT id FROM bookmarks WHERE article_id = ? AND user_id = ?
    ''', (bookmark.article_id, user_id))
    existing = cursor.fetchone()
    
    if existing:
        # Remove bookmark
        cursor.execute("DELETE FROM bookmarks WHERE id = ?", (existing['id'],))
        conn.commit()
        conn.close()
        return {"bookmarked": False, "message": "Bookmark removed"}
    else:
        # Add bookmark
        cursor.execute('''
            INSERT INTO bookmarks (article_id, user_id) VALUES (?, ?)
        ''', (bookmark.article_id, user_id))
        conn.commit()
        conn.close()
        return {"bookmarked": True, "message": "Article bookmarked"}


@router.get("/bookmarks", response_model=List[ArticleWithDetails])
def get_bookmarks(user_id: int = Depends(get_current_user)):
    """Get all bookmarked articles for the current user"""
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
        FROM bookmarks b
        JOIN articles a ON b.article_id = a.id
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    ''', (user_id,))
    
    articles = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in articles]


@router.get("/bookmarks/{article_id}/status")
def get_bookmark_status(article_id: int, user_id: int = Depends(get_current_user)):
    """Check if user has bookmarked an article"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM bookmarks WHERE article_id = ? AND user_id = ?
    ''', (article_id, user_id))
    
    bookmarked = cursor.fetchone() is not None
    conn.close()
    
    return {"bookmarked": bookmarked}
