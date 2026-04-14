import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="PyTech Hub - Python Development",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #1e3a5f;
        --secondary: #3b82f6;
        --accent: #10b981;
        --background: #0f172a;
        --surface: #1e293b;
        --text: #f1f5f9;
        --text-muted: #94a3b8;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Hero section */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(145deg, #1e293b, #334155);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #334155;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Stats section */
    .stat-card {
        background: linear-gradient(145deg, #1e3a5f, #1e293b);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #3b82f6;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3b82f6;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Code block styling */
    .code-block {
        background: #0f172a;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #334155;
        font-family: 'Fira Code', monospace;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #10b981);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 3rem 0 1.5rem 0;
        text-align: center;
    }
    
    .section-subheader {
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #1e293b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Testimonial card */
    .testimonial-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    /* Course card */
    .course-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
    
    .course-badge {
        display: inline-block;
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Courses", "Projects", "Resources", "Community", "Contact"],
    label_visibility="collapsed"
)

# ==================== HOME PAGE ====================
if page == "Home":
    # Hero Section
    st.markdown('<h1 class="hero-title">PyTech Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Master Python Development with Industry-Leading Courses and Real-World Projects</p>', unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        c1, c2 = st.columns(2)
        with c1:
            st.button("Start Learning", use_container_width=True)
        with c2:
            st.button("View Courses", use_container_width=True)
    
    st.markdown("---")
    
    # Stats Section
    st.markdown('<h2 class="section-header">Trusted by Developers Worldwide</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("50K+", "Active Learners"),
        ("200+", "Video Tutorials"),
        ("95%", "Completion Rate"),
        ("4.9", "Average Rating")
    ]
    
    for col, (number, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Section
    st.markdown('<h2 class="section-header">Why Choose PyTech Hub?</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subheader">Everything you need to become a professional Python developer</p>', unsafe_allow_html=True)
    
    features = [
        ("🚀", "Project-Based Learning", "Build real applications from day one. Learn by doing with hands-on projects."),
        ("🎯", "Industry-Ready Skills", "Master the technologies that companies are actually hiring for."),
        ("👥", "Expert Instructors", "Learn from developers with 10+ years of industry experience."),
        ("📱", "Learn Anywhere", "Access courses on any device, anytime. Your progress syncs automatically."),
        ("🏆", "Certifications", "Earn recognized certificates to showcase your Python expertise."),
        ("💬", "Community Support", "Join 50K+ developers helping each other succeed.")
    ]
    
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
    
    st.markdown("---")
    
    # Popular Technologies
    st.markdown('<h2 class="section-header">Technologies We Cover</h2>', unsafe_allow_html=True)
    
    tech_data = pd.DataFrame({
        'Technology': ['Python Core', 'Django', 'FastAPI', 'Data Science', 'Machine Learning', 'Automation'],
        'Courses': [45, 32, 28, 38, 42, 25],
        'Projects': [120, 85, 72, 95, 110, 65]
    })
    
    fig = px.bar(
        tech_data, 
        x='Technology', 
        y=['Courses', 'Projects'],
        barmode='group',
        color_discrete_sequence=['#3b82f6', '#10b981']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== COURSES PAGE ====================
elif page == "Courses":
    st.markdown('<h1 class="hero-title">Our Courses</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">From beginner to advanced - find the perfect course for your journey</p>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        level = st.selectbox("Difficulty Level", ["All Levels", "Beginner", "Intermediate", "Advanced"])
    with col2:
        category = st.selectbox("Category", ["All Categories", "Web Development", "Data Science", "Machine Learning", "Automation"])
    with col3:
        sort_by = st.selectbox("Sort By", ["Most Popular", "Newest", "Highest Rated", "Price: Low to High"])
    
    st.markdown("---")
    
    # Course listings
    courses = [
        {
            "title": "Python Fundamentals Masterclass",
            "level": "Beginner",
            "duration": "40 hours",
            "rating": 4.9,
            "students": 15420,
            "price": "$49.99",
            "instructor": "Dr. Sarah Chen",
            "description": "Start your Python journey with comprehensive coverage of fundamentals, data structures, and OOP."
        },
        {
            "title": "Django Web Development Pro",
            "level": "Intermediate",
            "duration": "55 hours",
            "rating": 4.8,
            "students": 8932,
            "price": "$79.99",
            "instructor": "Michael Torres",
            "description": "Build production-ready web applications with Django, REST APIs, and deployment strategies."
        },
        {
            "title": "FastAPI: Modern API Development",
            "level": "Intermediate",
            "duration": "32 hours",
            "rating": 4.9,
            "students": 6541,
            "price": "$69.99",
            "instructor": "Elena Rodriguez",
            "description": "Create high-performance APIs with FastAPI, async programming, and best practices."
        },
        {
            "title": "Machine Learning with Python",
            "level": "Advanced",
            "duration": "65 hours",
            "rating": 4.7,
            "students": 12350,
            "price": "$99.99",
            "instructor": "Dr. James Liu",
            "description": "Master ML algorithms, neural networks, and deploy models to production."
        },
        {
            "title": "Python for Data Science",
            "level": "Intermediate",
            "duration": "48 hours",
            "rating": 4.8,
            "students": 18750,
            "price": "$69.99",
            "instructor": "Anna Kowalski",
            "description": "Learn pandas, numpy, matplotlib, and statistical analysis for data-driven insights."
        },
        {
            "title": "Automation with Python",
            "level": "Beginner",
            "duration": "28 hours",
            "rating": 4.6,
            "students": 9820,
            "price": "$39.99",
            "instructor": "David Park",
            "description": "Automate repetitive tasks, web scraping, file handling, and system administration."
        }
    ]
    
    for course in courses:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="course-card">
                    <span class="course-badge">{course['level']}</span>
                    <h3 style="color: #f1f5f9; margin: 0.5rem 0;">{course['title']}</h3>
                    <p style="color: #94a3b8; margin-bottom: 0.5rem;">{course['description']}</p>
                    <div style="display: flex; gap: 2rem; color: #64748b; font-size: 0.85rem;">
                        <span>⏱️ {course['duration']}</span>
                        <span>⭐ {course['rating']}</span>
                        <span>👥 {course['students']:,} students</span>
                        <span>👤 {course['instructor']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='text-align: center; padding-top: 1.5rem;'><span style='font-size: 1.5rem; font-weight: 700; color: #10b981;'>{course['price']}</span></div>", unsafe_allow_html=True)
                st.button("Enroll Now", key=f"enroll_{course['title']}", use_container_width=True)

# ==================== PROJECTS PAGE ====================
elif page == "Projects":
    st.markdown('<h1 class="hero-title">Real-World Projects</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Build your portfolio with industry-relevant projects</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    projects = [
        {
            "name": "E-Commerce Platform",
            "tech": ["Django", "PostgreSQL", "Stripe", "Redis"],
            "difficulty": "Advanced",
            "description": "Build a full-featured online store with cart, checkout, payments, and admin dashboard.",
            "time": "40-50 hours"
        },
        {
            "name": "Social Media Dashboard",
            "tech": ["FastAPI", "React", "MongoDB", "JWT"],
            "difficulty": "Intermediate",
            "description": "Create a social analytics tool that tracks engagement across multiple platforms.",
            "time": "25-35 hours"
        },
        {
            "name": "ML Stock Predictor",
            "tech": ["TensorFlow", "Pandas", "Streamlit", "yfinance"],
            "difficulty": "Advanced",
            "description": "Develop a machine learning model to predict stock prices with real-time data.",
            "time": "30-40 hours"
        },
        {
            "name": "Task Automation Bot",
            "tech": ["Python", "Selenium", "Schedule", "SMTP"],
            "difficulty": "Beginner",
            "description": "Automate daily tasks like data collection, email sending, and report generation.",
            "time": "15-20 hours"
        },
        {
            "name": "Real-Time Chat Application",
            "tech": ["FastAPI", "WebSockets", "Redis", "Vue.js"],
            "difficulty": "Intermediate",
            "description": "Build a scalable chat application with real-time messaging and notifications.",
            "time": "20-30 hours"
        },
        {
            "name": "Data Pipeline System",
            "tech": ["Apache Airflow", "PostgreSQL", "Docker", "AWS"],
            "difficulty": "Advanced",
            "description": "Create an ETL pipeline for processing and analyzing large datasets.",
            "time": "35-45 hours"
        }
    ]
    
    cols = st.columns(2)
    for i, project in enumerate(projects):
        with cols[i % 2]:
            tech_badges = " ".join([f'<span style="background: #1e3a5f; color: #3b82f6; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-right: 0.25rem;">{t}</span>' for t in project['tech']])
            
            st.markdown(f"""
            <div class="feature-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <span class="course-badge">{project['difficulty']}</span>
                    <span style="color: #64748b; font-size: 0.85rem;">⏱️ {project['time']}</span>
                </div>
                <h3 style="color: #f1f5f9; margin: 0.5rem 0;">{project['name']}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.75rem;">{project['description']}</p>
                <div>{tech_badges}</div>
            </div>
            """, unsafe_allow_html=True)
            st.button("Start Project", key=f"project_{project['name']}", use_container_width=True)

# ==================== RESOURCES PAGE ====================
elif page == "Resources":
    st.markdown('<h1 class="hero-title">Learning Resources</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Free tutorials, guides, and tools to accelerate your learning</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📚 Tutorials", "📝 Cheat Sheets", "🛠️ Tools"])
    
    with tab1:
        st.markdown("### Latest Tutorials")
        tutorials = [
            ("Getting Started with Python 3.12", "Learn about the latest features in Python 3.12", "15 min read"),
            ("Building REST APIs with FastAPI", "Complete guide to creating modern APIs", "25 min read"),
            ("Python Async/Await Explained", "Master asynchronous programming in Python", "20 min read"),
            ("Testing Best Practices with Pytest", "Write reliable tests for your applications", "18 min read"),
            ("Docker for Python Developers", "Containerize your Python applications", "22 min read"),
        ]
        
        for title, desc, time in tutorials:
            st.markdown(f"""
            <div class="course-card">
                <h4 style="color: #f1f5f9; margin: 0 0 0.25rem 0;">{title}</h4>
                <p style="color: #94a3b8; margin: 0 0 0.5rem 0; font-size: 0.9rem;">{desc}</p>
                <span style="color: #64748b; font-size: 0.8rem;">📖 {time}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Python Cheat Sheets")
        cheat_sheets = [
            "Python Basics Quick Reference",
            "Pandas Operations Cheat Sheet",
            "NumPy Array Methods",
            "Django ORM Commands",
            "Regular Expressions Guide",
            "Git Commands for Python Projects"
        ]
        
        cols = st.columns(2)
        for i, sheet in enumerate(cheat_sheets):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="course-card" style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #f1f5f9;">📄 {sheet}</span>
                    <span style="color: #3b82f6; cursor: pointer;">Download →</span>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Recommended Tools")
        tools = [
            ("VS Code", "Lightweight and powerful code editor", "Free"),
            ("PyCharm", "Full-featured Python IDE", "Free/Pro"),
            ("Postman", "API testing and documentation", "Free"),
            ("Docker Desktop", "Container management", "Free"),
            ("GitHub Copilot", "AI-powered code completion", "$10/mo"),
        ]
        
        for name, desc, price in tools:
            st.markdown(f"""
            <div class="course-card" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #f1f5f9; font-weight: 600;">{name}</span>
                    <p style="color: #94a3b8; margin: 0; font-size: 0.85rem;">{desc}</p>
                </div>
                <span style="color: #10b981; font-weight: 600;">{price}</span>
            </div>
            """, unsafe_allow_html=True)

# ==================== COMMUNITY PAGE ====================
elif page == "Community":
    st.markdown('<h1 class="hero-title">Join Our Community</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Connect with 50,000+ Python developers worldwide</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Community Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">50K+</div>
            <div class="stat-label">Community Members</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">2.5K</div>
            <div class="stat-label">Daily Discussions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">98%</div>
            <div class="stat-label">Questions Answered</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Testimonials
    st.markdown('<h2 class="section-header">What Our Community Says</h2>', unsafe_allow_html=True)
    
    testimonials = [
        {
            "text": "PyTech Hub transformed my career. I went from knowing nothing about programming to landing a job as a Python developer in 6 months.",
            "author": "Jessica M.",
            "role": "Junior Developer at Tech Corp"
        },
        {
            "text": "The project-based approach is exactly what I needed. The community is incredibly supportive and always ready to help.",
            "author": "Alex K.",
            "role": "Data Analyst"
        },
        {
            "text": "Best investment I ever made in my education. The FastAPI course alone was worth 10x what I paid.",
            "author": "Mohammed R.",
            "role": "Backend Engineer"
        }
    ]
    
    for testimonial in testimonials:
        st.markdown(f"""
        <div class="testimonial-card">
            <p style="color: #f1f5f9; font-style: italic; margin-bottom: 1rem;">"{testimonial['text']}"</p>
            <div style="color: #3b82f6; font-weight: 600;">{testimonial['author']}</div>
            <div style="color: #64748b; font-size: 0.85rem;">{testimonial['role']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Activity Chart
    st.markdown('<h2 class="section-header">Community Activity</h2>', unsafe_allow_html=True)
    
    activity_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Posts': [450, 520, 480, 610, 580, 320, 280],
        'Comments': [1200, 1450, 1380, 1650, 1520, 890, 720]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=activity_data['Day'], y=activity_data['Posts'], 
                             mode='lines+markers', name='Posts', line=dict(color='#3b82f6', width=3)))
    fig.add_trace(go.Scatter(x=activity_data['Day'], y=activity_data['Comments'], 
                             mode='lines+markers', name='Comments', line=dict(color='#10b981', width=3)))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== CONTACT PAGE ====================
elif page == "Contact":
    st.markdown('<h1 class="hero-title">Get In Touch</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">We would love to hear from you</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Send Us a Message")
        
        name = st.text_input("Your Name")
        email = st.text_input("Email Address")
        subject = st.selectbox("Subject", [
            "General Inquiry",
            "Course Support",
            "Technical Issue",
            "Partnership Opportunity",
            "Other"
        ])
        message = st.text_area("Your Message", height=150)
        
        if st.button("Send Message", use_container_width=True):
            if name and email and message:
                st.success("Thank you for your message! We'll get back to you within 24 hours.")
            else:
                st.error("Please fill in all required fields.")
    
    with col2:
        st.markdown("### Contact Information")
        
        st.markdown("""
        <div class="feature-card" style="margin-bottom: 1rem;">
            <div style="color: #3b82f6; font-size: 1.5rem; margin-bottom: 0.5rem;">📧</div>
            <div style="color: #f1f5f9; font-weight: 600;">Email</div>
            <div style="color: #94a3b8;">support@pytechhub.com</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" style="margin-bottom: 1rem;">
            <div style="color: #3b82f6; font-size: 1.5rem; margin-bottom: 0.5rem;">💬</div>
            <div style="color: #f1f5f9; font-weight: 600;">Discord</div>
            <div style="color: #94a3b8;">discord.gg/pytechhub</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" style="margin-bottom: 1rem;">
            <div style="color: #3b82f6; font-size: 1.5rem; margin-bottom: 0.5rem;">🐦</div>
            <div style="color: #f1f5f9; font-weight: 600;">Twitter</div>
            <div style="color: #94a3b8;">@pytechhub</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div style="color: #3b82f6; font-size: 1.5rem; margin-bottom: 0.5rem;">📍</div>
            <div style="color: #f1f5f9; font-weight: 600;">Location</div>
            <div style="color: #94a3b8;">San Francisco, CA</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748b;">
    <p>© 2026 PyTech Hub. All rights reserved.</p>
    <p style="font-size: 0.85rem; margin-top: 0.5rem;">
        Built with ❤️ using Python and Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
