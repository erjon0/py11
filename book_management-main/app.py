import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import json

# Configuration
BASE_URL = "http://localhost:8000/api"

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
        color: #1E3A8A;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-top: 0;
    }
    .article-card {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #E2E8F0;
    }
    .article-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1E293B;
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
        color: white;
    }
    .stat-card {
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 0.875rem;
        opacity: 0.9;
    }
    .stButton>button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# Session state initialization
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'


init_session_state()


# API Helper Functions
def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def api_get(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=get_headers())
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Make sure it's running on port 8000.")
        return None


def api_post(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=get_headers())
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API server"}, 500


def api_put(endpoint, data):
    try:
        response = requests.put(f"{BASE_URL}{endpoint}", json=data, headers=get_headers())
        return response.json(), response.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API server"}, 500


def api_delete(endpoint):
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}", headers=get_headers())
        return response.json() if response.content else {}, response.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API server"}, 500


# Authentication Functions
def login(username, password):
    data, status = api_post("/users/login", {"username": username, "password": password})
    if status == 200:
        st.session_state.logged_in = True
        st.session_state.token = data.get('token')
        st.session_state.user = {
            'id': data.get('user_id'),
            'username': data.get('username'),
            'email': data.get('email')
        }
        return True, "Login successful!"
    return False, data.get('detail', 'Login failed')


def register(username, email, password):
    data, status = api_post("/users/register", {
        "username": username,
        "email": email,
        "password": password
    })
    if status == 200:
        st.session_state.logged_in = True
        st.session_state.token = data.get('token')
        st.session_state.user = {
            'id': data.get('user_id'),
            'username': data.get('username'),
            'email': email
        }
        return True, "Registration successful!"
    return False, data.get('detail', 'Registration failed')


def logout():
    api_post("/users/logout", {})
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user = None


# UI Components
def render_sidebar():
    with st.sidebar:
        st.markdown("### 📰 NewsHub")
        
        if st.session_state.logged_in:
            st.markdown(f"**Welcome, {st.session_state.user['username']}!**")
            st.divider()
            
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.button("🔥 Trending", use_container_width=True):
                st.session_state.current_page = 'trending'
                st.rerun()
            
            if st.button("✍️ Write Article", use_container_width=True):
                st.session_state.current_page = 'write'
                st.rerun()
            
            if st.button("📝 My Articles", use_container_width=True):
                st.session_state.current_page = 'my_articles'
                st.rerun()
            
            if st.button("🔖 Bookmarks", use_container_width=True):
                st.session_state.current_page = 'bookmarks'
                st.rerun()
            
            if st.button("📊 Analytics", use_container_width=True):
                st.session_state.current_page = 'analytics'
                st.rerun()
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        else:
            st.info("Login to access all features")
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
                        success, msg = login(username, password)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            
            with tab2:
                with st.form("register_form"):
                    new_username = st.text_input("Username", key="reg_user")
                    new_email = st.text_input("Email")
                    new_password = st.text_input("Password", type="password", key="reg_pass")
                    if st.form_submit_button("Register", use_container_width=True):
                        success, msg = register(new_username, new_email, new_password)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
        
        # Categories filter
        st.divider()
        st.markdown("### Categories")
        categories = api_get("/categories")
        if categories:
            for cat in categories:
                if st.button(f"{cat['name']}", key=f"cat_{cat['id']}", use_container_width=True):
                    st.session_state.current_page = 'home'
                    st.session_state.filter_category = cat['id']
                    st.rerun()


