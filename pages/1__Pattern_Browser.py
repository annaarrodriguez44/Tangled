"""
Crochet Pattern Project Planner - Complete Workflow
From pattern selection to purchase links and inspiration
"""

import streamlit as st
import pandas as pd
import chromadb
from datetime import datetime
import os

# Import your existing functions
import sys
sys.path.append('.')

from slice10_yarn_match import calculate_match_score, load_databases, normalize_yarn_weight

# Add navigation
st.markdown('<a href="/" target="_self" style="text-decoration:none;"><button style="float:right; background:#E8819C; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer;">🏠 Home</button></a>', unsafe_allow_html=True)

# Temperature-based location data (average temps in Celsius)
LOCATION_TEMPS = {
    "Sweden (Stockholm)": {"winter": -3, "spring": 5, "summer": 18, "fall": 8},
    "Spain (Madrid)": {"winter": 6, "spring": 14, "summer": 25, "fall": 15},
    "UK (London)": {"winter": 5, "spring": 11, "summer": 18, "fall": 12},
    "USA (New York)": {"winter": 0, "spring": 12, "summer": 24, "fall": 13},
    "Canada (Toronto)": {"winter": -4, "spring": 9, "summer": 22, "fall": 10},
    "Australia (Sydney)": {"winter": 13, "spring": 18, "summer": 23, "fall": 19},
    "Germany (Berlin)": {"winter": 0, "spring": 9, "summer": 19, "fall": 10},
    "France (Paris)": {"winter": 4, "spring": 11, "summer": 20, "fall": 12},
    "Italy (Rome)": {"winter": 8, "spring": 14, "summer": 25, "fall": 17},
    "Netherlands (Amsterdam)": {"winter": 3, "spring": 10, "summer": 17, "fall": 11},
    "Custom": {"winter": 10, "spring": 15, "summer": 20, "fall": 12}
}

# Page config
st.set_page_config(
    page_title="Crochet Project Planner",
    page_icon="🧶",
    layout="wide"
)

# Initialize
@st.cache_data
def load_data():
    patterns_df, yarn_df = load_databases()
    return patterns_df, yarn_df

@st.cache_resource
def load_vector_db():
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name="crochet_patterns")
        return client, collection
    except:
        # Vector DB not available in deployment - return None
        return None, None

def get_current_season():
    """Determine current season based on month"""
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"

def get_temp_for_location_and_season(location, season):
    """Get average temperature for location and season"""
    return LOCATION_TEMPS.get(location, LOCATION_TEMPS["Custom"])[season]

