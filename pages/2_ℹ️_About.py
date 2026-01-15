"""
About Tangled - Learn More About Our Platform
"""

import streamlit as st

# Crochet-themed styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Nunito:wght@400;700;800&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background-color: #FFF5F7;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(232,129,156,.03) 35px, rgba(232,129,156,.03) 70px),
            repeating-linear-gradient(-45deg, transparent, transparent 35px, rgba(244,168,184,.03) 35px, rgba(244,168,184,.03) 70px);
    }
    html, body, [class*="css"], p, div, span {
        font-family: Georgia, serif !important;
    }
    h1, h2, h3 {
        font-family: 'Sacramento', cursive !important;
        color: #D66B87;
    }
    .stat-number { font-family: 'Nunito', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)

st.set_page_config(
    page_title="About - Tangled",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About Tangled")

st.markdown("""
## What is Tangled?

**Tangled** is an AI-powered crochet pattern management and yarn recommendation system designed to help crocheters 
find the perfect patterns and yarns for their projects.

### 🎯 Our Mission

To make crochet project planning easier, smarter, and more enjoyable by combining:
- **Artificial Intelligence** for pattern extraction and understanding
- **Temperature-aware matching** for season-appropriate yarn recommendations
- **Smart algorithms** that consider multiple factors for yarn selection

---

## 🔧 How It Works

### 1. **Pattern Extraction**
We use Google's Gemini AI to extract detailed information from PDF crochet patterns:
- Pattern name and structure
- Required yarn weight and composition
- Hook size and difficulty level
- Stitches needed and materials list

### 2. **Yarn Database**
Our database contains **102 different yarns** with detailed information:
- Fiber composition (cotton, wool, acrylic, etc.)
- Price and brand
- Yarn thickness
- User ratings

### 3. **Smart Matching Algorithm**
When you select a pattern, our algorithm calculates compatibility scores based on:
- **Pattern requirements** (yarn weight, hook size)
- **Temperature suitability** (your location and current season)
- **Fiber composition** match
- **Yarn thickness** and warmth
- **Quality ratings** and price

### 4. **Temperature-Aware Recommendations**
Unlike simple seasonal recommendations, Tangled considers:
- **Your actual location** (Sweden winter ≠ Spain winter)
- **Current temperature** ranges for each season
- **Yarn fiber warmth** (wool for cold, cotton for warm)
- **Thickness multiplier** (bulky = warmer than fingering)

---

## 🌟 Key Features

### For Pattern Selection
✅ Browse 18+ curated crochet patterns  
✅ Filter by difficulty (beginner to expert)  
✅ Search by yarn weight  
✅ Text search across all fields  
✅ Save favorite patterns  

### For Yarn Recommendations
✅ Top 3 yarn matches per pattern  
✅ Temperature-based scoring  
✅ Detailed composition breakdown  
✅ Price and rating information  
✅ Direct purchase links (Hobbii, Katia)  

### For Project Planning
✅ Project cost calculator  
✅ Shopping list generator  
✅ Materials checklist  
✅ PDF pattern downloads  
✅ Stitch tutorial links  

---

## 📊 The Technology

**Built with:**
- **Streamlit** - Web interface
- **Google Gemini Pro** - AI pattern extraction
- **ChromaDB** - Vector database for semantic search
- **Pandas** - Data manipulation
- **Python** - Core programming language

**Algorithms:**
- Multi-factor scoring (70% pattern match + 30% temperature)
- Yarn thickness warmth adjustment
- Dynamic temperature range calculation
- Fiber composition analysis

---

## 🎨 Why "Tangled"?

The name represents the beautiful complexity of crochet:
- Yarns intertwining to create patterns
- The web of connections between patterns, yarns, and seasons
- The joy of getting "tangled up" in a new crochet project

---

## 👩‍💻 Developer

Created by **Anna R.** as part of a biomedical engineering Python course project.

**Project Timeline:**
- Started: October 28, 2025
- Core features completed: November 11, 2025
- Web deployment: November 18, 2025
- Multi-page redesign: December 2025

---

## 📈 Project Stats

- **18 unique patterns** extracted from PDFs
- **102 yarns** in the database
- **10+ locations** with temperature data
- **9 fields** extracted per pattern
- **5 scoring factors** for yarn matching

---

## 🔮 Future Plans

- [ ] Mobile app version
- [ ] User accounts and saved projects
- [ ] Community pattern sharing
- [ ] More international yarn brands
- [ ] Video pattern support
- [ ] Stitch dictionary integration
- [ ] Yarn substitution calculator
- [ ] Project gallery

---

## 📬 Feedback

Have suggestions or found a bug? We'd love to hear from you!

Contact: [Your contact info here]

---

## 📄 License

Open source under MIT License. Feel free to use for your own crochet projects!

---

<div style='text-align: center; color: #666; margin-top: 3rem;'>
    <p>Built with ❤️ for crochet enthusiasts</p>
</div>
""", unsafe_allow_html=True)
