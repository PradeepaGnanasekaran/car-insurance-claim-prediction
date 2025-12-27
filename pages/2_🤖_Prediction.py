import streamlit as st
import pandas as pd
import joblib
import shap
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Prediction", layout="wide", page_icon="🚗")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #000000; }
    
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #8b5cf6 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem auto 2rem auto;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .main-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .section-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        font-weight: 700;
        font-size: 1.5rem;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    .stSuccess, .stInfo, .stWarning, .stError {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    h3 {
        color: white !important;
        font-weight: 700 !important;
    }
    
    .stMarkdown {
        color: rgba(255, 255, 255, 0.85);
    }
    
    p, li, span {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.05rem;
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
    
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    label {
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 0.8rem 3rem !important;
        border-radius: 50px !important;
        border: none !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.7) !important;
    }
    
    .risk-badge {
        display: inline-block;
        padding: 1.2rem 2.5rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: 800;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ffaa00 0%, #ff8800 100%);
        color: white;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #00cc66 0%, #009944 100%);
        color: white;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1 class="main-title">🚗 Insurance Claim Risk Prediction</h1>
    <p class="main-subtitle">AI-Powered Risk Assessment for Smarter Insurance Decisions</p>
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

model = joblib.load("models/model.pkl")
df_template = pd.read_csv("data/raw/train.csv")
df_template = df_template.select_dtypes(include=["int64", "float64"])
df_template = df_template.drop(columns=["is_claim"])

st.markdown('<h2 class="section-header">📋 Customer Information Input</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="section-explanation">
    <p>Enter <span class="purple-text">customer details</span> to assess their insurance claim risk. Our AI model analyzes <span class="purple-text">multiple factors</span> to provide accurate <span class="purple-text">risk predictions</span> and actionable insights.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
input_data = {}
cols = st.columns(3)

for i, col in enumerate(df_template.columns):
    with cols[i % 3]:
        input_data[col] = st.number_input(
            label=col.replace("_", " ").title(),
            value=float(df_template[col].mean()),
            key=f"input_{col}"
        )

input_df = pd.DataFrame([input_data])
st.markdown('</div>', unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns([2, 4, 2])
with button_col2:
    predict_button = st.button("🔍 Analyze Risk Profile")

if predict_button:
    prob = model.predict_proba(input_df)[0][1]
    
    st.markdown('<h2 class="section-header">📊 Risk Assessment Results</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Review the <span class="purple-text">AI-generated risk score</span> and classification. The gauge shows <span class="purple-text">claim probability</span> from 0-100%, with color-coded risk zones for <span class="purple-text">quick decision-making</span>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prob * 100,
        title={'text': "Claim Probability (%)", 'font': {'size': 24, 'color': '#ffffff'}},
        delta={'reference': 25, 'increasing': {'color': "#ff4444"}},
        number={'suffix': "%", 'font': {'size': 40, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#666"},
            'bar': {'color': "#667eea", 'thickness': 0.75},
            'bgcolor': "rgba(255, 255, 255, 0.03)",
            'borderwidth': 2,
            'bordercolor': "rgba(102, 126, 234, 0.3)",
            'steps': [
                {'range': [0, 20], 'color': "#004d00"},
                {'range': [20, 40], 'color': "#1a5c00"},
                {'range': [40, 60], 'color': "#806600"},
                {'range': [60, 80], 'color': "#cc4400"},
                {'range': [80, 100], 'color': "#990000"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': prob * 100
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font={'color': "#ffffff", 'family': "Inter"},
        height=400,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if prob >= 0.35:
        st.markdown(f'<div style="text-align: center;"><span class="risk-badge risk-high">🚨 HIGH RISK — {round(prob*100, 2)}%</span></div>', unsafe_allow_html=True)
        st.error("⚠️ This profile shows elevated risk indicators. Further review recommended.")
    elif prob >= 0.18:
        st.markdown(f'<div style="text-align: center;"><span class="risk-badge risk-medium">⚠️ MEDIUM RISK — {round(prob*100, 2)}%</span></div>', unsafe_allow_html=True)
        st.warning("📊 This profile shows moderate risk levels. Standard procedures apply.")
    else:
        st.markdown(f'<div style="text-align: center;"><span class="risk-badge risk-low">✅ LOW RISK — {round(prob*100, 2)}%</span></div>', unsafe_allow_html=True)
        st.success("🎉 This profile shows low risk indicators. Proceed with confidence.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🔍 Feature Impact Analysis (SHAP)</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Understand <span class="purple-text">which factors drive the prediction</span>. SHAP values show the <span class="purple-text">contribution of each feature</span> to the risk score. Red bars <span class="purple-text">increase risk</span>, green bars <span class="purple-text">decrease risk</span>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    explainer = shap.TreeExplainer(model.named_steps["model"])
    shap_values = explainer.shap_values(input_df)
    
    if isinstance(shap_values, list):
        shap_vals = shap_values[0]
    else:
        shap_vals = shap_values
    
    shap_df = pd.DataFrame({
        "Feature": [col.replace("_", " ").title() for col in input_df.columns],
        "Impact Score": shap_vals[0]
    }).sort_values(by="Impact Score", key=abs, ascending=False)
    
    fig_impact = go.Figure()
    colors = ['#ff4444' if x > 0 else '#00cc66' for x in shap_df.head(10)["Impact Score"]]
    
    fig_impact.add_trace(go.Bar(
        y=shap_df.head(10)["Feature"],
        x=shap_df.head(10)["Impact Score"],
        orientation='h',
        marker=dict(color=colors),
        text=shap_df.head(10)["Impact Score"].round(4),
        textposition='auto',
    ))
    
    fig_impact.update_layout(
        title="Top 10 Feature Impacts",
        xaxis_title="SHAP Value",
        yaxis_title="Feature",
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font={'color': "#ffffff", 'family': "Inter"},
        height=500,
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig_impact, use_container_width=True)
    st.dataframe(shap_df.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    os.makedirs("predictions", exist_ok=True)
    save_df = input_df.copy()
    save_df["risk_score"] = prob
    save_path = "predictions/predictions_log.csv"
    save_df.to_csv(save_path, mode="a", header=not os.path.exists(save_path), index=False)
    st.success("✅ Prediction saved successfully to database!")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p style='margin: 0;'>Built with ❤️ using Streamlit & Plotly</p>
    <p style='margin: 5px 0 0 0;'>Data Science Project | GUVI Trainee</p>
</div>
""", unsafe_allow_html=True)