def get_yarn_temp_range(yarn_row):
    """Determine comfortable temperature range for yarn based on composition and thickness"""
    cotton = yarn_row.get('Cotton (%)', 0)
    linen = yarn_row.get('Linen (%)', 0)
    bamboo = yarn_row.get('Bamboo/Viscouse (%)', 0)
    acrylic = yarn_row.get('Acrylic (%)', 0)
    wool = yarn_row.get('Wool (%)', 0)
    mohair = yarn_row.get('Mohair/Alpaca (%)', 0)
    
    # Get yarn thickness for warmth adjustment
    thickness = str(yarn_row.get('Yarn thikness', '')).lower()
    thickness_multiplier = 1.0
    
    # Thicker yarn = warmer at same composition
    if 'super bulky' in thickness or 'jumbo' in thickness:
        thickness_multiplier = 1.4
    elif 'bulky' in thickness or 'chunky' in thickness:
        thickness_multiplier = 1.25
    elif 'worsted' in thickness or 'aran' in thickness:
        thickness_multiplier = 1.1
    elif 'dk' in thickness or 'light worsted' in thickness:
        thickness_multiplier = 1.0
    elif 'sport' in thickness or 'baby' in thickness:
        thickness_multiplier = 0.9
    elif 'fingering' in thickness or 'sock' in thickness:
        thickness_multiplier = 0.8
    elif 'lace' in thickness or 'thread' in thickness:
        thickness_multiplier = 0.7
    
    # Calculate warmth based on fiber composition
    cool_fiber_pct = cotton + linen + bamboo  # Breathable, cool
    warm_fiber_pct = wool + mohair  # Insulating, warm
    
    # Base temperature ranges
    if warm_fiber_pct > 50:
        base_min, base_max, base_ideal = -10, 15, 5
        fiber_type = "Warm (Wool/Alpaca)"
    elif cool_fiber_pct > 50:
        base_min, base_max, base_ideal = 15, 35, 22
        fiber_type = "Cool (Cotton/Linen)"
    elif acrylic > 70:
        base_min, base_max, base_ideal = 5, 20, 12
        fiber_type = "All-season (Acrylic)"
    else:
        base_min, base_max, base_ideal = 5, 25, 15
        fiber_type = "Blend"
    
    # Adjust for thickness (thicker = shifts toward cooler temps)
    # For warm fibers: thicker extends cold tolerance
    # For cool fibers: thicker reduces heat tolerance
    if warm_fiber_pct > 50:
        adjusted_min = base_min - (5 * (thickness_multiplier - 1))
        adjusted_max = base_max + (3 * (thickness_multiplier - 1))
    elif cool_fiber_pct > 50:
        adjusted_min = base_min + (5 * (thickness_multiplier - 1))
        adjusted_max = base_max - (3 * (thickness_multiplier - 1))
    else:
        adjusted_min = base_min
        adjusted_max = base_max
    
    return {
        "min": int(adjusted_min),
        "max": int(adjusted_max),
        "ideal": base_ideal,
        "type": f"{fiber_type} ({thickness.title() if thickness else 'Standard'})"
    }

def calculate_temp_match_score(yarn_temp_range, current_temp):
    """Calculate how well yarn matches current temperature (0-30 points)"""
    yarn_min = yarn_temp_range["min"]
    yarn_max = yarn_temp_range["max"]
    yarn_ideal = yarn_temp_range["ideal"]
    
    if yarn_min <= current_temp <= yarn_max:
        # Inside range - calculate distance from ideal
        distance_from_ideal = abs(current_temp - yarn_ideal)
        score = 30 - (distance_from_ideal * 1.5)
        return max(0, score)
    else:
        # Outside range - steep penalty
        if current_temp < yarn_min:
            distance = yarn_min - current_temp
        else:
            distance = current_temp - yarn_max
        score = 30 - (distance * 3)
        return max(0, score)

def determine_yarn_season(yarn_row):
    """Determine if yarn is suitable for current season based on composition"""
    # Summer yarns: cotton, linen, bamboo
    summer_score = yarn_row.get('Cotton (%)', 0) + yarn_row.get('Linen (%)', 0) + yarn_row.get('Bamboo/Viscouse (%)', 0)
    
    # Winter yarns: wool, mohair, alpaca
    winter_score = yarn_row.get('Wool (%)', 0) + yarn_row.get('Mohair/Alpaca (%)', 0)
    
    # All-season: acrylic, blends
    allseason_score = yarn_row.get('Acrylic (%)', 0)
    
    if summer_score > 50:
        return "Summer"
    elif winter_score > 50:
        return "Winter"
    elif allseason_score > 70:
        return "All-Season"
    else:
        return "Spring/Fall"

def get_yarn_store_url(yarn_name, brand):
    """Generate potential store URLs for yarn"""
    # This is a simplified version - you'd need actual URL mapping
    yarn_clean = yarn_name.lower().replace(' ', '-')
    brand_clean = str(brand).lower() if pd.notna(brand) else 'hobbii'
    
    urls = []
    
    # Hobbii
    urls.append(f"https://hobbii.com/search?q={yarn_clean}")
    
    # Katia
    if 'katia' in brand_clean:
        urls.append(f"https://www.katia.com/ES/yarns.html?q={yarn_clean}")
    
    return urls

