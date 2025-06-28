# ui/streamlit_app.py
import sys
import os
import time
import streamlit as st
import yaml
from dotenv import load_dotenv

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraping.rss_scraper import fetch_articles
from chains.filter_chain import classify_and_score_articles
from delivery.emailer import send_email
from app import filter_and_rank_articles

# Load environment variables
load_dotenv()

# Load config
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config.yaml")
with open(config_path, encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Enhanced page config
st.set_page_config(
    page_title="AI News Filter", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Custom header */
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .custom-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .custom-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #4f46e5;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #6b7280;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Article cards */
    .article-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #4f46e5;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .article-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        border-left-color: #7c3aed;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .status-warning {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .status-error {
        background: linear-gradient(90deg, #ef4444, #dc2626);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    
    /* Selectbox and inputs */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
<div class="custom-header">
    <h1>🧠 AI News Intelligence</h1>
    <p>Advanced news classification and delivery platform powered by artificial intelligence</p>
</div>
""", unsafe_allow_html=True)

# Sidebar UI with enhanced styling
with st.sidebar:
    st.markdown('<div class="section-header">🔍 Configuration</div>', unsafe_allow_html=True)
    
    topic = st.selectbox("Select Topic", [
        "education", "technology", "science", "health", "business", "finance", "environment"
    ], index=0, help="Choose the topic you want to filter news for")

    col1, col2 = st.columns(2)
    with col1:
        region = st.radio("Region", ["India", "Global"], index=0)
    with col2:
        content_type = st.radio("Content", ["General", "Sensitive"], index=0)
    
    num_articles = st.slider("Max Articles", 5, 100, 10, 5, help="Maximum number of articles to retrieve")

    st.markdown('<div class="section-header">📩 Email Delivery</div>', unsafe_allow_html=True)
    recipient_input = st.text_input("Recipients (comma-separated):", placeholder="email1@example.com, email2@example.com")
    recipient_emails = [e.strip() for e in recipient_input.split(",") if e.strip()]
    
    if recipient_emails:
        st.success(f"✅ {len(recipient_emails)} recipient(s) configured")

    st.markdown('<div class="section-header">⚙️ Advanced Settings</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        batch_size = st.slider("Batch Size", 5, 20, 10, help="Number of articles to process at once")
    with col2:
        min_score = st.slider("Min Score", 0, 100, 30, help="Minimum relevance score threshold")
    
    use_prefilter = st.checkbox("Use Keyword Pre-Filter", True, help="Apply keyword filtering before AI classification")

    st.markdown("---")
    submit = st.button("🚀 Start Analysis", help="Begin fetching and analyzing articles")

# Main content area
if submit:
    start_time = time.time()
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown(f'<div class="status-success">🔄 Processing {topic.title()} ({region})</div>', unsafe_allow_html=True)

    status_container = st.container()
    progress_container = st.container()
    
    with progress_container:
        progress = st.progress(0)
        status = st.empty()

    # Step 1: Fetch
    with status_container:
        st.markdown("### 📡 Phase 1: Article Fetching")
        status.text("🔍 Searching for relevant articles...")
    
    articles = fetch_articles(topic, region.lower())
    total_fetched = len(articles)
    progress.progress(10)
    
    if total_fetched > 0:
        st.markdown(f'<div class="status-success">✅ Successfully fetched {total_fetched} articles</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-error">❌ No articles found. Try a different topic or region.</div>', unsafe_allow_html=True)
        st.stop()

    # Step 2: Classify
    with status_container:
        st.markdown("### 🧠 Phase 2: AI Classification")
        status.text("🤖 Analyzing articles with AI classifier...")
    
    scored = classify_and_score_articles(
        articles,
        batch_size=batch_size,
        use_prefilter=use_prefilter,
        min_score=min_score,
        topic=topic
    )
    progress.progress(60)
    
    if len(scored) > 0:
        st.markdown(f'<div class="status-success">✅ {len(scored)} articles passed classification filters</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-warning">⚠️ No articles passed classification filters</div>', unsafe_allow_html=True)
        st.stop()

    # Step 3: Filter
    with status_container:
        st.markdown("### 📄 Phase 3: Final Filtering")
        status.text("🔧 Applying user preferences...")
    
    user_filter = {
        "topic": topic,
        "region": region,
        "content_type": content_type
    }
    final = filter_and_rank_articles(scored, user_filter, max_articles=num_articles)
    progress.progress(85)
    
    st.markdown(f'<div class="status-success">✅ {len(final)} articles match your preferences</div>', unsafe_allow_html=True)

    # Step 4: Display Results
    # Step 4: Display Results
    with status_container:
        st.markdown("### 📊 Results")
        status.text("📤 Preparing results...")

    if final:
        st.markdown("#### 📰 Filtered Articles")

        for idx, article in enumerate(final, 1):
            classification = article.get("classification", {})
            region_val = classification.get("region", "Unknown")
            source_name = article.get("source", "Unknown")

            with st.expander(f"{idx}. {article['title']}", expanded=False):
                st.markdown(f"🔗 **[Read Full Article]({article['link']})**")
                if article.get("summary"):
                    st.markdown(f"📝 **Summary:** {article['summary']}")
                st.caption(f"🌐 **Source:** {source_name} | 🗺️ **Region:** {region_val}")

        
            # Email functionality
        if recipient_emails:
            try:
                email_articles = [{
                    'title': a['title'],
                    'link': a['link'],
                    'summary': a.get('summary', ''),
                    'image': a.get('image', '')
                } for a in final]

                send_email(email_articles, topic=topic, recipients=recipient_emails)
                st.markdown(f'<div class="status-success">📧 Email sent successfully to {len(recipient_emails)} recipients</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="status-error">❌ Email sending failed: {e}</div>', unsafe_allow_html=True)

        else:
            st.markdown('<div class="status-warning">⚠️ No articles matched your criteria</div>', unsafe_allow_html=True)
            
        progress.progress(100)
        status.empty()

        # Enhanced Summary Metrics
        st.markdown("---")
        st.markdown("### 📊 Performance Analytics")
        
        # Create metric cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        duration = time.time() - start_time
        efficiency = (len(final) / max(total_fetched, 1)) * 100

        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_fetched}</div>
                <div class="metric-label">Fetched</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(scored)}</div>
                <div class="metric-label">Classified</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(final)}</div>
                <div class="metric-label">Final</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{duration:.1f}s</div>
                <div class="metric-label">Duration</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{efficiency:.0f}%</div>
                <div class="metric-label">Efficiency</div>
            </div>
            """, unsafe_allow_html=True)

        # Enhanced sidebar summary
        with st.sidebar:
            st.markdown('<div class="section-header">📋 Session Summary</div>', unsafe_allow_html=True)
            st.markdown(f"""
            **🎯 Topic:** {topic.title()}  
            **🌍 Region:** {region}  
            **📄 Content:** {content_type}  
            **📊 Max Articles:** {num_articles}  
            **⚙️ Batch Size:** {batch_size}  
            **🎚️ Min Score:** {min_score}  
            **⏱️ Duration:** {duration:.1f}s  
            """)
            
            if recipient_emails:
                st.markdown(f"**📧 Recipients:** {len(recipient_emails)}")
                for email in recipient_emails:
                    st.markdown(f"• {email}")

# Footer with branding
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem 0;">
    <p><strong>AI News Intelligence Platform</strong> • Powered by Advanced Machine Learning</p>
    <p style="font-size: 0.9rem;">Delivering personalized, relevant news content with AI precision</p>
</div>
""", unsafe_allow_html=True)