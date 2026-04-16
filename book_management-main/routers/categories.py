import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.news import Category, CategoryCreate
from database import get_db_connection
from auth.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[Category])
def get_categories():
    """Get all categories"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, description, color FROM categories ORDER BY name")
    categories = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in categories]


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int):
    """Get a single category by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, description, color FROM categories WHERE id = ?", (category_id,))
    category = cursor.fetchone()
    conn.close()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return dict(category)


@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, user_id: int = Depends(get_current_user)):
    """Create a new category (admin only in production)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO categories (name, description, color)
            VALUES (?, ?, ?)
        ''', (category.name, category.description, category.color))
        conn.commit()
        category_id = cursor.lastrowid
        conn.close()
        
        return Category(id=category_id, **category.dict())
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=409, detail=f"Category '{category.name}' already exists")


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, user_id: int = Depends(get_current_user)):
    """Update a category"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE categories SET name = ?, description = ?, color = ?
        WHERE id = ?
    ''', (category.name, category.description, category.color, category_id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")
    
    conn.commit()
    conn.close()
    
    return Category(id=category_id, **category.dict())


@router.delete("/{category_id}")
def delete_category(category_id: int, user_id: int = Depends(get_current_user)):
    """Delete a category"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")
    
    conn.commit()
    conn.close()
    
    return {"detail": "Category deleted successfully"}
