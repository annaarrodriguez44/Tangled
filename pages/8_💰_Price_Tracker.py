"""
Yarn Price History Tracker
Track yarn prices over time and get notified of sales
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Price Tracker - Tangled",
    page_icon="💰",
    layout="wide"
)

# File paths
PRICE_HISTORY_FILE = "yarn_price_history.xlsx"
YARN_DB_FILE = "Database_YARN.xlsx"

def load_price_history():
    if os.path.exists(PRICE_HISTORY_FILE):
        try:
            return pd.read_excel(PRICE_HISTORY_FILE)
        except:
            return pd.DataFrame(columns=[
                'Yarn_Name', 'Brand', 'Price', 'Date_Recorded', 'Store', 'Link', 'Notes'
            ])
    return pd.DataFrame(columns=[
        'Yarn_Name', 'Brand', 'Price', 'Date_Recorded', 'Store', 'Link', 'Notes'
    ])

def load_yarn_db():
    if os.path.exists(YARN_DB_FILE):
        try:
            return pd.read_excel(YARN_DB_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_price_history(df):
    df.to_excel(PRICE_HISTORY_FILE, index=False)

def get_price_trend(yarn_name, price_df):
    """Get price trend for a specific yarn"""
    yarn_prices = price_df[price_df['Yarn_Name'] == yarn_name].copy()
    if not yarn_prices.empty:
        yarn_prices['Date_Recorded'] = pd.to_datetime(yarn_prices['Date_Recorded'])
        yarn_prices = yarn_prices.sort_values('Date_Recorded')
        return yarn_prices
    return None

def detect_sale(yarn_name, price_df, threshold=0.20):
    """Detect if yarn is on sale (>20% off)"""
    trend = get_price_trend(yarn_name, price_df)
    if trend is not None and len(trend) >= 2:
        latest_price = trend.iloc[-1]['Price']
        previous_avg = trend.iloc[:-1]['Price'].mean()
        
        if previous_avg > 0:
            discount = (previous_avg - latest_price) / previous_avg
            if discount >= threshold:
                return True, discount * 100
    return False, 0

# Initialize session state
if 'price_history_df' not in st.session_state:
    st.session_state.price_history_df = load_price_history()

yarn_db = load_yarn_db()

# Header
st.title("💰 Yarn Price History Tracker")
st.markdown("Track yarn prices over time and never miss a sale!")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Price Trends", "➕ Add Price", "🔔 Sale Alerts"])

with tab1:
    st.header("Price Trends")
    
    if st.session_state.price_history_df.empty:
        st.info("No price data yet. Start tracking prices in the 'Add Price' tab!")
    else:
        df = st.session_state.price_history_df.copy()
        
        # Get unique yarns
        unique_yarns = sorted(df['Yarn_Name'].unique().tolist())
        
        selected_yarn = st.selectbox("Select Yarn to View Trend", unique_yarns)
        
        if selected_yarn:
            trend_data = get_price_trend(selected_yarn, df)
            
            if trend_data is not None and len(trend_data) > 0:
                # Price statistics
                col1, col2, col3, col4 = st.columns(4)
                
                current_price = trend_data.iloc[-1]['Price']
                avg_price = trend_data['Price'].mean()
                min_price = trend_data['Price'].min()
                max_price = trend_data['Price'].max()
                
                with col1:
                    st.metric("Current Price", f"€{current_price:.2f}")
                
                with col2:
                    st.metric("Average Price", f"€{avg_price:.2f}")
                
                with col3:
                    st.metric("Lowest Price", f"€{min_price:.2f}")
                
                with col4:
                    st.metric("Highest Price", f"€{max_price:.2f}")
                
                # Price trend chart
                st.subheader("Price Over Time")
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=trend_data['Date_Recorded'],
                    y=trend_data['Price'],
                    mode='lines+markers',
                    name='Price',
                    line=dict(color='#E8819C', width=3),
                    marker=dict(size=8)
                ))
                
                # Add average line
                fig.add_hline(
                    y=avg_price,
                    line_dash="dash",
                    line_color="gray",
                    annotation_text="Average"
                )
                
                fig.update_layout(
                    title=f"Price History: {selected_yarn}",
                    xaxis_title="Date",
                    yaxis_title="Price (€)",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Price history table
                st.subheader("Price History Details")
                
                display_df = trend_data[['Date_Recorded', 'Price', 'Store', 'Notes']].copy()
                display_df['Date_Recorded'] = display_df['Date_Recorded'].dt.strftime('%Y-%m-%d')
                display_df = display_df.sort_values('Date_Recorded', ascending=False)
                
                st.dataframe(display_df, hide_index=True, use_container_width=True)
                
                # Check if on sale
                is_sale, discount = detect_sale(selected_yarn, df)
                if is_sale:
                    st.success(f"🎉 This yarn is currently {discount:.0f}% off! Great time to buy!")

with tab2:
    st.header("Add Price Record")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("Track prices from your favorite stores to catch the best deals!")
    
    with col2:
        import_option = st.selectbox("Quick add from:", ["Manual Entry", "From Yarn Database"])
    
    with st.form("add_price_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            if import_option == "From Yarn Database" and not yarn_db.empty:
                yarn_names = sorted(yarn_db['Yarn Name'].dropna().unique().tolist())
                yarn_name = st.selectbox("Yarn Name*", yarn_names)
                
                # Auto-fill brand if available
                selected_yarn_info = yarn_db[yarn_db['Yarn Name'] == yarn_name].iloc[0] if not yarn_db[yarn_db['Yarn Name'] == yarn_name].empty else None
                default_brand = selected_yarn_info['Brand'] if selected_yarn_info is not None and 'Brand' in selected_yarn_info else ""
                brand = st.text_input("Brand*", value=default_brand)
            else:
                yarn_name = st.text_input("Yarn Name*", placeholder="e.g., Cotton Merino")
                brand = st.text_input("Brand*", placeholder="e.g., Drops")
            
            price = st.number_input("Price (€)*", min_value=0.0, value=0.0, step=0.50)
            date_recorded = st.date_input("Date*", value=datetime.now())
        
        with col2:
            store = st.text_input("Store", placeholder="e.g., Wool Warehouse, LoveCrafts")
            link = st.text_input("Product Link (optional)", placeholder="https://...")
            notes = st.text_area("Notes", placeholder="e.g., Sale price, bulk discount")
        
        submitted = st.form_submit_button("💾 Save Price")
        
        if submitted:
            if yarn_name and brand and price > 0:
                new_price = {
                    'Yarn_Name': yarn_name,
                    'Brand': brand,
                    'Price': price,
                    'Date_Recorded': date_recorded.strftime("%Y-%m-%d"),
                    'Store': store,
                    'Link': link,
                    'Notes': notes
                }
                
                st.session_state.price_history_df = pd.concat(
                    [st.session_state.price_history_df, pd.DataFrame([new_price])],
                    ignore_index=True
                )
                
                save_price_history(st.session_state.price_history_df)
                st.success(f"✅ Price recorded for {yarn_name}!")
                
                # Check if this is a sale
                is_sale, discount = detect_sale(yarn_name, st.session_state.price_history_df)
                if is_sale:
                    st.balloons()
                    st.success(f"🎉 Great deal! This is {discount:.0f}% cheaper than usual!")
            else:
                st.error("Please fill in all required fields")

with tab3:
    st.header("🔔 Sale Alerts")
    
    if st.session_state.price_history_df.empty:
        st.info("Start tracking prices to see sale alerts here!")
    else:
        df = st.session_state.price_history_df.copy()
        
        # Set alert threshold
        threshold = st.slider("Sale threshold (%)", 10, 50, 20, step=5, help="Alert when price drops by this percentage")
        
        st.divider()
        
        # Check all yarns for sales
        unique_yarns = df['Yarn_Name'].unique()
        sales_found = []
        
        for yarn in unique_yarns:
            is_sale, discount = detect_sale(yarn, df, threshold=threshold/100)
            if is_sale:
                trend = get_price_trend(yarn, df)
                current_price = trend.iloc[-1]['Price']
                previous_avg = trend.iloc[:-1]['Price'].mean()
                
                sales_found.append({
                    'Yarn': yarn,
                    'Current': current_price,
                    'Previous Avg': previous_avg,
                    'Discount': discount,
                    'Store': trend.iloc[-1]['Store']
                })
        
        if not sales_found:
            st.success(f"No yarns are currently {threshold}%+ off. Keep tracking prices!")
        else:
            st.success(f"🎉 Found {len(sales_found)} yarn(s) on sale!")
            
            for sale in sales_found:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### 🧶 {sale['Yarn']}")
                        if sale['Store']:
                            st.caption(f"Store: {sale['Store']}")
                    
                    with col2:
                        st.metric("Current Price", f"€{sale['Current']:.2f}", 
                                 delta=f"-€{sale['Previous Avg'] - sale['Current']:.2f}")
                    
                    with col3:
                        st.metric("Discount", f"{sale['Discount']:.0f}% OFF", delta_color="inverse")
                    
                    st.divider()
        
        st.subheader("Price Drop History")
        st.markdown("Track how often yarns go on sale to time your purchases!")
        
        # Calculate price volatility for each yarn
        if len(unique_yarns) > 0:
            volatility_data = []
            
            for yarn in unique_yarns:
                trend = get_price_trend(yarn, df)
                if trend is not None and len(trend) >= 2:
                    price_range = trend['Price'].max() - trend['Price'].min()
                    avg_price = trend['Price'].mean()
                    volatility = (price_range / avg_price) * 100 if avg_price > 0 else 0
                    
                    volatility_data.append({
                        'Yarn': yarn,
                        'Price Variation': volatility,
                        'Times Tracked': len(trend)
                    })
            
            if volatility_data:
                vol_df = pd.DataFrame(volatility_data).sort_values('Price Variation', ascending=False)
                
                st.write("**Yarns with Most Price Variation** (Best candidates for sale watching)")
                st.dataframe(vol_df, hide_index=True, use_container_width=True)

# Footer
st.divider()
st.caption("💡 Tip: Track prices regularly to identify seasonal patterns and best buying times!")
