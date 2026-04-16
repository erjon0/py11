import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration
BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="NewsHub - Share & Discover News",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-top: 0;
    }
    .article-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
    }
    .article-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .article-meta {
        font-size: 0.875rem;
        color: #64748B;
    }
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #3B82F6, #1E40AF);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 0.875rem;
        opacity: 0.9;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
    }
    div[data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)


# Session state initialization
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'


# API Helper Functions
def api_get(endpoint, params=None):
    """Make a GET request to the API."""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API server. Make sure the backend is running.")
        return None


def api_post(endpoint, data=None, params=None):
    """Make a POST request to the API."""
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data, params=params)
        return response
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API server.")
        return None


def api_put(endpoint, data=None, params=None):
    """Make a PUT request to the API."""
    try:
        response = requests.put(f"{BASE_URL}{endpoint}", json=data, params=params)
        return response
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API server.")
        return None


def api_delete(endpoint, params=None):
    """Make a DELETE request to the API."""
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}", params=params)
        return response
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API server.")
        return None


# Authentication Functions
def login_user(username, password):
    """Login a user."""
    response = api_post("/users/login", {"username": username, "password": password})
    if response and response.status_code == 200:
        st.session_state.user = response.json()
        return True
    return False


def register_user(username, email, password):
    """Register a new user."""
    response = api_post("/users/register", {
        "username": username,
        "email": email,
        "password": password
    })
    if response and response.status_code == 200:
        st.session_state.user = response.json()
        return True, None
    elif response:
        return False, response.json().get('detail', 'Registration failed')
    return False, "Connection error"


def logout_user():
    """Logout the current user."""
    st.session_state.user = None
    st.session_state.page = 'home'


