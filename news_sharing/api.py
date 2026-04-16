from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

from database import get_db_connection, init_database
from models import (
    UserCreate, UserResponse, UserLogin,
    CategoryCreate, CategoryResponse,
    ArticleCreate, ArticleUpdate, ArticleResponse,
    CommentCreate, CommentResponse,
    LikeResponse, BookmarkResponse
)
from auth import create_user, authenticate_user, get_user_by_id

# Initialize FastAPI app
app = FastAPI(title="News Sharing API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_database()


# ==================== USER ROUTES ====================

@app.post("/users/register", response_model=UserResponse)
def register_user(user: UserCreate):
    """Register a new user."""
    new_user = create_user(user.username, user.email, user.password)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    return new_user


@app.post("/users/login")
def login_user(credentials: UserLogin):
    """Login a user."""
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get user by ID."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ==================== CATEGORY ROUTES ====================

@app.get("/categories/", response_model=List[CategoryResponse])
def get_categories():
    """Get all categories."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY name')
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return categories


@app.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate):
    """Create a new category."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO categories (name, description, color)
            VALUES (?, ?, ?)
        ''', (category.name, category.description, category.color))
        category_id = cursor.lastrowid
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )
    
    cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    new_category = dict(cursor.fetchone())
    conn.close()
    return new_category


# ==================== ARTICLE ROUTES ====================

@app.get("/articles/", response_model=List[ArticleResponse])
def get_articles(
    category_id: Optional[int] = None,
    author_id: Optional[int] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, le=100),
    offset: int = 0
):
    """Get all articles with optional filters."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            a.*,
            u.username as author_name,
            c.name as category_name,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.is_published = 1
    '''
    params = []
    
    if category_id:
        query += ' AND a.category_id = ?'
        params.append(category_id)
    
    if author_id:
        query += ' AND a.author_id = ?'
        params.append(author_id)
    
    if search:
        query += ' AND (a.title LIKE ? OR a.content LIKE ?)'
        search_term = f'%{search}%'
        params.extend([search_term, search_term])
    
    query += ' ORDER BY a.created_at DESC LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    articles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return articles


@app.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int):
    """Get a single article by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Increment view count
    cursor.execute('UPDATE articles SET views = views + 1 WHERE id = ?', (article_id,))
    conn.commit()
    
    cursor.execute('''
        SELECT 
            a.*,
            u.username as author_name,
            c.name as category_name,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return dict(article)


@app.post("/articles/", response_model=ArticleResponse)
def create_article(article: ArticleCreate, author_id: int):
    """Create a new article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate summary if not provided
    summary = article.summary or article.content[:200] + '...' if len(article.content) > 200 else article.content
    
    cursor.execute('''
        INSERT INTO articles (title, content, summary, image_url, source_url, author_id, category_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        article.title,
        article.content,
        summary,
        article.image_url,
        article.source_url,
        author_id,
        article.category_id
    ))
    
    article_id = cursor.lastrowid
    conn.commit()
    
    # Fetch the created article with joins
    cursor.execute('''
        SELECT 
            a.*,
            u.username as author_name,
            c.name as category_name,
            0 as likes_count,
            0 as comments_count
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.id = ?
    ''', (article_id,))
    
    new_article = dict(cursor.fetchone())
    conn.close()
    return new_article


@app.put("/articles/{article_id}", response_model=ArticleResponse)
def update_article(article_id: int, article: ArticleUpdate, user_id: int):
    """Update an article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if article exists and user is the author
    cursor.execute('SELECT author_id FROM articles WHERE id = ?', (article_id,))
    existing = cursor.fetchone()
    
    if not existing:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if existing['author_id'] != user_id:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own articles"
        )
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    if article.title is not None:
        update_fields.append('title = ?')
        params.append(article.title)
    if article.content is not None:
        update_fields.append('content = ?')
        params.append(article.content)
    if article.summary is not None:
        update_fields.append('summary = ?')
        params.append(article.summary)
    if article.image_url is not None:
        update_fields.append('image_url = ?')
        params.append(article.image_url)
    if article.source_url is not None:
        update_fields.append('source_url = ?')
        params.append(article.source_url)
    if article.category_id is not None:
        update_fields.append('category_id = ?')
        params.append(article.category_id)
    if article.is_published is not None:
        update_fields.append('is_published = ?')
        params.append(1 if article.is_published else 0)
    
    update_fields.append('updated_at = ?')
    params.append(datetime.now().isoformat())
    params.append(article_id)
    
    cursor.execute(f'''
        UPDATE articles SET {', '.join(update_fields)} WHERE id = ?
    ''', params)
    
    conn.commit()
    
    # Fetch updated article
    cursor.execute('''
        SELECT 
            a.*,
            u.username as author_name,
            c.name as category_name,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.id = ?
    ''', (article_id,))
    
    updated_article = dict(cursor.fetchone())
    conn.close()
    return updated_article


@app.delete("/articles/{article_id}")
def delete_article(article_id: int, user_id: int):
    """Delete an article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if article exists and user is the author
    cursor.execute('SELECT author_id FROM articles WHERE id = ?', (article_id,))
    existing = cursor.fetchone()
    
    if not existing:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if existing['author_id'] != user_id:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own articles"
        )
    
    cursor.execute('DELETE FROM articles WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Article deleted successfully"}


# ==================== COMMENT ROUTES ====================

@app.get("/articles/{article_id}/comments", response_model=List[CommentResponse])
def get_comments(article_id: int):
    """Get all comments for an article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.*, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.article_id = ?
        ORDER BY c.created_at DESC
    ''', (article_id,))
    
    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comments