# Load data
patterns_df, yarn_df = load_data()
client, collection = load_vector_db()

# Get unique patterns (remove duplicates)
unique_patterns = patterns_df.drop_duplicates(subset=['Pattern Name'])
current_season = get_current_season()

# Header
st.title("🧶 Crochet Project Planner")

# Location selector at top
col_header1, col_header2 = st.columns([2, 1])

with col_header1:
    user_location = st.selectbox(
        "📍 Your Location",
        list(LOCATION_TEMPS.keys()),
        index=0,
        help="Select your location for temperature-based yarn recommendations"
    )

with col_header2:
    if user_location == "Custom":
        current_temp = st.number_input(
            "Current Temp (°C)",
            min_value=-20,
            max_value=40,
            value=15,
            help="Enter your current temperature"
        )
    else:
        current_temp = get_temp_for_location_and_season(user_location, current_season)
        st.metric("Current Temp", f"{current_temp}°C", delta=f"{current_season.title()}")

st.markdown(f"🌡️ **Temperature-based recommendations for {user_location}** | Current: **{current_temp}°C**")
st.markdown("---")

# Sidebar - Browse patterns
st.sidebar.header("🔍 Find Your Pattern")

# Search
search_query = st.sidebar.text_input("Search patterns", placeholder="e.g., baby blanket, summer top")

# Filters
st.sidebar.subheader("Filters")

# Favorites filter
if 'favorites' in st.session_state and st.session_state.favorites:
    show_favorites_only = st.sidebar.checkbox(f"⭐ Show favorites only ({len(st.session_state.favorites)})")
else:
    show_favorites_only = False

difficulties = ["All"] + sorted(unique_patterns['Difficulty Level'].dropna().unique().tolist())
selected_difficulty = st.sidebar.selectbox("Difficulty", difficulties)

yarn_weights = ["All"] + sorted(unique_patterns['Yarn Weight'].dropna().unique().tolist())
selected_yarn_weight = st.sidebar.selectbox("Yarn Weight", yarn_weights)

# Advanced Filters
with st.sidebar.expander("🔧 Advanced Filters"):
    # Season filter
    season_filter = st.multiselect(
        "Best Season",
        ["Spring", "Summer", "Fall", "Winter"],
        help="Filter by recommended season"
    )
    
    # Project type filter
    project_type = st.selectbox(
        "Project Type",
        ["All", "Clothing", "Home Decor", "Toys/Amigurumi", "Accessories"],
        help="Filter by type of project"
    )
    
    # Estimated time filter
    time_estimate = st.selectbox(
        "Time to Complete",
        ["All", "Quick (< 5 hours)", "Weekend (5-20 hours)", "Week (20-40 hours)", "Long-term (40+ hours)"],
        help="Estimated time to complete"
    )
    
    # Color complexity
    color_count = st.selectbox(
        "Color Complexity",
        ["All", "1 Color", "2-3 Colors", "4+ Colors"],
        help="Number of colors needed"
    )

# Apply filters
filtered_df = unique_patterns.copy()

# Favorites filter
if show_favorites_only and 'favorites' in st.session_state:
    filtered_df = filtered_df[filtered_df['Pattern Name'].isin(st.session_state.favorites)]

if selected_difficulty != "All":
    filtered_df = filtered_df[filtered_df['Difficulty Level'] == selected_difficulty]

if selected_yarn_weight != "All":
    filtered_df = filtered_df[filtered_df['Yarn Weight'] == selected_yarn_weight]

# Advanced Filters Application
if season_filter:
    # Infer season from yarn composition and weight
    # Cool yarns (cotton) = Summer/Spring, Warm yarns (wool) = Winter/Fall
    season_mask = filtered_df['Recommended Yarn Composition'].str.contains('cotton|linen', case=False, na=False)
    if "Summer" in season_filter or "Spring" in season_filter:
        filtered_df = filtered_df[season_mask]
    elif "Winter" in season_filter or "Fall" in season_filter:
        filtered_df = filtered_df[~season_mask]

