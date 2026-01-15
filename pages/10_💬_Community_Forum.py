import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Community Forum", page_icon="💬", layout="wide")

# File to store comments
COMMENTS_FILE = "community_comments.xlsx"

def load_comments():
    """Load comments from Excel file"""
    if os.path.exists(COMMENTS_FILE):
        try:
            df = pd.read_excel(COMMENTS_FILE)
            return df
        except:
            return create_empty_comments()
    return create_empty_comments()

def create_empty_comments():
    """Create empty comments DataFrame"""
    return pd.DataFrame(columns=[
        'Comment_ID', 'Username', 'Category', 'Subject', 'Message', 
        'Timestamp', 'Likes', 'Pattern_Referenced', 'Tags'
    ])

def save_comments(df):
    """Save comments to Excel file"""
    df.to_excel(COMMENTS_FILE, index=False)

def add_comment(username, category, subject, message, pattern_ref, tags):
    """Add a new comment"""
    df = load_comments()
    
    new_comment = pd.DataFrame([{
        'Comment_ID': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'Username': username,
        'Category': category,
        'Subject': subject,
        'Message': message,
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Likes': 0,
        'Pattern_Referenced': pattern_ref,
        'Tags': tags
    }])
    
    df = pd.concat([df, new_comment], ignore_index=True)
    save_comments(df)
    return True

def like_comment(comment_id):
    """Add a like to a comment"""
    df = load_comments()
    df.loc[df['Comment_ID'] == comment_id, 'Likes'] += 1
    save_comments(df)

# Custom CSS
st.markdown("""
<style>
    .comment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #E8819C;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .comment-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .username {
        font-weight: bold;
        color: #E8819C;
        font-size: 1.1rem;
    }
    .timestamp {
        color: #666;
        font-size: 0.9rem;
    }
    .subject {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .message {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .comment-footer {
        display: flex;
        gap: 1rem;
        align-items: center;
        color: #888;
        font-size: 0.9rem;
    }
    .category-badge {
        background: #E8819C;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        display: inline-block;
    }
    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)

# Header
st.title("💬 Community Forum")
st.markdown("**Connect with fellow crocheters, share tips, and discuss patterns!**")
st.markdown("---")

# Load comments
comments_df = load_comments()

# Sidebar stats
with st.sidebar:
    st.markdown("### 📊 Forum Stats")
    total_comments = len(comments_df)
    total_likes = comments_df['Likes'].sum() if not comments_df.empty else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Comments", total_comments)
    with col2:
        st.metric("❤️ Total Likes", int(total_likes))
    
    st.markdown("---")
    
    # Category filter
    st.markdown("### 🔍 Filter by Category")
    categories = ['All'] + comments_df['Category'].unique().tolist() if not comments_df.empty else ['All']
    selected_category = st.selectbox("Category", categories, key="cat_filter")
    
    # Search
    st.markdown("### 🔎 Search")
    search_term = st.text_input("Search comments...", key="search")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📝 Post Comment", "💬 View Comments", "🔥 Popular"])

# Tab 1: Post Comment
with tab1:
    st.markdown("### Share Your Thoughts")
    
    with st.form("post_comment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Your Name*", placeholder="CrochetLover123")
            category = st.selectbox("Category*", [
                "General Discussion",
                "Pattern Help",
                "Yarn Recommendations",
                "Project Showcase",
                "Tips & Tricks",
                "Beginner Questions",
                "Advanced Techniques",
                "Troubleshooting",
                "Inspiration",
                "Off Topic"
            ])
        
        with col2:
            subject = st.text_input("Subject*", placeholder="Help with tension issues...")
            pattern_ref = st.text_input("Pattern Name (optional)", placeholder="e.g., Bobby Granny Square Blanket")
        
        message = st.text_area(
            "Your Message*", 
            placeholder="Share your thoughts, questions, tips, or project updates...",
            height=150
        )
        
        tags = st.text_input("Tags (optional)", placeholder="granny-square, beginner, cotton")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            submit = st.form_submit_button("🚀 Post Comment", use_container_width=True)
        
        if submit:
            if username and category and subject and message:
                add_comment(username, category, subject, message, pattern_ref, tags)
                st.success("✅ Comment posted successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (Name, Category, Subject, Message)")

# Tab 2: View Comments
with tab2:
    # Filter comments
    filtered_df = comments_df.copy()
    
    if selected_category != 'All' and not filtered_df.empty:
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    
    if search_term and not filtered_df.empty:
        mask = (
            filtered_df['Subject'].str.contains(search_term, case=False, na=False) |
            filtered_df['Message'].str.contains(search_term, case=False, na=False) |
            filtered_df['Username'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Sort options
    col1, col2 = st.columns([3, 1])
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Most Liked"])
    
    if sort_by == "Newest First":
        filtered_df = filtered_df.sort_values('Timestamp', ascending=False)
    elif sort_by == "Oldest First":
        filtered_df = filtered_df.sort_values('Timestamp', ascending=True)
    else:  # Most Liked
        filtered_df = filtered_df.sort_values('Likes', ascending=False)
    
    st.markdown(f"### {len(filtered_df)} Comments")
    
    if filtered_df.empty:
        st.info("🔍 No comments yet. Be the first to start the conversation!")
    else:
        # Display comments
        for idx, row in filtered_df.iterrows():
            with st.container():
                # Comment card
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="comment-card">
                        <div class="comment-header">
                            <span class="username">👤 {row['Username']}</span>
                            <span class="timestamp">🕐 {row['Timestamp']}</span>
                        </div>
                        <div class="subject">{row['Subject']}</div>
                        <span class="category-badge">{row['Category']}</span>
                        <div class="message">{row['Message']}</div>
                        <div class="comment-footer">
                            <span>❤️ {int(row['Likes'])} likes</span>
                            {f"<span>🧶 Pattern: {row['Pattern_Referenced']}</span>" if pd.notna(row['Pattern_Referenced']) and row['Pattern_Referenced'] else ""}
                            {f"<span>🏷️ {row['Tags']}</span>" if pd.notna(row['Tags']) and row['Tags'] else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button(f"❤️ Like", key=f"like_{row['Comment_ID']}"):
                        like_comment(row['Comment_ID'])
                        st.rerun()

# Tab 3: Popular
with tab3:
    st.markdown("### 🔥 Most Popular Comments")
    
    if comments_df.empty:
        st.info("No comments yet!")
    else:
        popular_df = comments_df.sort_values('Likes', ascending=False).head(10)
        
        for idx, row in popular_df.iterrows():
            with st.container():
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="comment-card">
                        <div class="comment-header">
                            <span class="username">👤 {row['Username']}</span>
                            <span class="timestamp">🕐 {row['Timestamp']}</span>
                        </div>
                        <div class="subject">{row['Subject']}</div>
                        <span class="category-badge">{row['Category']}</span>
                        <div class="message">{row['Message']}</div>
                        <div class="comment-footer">
                            <span>❤️ {int(row['Likes'])} likes</span>
                            {f"<span>🧶 Pattern: {row['Pattern_Referenced']}</span>" if pd.notna(row['Pattern_Referenced']) and row['Pattern_Referenced'] else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button(f"❤️ Like", key=f"popular_like_{row['Comment_ID']}"):
                        like_comment(row['Comment_ID'])
                        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💬 Community Guidelines: Be respectful, helpful, and kind to fellow crocheters!</p>
    <p>Share your knowledge, ask questions, and celebrate each other's projects 🧶✨</p>
</div>
""", unsafe_allow_html=True)
