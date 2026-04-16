from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User models
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None
    is_admin: bool = False


class UserLogin(BaseModel):
    username: str
    password: str


# Category models
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: str = '#3B82F6'


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int


# Article models
class ArticleBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    category_id: Optional[int] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None


class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    views: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_published: bool = True
    author_name: Optional[str] = None
    category_name: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0


# Comment models
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    article_id: int


class CommentResponse(CommentBase):
    id: int
    article_id: int
    user_id: int
    username: Optional[str] = None
    created_at: Optional[datetime] = None


# Like/Bookmark models
class LikeResponse(BaseModel):
    id: int
    article_id: int
    user_id: int


class BookmarkResponse(BaseModel):
    id: int
    article_id: int
    user_id: int