if project_type != "All":
    # Infer project type from pattern name/structure
    type_patterns = {
        "Clothing": r'top|shirt|sweater|cardigan|dress|pants|skirt|hat|scarf',
        "Home Decor": r'blanket|cushion|pillow|basket|rug|coaster',
        "Toys/Amigurumi": r'ami|toy|doll|animal|plush|bear|bunny',
        "Accessories": r'bag|pouch|purse|keychain|headband|mitt'
    }
    if project_type in type_patterns:
        pattern = type_patterns[project_type]
        mask = filtered_df['Pattern Name'].str.contains(pattern, case=False, na=False) | \
               filtered_df['Pattern Structure'].str.contains(pattern, case=False, na=False)
        filtered_df = filtered_df[mask]

if time_estimate != "All":
    # Estimate based on difficulty and structure
    if time_estimate == "Quick (< 5 hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'].isin(['Beginner', 'Easy'])]
    elif time_estimate == "Weekend (5-20 hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'].isin(['Easy', 'Intermediate'])]
    elif time_estimate == "Week (20-40 hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'] == 'Intermediate']
    elif time_estimate == "Long-term (40+ hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'].isin(['Advanced', 'Expert'])]

if color_count != "All":
    # Infer from recommended colors if available
    if "Recommended Colors" in filtered_df.columns:
        if color_count == "1 Color":
            mask = filtered_df['Recommended Colors'].str.contains(r'^\d+$', na=False) & \
                   (filtered_df['Recommended Colors'].astype(str).str.extract(r'(\d+)', expand=False).astype(float) == 1)
            filtered_df = filtered_df[mask | filtered_df['Recommended Colors'].isna()]

if search_query:
    # Simple text search
    mask = filtered_df['Pattern Name'].str.contains(search_query, case=False, na=False) | \
           filtered_df['Pattern Structure'].str.contains(search_query, case=False, na=False) | \
           filtered_df['Stitches Required'].str.contains(search_query, case=False, na=False)
    filtered_df = filtered_df[mask]

# Main area - Pattern selection
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(filtered_df)} patterns found**")

selected_pattern_name = st.sidebar.selectbox(
    "Select a pattern",
    filtered_df['Pattern Name'].tolist()
)

# Get selected pattern details
selected_pattern = filtered_df[filtered_df['Pattern Name'] == selected_pattern_name].iloc[0]

# MAIN CONTENT - PROJECT PLANNING

# Section 1: Pattern Overview
col_header_pattern, col_fav = st.columns([4, 1])

with col_header_pattern:
    st.header(f"📋 {selected_pattern['Pattern Name']}")

with col_fav:
    # Simple favorite toggle (stores in session state)
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    is_favorite = selected_pattern['Pattern Name'] in st.session_state.favorites
    
    if st.button("⭐ Favorite" if not is_favorite else "💫 Favorited", key="fav_btn"):
        if is_favorite:
            st.session_state.favorites.remove(selected_pattern['Pattern Name'])
        else:
            st.session_state.favorites.append(selected_pattern['Pattern Name'])
        st.rerun()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Difficulty", selected_pattern['Difficulty Level'])
with col2:
    st.metric("Yarn Weight", selected_pattern['Yarn Weight'])
with col3:
    st.metric("Hook Size", f"{selected_pattern['Hook Size (mm)']}mm")
with col4:
    st.metric("Structure", selected_pattern['Pattern Structure'][:20] + "...")

st.markdown("---")

# Section 2: Stitches Needed
st.subheader("🪡 Stitches You'll Need")
stitches = str(selected_pattern['Stitches Required']).split(',')
st.markdown("**Required stitches:**")

# Display stitches as pills
stitch_html = ""
for stitch in stitches:
    stitch = stitch.strip()
    stitch_html += f'<span style="background-color: #E8F4F8; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block;">{stitch}</span>'

