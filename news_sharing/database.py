import sqlite3
from datetime import datetime


def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('news.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    """Set up the SQLite database with all required tables."""
    conn = get_db_connection()
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

    # News articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            summary TEXT,
            image_url TEXT,
            source_url TEXT,
            author_id INTEGER NOT NULL,
            category_id INTEGER,
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

    conn.commit()
    return conn, cursor


def seed_categories(cursor, conn):
    """Seed initial categories."""
    categories = [
        ('Technology', 'Latest tech news and innovations', '#3B82F6'),
        ('Politics', 'Political news and updates', '#EF4444'),
        ('Sports', 'Sports news and highlights', '#10B981'),
        ('Entertainment', 'Movies, music, and celebrity news', '#F59E0B'),
        ('Business', 'Business and finance news', '#6366F1'),
        ('Science', 'Scientific discoveries and research', '#8B5CF6'),
        ('Health', 'Health and wellness news', '#EC4899'),
        ('World', 'International news', '#14B8A6'),
    ]
    
    for name, description, color in categories:
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name, description, color)
            VALUES (?, ?, ?)
        ''', (name, description, color))
    
    conn.commit()


def init_database():
    """Initialize the database with tables and seed data."""
    conn, cursor = create_database()
    seed_categories(cursor, conn)
    return conn


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")
