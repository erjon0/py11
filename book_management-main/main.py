from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, categories, articles, interactions
from database import create_database, export_to_json, import_from_json

# Initialize FastAPI app
app = FastAPI(
    title="News Sharing Platform",
    description="A full-featured news sharing API with user authentication, articles, comments, likes, and bookmarks.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(articles.router, prefix="/api/articles", tags=["Articles"])
app.include_router(interactions.router, prefix="/api", tags=["Interactions"])


@app.on_event("startup")
def startup():
    """Initialize the database tables on startup"""
    create_database()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the News Sharing Platform API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/export-json")
def export_data():
    """Export all data to JSON file"""
    data = export_to_json()
    return {"message": "Data exported successfully", "file": "data_backup.json"}


@app.post("/api/import-json")
def import_data():
    """Import data from JSON file"""
    success = import_from_json()
    if success:
        return {"message": "Data imported successfully"}
    return {"message": "No backup file found"}