st.markdown(stitch_html, unsafe_allow_html=True)

st.markdown("""
💡 **New to these stitches?** Search YouTube for tutorials:
- [Single Crochet (sc)](https://www.youtube.com/results?search_query=crochet+single+crochet+tutorial)
- [Double Crochet (dc)](https://www.youtube.com/results?search_query=crochet+double+crochet+tutorial)
""")

st.markdown("---")

# Section 3: Yarn Recommendations (TEMPERATURE-AWARE)
st.subheader(f"🧵 Top Yarn Recommendations for {current_temp}°C")

# Calculate match scores for all yarns
yarn_matches = []
for idx, yarn_row in yarn_df.iterrows():
    # Base pattern match score
    base_score = calculate_match_score(selected_pattern, yarn_row)
    
    # Temperature suitability score
    yarn_temp_range = get_yarn_temp_range(yarn_row)
    temp_score = calculate_temp_match_score(yarn_temp_range, current_temp)
    
    # Combined: 70% pattern match + 30% temperature match
    total_score = (base_score * 0.7) + temp_score
    
    yarn_matches.append({
        'name': yarn_row['Name of the product'],
        'score': total_score,
        'base_score': base_score,
        'temp_score': temp_score,
        'price': yarn_row['Price (€)'],
        'rating': yarn_row['Rating (★)'],
        'brand': yarn_row.get('Brand', 'Unknown'),
        'temp_range': yarn_temp_range,
        'cotton': yarn_row.get('Cotton (%)', 0),
        'acrylic': yarn_row.get('Acrylic (%)', 0),
        'wool': yarn_row.get('Wool (%)', 0),
        'weight': yarn_row.get('Yarn thikness', 'Unknown')
    })

# Sort and get top 3
yarn_matches_df = pd.DataFrame(yarn_matches).sort_values('score', ascending=False).head(3)

for idx, yarn in yarn_matches_df.iterrows():
    with st.expander(f"✨ {yarn['name']} - {yarn['score']:.0f}% Match", expanded=(idx==0)):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Price:** €{yarn['price']:.2f} per ball")
            st.markdown(f"**Rating:** {'⭐' * int(yarn['rating'])}")
            
            # Temperature comfort info
            temp_range = yarn['temp_range']
            st.markdown(f"**Fiber Type:** {temp_range['type']}")
            st.markdown(f"**Comfort Range:** {temp_range['min']}°C to {temp_range['max']}°C (ideal: {temp_range['ideal']}°C)")
            
            # Temperature match indicator
            if temp_range['min'] <= current_temp <= temp_range['max']:
                distance = abs(current_temp - temp_range['ideal'])
                if distance <= 3:
                    st.success(f"🌡️ Perfect for {current_temp}°C!")
                elif distance <= 7:
                    st.info(f"✅ Good for {current_temp}°C")
                else:
                    st.warning(f"⚠️ Usable at {current_temp}°C but not ideal")
            else:
                if current_temp < temp_range['min']:
                    st.error(f"❄️ Too cold for this yarn ({current_temp}°C < {temp_range['min']}°C)")
                else:
                    st.error(f"🔥 Too hot for this yarn ({current_temp}°C > {temp_range['max']}°C)")
            
            st.markdown(f"**Weight:** {yarn['weight']}")
            
            # Composition
            comp_parts = []
            if yarn['cotton'] > 0:
                comp_parts.append(f"{int(yarn['cotton'])}% Cotton")
            if yarn['acrylic'] > 0:
                comp_parts.append(f"{int(yarn['acrylic'])}% Acrylic")
            if yarn['wool'] > 0:
                comp_parts.append(f"{int(yarn['wool'])}% Wool")
            
            st.markdown(f"**Composition:** {', '.join(comp_parts)}")
            
            # Score breakdown
            with st.expander("📊 Score Breakdown"):
                st.markdown(f"- Pattern Match: {yarn['base_score']:.1f}%")
                st.markdown(f"- Temperature Match: {yarn['temp_score']:.1f}/30 pts")
                st.markdown(f"- **Total: {yarn['score']:.1f}%**")
        
        with col2:
            st.markdown("**Where to Buy:**")
            urls = get_yarn_store_url(yarn['name'], yarn['brand'])
            for url in urls:
                if 'hobbii' in url:
                    st.markdown(f"🛒 [Hobbii.com]({url})")
                elif 'katia' in url:
                    st.markdown(f"🛒 [Katia.es]({url})")

