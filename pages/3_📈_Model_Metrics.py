import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

st.set_page_config(page_title="Model Metrics", layout="wide", page_icon="📈")

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
    
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(102, 126, 234, 0.5);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 500;
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
    
    .chart-container h4 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
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
    
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1 class="main-title">📈 Model Performance Dashboard</h1>
    <p class="main-subtitle">Advanced Analytics & Comprehensive Model Evaluation</p>
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

try:
    with st.spinner("🔄 Loading model and evaluating performance..."):
        model = joblib.load("models/model.pkl")
        df = pd.read_csv("data/raw/train.csv")
        
        df_numeric = df.select_dtypes(include=["int64", "float64"])
        X = df_numeric.drop("is_claim", axis=1)
        y = df_numeric["is_claim"]
        
        y_pred = model.predict(X)
        y_prob = model.predict_proba(X)[:, 1]
    
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    
    st.markdown('<h2 class="section-header">🎯 Key Performance Metrics</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Evaluate the model's <span class="purple-text">overall performance</span> using critical metrics. <span class="purple-text">Accuracy</span> shows correct predictions, <span class="purple-text">Precision</span> measures positive prediction accuracy, <span class="purple-text">Recall</span> captures actual positive identification, and <span class="purple-text">F1 Score</span> balances precision and recall.</p>
    </div>
    """, unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{accuracy*100:.2f}%</div><div class="metric-label">📊 Accuracy</div></div>', unsafe_allow_html=True)
    with metric_col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{precision*100:.2f}%</div><div class="metric-label">🎯 Precision</div></div>', unsafe_allow_html=True)
    with metric_col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{recall*100:.2f}%</div><div class="metric-label">🔍 Recall</div></div>', unsafe_allow_html=True)
    with metric_col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{f1*100:.2f}%</div><div class="metric-label">⚖️ F1 Score</div></div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">📊 Detailed Classification Report</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Comprehensive breakdown of <span class="purple-text">class-wise performance</span> metrics. Review <span class="purple-text">precision, recall, and F1 scores</span> for each class to understand model behavior across different prediction scenarios.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    report = classification_report(y, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose().round(3)
    st.dataframe(report_df.style.background_gradient(cmap='RdYlGn', subset=['precision', 'recall', 'f1-score']), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🎲 Confusion Matrix & ROC Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Visualize <span class="purple-text">prediction accuracy</span> with confusion matrix showing true/false positives and negatives. The <span class="purple-text">ROC curve</span> illustrates the trade-off between true positive and false positive rates across different thresholds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Confusion Matrix")
        
        cm = confusion_matrix(y, y_pred)
        fig = go.Figure(data=go.Heatmap(z=cm, x=['Predicted No Claim', 'Predicted Claim'], y=['Actual No Claim', 'Actual Claim'], text=cm, texttemplate='%{text}', textfont={"size": 20, "color": "white"}, colorscale='Viridis', showscale=True))
        fig.update_layout(title="Confusion Matrix", height=450, xaxis_title="Predicted Label", yaxis_title="True Label", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
        
        tn, fp, fn, tp = cm.ravel()
        cm_col1, cm_col2 = st.columns(2)
        with cm_col1:
            st.metric("True Positives", f"{tp:,}")
            st.metric("False Positives", f"{fp:,}")
        with cm_col2:
            st.metric("True Negatives", f"{tn:,}")
            st.metric("False Negatives", f"{fn:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### ROC Curve")
        
        fpr, tpr, thresholds = roc_curve(y, y_prob)
        roc_auc = auc(fpr, tpr)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'ROC Curve (AUC = {roc_auc:.3f})', line=dict(color='#667eea', width=3)))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random Classifier', line=dict(color='gray', width=2, dash='dash')))
        fig.update_layout(title=f"ROC Curve (AUC = {roc_auc:.3f})", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", height=450, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("AUC Score", f"{roc_auc:.4f}")
        if roc_auc >= 0.9:
            st.success("🌟 Excellent model performance!")
        elif roc_auc >= 0.8:
            st.info("✅ Good model performance")
        else:
            st.warning("⚠️ Model could be improved")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">📉 Precision-Recall Curve</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Analyze the <span class="purple-text">precision-recall trade-off</span> across different classification thresholds. The <span class="purple-text">Average Precision</span> score summarizes the curve as a weighted mean of precisions at each threshold.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    precision_vals, recall_vals, pr_thresholds = precision_recall_curve(y, y_prob)
    avg_precision = average_precision_score(y, y_prob)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recall_vals, y=precision_vals, mode='lines', name=f'PR Curve (AP = {avg_precision:.3f})', line=dict(color='#764ba2', width=3), fill='tozeroy', fillcolor='rgba(118, 75, 162, 0.2)'))
    fig.update_layout(title=f"Precision-Recall Curve (Average Precision = {avg_precision:.3f})", xaxis_title="Recall", yaxis_title="Precision", height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🔥 Feature Importance Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Discover which features have the <span class="purple-text">strongest influence</span> on model predictions. <span class="purple-text">Feature importance</span> helps identify key drivers of insurance claims and guides feature engineering efforts.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    try:
        importances = model.named_steps["model"].feature_importances_
        feature_names = X.columns
        
        feat_df = pd.DataFrame({"Feature": feature_names, "Importance": importances}).sort_values(by="Importance", ascending=False)
        top_features = feat_df.head(20)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=top_features['Importance'], y=top_features['Feature'], orientation='h', marker=dict(color=top_features['Importance'], colorscale='Viridis', showscale=True, colorbar=dict(title="Importance")), text=top_features['Importance'].round(4), textposition='auto'))
        fig.update_layout(title="Top 20 Most Important Features", xaxis_title="Feature Importance", yaxis_title="Feature", height=700, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 Complete Feature Importance Table")
        feat_df_display = feat_df.copy()
        feat_df_display['Importance'] = feat_df_display['Importance'].round(6)
        feat_df_display['Rank'] = range(1, len(feat_df_display) + 1)
        st.dataframe(feat_df_display[['Rank', 'Feature', 'Importance']], use_container_width=True, height=400)
    except AttributeError:
        st.warning("⚠️ Feature importance not available for this model type")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">📊 Prediction Score Distribution</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Examine how <span class="purple-text">prediction probabilities</span> are distributed across actual claim and non-claim cases. Well-separated distributions indicate <span class="purple-text">strong model discrimination</span> capability.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=y_prob[y == 1], name='Actual Claims', marker_color='#ef4444', opacity=0.7, nbinsx=50))
    fig.add_trace(go.Histogram(x=y_prob[y == 0], name='No Claims', marker_color='#10b981', opacity=0.7, nbinsx=50))
    fig.update_layout(title="Distribution of Prediction Scores by Actual Class", xaxis_title="Predicted Probability", yaxis_title="Frequency", height=500, barmode='overlay', showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">📝 Model Summary</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-explanation">
        <p>Review <span class="purple-text">comprehensive model information</span> and overall <span class="purple-text">performance assessment</span>. This summary helps determine model readiness for production deployment.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.markdown("### Model Information")
        st.write(f"**Model Type:** {type(model.named_steps['model']).__name__}")
        st.write(f"**Number of Features:** {X.shape[1]}")
        st.write(f"**Training Samples:** {X.shape[0]:,}")
        st.write(f"**Positive Class Rate:** {(y.sum() / len(y) * 100):.2f}%")
    with summary_col2:
        st.markdown("### Performance Summary")
        fpr, tpr, _ = roc_curve(y, y_prob)
        roc_auc = auc(fpr, tpr)
        if accuracy >= 0.9 and roc_auc >= 0.9:
            st.success("🌟 **Excellent Performance** - Model is production-ready")
        elif accuracy >= 0.8 and roc_auc >= 0.8:
            st.info("✅ **Good Performance** - Model performs well")
        else:
            st.warning("⚠️ **Moderate Performance** - Consider model improvement")
        st.write(f"**Overall Accuracy:** {accuracy*100:.2f}%")
        st.write(f"**ROC AUC Score:** {roc_auc:.4f}")
        st.write(f"**Average Precision:** {avg_precision:.4f}")
    st.markdown('</div>', unsafe_allow_html=True)

except FileNotFoundError as e:
    st.error(f"❌ Required file not found: {str(e)}")
    st.info("Please ensure 'models/model.pkl' and 'data/raw/train.csv' exist.")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.exception(e)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p style='margin: 0;'>Built with ❤️ using Streamlit & Plotly</p>
    <p style='margin: 5px 0 0 0;'>Data Science Project | GUVI Trainee</p>
</div>
""", unsafe_allow_html=True)