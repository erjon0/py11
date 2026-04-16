# NewsHub - News Sharing Platform

A full-stack news sharing website built with Streamlit (frontend) and FastAPI (backend).

## Features

- **User Authentication**: Register, login, logout with session tokens
- **Article Management**: Create, edit, delete articles with rich content
- **Categories**: 8 predefined news categories with color coding
- **Interactions**: Like, comment, and bookmark articles
- **Search**: Full-text search across articles
- **Trending**: View popular articles by engagement
- **Analytics**: Personal dashboard with stats and charts
- **JSON Export/Import**: Backup and restore data

## Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: FastAPI with SQLite database
- **Data**: SQLite for persistence, JSON for backups
- **Charts**: Plotly for visualizations

## Quick Start

1. Install dependencies:
```bash
cd book_management-main
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Access the app:
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## Running Separately

**Start the API server:**
```bash
uvicorn main:app --reload --port 8000
```

**Start the Streamlit app:**
```bash
streamlit run app.py
```

## API Endpoints

### Users
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user
- `POST /api/users/logout` - Logout user
- `GET /api/users/me` - Get current user info
- `GET /api/users/stats` - Get user statistics

### Articles
- `GET /api/articles` - List articles (with filters)
- `GET /api/articles/trending` - Get trending articles
- `GET /api/articles/my-articles` - Get user's articles
- `GET /api/articles/{id}` - Get single article
- `POST /api/articles` - Create article
- `PUT /api/articles/{id}` - Update article
- `DELETE /api/articles/{id}` - Delete article

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Interactions
- `GET /api/comments/{article_id}` - Get comments
- `POST /api/comments` - Add comment
- `DELETE /api/comments/{id}` - Delete comment
- `POST /api/likes` - Toggle like
- `GET /api/likes/{article_id}/status` - Check like status
- `POST /api/bookmarks` - Toggle bookmark
- `GET /api/bookmarks` - Get bookmarked articles

### Data
- `POST /api/export-json` - Export data to JSON
- `POST /api/import-json` - Import data from JSON

## Database Schema

- **users**: id, username, email, password_hash, created_at, is_admin
- **categories**: id, name, description, color
- **articles**: id, title, content, summary, author_id, category_id, image_url, views, created_at, updated_at, is_published
- **comments**: id, article_id, user_id, content, created_at
- **likes**: id, article_id, user_id, created_at
- **bookmarks**: id, article_id, user_id, created_at
