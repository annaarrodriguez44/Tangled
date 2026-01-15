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
    initial_sidebar_state="collapsed"
)

# Hero Section with Crochet-themed Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sacramento&family=Nunito:wght@400;700;800&display=swap');
    
    /* Crochet-themed background pattern */
    [data-testid="stAppViewContainer"] {
        background-color: #FFF5F7;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(232,129,156,.03) 35px, rgba(232,129,156,.03) 70px),
            repeating-linear-gradient(-45deg, transparent, transparent 35px, rgba(244,168,184,.03) 35px, rgba(244,168,184,.03) 70px);
    }
    
    /* Main content background */
    [data-testid="stAppViewContainer"] > div:first-child {
        background: transparent;
    }
    
    /* Global typography */
    html, body, [class*="css"], p, div, span {
        font-family: Georgia, serif !important;
    }
    
    h1, h2, h3, .hero-title {
        font-family: 'Sacramento', cursive !important;
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* Back to home button */
    .back-home {
        position: fixed;
        top: 20px;
        left: 20px;
        background: linear-gradient(135deg, #E8819C, #F4A8B8);
        color: white;
        padding: 12px 24px;
        border-radius: 30px;
        text-decoration: none;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(232,129,156,0.4);
        z-index: 999;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .back-home:hover {
        background: linear-gradient(135deg, #d66b87, #E8819C);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(232,129,156,0.6);
    }
    
    /* Animated hero section with yarn ball pattern */
    .hero-section {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFC4D6 25%, #F4A8B8 50%, #E8819C 75%, #D66B87 100%);
        padding: 5rem 2rem;
        border-radius: 30px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 15px 50px rgba(232, 129, 156, 0.4);
        position: relative;
        overflow: hidden;
        border: 3px solid rgba(255,255,255,0.3);
    }
    
    /* Floating yarn balls animation */
    .hero-section::before {
        content: "🧶";
        position: absolute;
        font-size: 3rem;
        opacity: 0.15;
        animation: float1 6s ease-in-out infinite;
        top: 20%;
        left: 10%;
    }
    .hero-section::after {
        content: "🧵";
        position: absolute;
        font-size: 2.5rem;
        opacity: 0.15;
        animation: float2 7s ease-in-out infinite;
        top: 60%;
        right: 15%;
    }
    
    @keyframes float1 {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(10deg); }
    }
    @keyframes float2 {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-30px) rotate(-10deg); }
    }
    
    .hero-title {
        font-family: 'Sacramento', cursive !important;
        font-size: 7rem;
        font-weight: 400;
        margin-bottom: 1rem;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ffffff, #fff5f7, #ffe5ec);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .hero-subtitle {
        font-family: Georgia, serif;
        font-size: 2.2rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Enhanced stat boxes */
    .stat-box {
        background: linear-gradient(135deg, #ffffff, #FFF5F7);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #FFE5EC;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(232,129,156,0.1);
    }
    .stat-box:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 10px 30px rgba(232,129,156,0.3);
        border-color: #E8819C;
    }
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #E8819C, #F4A8B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Nunito', sans-serif;
    }
    .stat-label {
        font-size: 1.1rem;
        color: #666;
        font-weight: 600;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <div class="hero-title">Tangled</div>
    <div class="hero-subtitle">🧶 Your Smart Crochet Companion 🧶</div>
    <p style="font-size: 1.2rem; margin-top: 1rem;">Find patterns, match perfect yarns, and plan your next crochet project<br>with AI-powered recommendations</p>
</div>
""", unsafe_allow_html=True)

# Crochet Image Collage
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; flex-wrap: wrap;">
        <div style="font-size: 5rem; opacity: 0.8; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">🧶</div>
        <div style="font-size: 4rem; opacity: 0.8; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">🧵</div>
        <div style="font-size: 5rem; opacity: 0.8; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">🪡</div>
        <div style="font-size: 4rem; opacity: 0.8; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">✂️</div>
        <div style="font-size: 5rem; opacity: 0.8; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">🎀</div>
        <div style="font-size: 4rem; opacity: 0.8; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">🧶</div>
        <div style="font-size: 5rem; opacity: 0.8; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));">🪢</div>
    </div>
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

# Custom CSS for feature cards with enhanced design
st.markdown("""
<style>
    .feature-card {
        background: linear-gradient(135deg, #ffffff, #FFF5F7);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(232,129,156,0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid #FFE5EC;
        height: 100%;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(232,129,156,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s;
    }
    .feature-card:hover::before {
        opacity: 1;
    }
    .feature-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 15px 40px rgba(232,129,156,0.4);
        border-color: #E8819C;
    }
    .feature-icon-big {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        transition: transform 0.4s;
        filter: drop-shadow(0 4px 8px rgba(232,129,156,0.3));
    }
    .feature-card:hover .feature-icon-big {
        transform: scale(1.2) rotate(5deg);
    }
    .feature-title-big {
        font-size: 1.5rem;
        font-weight: 700;
        color: #D66B87;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Sacramento', cursive;
    }
    .feature-desc {
        color: #666;
        text-align: center;
        font-size: 1rem;
        line-height: 1.7;
        font-family: Georgia, serif;
    }
    
    /* Section headers */
    h2, h3 {
        font-family: 'Sacramento', cursive;
        color: #D66B87;
        font-weight: 400;
    }
    
    /* CTA Section Enhancement */
    .cta-section {
        background: linear-gradient(135deg, #FFE5EC, #FFC4D6, #F4A8B8);
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(232,129,156,0.3);
        border: 3px solid rgba(255,255,255,0.5);
    }
    .cta-section h2 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        font-size: 2.5rem;
    }
    .cta-section p {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
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
<div class="cta-section">
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
