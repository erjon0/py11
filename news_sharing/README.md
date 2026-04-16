# NewsHub - News Sharing Platform

A full-stack news sharing website built with Streamlit (frontend) and FastAPI (backend) with SQLite database.

## Features

- **User Authentication**: Register, login, and manage your account
- **Article Management**: Create, edit, delete, and publish news articles
- **Categories**: Browse articles by category (Technology, Politics, Sports, etc.)
- **Social Features**: Like, comment, and bookmark articles
- **Search**: Search articles by title or content
- **Analytics Dashboard**: View trending articles and platform statistics
- **Responsive Design**: Clean, modern UI with Streamlit

## Project Structure

```
news_sharing/
├── api.py          # FastAPI backend with all API routes
├── app.py          # Streamlit frontend application
├── auth.py         # Authentication utilities
├── database.py     # SQLite database setup and utilities
├── models.py       # Pydantic models for data validation
├── requirements.txt
├── run.py          # Script to run both servers
└── README.md
```

## Installation

1. Navigate to the news_sharing directory:
   ```bash
   cd news_sharing
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Run both servers together
```bash
python run.py
```

### Option 2: Run servers separately

Terminal 1 - Start the API server:
```bash
uvicorn api:app --reload --port 8000
```

Terminal 2 - Start the Streamlit app:
```bash
streamlit run app.py
```

## Access the Application

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API (FastAPI)**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Users
- `POST /users/register` - Register a new user
- `POST /users/login` - Login
- `GET /users/{user_id}` - Get user details

### Articles
- `GET /articles/` - List all articles (with filters)
- `GET /articles/{id}` - Get single article
- `POST /articles/` - Create article
- `PUT /articles/{id}` - Update article
- `DELETE /articles/{id}` - Delete article

### Categories
- `GET /categories/` - List all categories
- `POST /categories/` - Create category

### Comments
- `GET /articles/{id}/comments` - Get comments for article
- `POST /comments/` - Create comment
- `DELETE /comments/{id}` - Delete comment

### Interactions
- `POST /articles/{id}/like` - Toggle like
- `POST /articles/{id}/bookmark` - Toggle bookmark
- `GET /users/{id}/bookmarks` - Get user bookmarks

### Statistics
- `GET /stats/trending` - Get trending articles
- `GET /stats/overview` - Get platform statistics

## Database

The application uses SQLite with the following tables:
- `users` - User accounts
- `categories` - News categories
- `articles` - News articles
- `comments` - Article comments
- `likes` - Article likes
- `bookmarks` - User bookmarks
