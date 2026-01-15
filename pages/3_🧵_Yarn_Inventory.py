"""
Yarn Inventory Tracker
Track your personal yarn stash with quantities, locations, and purchase info
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

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
        font-family: 'Great Vibes', cursive !important;
        color: #D66B87;
    }
    .stat-number { font-family: 'Nunito', sans-serif !important; }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)

st.set_page_config(
    page_title="Yarn Inventory - Tangled",
    page_icon="🧵",
    layout="wide"
)

# File path for inventory
INVENTORY_FILE = "yarn_inventory.xlsx"

def load_inventory():
    """Load yarn inventory from Excel file"""
    if os.path.exists(INVENTORY_FILE):
        try:
            return pd.read_excel(INVENTORY_FILE)
        except:
            return create_empty_inventory()
    else:
        return create_empty_inventory()

def create_empty_inventory():
    """Create empty inventory DataFrame with proper columns"""
    return pd.DataFrame(columns=[
        'Yarn_Name', 'Brand', 'Color', 'Weight', 'Fiber_Content',
        'Quantity_Skeins', 'Grams_Per_Skein', 'Total_Grams',
        'Needle_Hook_Size', 'Yarn_Thickness', 'Season',
        'Location', 'Purchase_Date', 'Purchase_Price', 'Notes', 'Date_Added'
    ])

def save_inventory(df):
    """Save inventory to Excel file"""
    df.to_excel(INVENTORY_FILE, index=False)

# Initialize session state
if 'inventory_df' not in st.session_state:
    st.session_state.inventory_df = load_inventory()

# Header
st.title("🧵 My Yarn Inventory")
st.markdown("Track your yarn stash and never forget what you have!")

# Sidebar for actions
with st.sidebar:
    st.header("Actions")
    action = st.radio(
        "What would you like to do?",
        ["View Inventory", "Add New Yarn", "Edit/Delete Yarn", "Statistics"]
    )

# Main content based on action
if action == "View Inventory":
    st.header("📦 Your Yarn Stash")
    
    # Filters - First row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_weight = st.multiselect(
            "Filter by Weight",
            options=["All"] + sorted(st.session_state.inventory_df['Weight'].dropna().unique().tolist()) if not st.session_state.inventory_df.empty else ["All"],
            default=["All"]
        )
    
    with col2:
        filter_brand = st.multiselect(
            "Filter by Brand",
            options=["All"] + sorted(st.session_state.inventory_df['Brand'].dropna().unique().tolist()) if not st.session_state.inventory_df.empty else ["All"],
            default=["All"]
        )
    
    with col3:
        search_term = st.text_input("🔍 Search", placeholder="Search yarn name or color...")
    
    # Filters - Second row
    col4, col5, col6 = st.columns(3)
    
    with col4:
        # Needle/Hook Size filter
        if 'Needle_Hook_Size' in st.session_state.inventory_df.columns:
            filter_hook = st.multiselect(
                "Filter by Needle/Hook Size",
                options=["All"] + sorted(st.session_state.inventory_df['Needle_Hook_Size'].dropna().unique().tolist()) if not st.session_state.inventory_df.empty else ["All"],
                default=["All"]
            )
        else:
            filter_hook = ["All"]
    
    with col5:
        # Yarn Thickness filter (alternative to weight)
        if 'Yarn_Thickness' in st.session_state.inventory_df.columns:
            filter_thickness = st.multiselect(
                "Filter by Yarn Thickness",
                options=["All"] + sorted(st.session_state.inventory_df['Yarn_Thickness'].dropna().unique().tolist()) if not st.session_state.inventory_df.empty else ["All"],
                default=["All"]
            )
        else:
            filter_thickness = ["All"]
    
    with col6:
        # Season filter
        if 'Season' in st.session_state.inventory_df.columns:
            filter_season = st.multiselect(
                "Filter by Season",
                options=["All"] + sorted(st.session_state.inventory_df['Season'].dropna().unique().tolist()) if not st.session_state.inventory_df.empty else ["All"],
                default=["All"]
            )
        else:
            filter_season = ["All"]
    
    # Apply filters
    filtered_df = st.session_state.inventory_df.copy()
    
    if not filtered_df.empty:
        if "All" not in filter_weight and filter_weight:
            filtered_df = filtered_df[filtered_df['Weight'].isin(filter_weight)]
        
        if "All" not in filter_brand and filter_brand:
            filtered_df = filtered_df[filtered_df['Brand'].isin(filter_brand)]
        
        if "All" not in filter_hook and filter_hook and 'Needle_Hook_Size' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Needle_Hook_Size'].isin(filter_hook)]
        
        if "All" not in filter_thickness and filter_thickness and 'Yarn_Thickness' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Yarn_Thickness'].isin(filter_thickness)]
        
        if "All" not in filter_season and filter_season and 'Season' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Season'].isin(filter_season)]
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['Yarn_Name'].str.contains(search_term, case=False, na=False) |
                filtered_df['Color'].str.contains(search_term, case=False, na=False)
            ]
    
    # Display inventory
    if filtered_df.empty:
        st.info("No yarns in inventory yet. Add your first yarn using 'Add New Yarn' in the sidebar!")
    else:
        st.write(f"**Total yarns found:** {len(filtered_df)}")
        
        # Display as cards
        for idx, row in filtered_df.iterrows():
            with st.expander(f"🧶 {row['Yarn_Name']} - {row['Color']} ({row['Quantity_Skeins']} skeins)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Brand:** {row['Brand']}")
                    st.write(f"**Weight:** {row['Weight']}")
                    st.write(f"**Fiber:** {row['Fiber_Content']}")
                    st.write(f"**Quantity:** {row['Quantity_Skeins']} skeins ({row['Total_Grams']}g total)")
                
                with col2:
                    st.write(f"**Location:** {row['Location']}")
                    st.write(f"**Purchased:** {row['Purchase_Date']}")
                    st.write(f"**Price:** €{row['Purchase_Price']}")
                    if pd.notna(row['Notes']):
                        st.write(f"**Notes:** {row['Notes']}")

elif action == "Add New Yarn":
    st.header("➕ Add New Yarn to Inventory")
    
    with st.form("add_yarn_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            yarn_name = st.text_input("Yarn Name*", placeholder="e.g., Drops Cotton Merino")
            brand = st.text_input("Brand*", placeholder="e.g., Drops")
            color = st.text_input("Color*", placeholder="e.g., Navy Blue")
            weight = st.selectbox("Yarn Weight*", ["Lace", "Fingering", "Sport", "DK", "Worsted", "Aran", "Bulky", "Super Bulky", "Jumbo"])
            fiber_content = st.text_input("Fiber Content*", placeholder="e.g., 50% Cotton, 50% Merino Wool")
            needle_hook_size = st.text_input("Needle/Hook Size", placeholder="e.g., 3.5mm, 4mm")
            yarn_thickness = st.selectbox("Yarn Thickness", ["Not specified", "Very Fine", "Fine", "Light", "Medium", "Bulky", "Super Bulky", "Jumbo"])
        
        with col2:
            season = st.selectbox("Best Season", ["Not specified", "Spring", "Summer", "Fall", "Winter", "All Season"])
            quantity = st.number_input("Number of Skeins*", min_value=1, value=1, step=1)
            grams_per_skein = st.number_input("Grams per Skein*", min_value=1, value=50, step=10)
            location = st.text_input("Storage Location", placeholder="e.g., Blue bin, Bedroom closet")
            purchase_date = st.date_input("Purchase Date", value=datetime.now())
            purchase_price = st.number_input("Purchase Price (€)", min_value=0.0, value=0.0, step=0.50)
            notes = st.text_area("Notes", placeholder="Any additional information...")
        
        submitted = st.form_submit_button("✅ Add to Inventory")
        
        if submitted:
            if yarn_name and brand and color:
                total_grams = quantity * grams_per_skein
                
                new_yarn = {
                    'Yarn_Name': yarn_name,
                    'Brand': brand,
                    'Color': color,
                    'Weight': weight,
                    'Fiber_Content': fiber_content,
                    'Quantity_Skeins': quantity,
                    'Needle_Hook_Size': needle_hook_size if needle_hook_size else "Not specified",
                    'Yarn_Thickness': yarn_thickness,
                    'Season': season,
                    'Grams_Per_Skein': grams_per_skein,
                    'Total_Grams': total_grams,
                    'Location': location,
                    'Purchase_Date': purchase_date.strftime("%Y-%m-%d"),
                    'Purchase_Price': purchase_price,
                    'Notes': notes,
                    'Date_Added': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.session_state.inventory_df = pd.concat(
                    [st.session_state.inventory_df, pd.DataFrame([new_yarn])],
                    ignore_index=True
                )
                
                save_inventory(st.session_state.inventory_df)
                st.success(f"✅ Added {yarn_name} to your inventory!")
                st.balloons()
            else:
                st.error("Please fill in all required fields (marked with *)")

elif action == "Edit/Delete Yarn":
    st.header("✏️ Edit or Delete Yarn")
    
    if st.session_state.inventory_df.empty:
        st.info("No yarns in inventory to edit.")
    else:
        # Select yarn to edit
        yarn_options = [
            f"{row['Yarn_Name']} - {row['Color']} ({row['Brand']})"
            for _, row in st.session_state.inventory_df.iterrows()
        ]
        
        selected_yarn = st.selectbox("Select yarn to edit/delete:", yarn_options)
        
        if selected_yarn:
            selected_idx = yarn_options.index(selected_yarn)
            yarn_data = st.session_state.inventory_df.iloc[selected_idx]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("Edit Yarn Details")
            
            with col2:
                if st.button("🗑️ Delete This Yarn", type="secondary"):
                    st.session_state.inventory_df = st.session_state.inventory_df.drop(selected_idx).reset_index(drop=True)
                    save_inventory(st.session_state.inventory_df)
                    st.success("Yarn deleted!")
                    st.rerun()
            
            # Edit form
            with st.form("edit_yarn_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_quantity = st.number_input("Number of Skeins", value=int(yarn_data['Quantity_Skeins']), min_value=0)
                    new_location = st.text_input("Location", value=str(yarn_data['Location']))
                    new_price = st.number_input("Price (€)", value=float(yarn_data['Purchase_Price']), min_value=0.0, step=0.50)
                
                with col2:
                    new_notes = st.text_area("Notes", value=str(yarn_data['Notes']) if pd.notna(yarn_data['Notes']) else "")
                
                update_submitted = st.form_submit_button("💾 Update Yarn")
                
                if update_submitted:
                    st.session_state.inventory_df.at[selected_idx, 'Quantity_Skeins'] = new_quantity
                    st.session_state.inventory_df.at[selected_idx, 'Total_Grams'] = new_quantity * yarn_data['Grams_Per_Skein']
                    st.session_state.inventory_df.at[selected_idx, 'Location'] = new_location
                    st.session_state.inventory_df.at[selected_idx, 'Purchase_Price'] = new_price
                    st.session_state.inventory_df.at[selected_idx, 'Notes'] = new_notes
                    
                    save_inventory(st.session_state.inventory_df)
                    st.success("✅ Yarn updated!")

elif action == "Statistics":
    st.header("📊 Yarn Stash Statistics")
    
    if st.session_state.inventory_df.empty:
        st.info("Add yarns to your inventory to see statistics!")
    else:
        df = st.session_state.inventory_df
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Yarns", len(df))
        
        with col2:
            total_skeins = df['Quantity_Skeins'].sum()
            st.metric("Total Skeins", int(total_skeins))
        
        with col3:
            total_weight = df['Total_Grams'].sum() / 1000  # Convert to kg
            st.metric("Total Weight", f"{total_weight:.2f} kg")
        
        with col4:
            total_value = df['Purchase_Price'].sum()
            st.metric("Total Value", f"€{total_value:.2f}")
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Yarns by Weight")
            weight_counts = df['Weight'].value_counts()
            st.bar_chart(weight_counts)
        
        with col2:
            st.subheader("Yarns by Brand")
            brand_counts = df['Brand'].value_counts().head(10)
            st.bar_chart(brand_counts)
        
        st.divider()
        
        # Most/Least stocked
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔝 Most Stocked Colors")
            top_colors = df.nlargest(5, 'Quantity_Skeins')[['Yarn_Name', 'Color', 'Quantity_Skeins']]
            st.dataframe(top_colors, hide_index=True)
        
        with col2:
            st.subheader("⚠️ Low Stock (< 2 skeins)")
            low_stock = df[df['Quantity_Skeins'] < 2][['Yarn_Name', 'Color', 'Quantity_Skeins']]
            if low_stock.empty:
                st.success("All yarns well stocked!")
            else:
                st.dataframe(low_stock, hide_index=True)

# Footer
st.divider()
st.caption("💡 Tip: Keep your inventory updated when you use yarn for projects!")
