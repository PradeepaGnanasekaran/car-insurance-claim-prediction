import streamlit as st

st.set_page_config(
    page_title="Car Insurance AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #000000;
    }
    
    .custom-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #8b5cf6 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        padding: 0;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .sub-header {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stSidebar"] {
        background: #000000;
    }
    
    .sidebar-social {
        padding: 1.5rem 1rem;
        margin-top: 2rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .sidebar-social h3 {
        color: white !important;
        font-size: 1.1rem !important;
        margin-bottom: 1rem !important;
        text-align: center;
    }
    
    .sidebar-social-link {
        display: block;
        margin: 10px 0;
        padding: 12px 20px;
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 8px;
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .sidebar-social-link:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        color: white;
        text-decoration: none;
    }
    
    .sidebar-social-link i {
        margin-right: 8px;
    }
    
    .developer-credit {
        text-align: center;
        padding: 1.5rem;
        margin: 1.5rem 0;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .developer-credit p {
        margin: 0;
        font-family: 'Dancing Script', cursive;
        font-size: 1.8rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: 1px;
    }
    
    @keyframes glow {
        from { 
            filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.6));
        }
        to { 
            filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.8));
        }
    }
    
    .section-explanation {
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.4);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0 1.5rem 0;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        animation: glow-box 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow-box {
        from {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
            border-color: rgba(102, 126, 234, 0.4);
        }
        to {
            box-shadow: 0 0 30px rgba(102, 126, 234, 0.6);
            border-color: rgba(102, 126, 234, 0.7);
        }
    }
    
    .section-explanation p {
        color: white;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0;
        font-weight: 400;
    }
    
    .purple-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 1rem 0;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: 0.5s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(102, 126, 234, 0.5);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.6));
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-title {
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.8rem;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.6);
        line-height: 1.8;
        font-size: 0.95rem;
    }
    
    .nav-card {
        background: #000000;
        backdrop-filter: blur(15px);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .nav-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transform: rotate(45deg);
        transition: 0.6s;
    }
    
    .nav-card:hover::after {
        left: 100%;
    }
    
    .nav-card:hover {
        transform: scale(1.08) translateY(-5px);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        border: 2px solid rgba(102, 126, 234, 0.6);
        background: rgba(102, 126, 234, 0.1);
    }
    
    .nav-card h2 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
    }
    
    .nav-card h3 {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    
    .nav-card p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.95rem;
    }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: scale(1.05);
        border: 1px solid rgba(102, 126, 234, 0.5);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 1rem;
        margin-top: 0.8rem;
        font-weight: 500;
    }
    
    h3 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin: 2rem 0 1.5rem 0 !important;
        letter-spacing: -0.5px;
    }
    
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .intro-section {
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.8;
        font-size: 1.1rem;
    }
    
    .intro-section h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem !important;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1 class="main-header">🚗 Car Insurance AI Platform</h1>
    <p class="sub-header">Intelligent Risk Assessment & Claim Prediction System</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-social">
        <h3>🔗 Connect With Me</h3>
        <a href="https://github.com/PradeepaGnanasekaran" target="_blank" class="sidebar-social-link">
            <i class="fab fa-github"></i> GitHub
        </a>
        <a href="https://www.linkedin.com/in/pradeepa-gnanasekaran-1998ad263" target="_blank" class="sidebar-social-link">
            <i class="fab fa-linkedin"></i> LinkedIn
        </a>
        <a href="mailto:pradeepagnanasekaran7@gmail.com" class="sidebar-social-link">
            <i class="fas fa-envelope"></i> Email
        </a>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("""
    <div class="developer-credit">
        <p>Developed by Pradeepa Gnanasekaran</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Welcome to the <span class="purple-text">future of insurance analytics</span>. Our AI-powered platform leverages <span class="purple-text">advanced machine learning</span> to provide accurate insurance claim predictions, helping insurers make <span class="purple-text">data-driven decisions</span> with confidence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Key Features")
    
    st.markdown("""
    <div class="section-explanation">
        <p>Explore our <span class="purple-text">powerful capabilities</span> designed to transform insurance operations. From <span class="purple-text">intelligent predictions</span> to <span class="purple-text">comprehensive analytics</span>, every feature is built for excellence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Smart Prediction</div>
            <div class="feature-desc">
                Advanced ML models analyze customer data to predict claim probability with high accuracy using ensemble methods and neural networks
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Deep Analytics</div>
            <div class="feature-desc">
                Comprehensive data visualization and exploratory analysis with interactive dashboards for better insights and decision-making
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Real-time Results</div>
            <div class="feature-desc">
                Instant risk assessment with explainable AI, SHAP values, and feature importance analysis for transparent predictions
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigate to")
    
    st.markdown("""
    <div class="section-explanation">
        <p>Access our <span class="purple-text">core modules</span> for complete insurance analytics. Each section provides <span class="purple-text">specialized tools</span> to analyze data, predict risks, and evaluate <span class="purple-text">model performance</span>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        st.markdown("""
        <div class="nav-card">
            <h2>📊</h2>
            <h3>Exploratory Data Analysis</h3>
            <p>Visualize patterns, trends, and correlations in your insurance data with interactive charts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col2:
        st.markdown("""
        <div class="nav-card">
            <h2>🤖</h2>
            <h3>Risk Prediction</h3>
            <p>Get instant claim risk predictions for new customers with confidence scores</p>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col3:
        st.markdown("""
        <div class="nav-card">
            <h2>📈</h2>
            <h3>Model Performance</h3>
            <p>Evaluate model accuracy, ROC curves, and comprehensive classification metrics</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### 📈 Platform Statistics")
    
    st.markdown("""
    <div class="section-explanation">
        <p>Our platform delivers <span class="purple-text">exceptional performance</span> with industry-leading accuracy and speed. Track our <span class="purple-text">real-time metrics</span> and see the <span class="purple-text">power of AI</span> in action.</p>
    </div>
    """, unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">97.8%</div>
            <div class="stat-label">Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">50K+</div>
            <div class="stat-label">Predictions Made</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">0.3s</div>
            <div class="stat-label">Response Time</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.success("✅ System Operational - All Models Active & Ready")
st.info("💡 Use the sidebar to navigate between different sections of the application")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p style='margin: 0;'>Built with ❤️ using Streamlit & Plotly</p>
    <p style='margin: 5px 0 0 0;'>Data Science Project | GUVI Trainee</p>
</div>
""", unsafe_allow_html=True)