# Sidebar Navigation
def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown("## 📰 NewsHub")
        st.markdown("---")
        
        # User section
        if st.session_state.user:
            st.markdown(f"**Welcome, {st.session_state.user['username']}!**")
            
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("📝 Write Article", use_container_width=True):
                st.session_state.page = 'write'
                st.rerun()
            
            if st.button("📚 My Articles", use_container_width=True):
                st.session_state.page = 'my_articles'
                st.rerun()
            
            if st.button("🔖 Bookmarks", use_container_width=True):
                st.session_state.page = 'bookmarks'
                st.rerun()
            
            if st.button("📊 Analytics", use_container_width=True):
                st.session_state.page = 'analytics'
                st.rerun()
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
        else:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
            
            if st.button("📝 Register", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("---")
        
        # Categories filter
        st.markdown("### Categories")
        categories = api_get("/categories/")
        if categories:
            if st.button("All Categories", use_container_width=True):
                st.session_state.selected_category = None
                st.session_state.page = 'home'
                st.rerun()
            
            for cat in categories:
                if st.button(f"{cat['name']}", key=f"cat_{cat['id']}", use_container_width=True):
                    st.session_state.selected_category = cat['id']
                    st.session_state.page = 'home'
                    st.rerun()


# Page Renderers
def render_home():
    """Render the home page with news feed."""
    st.markdown('<h1 class="main-header">Latest News</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Stay informed with the latest stories</p>', unsafe_allow_html=True)
    
    # Search bar
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input("🔍 Search articles", placeholder="Search by title or content...")
    with col2:
        st.write("")
        st.write("")
        search_button = st.button("Search", use_container_width=True)
    
    # Fetch articles
    params = {}
    if hasattr(st.session_state, 'selected_category') and st.session_state.selected_category:
        params['category_id'] = st.session_state.selected_category
    if search_query:
        params['search'] = search_query
    
    articles = api_get("/articles/", params)
    
    if not articles:
        st.info("No articles found. Be the first to share news!")
        return
    
    # Display articles in a grid
    for i in range(0, len(articles), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(articles):
                article = articles[i + j]
                with col:
                    render_article_card(article)


def render_article_card(article):
    """Render an article card."""
    with st.container():
        # Category badge
        category_color = "#3B82F6"
        if article.get('category_name'):
            st.markdown(
                f'<span class="category-badge" style="background-color: {category_color}20; color: {category_color};">'
                f'{article["category_name"]}</span>',
                unsafe_allow_html=True
            )
        
        # Title
        st.markdown(f"### {article['title']}")
        
        # Meta info
        created_at = article.get('created_at', '')[:10] if article.get('created_at') else 'Unknown'
        st.markdown(
            f"<p class='article-meta'>By <strong>{article.get('author_name', 'Anonymous')}</strong> | "
            f"{created_at} | 👁 {article.get('views', 0)} views</p>",
            unsafe_allow_html=True
        )
        
        # Summary
        summary = article.get('summary', article.get('content', '')[:150])
        st.write(summary[:200] + '...' if len(summary) > 200 else summary)
        
        # Actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"❤️ {article.get('likes_count', 0)}", key=f"like_{article['id']}"):
                if st.session_state.user:
                    api_post(f"/articles/{article['id']}/like", params={"user_id": st.session_state.user['id']})
                    st.rerun()
                else:
                    st.warning("Please login to like articles")
        
        with col2:
            if st.button(f"💬 {article.get('comments_count', 0)}", key=f"comment_{article['id']}"):
                st.session_state.viewing_article = article['id']
                st.session_state.page = 'article'
                st.rerun()
        
        with col3:
            if st.button("📖 Read", key=f"read_{article['id']}"):
                st.session_state.viewing_article = article['id']
                st.session_state.page = 'article'
                st.rerun()
        
        st.markdown("---")


def render_article_page():
    """Render the full article page."""
    if not hasattr(st.session_state, 'viewing_article'):
        st.session_state.page = 'home'
        st.rerun()
        return
    
    article = api_get(f"/articles/{st.session_state.viewing_article}")
    
    if not article:
        st.error("Article not found")
        return
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    # Article header
    if article.get('category_name'):
        st.markdown(
            f'<span class="category-badge" style="background-color: #3B82F620; color: #3B82F6;">'
            f'{article["category_name"]}</span>',
            unsafe_allow_html=True
        )
    
    st.markdown(f"# {article['title']}")
    
    # Meta
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**Author:** {article.get('author_name', 'Anonymous')}")
    with col2:
        created_at = article.get('created_at', '')[:10] if article.get('created_at') else 'Unknown'
        st.markdown(f"**Published:** {created_at}")
    with col3:
        st.markdown(f"**Views:** {article.get('views', 0)}")
    with col4:
        st.markdown(f"**Likes:** {article.get('likes_count', 0)}")
    
    st.markdown("---")
    
    # Image
    if article.get('image_url'):
        st.image(article['image_url'], use_container_width=True)
    
    # Content
    st.markdown(article['content'])
    
    # Source
    if article.get('source_url'):
        st.markdown(f"[📎 Original Source]({article['source_url']})")
    
    st.markdown("---")
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.user:
            if st.button("❤️ Like this article"):
                api_post(f"/articles/{article['id']}/like", params={"user_id": st.session_state.user['id']})
                st.rerun()
    with col2:
        if st.session_state.user:
            if st.button("🔖 Bookmark"):
                api_post(f"/articles/{article['id']}/bookmark", params={"user_id": st.session_state.user['id']})
                st.success("Article bookmarked!")
    
    st.markdown("---")
    
    # Comments section
    st.markdown("## Comments")
    
    comments = api_get(f"/articles/{article['id']}/comments")
    
    # Add comment form
    if st.session_state.user:
        with st.form("comment_form"):
            comment_text = st.text_area("Write a comment...")
            submitted = st.form_submit_button("Post Comment")
            
            if submitted and comment_text.strip():
                response = api_post("/comments/", {
                    "article_id": article['id'],
                    "content": comment_text
                }, params={"user_id": st.session_state.user['id']})
                
                if response and response.status_code == 200:
                    st.success("Comment posted!")
                    st.rerun()
                else:
                    st.error("Failed to post comment")
    else:
        st.info("Please login to comment")
    
    # Display comments
    if comments:
        for comment in comments:
            with st.container():
                st.markdown(f"**{comment.get('username', 'Anonymous')}** - {comment.get('created_at', '')[:10]}")
                st.write(comment['content'])
                
                # Delete button for own comments
                if st.session_state.user and comment.get('user_id') == st.session_state.user['id']:
                    if st.button("🗑️ Delete", key=f"del_comment_{comment['id']}"):
                        api_delete(f"/comments/{comment['id']}", params={"user_id": st.session_state.user['id']})
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("No comments yet. Be the first to comment!")


def render_write_article():
    """Render the write article page."""
    if not st.session_state.user:
        st.warning("Please login to write articles")
        return
    
    st.markdown("# ✍️ Write New Article")
    st.markdown("Share your news with the community")
    
    categories = api_get("/categories/")
    category_options = {cat['name']: cat['id'] for cat in categories} if categories else {}
    
    with st.form("article_form"):
        title = st.text_input("Title *", placeholder="Enter a compelling headline...")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_category = st.selectbox("Category", list(category_options.keys()) if category_options else [])
        with col2:
            source_url = st.text_input("Source URL (optional)", placeholder="https://...")
        
        image_url = st.text_input("Image URL (optional)", placeholder="https://...")
        
        content = st.text_area("Content *", height=300, placeholder="Write your article here...")
        
        summary = st.text_area("Summary (optional)", height=100, 
                               placeholder="Brief summary of the article (auto-generated if left empty)")
        
        submitted = st.form_submit_button("📤 Publish Article", use_container_width=True)
        
        if submitted:
            if not title.strip() or not content.strip():
                st.error("Title and content are required")
            else:
                article_data = {
                    "title": title,
                    "content": content,
                    "summary": summary if summary else None,
                    "image_url": image_url if image_url else None,
                    "source_url": source_url if source_url else None,
                    "category_id": category_options.get(selected_category) if selected_category else None
                }
                
                response = api_post("/articles/", article_data, 
                                   params={"author_id": st.session_state.user['id']})
                
                if response and response.status_code == 200:
                    st.success("Article published successfully!")
                    st.session_state.page = 'my_articles'
                    st.rerun()
                else:
                    st.error("Failed to publish article")


def render_my_articles():
    """Render user's articles page."""
    if not st.session_state.user:
        st.warning("Please login to view your articles")
        return
    
    st.markdown("# 📚 My Articles")
    
    articles = api_get("/articles/", params={"author_id": st.session_state.user['id']})
    
    if not articles:
        st.info("You haven't written any articles yet.")
        if st.button("Write your first article"):
            st.session_state.page = 'write'
            st.rerun()
        return
    
    for article in articles:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"### {article['title']}")
                created_at = article.get('created_at', '')[:10] if article.get('created_at') else 'Unknown'
                st.markdown(f"Published: {created_at} | Views: {article.get('views', 0)} | "
                           f"Likes: {article.get('likes_count', 0)} | Comments: {article.get('comments_count', 0)}")
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{article['id']}"):
                    st.session_state.editing_article = article['id']
                    st.session_state.page = 'edit_article'
                    st.rerun()
                
                if st.button("🗑️ Delete", key=f"delete_{article['id']}"):
                    response = api_delete(f"/articles/{article['id']}", 
                                         params={"user_id": st.session_state.user['id']})
                    if response and response.status_code == 200:
                        st.success("Article deleted")
                        st.rerun()
            
            st.markdown("---")


def render_edit_article():
    """Render the edit article page."""
    if not st.session_state.user or not hasattr(st.session_state, 'editing_article'):
        st.session_state.page = 'my_articles'
        st.rerun()
        return
    
    article = api_get(f"/articles/{st.session_state.editing_article}")
    
    if not article:
        st.error("Article not found")
        return
    
    st.markdown("# ✏️ Edit Article")
    
    categories = api_get("/categories/")
    category_options = {cat['name']: cat['id'] for cat in categories} if categories else {}
    category_names = list(category_options.keys())
    
    # Find current category index
    current_category_index = 0
    if article.get('category_name') in category_names:
        current_category_index = category_names.index(article['category_name'])
    
    with st.form("edit_article_form"):
        title = st.text_input("Title *", value=article['title'])
        
        col1, col2 = st.columns(2)
        with col1:
            selected_category = st.selectbox("Category", category_names, index=current_category_index)
        with col2:
            source_url = st.text_input("Source URL", value=article.get('source_url', '') or '')
        
        image_url = st.text_input("Image URL", value=article.get('image_url', '') or '')
        
        content = st.text_area("Content *", value=article['content'], height=300)
        
        summary = st.text_area("Summary", value=article.get('summary', '') or '', height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)
        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state.page = 'my_articles'
                st.rerun()
        
        if submitted:
            if not title.strip() or not content.strip():
                st.error("Title and content are required")
            else:
                update_data = {
                    "title": title,
                    "content": content,
                    "summary": summary if summary else None,
                    "image_url": image_url if image_url else None,
                    "source_url": source_url if source_url else None,
                    "category_id": category_options.get(selected_category) if selected_category else None
                }
                
                response = api_put(f"/articles/{article['id']}", update_data,
                                  params={"user_id": st.session_state.user['id']})
                
                if response and response.status_code == 200:
                    st.success("Article updated successfully!")
                    st.session_state.page = 'my_articles'
                    st.rerun()
                else:
                    st.error("Failed to update article")


def render_bookmarks():
    """Render bookmarked articles page."""
    if not st.session_state.user:
        st.warning("Please login to view your bookmarks")
        return
    
    st.markdown("# 🔖 My Bookmarks")
    
    articles = api_get(f"/users/{st.session_state.user['id']}/bookmarks")
    
    if not articles:
        st.info("You haven't bookmarked any articles yet.")
        return
    
    for article in articles:
        render_article_card(article)


def render_analytics():
    """Render analytics dashboard."""
    st.markdown("# 📊 Analytics Dashboard")
    
    # Overview stats
    stats = api_get("/stats/overview")
    
    if stats:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Users", stats.get('total_users', 0))
        with col2:
            st.metric("Total Articles", stats.get('total_articles', 0))
        with col3:
            st.metric("Total Comments", stats.get('total_comments', 0))
        with col4:
            st.metric("Total Likes", stats.get('total_likes', 0))
        with col5:
            st.metric("Total Views", stats.get('total_views', 0))
    
    st.markdown("---")
    
    # Trending articles
    st.markdown("## 🔥 Trending Articles")
    
    trending = api_get("/stats/trending", params={"limit": 10})
    
    if trending:
        df_trending = pd.DataFrame(trending)
        
        # Create engagement chart
        fig = px.bar(
            df_trending,
            x='title',
            y=['views', 'likes_count', 'comments_count'],
            title='Article Engagement',
            labels={'value': 'Count', 'title': 'Article'},
            barmode='group'
        )
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Table view
        st.dataframe(
            df_trending[['title', 'author_name', 'category_name', 'views', 'likes_count', 'comments_count']],
            use_container_width=True
        )
    
    # Category distribution
    st.markdown("## 📁 Articles by Category")
    
    articles = api_get("/articles/", params={"limit": 100})
    
    if articles:
        df_articles = pd.DataFrame(articles)
        
        if 'category_name' in df_articles.columns:
            category_counts = df_articles['category_name'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            fig_pie = px.pie(
                category_counts,
                values='Count',
                names='Category',
                title='Distribution of Articles by Category',
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)


def render_login():
    """Render login page."""
    st.markdown("# 🔐 Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if username and password:
                    if login_user(username, password):
                        st.success("Login successful!")
                        st.session_state.page = 'home'
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
        
        st.markdown("---")
        st.markdown("Don't have an account?")
        if st.button("Register here", use_container_width=True):
            st.session_state.page = 'register'
            st.rerun()


def render_register():
    """Render registration page."""
    st.markdown("# 📝 Create Account")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            username = st.text_input("Username *")
            email = st.text_input("Email *")
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
            
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                if not all([username, email, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, error = register_user(username, email, password)
                    if success:
                        st.success("Account created successfully!")
                        st.session_state.page = 'home'
                        st.rerun()
                    else:
                        st.error(error)
        
        st.markdown("---")
        st.markdown("Already have an account?")
        if st.button("Login here", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()


# Main App Logic
def main():
    """Main application entry point."""
    render_sidebar()
    
    # Route to appropriate page
    page = st.session_state.page
    
    if page == 'home':
        render_home()
    elif page == 'article':
        render_article_page()
    elif page == 'write':
        render_write_article()
    elif page == 'my_articles':
        render_my_articles()
    elif page == 'edit_article':
        render_edit_article()
    elif page == 'bookmarks':
        render_bookmarks()
    elif page == 'analytics':
        render_analytics()
    elif page == 'login':
        render_login()
    elif page == 'register':
        render_register()
    else:
        render_home()


if __name__ == "__main__":
    main()