@app.post("/comments/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, user_id: int):
    """Create a new comment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO comments (article_id, user_id, content)
        VALUES (?, ?, ?)
    ''', (comment.article_id, user_id, comment.content))
    
    comment_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('''
        SELECT c.*, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.id = ?
    ''', (comment_id,))
    
    new_comment = dict(cursor.fetchone())
    conn.close()
    return new_comment


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, user_id: int):
    """Delete a comment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM comments WHERE id = ?', (comment_id,))
    existing = cursor.fetchone()
    
    if not existing:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if existing['user_id'] != user_id:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )
    
    cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Comment deleted successfully"}


# ==================== LIKE ROUTES ====================

@app.post("/articles/{article_id}/like")
def toggle_like(article_id: int, user_id: int):
    """Toggle like on an article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if already liked
    cursor.execute('''
        SELECT id FROM likes WHERE article_id = ? AND user_id = ?
    ''', (article_id, user_id))
    
    existing = cursor.fetchone()
    
    if existing:
        # Unlike
        cursor.execute('DELETE FROM likes WHERE id = ?', (existing['id'],))
        message = "Article unliked"
        liked = False
    else:
        # Like
        cursor.execute('''
            INSERT INTO likes (article_id, user_id) VALUES (?, ?)
        ''', (article_id, user_id))
        message = "Article liked"
        liked = True
    
    conn.commit()
    
    # Get updated like count
    cursor.execute('SELECT COUNT(*) as count FROM likes WHERE article_id = ?', (article_id,))
    likes_count = cursor.fetchone()['count']
    
    conn.close()
    return {"message": message, "liked": liked, "likes_count": likes_count}


@app.get("/articles/{article_id}/liked")
def check_if_liked(article_id: int, user_id: int):
    """Check if user has liked an article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM likes WHERE article_id = ? AND user_id = ?
    ''', (article_id, user_id))
    
    liked = cursor.fetchone() is not None
    conn.close()
    return {"liked": liked}


# ==================== BOOKMARK ROUTES ====================

@app.post("/articles/{article_id}/bookmark")
def toggle_bookmark(article_id: int, user_id: int):
    """Toggle bookmark on an article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if already bookmarked
    cursor.execute('''
        SELECT id FROM bookmarks WHERE article_id = ? AND user_id = ?
    ''', (article_id, user_id))
    
    existing = cursor.fetchone()
    
    if existing:
        # Remove bookmark
        cursor.execute('DELETE FROM bookmarks WHERE id = ?', (existing['id'],))
        message = "Bookmark removed"
        bookmarked = False
    else:
        # Add bookmark
        cursor.execute('''
            INSERT INTO bookmarks (article_id, user_id) VALUES (?, ?)
        ''', (article_id, user_id))
        message = "Article bookmarked"
        bookmarked = True
    
    conn.commit()
    conn.close()
    return {"message": message, "bookmarked": bookmarked}


@app.get("/users/{user_id}/bookmarks", response_model=List[ArticleResponse])
def get_user_bookmarks(user_id: int):
    """Get all bookmarked articles for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            a.*,
            u.username as author_name,
            c.name as category_name,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count
        FROM articles a
        JOIN bookmarks b ON a.id = b.article_id
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    ''', (user_id,))
    
    articles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return articles


# ==================== STATS ROUTES ====================

@app.get("/stats/trending")
def get_trending_articles(limit: int = 10):
    """Get trending articles based on views and engagement."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            a.*,
            u.username as author_name,
            c.name as category_name,
            (SELECT COUNT(*) FROM likes WHERE article_id = a.id) as likes_count,
            (SELECT COUNT(*) FROM comments WHERE article_id = a.id) as comments_count,
            (a.views + 
             (SELECT COUNT(*) FROM likes WHERE article_id = a.id) * 2 +
             (SELECT COUNT(*) FROM comments WHERE article_id = a.id) * 3) as engagement_score
        FROM articles a
        LEFT JOIN users u ON a.author_id = u.id
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.is_published = 1
        ORDER BY engagement_score DESC
        LIMIT ?
    ''', (limit,))
    
    articles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return articles


@app.get("/stats/overview")
def get_stats_overview():
    """Get overall statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    cursor.execute('SELECT COUNT(*) as count FROM users')
    stats['total_users'] = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM articles WHERE is_published = 1')
    stats['total_articles'] = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM comments')
    stats['total_comments'] = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM likes')
    stats['total_likes'] = cursor.fetchone()['count']
    
    cursor.execute('SELECT SUM(views) as total FROM articles')
    result = cursor.fetchone()
    stats['total_views'] = result['total'] if result['total'] else 0
    
    conn.close()
    return stats


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
