"""
Pattern Comparison Tool
Compare multiple crochet patterns side-by-side
"""

import streamlit as st
import pandas as pd
import os

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)

st.set_page_config(
    page_title="Pattern Comparison - Tangled",
    page_icon="⚖️",
    layout="wide"
)

# File paths
PATTERNS_FILE = "pattern_database.xlsx"
YARN_DB_FILE = "Database_YARN.xlsx"

@st.cache_data
def load_patterns():
    """Load pattern database"""
    if os.path.exists(PATTERNS_FILE):
        try:
            return pd.read_excel(PATTERNS_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data
def load_yarn_db():
    """Load yarn database"""
    if os.path.exists(YARN_DB_FILE):
        try:
            return pd.read_excel(YARN_DB_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def get_pattern_cost_estimate(pattern, yarn_db):
    """Estimate cost range for a pattern"""
    try:
        yarn_weight = pattern['Yarn_Weight']
        # Filter yarns by weight
        matching_yarns = yarn_db[yarn_db['Yarn_Thickness'].str.contains(yarn_weight, case=False, na=False)]
        
        if not matching_yarns.empty:
            min_price = matching_yarns['Price'].min()
            max_price = matching_yarns['Price'].max()
            avg_price = matching_yarns['Price'].mean()
            
            # Estimate balls needed based on pattern type
            balls_needed = 3  # Default estimate
            
            return {
                'min': min_price * balls_needed,
                'max': max_price * balls_needed,
                'avg': avg_price * balls_needed
            }
    except:
        pass
    
    return {'min': 0, 'max': 0, 'avg': 0}

# Load data
patterns_df = load_patterns()
yarn_db = load_yarn_db()

# Header
st.title("⚖️ Pattern Comparison Tool")
st.markdown("Compare up to 3 patterns side-by-side to help you decide what to make next!")

if patterns_df.empty:
    st.error("No patterns found in database. Please add patterns first!")
else:
    # Pattern selection
    pattern_names = sorted(patterns_df['Pattern Name'].dropna().unique().tolist())
    
    st.subheader("Select Patterns to Compare")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pattern1 = st.selectbox("Pattern 1", ["None"] + pattern_names, key="p1")
    
    with col2:
        pattern2 = st.selectbox("Pattern 2", ["None"] + pattern_names, key="p2")
    
    with col3:
        pattern3 = st.selectbox("Pattern 3", ["None"] + pattern_names, key="p3")
    
    # Get selected patterns
    selected_patterns = [p for p in [pattern1, pattern2, pattern3] if p != "None"]
    
    if len(selected_patterns) < 2:
        st.info("👆 Select at least 2 patterns to compare")
    else:
        st.divider()
        
        # Create comparison table
        comparison_data = []
        
        for pattern_name in selected_patterns:
            pattern = patterns_df[patterns_df['Pattern_Name'] == pattern_name].iloc[0]
            
            # Get cost estimate
            cost_est = get_pattern_cost_estimate(pattern, yarn_db)
            
            comparison_data.append({
                'Pattern': pattern_name,
                'Difficulty': pattern.get('Difficulty_Level', 'Unknown'),
                'Yarn Weight': pattern.get('Yarn_Weight', 'Unknown'),
                'Hook Size': pattern.get('Hook_Size', 'Unknown'),
                'Structure': pattern.get('Pattern_Structure', 'Unknown'),
                'Stitches': pattern.get('Stitches_Required', 'Unknown'),
                'Est. Cost': f"€{cost_est['avg']:.2f}" if cost_est['avg'] > 0 else 'N/A'
            })
        
        # Display comparison table
        st.subheader("📊 Quick Comparison")
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, hide_index=True, use_container_width=True)
        
        st.divider()
        
        # Detailed comparison
        st.subheader("🔍 Detailed Comparison")
        
        # Create columns for each pattern
        cols = st.columns(len(selected_patterns))
        
        for idx, pattern_name in enumerate(selected_patterns):
            pattern = patterns_df[patterns_df['Pattern_Name'] == pattern_name].iloc[0]
            cost_est = get_pattern_cost_estimate(pattern, yarn_db)
            
            with cols[idx]:
                st.markdown(f"### {pattern_name}")
                
                # Difficulty badge
                difficulty = pattern.get('Difficulty_Level', 'Unknown')
                difficulty_colors = {
                    'Beginner': '🟢',
                    'Easy': '🟢',
                    'Intermediate': '🟡',
                    'Advanced': '🟠',
                    'Expert': '🔴'
                }
                difficulty_emoji = difficulty_colors.get(difficulty, '⚪')
                st.markdown(f"**Difficulty:** {difficulty_emoji} {difficulty}")
                
                st.markdown("---")
                
                # Materials section
                st.markdown("**📦 Materials**")
                st.write(f"• Yarn: {pattern.get('Yarn_Weight', 'Unknown')}")
                st.write(f"• Hook: {pattern.get('Hook_Size', 'Unknown')}")
                if pd.notna(pattern.get('Materials_Needed')):
                    st.write(f"• Other: {pattern.get('Materials_Needed', '')[:50]}...")
                
                st.markdown("---")
                
                # Technical details
                st.markdown("**🧶 Technical Details**")
                st.write(f"• Structure: {pattern.get('Pattern_Structure', 'Unknown')}")
                if pd.notna(pattern.get('Stitches_Required')):
                    stitches = str(pattern.get('Stitches_Required', ''))
                    st.write(f"• Stitches: {stitches[:40]}...")
                
                st.markdown("---")
                
                # Cost estimate
                st.markdown("**💰 Estimated Cost**")
                if cost_est['avg'] > 0:
                    st.write(f"Range: €{cost_est['min']:.2f} - €{cost_est['max']:.2f}")
                    st.write(f"Average: €{cost_est['avg']:.2f}")
                else:
                    st.write("Cost estimate not available")
                
                st.markdown("---")
                
                # Yarn composition
                if pd.notna(pattern.get('Recommended_Yarn_Composition')):
                    st.markdown("**🎨 Recommended Fiber**")
                    st.write(pattern.get('Recommended_Yarn_Composition', ''))
        
        st.divider()
        
        # Comparison insights
        st.subheader("💡 Comparison Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Easiest Pattern**")
            difficulty_order = ['Beginner', 'Easy', 'Intermediate', 'Advanced', 'Expert']
            easiest = None
            easiest_idx = 999
            
            for pattern_name in selected_patterns:
                pattern = patterns_df[patterns_df['Pattern_Name'] == pattern_name].iloc[0]
                diff = pattern.get('Difficulty_Level', 'Unknown')
                if diff in difficulty_order:
                    idx = difficulty_order.index(diff)
                    if idx < easiest_idx:
                        easiest_idx = idx
                        easiest = pattern_name
            
            if easiest:
                st.success(f"✨ {easiest}")
            else:
                st.info("Difficulty levels not comparable")
        
        with col2:
            st.markdown("**💵 Most Affordable**")
            cheapest = None
            cheapest_cost = float('inf')
            
            for pattern_name in selected_patterns:
                pattern = patterns_df[patterns_df['Pattern_Name'] == pattern_name].iloc[0]
                cost = get_pattern_cost_estimate(pattern, yarn_db)
                if cost['avg'] > 0 and cost['avg'] < cheapest_cost:
                    cheapest_cost = cost['avg']
                    cheapest = pattern_name
            
            if cheapest:
                st.success(f"💰 {cheapest} (~€{cheapest_cost:.2f})")
            else:
                st.info("Cost estimates not available")
        
        # Pros/Cons section
        st.divider()
        st.subheader("✅ ❌ Quick Pros & Cons")
        
        cols = st.columns(len(selected_patterns))
        
        for idx, pattern_name in enumerate(selected_patterns):
            pattern = patterns_df[patterns_df['Pattern_Name'] == pattern_name].iloc[0]
            
            with cols[idx]:
                st.markdown(f"**{pattern_name}**")
                
                # Pros
                st.markdown("✅ **Pros:**")
                pros = []
                
                diff = pattern.get('Difficulty_Level', '')
                if diff in ['Beginner', 'Easy']:
                    pros.append("• Easy to complete")
                
                cost = get_pattern_cost_estimate(pattern, yarn_db)
                if cost['avg'] > 0 and cost['avg'] < 20:
                    pros.append("• Affordable")
                
                structure = str(pattern.get('Pattern_Structure', '')).lower()
                if 'rounds' in structure or 'round' in structure:
                    pros.append("• Worked in rounds")
                
                if not pros:
                    pros.append("• Unique pattern")
                
                for pro in pros:
                    st.write(pro)
                
                # Cons
                st.markdown("❌ **Cons:**")
                cons = []
                
                if diff in ['Advanced', 'Expert']:
                    cons.append("• Challenging skill level")
                
                if cost['avg'] > 30:
                    cons.append("• Higher material cost")
                
                stitches = str(pattern.get('Stitches_Required', '')).lower()
                if 'special' in stitches:
                    cons.append("• Requires special stitches")
                
                if not cons:
                    cons.append("• None identified")
                
                for con in cons:
                    st.write(con)
        
        st.divider()
        
        # Decision helper
        st.subheader("🎲 Need Help Deciding?")
        
        if st.button("🎲 Pick a Random Pattern for Me!", type="primary"):
            import random
            choice = random.choice(selected_patterns)
            st.balloons()
            st.success(f"✨ You should make: **{choice}**!")
            st.write("Sometimes the best decision is a random one! 🎉")

# Footer
st.divider()
st.caption("💡 Tip: Compare patterns based on your current skill level and available time!")
