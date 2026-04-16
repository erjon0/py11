from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# User Models
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    created_at: Optional[str] = None
    is_admin: int = 0


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: int = 0


# Category Models
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = '#3B82F6'


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int


# Article Models
class ArticleBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_published: Optional[int] = None


class Article(ArticleBase):
    id: int
    author_id: int
    views: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_published: int = 1


class ArticleWithDetails(Article):
    author_name: Optional[str] = None
    category_name: Optional[str] = None
    category_color: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0


# Comment Models
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    article_id: int


class Comment(CommentBase):
    id: int
    article_id: int
    user_id: int
    created_at: Optional[str] = None


class CommentWithUser(Comment):
    username: Optional[str] = None


# Like Models
class LikeCreate(BaseModel):
    article_id: int


class Like(BaseModel):
    id: int
    article_id: int
    user_id: int
    created_at: Optional[str] = None


# Bookmark Models
class BookmarkCreate(BaseModel):
    article_id: int


class Bookmark(BaseModel):
    id: int
    article_id: int
    user_id: int
    created_at: Optional[str] = None


# Statistics Models
class UserStats(BaseModel):
    total_articles: int
    total_likes_received: int
    total_comments_received: int
    total_views: int


class SiteStats(BaseModel):
    total_users: int
    total_articles: int
    total_comments: int
    total_likes: int
    articles_by_category: dict
