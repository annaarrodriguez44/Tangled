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
        <div class="feature-title">Browse Patterns</div>
        <p>Explore our curated collection of crochet patterns. Filter by difficulty, yarn weight, and style.</p>
        <br>
        <a href="/Pattern_Browser" target="_self">
            <button style="background:#E8819C; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                Start Browsing →
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🌡️</div>
        <div class="feature-title">Smart Yarn Matching</div>
        <p>Get temperature-aware yarn recommendations based on your location and the season.</p>
        <br>
        <a href="/Pattern_Browser" target="_self">
            <button style="background:#E8819C; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                Find Yarns →
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">💰</div>
        <div class="feature-title">Project Planning</div>
        <p>Calculate costs, create shopping lists, and save your favorite patterns for later.</p>
        <br>
        <a href="/Pattern_Browser" target="_self">
            <button style="background:#E8819C; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                Plan Project →
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

# CTA Section
st.markdown("""
<div style="background:#F0F2F6; padding:2rem; border-radius:12px; text-align:center;">
    <h2>Ready to Start Your Next Project?</h2>
    <p>Join crafters using Tangled to find the perfect patterns and yarns</p>
    <br>
    <a href="/Pattern_Browser" target="_self">
        <button style="background:#E8819C; color:white; border:none; padding:15px 40px; border-radius:8px; cursor:pointer; font-size:1.2rem;">
            🧶 Start Now
        </button>
    </a>
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
