#!/usr/bin/env python3
# app.py - Streamlit tech website

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="TechCo — Python Streamlit", page_icon=":computer:", layout="wide")

# -- Helper functions ---------------------------------------------------------

def hero(title, subtitle):
    st.markdown(f"# {title}")
    st.markdown(f"_{subtitle}_)"


def feature_card(icon, title, desc):
    st.markdown(f"### {icon} {title}")
    st.write(desc)


# -- Sidebar -----------------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Products", "About", "Contact"])

# -- Home --------------------------------------------------------------------
if page == "Home":
    hero("TechCo — Build the future with Python", "Simple, fast, and reliable engineering powered by open-source")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("What we do")
        st.write(
            "We build data-driven web apps, ML prototypes, and tools to accelerate product development. "
            "This demo site is built with Streamlit and is fully editable in Python."
        )

        st.subheader("Key metrics")
        metrics = pd.DataFrame({
            "Quarter": ["Q1", "Q2", "Q3", "Q4"],
            "Active Users": [1200, 2100, 3400, 4800],
            "Uptime %": [99.5, 99.7, 99.8, 99.9],
        })
        fig = px.line(metrics, x="Quarter", y="Active Users", title="Active Users over time")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Features")
        feature_card("🚀", "Fast prototypes", "Ship prototypes in days using Python and Streamlit.")
        feature_card("🔒", "Secure by default", "We follow best practices for secrets and deployment.")
        feature_card("⚙️", "Integrations", "Connect to databases, ML models, and 3rd-party APIs.")

# -- Products ----------------------------------------------------------------
elif page == "Products":
    st.title("Products & Solutions")
    st.write("Explore a few example products built with Python and Streamlit.")

    p1, p2, p3 = st.columns(3)
    with p1:
        st.image("https://picsum.photos/seed/p1/400/250", caption="Data Dashboard")
        st.write("Interactive analytics dashboards for monitoring and decision-making.")
    with p2:
        st.image("https://picsum.photos/seed/p2/400/250", caption="ML Prototype")
        st.write("Rapid ML prototype deployments with explainability and monitoring.")
    with p3:
        st.image("https://picsum.photos/seed/p3/400/250", caption="Internal Tools")
        st.write("Admin and productivity tools to streamline team workflows.")

# -- About -------------------------------------------------------------------
elif page == "About":
    st.title("About TechCo")
    st.write("Mission: Enable teams to ship data products quickly and safely.")

    st.subheader("Team")
    team = [
        {"name": "Alex Doe", "role": "Founder & CEO"},
        {"name": "Sam Lee", "role": "CTO"},
        {"name": "J. Smith", "role": "Lead Data Scientist"},
    ]
    for member in team:
        st.markdown(f"**{member['name']}** — {member['role']}")

# -- Contact -----------------------------------------------------------------
elif page == "Contact":
    st.title("Contact")
    st.write("Get in touch or send feedback.")

    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")

        if submitted:
            if not name or not email or not message:
                st.error("Please complete all fields before sending.")
            else:
                st.success("Thanks for your message — we'll get back to you soon!")
                st.write("---")
                st.markdown(f"**Name:** {name}")
                st.markdown(f"**Email:** {email}")
                st.markdown(f"**Message:** {message}")

    st.markdown("\nOr email us directly: [contact@techco.example](mailto:contact@techco.example)")

# -- Footer ------------------------------------------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Python and Streamlit")


if __name__ == '__main__':
    pass
