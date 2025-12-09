"""
Tangled - Crochet Pattern Planner
Homepage
"""

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Tangled - Crochet Pattern Planner",
    page_icon="🧶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hero Section
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #E8819C 0%, #F4A8B8 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .feature-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
        transition: transform 0.3s;
    }
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .stat-box {
        background: #F0F2F6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E8819C;
    }
    .stat-label {
        font-size: 1rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <div class="hero-title">🧶 Tangled</div>
    <div class="hero-subtitle">Your Smart Crochet Companion</div>
    <p>Find patterns, match perfect yarns, and plan your next crochet project with AI-powered recommendations</p>
</div>
""", unsafe_allow_html=True)

# Stats Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">18+</div>
        <div class="stat-label">Crochet Patterns</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">102</div>
        <div class="stat-label">Yarn Options</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">10+</div>
        <div class="stat-label">Locations</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">AI</div>
        <div class="stat-label">Powered Matching</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# How It Works Section
st.markdown("## 🎯 How It Works")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 1️⃣")
    st.markdown("**Set Your Location**")
    st.write("Tell us where you are to get temperature-based recommendations")

with col2:
    st.markdown("### 2️⃣")
    st.markdown("**Browse Patterns**")
    st.write("Filter and search through our collection to find your perfect project")

with col3:
    st.markdown("### 3️⃣")
    st.markdown("**Get Recommendations**")
    st.write("AI matches the best yarns for your pattern and local climate")

with col4:
    st.markdown("### 4️⃣")
    st.markdown("**Start Creating**")
    st.write("Download your pattern, get your shopping list, and start crocheting!")

st.markdown("<br><br>", unsafe_allow_html=True)

# Quick Access Section - Beautiful Feature Cards
st.markdown("## 🚀 Explore All Features")
st.markdown("Click any card to start using that tool")
st.markdown("<br>", unsafe_allow_html=True)

# Custom CSS for feature cards
st.markdown("""
<style>
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        border: 2px solid #f0f0f0;
        height: 100%;
        cursor: pointer;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(232,129,156,0.3);
        border-color: #E8819C;
    }
    .feature-icon-big {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-title-big {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #666;
        text-align: center;
        font-size: 0.95rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Row 1: Pattern & Browsing
st.markdown("### 📚 Pattern Management")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">🔍</div>
        <div class="feature-title-big">Pattern Browser</div>
        <div class="feature-desc">Browse 18+ patterns with advanced filters by difficulty, yarn weight, season, project type, and more</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Pattern Browser", use_container_width=True, key="nav_browser", type="primary"):
        st.switch_page("pages/1__Pattern_Browser.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">⚖️</div>
        <div class="feature-title-big">Pattern Comparison</div>
        <div class="feature-desc">Compare 2-3 patterns side-by-side with cost estimates and pros/cons analysis</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Pattern Comparison", use_container_width=True, key="nav_compare", type="primary"):
        st.switch_page("pages/5_⚖️_Pattern_Comparison.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">📚</div>
        <div class="feature-title-big">Add Patterns (AI)</div>
        <div class="feature-desc">Batch process PDF patterns with AI-powered extraction using Gemini Pro</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Pattern Upload", use_container_width=True, key="nav_add", type="primary"):
        st.switch_page("pages/9_📚_Add_Patterns.py")

st.markdown("<br>", unsafe_allow_html=True)

# Row 2: Yarn & Inventory
st.markdown("### 🧵 Yarn & Inventory Management")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">🧵</div>
        <div class="feature-title-big">Yarn Inventory</div>
        <div class="feature-desc">Track your stash with statistics, low stock alerts, and searchable database</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Yarn Inventory", use_container_width=True, key="nav_inventory", type="primary"):
        st.switch_page("pages/3_🧵_Yarn_Inventory.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">💰</div>
        <div class="feature-title-big">Price Tracker</div>
        <div class="feature-desc">Monitor yarn prices over time with charts and automatic sale detection</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Price Tracker", use_container_width=True, key="nav_prices", type="primary"):
        st.switch_page("pages/8_💰_Price_Tracker.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">⭐</div>
        <div class="feature-title-big">Pattern Notes</div>
        <div class="feature-desc">Rate patterns, document modifications, and save tips for future projects</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Pattern Notes", use_container_width=True, key="nav_notes", type="primary"):
        st.switch_page("pages/7_⭐_Pattern_Notes.py")

st.markdown("<br>", unsafe_allow_html=True)

# Row 3: Project Tracking & Community
st.markdown("### 📝 Project Tracking & Community")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">📝</div>
        <div class="feature-title-big">Project Tracker</div>
        <div class="feature-desc">Track WIP and completed projects with progress percentages and time logging</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Project Tracker", use_container_width=True, key="nav_projects", type="primary"):
        st.switch_page("pages/4_📝_Project_Tracker.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">📸</div>
        <div class="feature-title-big">Photo Gallery</div>
        <div class="feature-desc">Showcase finished projects with photos, ratings, and searchable tags</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Photo Gallery", use_container_width=True, key="nav_gallery", type="primary"):
        st.switch_page("pages/6_📸_Photo_Gallery.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon-big">💬</div>
        <div class="feature-title-big">Community Forum</div>
        <div class="feature-desc">Chat with other crocheters, share tips, and discuss patterns in real-time</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Community Forum", use_container_width=True, key="nav_forum", type="primary"):
        st.switch_page("pages/10_💬_Community_Forum.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div style="background:#F0F2F6; padding:2rem; border-radius:12px; text-align:center;">
    <h2>Ready to Start Your Next Project?</h2>
    <p>All-in-one platform for crochet pattern planning, yarn management, and project tracking</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🧶 Tangled - Smart Crochet Pattern Planner | Built with ❤️ for crochet enthusiasts</p>
    <p>Temperature-aware recommendations • 18+ Patterns • 102 Yarns • AI-Powered</p>
</div>
""", unsafe_allow_html=True)