def render_article_card(article, show_actions=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Category badge
        cat_color = article.get('category_color', '#3B82F6')
        cat_name = article.get('category_name', 'General')
        st.markdown(f"""
            <span class="category-badge" style="background-color: {cat_color};">{cat_name}</span>
        """, unsafe_allow_html=True)
        
        # Title
        st.markdown(f"### {article['title']}")
        
        # Summary
        if article.get('summary'):
            st.markdown(article['summary'][:200] + "..." if len(article.get('summary', '')) > 200 else article.get('summary', ''))
        
        # Meta info
        author = article.get('author_name', 'Unknown')
        created = article.get('created_at', '')[:10] if article.get('created_at') else ''
        views = article.get('views', 0)
        likes = article.get('likes_count', 0)
        comments = article.get('comments_count', 0)
        
        st.markdown(f"**{author}** · {created} · 👁️ {views} · ❤️ {likes} · 💬 {comments}")
    
    with col2:
        if st.button("Read More", key=f"read_{article['id']}", use_container_width=True):
            st.session_state.current_page = 'article'
            st.session_state.current_article = article['id']
            st.rerun()
    
    st.divider()


def render_home():
    st.markdown('<h1 class="main-header">NewsHub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover and share the latest news</p>', unsafe_allow_html=True)
    
    # Search bar
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input("Search articles...", label_visibility="collapsed", placeholder="Search articles...")
    with col2:
        search_btn = st.button("🔍 Search", use_container_width=True)
    
    # Fetch articles
    endpoint = "/articles"
    params = []
    
    if hasattr(st.session_state, 'filter_category') and st.session_state.filter_category:
        params.append(f"category_id={st.session_state.filter_category}")
    
    if search_query and search_btn:
        params.append(f"search={search_query}")
    
    if params:
        endpoint += "?" + "&".join(params)
    
    articles = api_get(endpoint)
    
    if articles:
        for article in articles:
            render_article_card(article)
    else:
        st.info("No articles found. Be the first to write one!")


def render_trending():
    st.markdown("## 🔥 Trending Articles")
    st.markdown("Most popular articles based on views and engagement")
    
    articles = api_get("/articles/trending?limit=10")
    
    if articles:
        for i, article in enumerate(articles):
            col1, col2 = st.columns([1, 20])
            with col1:
                st.markdown(f"### #{i+1}")
            with col2:
                render_article_card(article, show_actions=True)
    else:
        st.info("No trending articles yet.")


def render_write_article():
    st.markdown("## ✍️ Write New Article")
    
    if not st.session_state.logged_in:
        st.warning("Please login to write articles.")
        return
    
    categories = api_get("/categories") or []
    
    with st.form("write_article"):
        title = st.text_input("Title", placeholder="Enter a compelling title...")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "Category",
                options=categories,
                format_func=lambda x: x['name']
            )
        with col2:
            image_url = st.text_input("Image URL (optional)", placeholder="https://...")
        
        summary = st.text_area("Summary", placeholder="Brief summary of your article...", max_chars=300)
        content = st.text_area("Content", placeholder="Write your full article here...", height=400)
        
        if st.form_submit_button("Publish Article", use_container_width=True):
            if title and content:
                data = {
                    "title": title,
                    "content": content,
                    "summary": summary,
                    "category_id": category['id'] if category else None,
                    "image_url": image_url if image_url else None
                }
                result, status = api_post("/articles", data)
                if status == 200:
                    st.success("Article published successfully!")
                    st.session_state.current_page = 'my_articles'
                    st.rerun()
                else:
                    st.error(result.get('detail', 'Failed to publish article'))
            else:
                st.error("Title and content are required.")