st.markdown("---")

# Section 4: Color Inspiration
st.subheader("🎨 Color Inspiration")

color_info = str(selected_pattern.get('Recommended Colors', 'Not specified'))
st.markdown(f"**Pattern suggests:** {color_info}")

st.markdown("""
💡 **Need color ideas?** Check out these resources:
- [Coolors.co](https://coolors.co/generate) - Color palette generator
- [Pinterest Color Palettes](https://www.pinterest.com/search/pins/?q=crochet%20color%20palette)
- [Ravelry Color Inspiration](https://www.ravelry.com/)
""")

# Pinterest search link for this specific pattern
pinterest_search = selected_pattern['Pattern Name'].replace(' ', '%20')
st.markdown(f"🔍 [Search '{selected_pattern['Pattern Name']}' on Pinterest](https://www.pinterest.com/search/pins/?q={pinterest_search}%20crochet)")

st.markdown("---")

# Section 5: Materials Checklist
st.subheader("📦 Complete Materials List")

materials = str(selected_pattern['Materials Needed'])
st.markdown(materials)

st.markdown("---")

# Section 6: Project Cost Calculator
st.subheader("💰 Project Cost Estimator")

col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    num_balls = st.number_input("Estimated balls/skeins needed", min_value=1, max_value=50, value=3, help="Check pattern for yarn requirements")
    
    if yarn_matches_df.iloc[0] is not None:
        selected_yarn_for_calc = yarn_matches_df.iloc[0]
        yarn_cost = selected_yarn_for_calc['price'] * num_balls
        
        st.markdown(f"**Yarn cost:** €{yarn_cost:.2f}")
        st.markdown(f"**Hook:** €5-15 (if needed)")
        st.markdown(f"**Notions:** €2-5")
        
        total_min = yarn_cost + 0
        total_max = yarn_cost + 20
        
        st.success(f"**Total Project Cost: €{total_min:.2f} - €{total_max:.2f}**")

with col_calc2:
    st.markdown("**Shopping List:**")
    shopping_list = f"""
    ✅ {selected_pattern['Pattern Name']}
    
    Materials:
    - {num_balls} balls of {yarn_matches_df.iloc[0]['name']}
    - {selected_pattern['Hook Size (mm)']}mm crochet hook
    - Scissors
    - Yarn needle
    - {selected_pattern['Materials Needed'][:100]}...
    
    Estimated Budget: €{total_min:.2f} - €{total_max:.2f}
    """
    
    st.download_button(
        label="📋 Download Shopping List",
        data=shopping_list,
        file_name=f"{selected_pattern['Pattern Name']}_shopping_list.txt",
        mime="text/plain"
    )

st.markdown("---")

# Section 7: Pattern PDF
st.subheader("📄 Pattern PDF")

pdf_filename = selected_pattern['Source File']
pdf_path = os.path.join('PDFPatterns', pdf_filename)

if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    
    st.download_button(
        label="📥 Download Pattern PDF",
        data=pdf_bytes,
        file_name=pdf_filename,
        mime="application/pdf"
    )
    
    st.info(f"💾 Pattern saved as: {pdf_filename}")
else:
    st.warning(f"PDF not found: {pdf_filename}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ for crochet enthusiasts | Season-aware yarn recommendations | Direct purchase links</p>
</div>
""", unsafe_allow_html=True)
