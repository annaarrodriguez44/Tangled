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

# Features Section
st.markdown("## ✨ What Can You Do?")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Browse & Compare Patterns</div>
        <p>18+ patterns with advanced filters. Compare patterns side-by-side and save favorites.</p>
        <br>
        <a href="/1__Pattern_Browser" target="_self">
            <button style="background:#E8819C; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                Start Browsing →
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🧵</div>
        <div class="feature-title">Yarn & Project Tracking</div>
        <p>Track your stash, monitor prices, and manage WIP projects with progress updates.</p>
        <br>
        <a href="/3_🧵_Yarn_Inventory" target="_self">
            <button style="background:#E8819C; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                Track Stash →
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📸</div>
        <div class="feature-title">Gallery & Notes</div>
        <p>Rate patterns, upload project photos, and document modifications for future reference.</p>
        <br>
        <a href="/6_📸_Photo_Gallery" target="_self">
            <button style="background:#E8819C; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                View Gallery →
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

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

# All Features Section
st.markdown("## 🌟 Complete Feature Set")
st.markdown("<br>", unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("#### 📚 Pattern Management")
    st.markdown("""
    - 🔍 **Pattern Browser** - 18+ patterns with filters
    - ⚖️ **Comparison Tool** - Compare 2-3 patterns
    - ⭐ **Ratings & Notes** - Document experience
    - 📚 **Batch Processor** - AI-powered PDF extraction
    """)
    
with feat_col2:
    st.markdown("#### 🧵 Yarn & Inventory")
    st.markdown("""
    - 🧵 **Yarn Inventory** - Track your stash
    - 💰 **Price Tracker** - Monitor sales & trends
    - 🌡️ **Smart Matching** - Temperature-aware
    - 📊 **Statistics** - Analyze your collection
    """)

with feat_col3:
    st.markdown("#### 📝 Project & Community")
    st.markdown("""
    - 📝 **Project Tracker** - Track WIP & completed
    - 📸 **Photo Gallery** - Showcase projects
    - 💬 **Community Forum** - Chat & share tips
    - 💡 **Tips Archive** - Save modifications
    """)

st.markdown("<br>", unsafe_allow_html=True)

# Quick Access Section
st.markdown("## 🚀 Quick Access to All Features")
st.markdown("Click any card to go directly to that feature!")
st.markdown("<br>", unsafe_allow_html=True)

# Row 1: Main features
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 **Pattern Browser**\n\nBrowse 18+ patterns with advanced filters", use_container_width=True, key="nav_browser"):
        st.switch_page("pages/1__Pattern_Browser.py")
    
    if st.button("📝 **Project Tracker**\n\nTrack WIP projects with progress", use_container_width=True, key="nav_projects"):
        st.switch_page("pages/4_📝_Project_Tracker.py")
    
    if st.button("💰 **Price Tracker**\n\nMonitor yarn prices & sales", use_container_width=True, key="nav_prices"):
        st.switch_page("pages/8_💰_Price_Tracker.py")

with col2:
    if st.button("🧵 **Yarn Inventory**\n\nManage your yarn stash", use_container_width=True, key="nav_inventory"):
        st.switch_page("pages/3_🧵_Yarn_Inventory.py")
    
    if st.button("📸 **Photo Gallery**\n\nShowcase finished projects", use_container_width=True, key="nav_gallery"):
        st.switch_page("pages/6_📸_Photo_Gallery.py")
    
    if st.button("📚 **Add Patterns**\n\nBatch process PDFs with AI", use_container_width=True, key="nav_add"):
        st.switch_page("pages/9_📚_Add_Patterns.py")

with col3:
    if st.button("⚖️ **Pattern Comparison**\n\nCompare patterns side-by-side", use_container_width=True, key="nav_compare"):
        st.switch_page("pages/5_⚖️_Pattern_Comparison.py")
    
    if st.button("⭐ **Pattern Notes**\n\nRate patterns & add notes", use_container_width=True, key="nav_notes"):
        st.switch_page("pages/7_⭐_Pattern_Notes.py")
    
    if st.button("💬 **Community Forum**\n\nChat & share with others", use_container_width=True, key="nav_forum"):
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
