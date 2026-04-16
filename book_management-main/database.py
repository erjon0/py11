import sqlite3
import json
import os
from datetime import datetime

DATABASE_PATH = 'news.db'
JSON_BACKUP_PATH = 'data_backup.json'


def get_db_connection():
    """Establish a connection to the SQLite database"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    """Set up the SQLite database with news sharing tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin INTEGER DEFAULT 0
        )
    ''')

    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            color TEXT DEFAULT '#3B82F6'
        )
    ''')

    # Articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            summary TEXT,
            author_id INTEGER NOT NULL,
            category_id INTEGER,
            image_url TEXT,
            views INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_published INTEGER DEFAULT 1,
            FOREIGN KEY (author_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Likes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(article_id, user_id),
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Bookmarks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(article_id, user_id),
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Insert default categories
    default_categories = [
        ('Technology', 'Tech news, gadgets, and innovations', '#3B82F6'),
        ('Politics', 'Political news and analysis', '#EF4444'),
        ('Sports', 'Sports news and updates', '#10B981'),
        ('Entertainment', 'Movies, music, and celebrity news', '#F59E0B'),
        ('Business', 'Business and financial news', '#6366F1'),
        ('Science', 'Scientific discoveries and research', '#8B5CF6'),
        ('Health', 'Health and wellness news', '#EC4899'),
        ('World', 'International news and events', '#14B8A6')
    ]

    for name, desc, color in default_categories:
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name, description, color) 
            VALUES (?, ?, ?)
        ''', (name, desc, color))

    conn.commit()
    conn.close()


def export_to_json():
    """Export all database data to JSON file"""
    conn = get_db_connection()
    cursor = conn.cursor()

    data = {
        'exported_at': datetime.now().isoformat(),
        'users': [],
        'categories': [],
        'articles': [],
        'comments': [],
        'likes': [],
        'bookmarks': []
    }

    # Export users (without password hashes for security)
    cursor.execute("SELECT id, username, email, created_at, is_admin FROM users")
    for row in cursor.fetchall():
        data['users'].append({
            'id': row['id'],
            'username': row['username'],
            'email': row['email'],
            'created_at': row['created_at'],
            'is_admin': row['is_admin']
        })

    # Export categories
    cursor.execute("SELECT * FROM categories")
    for row in cursor.fetchall():
        data['categories'].append(dict(row))

    # Export articles
    cursor.execute("SELECT * FROM articles")
    for row in cursor.fetchall():
        data['articles'].append(dict(row))

    # Export comments
    cursor.execute("SELECT * FROM comments")
    for row in cursor.fetchall():
        data['comments'].append(dict(row))

    # Export likes
    cursor.execute("SELECT * FROM likes")
    for row in cursor.fetchall():
        data['likes'].append(dict(row))

    # Export bookmarks
    cursor.execute("SELECT * FROM bookmarks")
    for row in cursor.fetchall():
        data['bookmarks'].append(dict(row))

    conn.close()

    with open(JSON_BACKUP_PATH, 'w') as f:
        json.dump(data, f, indent=2, default=str)

    return data


def import_from_json(json_path=JSON_BACKUP_PATH):
    """Import data from JSON file to database"""
    if not os.path.exists(json_path):
        return False

    with open(json_path, 'r') as f:
        data = json.load(f)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Import categories
    for cat in data.get('categories', []):
        cursor.execute('''
            INSERT OR REPLACE INTO categories (id, name, description, color)
            VALUES (?, ?, ?, ?)
        ''', (cat['id'], cat['name'], cat.get('description'), cat.get('color', '#3B82F6')))

    # Import articles
    for article in data.get('articles', []):
        cursor.execute('''
            INSERT OR REPLACE INTO articles 
            (id, title, content, summary, author_id, category_id, image_url, views, created_at, updated_at, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article['id'], article['title'], article['content'], article.get('summary'),
            article['author_id'], article.get('category_id'), article.get('image_url'),
            article.get('views', 0), article.get('created_at'), article.get('updated_at'),
            article.get('is_published', 1)
        ))

    # Import comments
    for comment in data.get('comments', []):
        cursor.execute('''
            INSERT OR REPLACE INTO comments (id, article_id, user_id, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (comment['id'], comment['article_id'], comment['user_id'], comment['content'], comment.get('created_at')))

    # Import likes
    for like in data.get('likes', []):
        cursor.execute('''
            INSERT OR IGNORE INTO likes (article_id, user_id, created_at)
            VALUES (?, ?, ?)
        ''', (like['article_id'], like['user_id'], like.get('created_at')))

    # Import bookmarks
    for bookmark in data.get('bookmarks', []):
        cursor.execute('''
            INSERT OR IGNORE INTO bookmarks (article_id, user_id, created_at)
            VALUES (?, ?, ?)
        ''', (bookmark['article_id'], bookmark['user_id'], bookmark.get('created_at')))

    conn.commit()
    conn.close()
    return True


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")