def render_article_detail():
    if not hasattr(st.session_state, 'current_article'):
        st.session_state.current_page = 'home'
        st.rerun()
        return
    
    article = api_get(f"/articles/{st.session_state.current_article}")
    
    if not article:
        st.error("Article not found.")
        return
    
    # Back button
    if st.button("← Back to Articles"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Article header
    cat_color = article.get('category_color', '#3B82F6')
    cat_name = article.get('category_name', 'General')
    st.markdown(f"""
        <span class="category-badge" style="background-color: {cat_color};">{cat_name}</span>
    """, unsafe_allow_html=True)
    
    st.markdown(f"# {article['title']}")
    
    # Meta
    author = article.get('author_name', 'Unknown')
    created = article.get('created_at', '')[:10] if article.get('created_at') else ''
    views = article.get('views', 0)
    st.markdown(f"**By {author}** · {created} · 👁️ {views} views")
    
    # Image
    if article.get('image_url'):
        st.image(article['image_url'], use_container_width=True)
    
    st.divider()
    
    # Content
    st.markdown(article['content'])
    
    st.divider()
    
    # Actions
    if st.session_state.logged_in:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Like button
            like_status = api_get(f"/likes/{article['id']}/status")
            liked = like_status.get('liked', False) if like_status else False
            like_count = like_status.get('count', 0) if like_status else 0
            
            if st.button(f"{'❤️' if liked else '🤍'} {like_count} Likes", use_container_width=True):
                api_post("/likes", {"article_id": article['id']})
                st.rerun()
        
        with col2:
            # Bookmark button
            bookmark_status = api_get(f"/bookmarks/{article['id']}/status")
            bookmarked = bookmark_status.get('bookmarked', False) if bookmark_status else False
            
            if st.button(f"{'🔖' if bookmarked else '📑'} {'Bookmarked' if bookmarked else 'Bookmark'}", use_container_width=True):
                api_post("/bookmarks", {"article_id": article['id']})
                st.rerun()
        
        with col3:
            st.markdown(f"💬 {article.get('comments_count', 0)} Comments")
    
    st.divider()
    
    # Comments section
    st.markdown("### Comments")
    
    comments = api_get(f"/comments/{article['id']}")
    
    if st.session_state.logged_in:
        with st.form("add_comment"):
            comment_text = st.text_area("Add a comment...", height=100)
            if st.form_submit_button("Post Comment"):
                if comment_text:
                    result, status = api_post("/comments", {
                        "article_id": article['id'],
                        "content": comment_text
                    })
                    if status == 200:
                        st.success("Comment posted!")
                        st.rerun()
                    else:
                        st.error("Failed to post comment")
    
    if comments:
        for comment in comments:
            with st.container():
                st.markdown(f"**{comment.get('username', 'Anonymous')}** · {comment.get('created_at', '')[:10]}")
                st.markdown(comment['content'])
                
                # Delete button if own comment
                if st.session_state.logged_in and st.session_state.user['id'] == comment.get('user_id'):
                    if st.button("Delete", key=f"del_comment_{comment['id']}"):
                        api_delete(f"/comments/{comment['id']}")
                        st.rerun()
                
                st.divider()
    else:
        st.info("No comments yet. Be the first to comment!")


def render_my_articles():
    st.markdown("## 📝 My Articles")
    
    if not st.session_state.logged_in:
        st.warning("Please login to view your articles.")
        return
    
    articles = api_get("/articles/my-articles")
    
    if articles:
        for article in articles:
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                cat_color = article.get('category_color', '#3B82F6')
                cat_name = article.get('category_name', 'General')
                st.markdown(f"""
                    <span class="category-badge" style="background-color: {cat_color};">{cat_name}</span>
                """, unsafe_allow_html=True)
                st.markdown(f"### {article['title']}")
                st.markdown(f"👁️ {article.get('views', 0)} · ❤️ {article.get('likes_count', 0)} · 💬 {article.get('comments_count', 0)}")
            
            with col2:
                if st.button("Edit", key=f"edit_{article['id']}", use_container_width=True):
                    st.session_state.current_page = 'edit_article'
                    st.session_state.edit_article_id = article['id']
                    st.rerun()
            
            with col3:
                if st.button("Delete", key=f"delete_{article['id']}", use_container_width=True):
                    api_delete(f"/articles/{article['id']}")
                    st.success("Article deleted!")
                    st.rerun()
            
            st.divider()
    else:
        st.info("You haven't written any articles yet.")
        if st.button("Write your first article"):
            st.session_state.current_page = 'write'
            st.rerun()


def render_edit_article():
    if not hasattr(st.session_state, 'edit_article_id'):
        st.session_state.current_page = 'my_articles'
        st.rerun()
        return
    
    article = api_get(f"/articles/{st.session_state.edit_article_id}")
    
    if not article:
        st.error("Article not found.")
        return
    
    st.markdown("## Edit Article")
    
    if st.button("← Back to My Articles"):
        st.session_state.current_page = 'my_articles'
        st.rerun()
    
    categories = api_get("/categories") or []
    
    with st.form("edit_article"):
        title = st.text_input("Title", value=article['title'])
        
        col1, col2 = st.columns(2)
        with col1:
            current_cat_index = 0
            for i, cat in enumerate(categories):
                if cat['id'] == article.get('category_id'):
                    current_cat_index = i
                    break
            
            category = st.selectbox(
                "Category",
                options=categories,
                format_func=lambda x: x['name'],
                index=current_cat_index
            )
        with col2:
            image_url = st.text_input("Image URL (optional)", value=article.get('image_url', ''))
        
        summary = st.text_area("Summary", value=article.get('summary', ''), max_chars=300)
        content = st.text_area("Content", value=article['content'], height=400)
        
        if st.form_submit_button("Update Article", use_container_width=True):
            data = {
                "title": title,
                "content": content,
                "summary": summary,
                "category_id": category['id'] if category else None,
                "image_url": image_url if image_url else None
            }
            result, status = api_put(f"/articles/{article['id']}", data)
            if status == 200:
                st.success("Article updated successfully!")
                st.session_state.current_page = 'my_articles'
                st.rerun()
            else:
                st.error(result.get('detail', 'Failed to update article'))


def render_bookmarks():
    st.markdown("## 🔖 Bookmarked Articles")
    
    if not st.session_state.logged_in:
        st.warning("Please login to view your bookmarks.")
        return
    
    articles = api_get("/bookmarks")
    
    if articles:
        for article in articles:
            render_article_card(article)
    else:
        st.info("No bookmarked articles yet.")


def render_analytics():
    st.markdown("## 📊 Analytics Dashboard")
    
    if not st.session_state.logged_in:
        st.warning("Please login to view analytics.")
        return
    
    stats = api_get("/users/stats")
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Articles", stats['total_articles'])
        
        with col2:
            st.metric("Total Views", stats['total_views'])
        
        with col3:
            st.metric("Likes Received", stats['total_likes_received'])
        
        with col4:
            st.metric("Comments Received", stats['total_comments_received'])
    
    # Charts
    articles = api_get("/articles/my-articles")
    
    if articles:
        st.divider()
        st.markdown("### Article Performance")
        
        df = pd.DataFrame(articles)
        
        if not df.empty:
            # Views chart
            fig_views = px.bar(
                df.head(10),
                x='title',
                y='views',
                title='Article Views',
                labels={'title': 'Article', 'views': 'Views'}
            )
            fig_views.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_views, use_container_width=True)
            
            # Engagement chart
            df['engagement'] = df['likes_count'] + df['comments_count']
            fig_engagement = px.bar(
                df.head(10),
                x='title',
                y=['likes_count', 'comments_count'],
                title='Article Engagement',
                labels={'title': 'Article', 'value': 'Count'},
                barmode='group'
            )
            fig_engagement.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_engagement, use_container_width=True)


# Main App
def main():
    render_sidebar()
    
    # Route to appropriate page
    page = st.session_state.current_page
    
    if page == 'home':
        render_home()
    elif page == 'trending':
        render_trending()
    elif page == 'write':
        render_write_article()
    elif page == 'article':
        render_article_detail()
    elif page == 'my_articles':
        render_my_articles()
    elif page == 'edit_article':
        render_edit_article()
    elif page == 'bookmarks':
        render_bookmarks()
    elif page == 'analytics':
        render_analytics()
    else:
        render_home()


if __name__ == "__main__":
    main()
