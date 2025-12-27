import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EDA Dashboard", layout="wide", page_icon="📊")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #000000; }
    .header-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #8b5cf6 100%); padding: 2.5rem 2rem; border-radius: 20px; text-align: center; margin: 1rem auto 2rem auto; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); }
    .main-title { color: white; font-size: 3rem; font-weight: 800; margin: 0; letter-spacing: -1px; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); }
    .main-subtitle { color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; margin-top: 0.5rem; font-weight: 400; }
    .section-header { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1.2rem; border-radius: 12px; color: white; font-weight: 700; font-size: 1.5rem; margin: 2rem 0 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 1px solid rgba(102, 126, 234, 0.3); }
    .metric-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); text-align: center; transition: all 0.3s ease; border: 1px solid rgba(102, 126, 234, 0.2); height: 100%; }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); border: 1px solid rgba(102, 126, 234, 0.5); }
    .metric-value { font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .metric-label { color: rgba(255, 255, 255, 0.7); font-size: 1rem; margin-top: 0.5rem; font-weight: 500; }
    .chart-container { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); padding: 2rem; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.08); }
    .chart-container h4 { color: white; font-weight: 600; margin-bottom: 1rem; }
    [data-testid="stDataFrame"] { background: rgba(255, 255, 255, 0.05); border-radius: 10px; }
    .stSelectbox label, .stMultiselect label { color: white !important; font-weight: 600; }
    .stSuccess, .stInfo, .stWarning, .stError { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 10px !important; color: white !important; }
    h3 { color: white !important; font-weight: 700 !important; }
    .stMarkdown { color: rgba(255, 255, 255, 0.85); }
    p, li, span { color: rgba(255, 255, 255, 0.85); font-size: 1.05rem; }
    [data-testid="stSidebar"] { background: #000000; }
    .sidebar-social { padding: 1.5rem 1rem; margin-top: 2rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); }
    .sidebar-social h3 { color: white !important; font-size: 1.1rem !important; margin-bottom: 1rem !important; text-align: center; }
    .sidebar-social-link { display: block; margin: 10px 0; padding: 12px 20px; background: rgba(102, 126, 234, 0.1); border: 2px solid rgba(102, 126, 234, 0.3); border-radius: 8px; color: #667eea; text-decoration: none; font-weight: 600; transition: all 0.3s ease; text-align: center; }
    .sidebar-social-link:hover { background: rgba(102, 126, 234, 0.2); border-color: #667eea; transform: translateX(5px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); color: white; text-decoration: none; }
    .sidebar-social-link i { margin-right: 8px; }
    .section-explanation { background: rgba(102, 126, 234, 0.1); border: 2px solid rgba(102, 126, 234, 0.4); border-radius: 12px; padding: 1.2rem; margin: 1rem 0 1.5rem 0; box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); animation: glow-box 2s ease-in-out infinite alternate; }
    @keyframes glow-box { from { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); border-color: rgba(102, 126, 234, 0.4); } to { box-shadow: 0 0 30px rgba(102, 126, 234, 0.6); border-color: rgba(102, 126, 234, 0.7); } }
    .section-explanation p { color: white; font-size: 1.05rem; line-height: 1.7; margin: 0; font-weight: 400; }
    .purple-text { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700; }
    .insights-container { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); padding: 2rem; border-radius: 15px; border: 1px solid rgba(102, 126, 234, 0.2); margin: 1rem 0; }
    .insight-column { color: rgba(255, 255, 255, 0.85); line-height: 2; }
    .insight-column h3 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 1.5rem !important; margin-bottom: 1.5rem !important; font-weight: 700 !important; }
    .insight-column ul { list-style: none; padding: 0; }
    .insight-column li { padding: 0.5rem 0; font-size: 1.05rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
    .insight-column li:last-child { border-bottom: none; }
    .insight-column strong { color: #667eea; font-weight: 600; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1 class="main-title">📊 Exploratory Data Analysis Dashboard</h1>
    <p class="main-subtitle">Explore 400K+ financial records with interactive visualizations</p>
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
    df = pd.read_csv("data/raw/train.csv")
    
    st.markdown('<h2 class="section-header">📋 Dataset Overview</h2>', unsafe_allow_html=True)
    met_col1, met_col2, met_col3, met_col4 = st.columns(4)
    with met_col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df):,}</div><div class="metric-label">📊 Total Records</div></div>', unsafe_allow_html=True)
    with met_col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df.columns)}</div><div class="metric-label">🎯 Features</div></div>', unsafe_allow_html=True)
    with met_col3:
        claim_rate = (df['is_claim'].sum() / len(df) * 100)
        st.markdown(f'<div class="metric-card"><div class="metric-value">{claim_rate:.1f}%</div><div class="metric-label">💰 Claim Rate</div></div>', unsafe_allow_html=True)
    with met_col4:
        missing = df.isnull().sum().sum()
        st.markdown(f'<div class="metric-card"><div class="metric-value">{missing}</div><div class="metric-label">🔍 Missing Values</div></div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🔍 Data Snapshot & Target Distribution</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-explanation"><p>Get a <span class="purple-text">quick overview</span> of your dataset with sample records and visualize the <span class="purple-text">distribution of insurance claims</span>. This helps identify <span class="purple-text">class imbalance</span> and understand the target variable\'s behavior.</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="chart-container"><h4>📄 Dataset Preview</h4>', unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-container"><h4>🎯 Claim Distribution</h4>', unsafe_allow_html=True)
        claim_counts = df['is_claim'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=['No Claim', 'Claim'], values=claim_counts.values, hole=0.4, marker=dict(colors=['#10b981', '#ef4444']), textfont=dict(size=16, color='white'))])
        fig.update_layout(height=350, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), legend=dict(font=dict(color='white')))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🎨 Categorical Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-explanation"><p>Explore <span class="purple-text">categorical features</span> and their relationship with insurance claims. Analyze the <span class="purple-text">distribution patterns</span> and discover which categories have <span class="purple-text">higher claim rates</span>.</p></div>', unsafe_allow_html=True)
    
    cat_columns = df.select_dtypes(include=['object']).columns.tolist()
    if cat_columns:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        selected_cat = st.selectbox("Select categorical feature", cat_columns)
        if selected_cat:
            cat_col1, cat_col2 = st.columns(2)
            with cat_col1:
                cat_counts = df[selected_cat].value_counts().head(10)
                fig = px.bar(x=cat_counts.index, y=cat_counts.values, title=f'Distribution of {selected_cat}', labels={'x': selected_cat, 'y': 'Count'}, color=cat_counts.values, color_continuous_scale='Viridis')
                fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
                st.plotly_chart(fig, use_container_width=True)
            with cat_col2:
                claim_by_cat = df.groupby(selected_cat)['is_claim'].mean().sort_values(ascending=False).head(10)
                fig = px.bar(x=claim_by_cat.index, y=claim_by_cat.values * 100, title=f'Claim Rate by {selected_cat}', labels={'x': selected_cat, 'y': 'Claim Rate (%)'}, color=claim_by_cat.values, color_continuous_scale='Reds')
                fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No categorical features found in the dataset")
    
    st.markdown('<h2 class="section-header">📈 Statistical Summary</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-explanation"><p>Dive into <span class="purple-text">descriptive statistics</span> of numerical features including <span class="purple-text">mean, median, standard deviation</span>, and quartiles. Understand the <span class="purple-text">data distribution</span> and identify potential outliers.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    summary_col1, summary_col2 = st.columns(2)
    with summary_col1:
        st.markdown("#### Numerical Features Statistics")
        numeric_summary = df.select_dtypes(include=['int64', 'float64']).describe()
        st.dataframe(numeric_summary, use_container_width=True, height=400)
    with summary_col2:
        st.markdown("#### Data Types Distribution")
        dtype_counts = df.dtypes.value_counts()
        fig = px.pie(values=dtype_counts.values, names=dtype_counts.index.astype(str), title="Column Data Types", hole=0.4)
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), legend=dict(font=dict(color='white')))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🔥 Feature Correlation Matrix</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-explanation"><p>Visualize <span class="purple-text">relationships between features</span> using correlation coefficients. Identify <span class="purple-text">highly correlated variables</span> and discover which features have the <span class="purple-text">strongest impact on claims</span>.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    if 'is_claim' in numeric_df.columns:
        target_corr = numeric_df.corr()['is_claim'].drop('is_claim').sort_values(ascending=False)
        corr_col1, corr_col2 = st.columns([1, 2])
        with corr_col1:
            st.markdown("#### Top Correlations with Target")
            top_pos = target_corr.head(10)
            fig = go.Figure()
            fig.add_trace(go.Bar(y=top_pos.index, x=top_pos.values, orientation='h', name='Positive', marker_color='#667eea'))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
            st.plotly_chart(fig, use_container_width=True)
        with corr_col2:
            st.markdown("#### Full Correlation Matrix")
            corr_matrix = numeric_df.corr()
            fig = go.Figure(data=go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns, colorscale='RdBu', zmid=0, text=corr_matrix.values.round(2), texttemplate='%{text}', textfont={"size": 7, "color": "white"}, colorbar=dict(title=dict(text="Correlation", font=dict(color='white')), tickfont=dict(color='white'))))
            fig.update_layout(height=500, xaxis_tickangle=-45, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">📊 Feature Distributions</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-explanation"><p>Examine the <span class="purple-text">distribution shapes</span> of numerical features with interactive histograms. Compare <span class="purple-text">claim vs non-claim distributions</span> and detect <span class="purple-text">skewness and outliers</span>.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    numeric_cols = numeric_df.columns.tolist()
    if 'is_claim' in numeric_cols:
        numeric_cols.remove('is_claim')
    st.markdown("#### Select Features to Visualize")
    selected_features = st.multiselect("Choose up to 6 features", numeric_cols, default=numeric_cols[:4] if len(numeric_cols) >= 4 else numeric_cols, max_selections=6)
    if selected_features:
        for i in range(0, len(selected_features), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(selected_features):
                    feature = selected_features[i + j]
                    with col:
                        fig = px.histogram(df, x=feature, color='is_claim', marginal='box', title=f'Distribution of {feature}', color_discrete_map={0: '#10b981', 1: '#ef4444'}, labels={'is_claim': 'Claim Status'}, nbins=50)
                        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), legend=dict(font=dict(color='white')))
                        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">📦 Distribution Comparison (Claim vs No Claim)</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-explanation"><p>Compare feature distributions between <span class="purple-text">claim and non-claim groups</span> using box plots. Identify <span class="purple-text">significant differences</span> in median values and spot <span class="purple-text">potential discriminating features</span>.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    if len(numeric_cols) > 0:
        selected_box_features = st.multiselect("Select features for box plot comparison", numeric_cols, default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols)
        if selected_box_features:
            for feature in selected_box_features:
                fig = px.box(df, x='is_claim', y=feature, color='is_claim', title=f'{feature} Distribution by Claim Status', color_discrete_map={0: '#10b981', 1: '#ef4444'}, labels={'is_claim': 'Claim Status'})
                fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), legend=dict(font=dict(color='white')))
                st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🔍 Data Quality Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    qual_col1, qual_col2 = st.columns(2)
    with qual_col1:
        st.markdown("#### Missing Values")
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        if len(missing_data) > 0:
            fig = px.bar(x=missing_data.values, y=missing_data.index, orientation='h', title='Missing Values by Feature', labels={'x': 'Count', 'y': 'Feature'}, color=missing_data.values, color_continuous_scale='Reds')
            fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'), yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No missing values found!")
    with qual_col2:
        st.markdown("#### Duplicate Records")
        duplicates = df.duplicated().sum()
        fig = go.Figure(go.Indicator(mode="number+delta", value=duplicates, title={'text': "Duplicate Rows", 'font': {'color': 'white'}}, delta={'reference': 0, 'increasing': {'color': "red"}}, domain={'x': [0, 1], 'y': [0, 1]}, number={'font': {'color': '#667eea', 'size': 60}}))
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
        if duplicates > 0:
            st.warning(f"⚠️ Found {duplicates} duplicate records")
        else:
            st.success("✅ No duplicate records found!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">💡 Key Insights</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-explanation"><p>Summarize <span class="purple-text">critical findings</span> from the exploratory analysis. Review <span class="purple-text">dataset characteristics</span>, assess <span class="purple-text">data quality</span>, and understand <span class="purple-text">target variable behavior</span> to guide modeling decisions.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="insights-container">', unsafe_allow_html=True)
    insight_col1, insight_col2 = st.columns(2)
    with insight_col1:
        st.markdown(f'<div class="insight-column"><h3>📊 Dataset Characteristics</h3><ul><li><strong>Total Samples:</strong> {len(df):,}</li><li><strong>Total Features:</strong> {len(df.columns)}</li><li><strong>Numeric Features:</strong> {len(df.select_dtypes(include=["int64", "float64"]).columns)}</li><li><strong>Categorical Features:</strong> {len(df.select_dtypes(include=["object"]).columns)}</li><li><strong>Missing Values:</strong> {df.isnull().sum().sum()}</li><li><strong>Duplicate Rows:</strong> {df.duplicated().sum()}</li></ul></div>', unsafe_allow_html=True)
    with insight_col2:
        claim_count = df['is_claim'].sum()
        no_claim_count = len(df) - claim_count
        balance_status = '⚖️ Balanced' if 40 <= claim_rate <= 60 else '⚠️ Imbalanced'
        st.markdown(f'<div class="insight-column"><h3>🎯 Target Variable Analysis</h3><ul><li><strong>Total Claims:</strong> {claim_count:,} ({claim_rate:.2f}%)</li><li><strong>No Claims:</strong> {no_claim_count:,} ({100-claim_rate:.2f}%)</li><li><strong>Class Balance:</strong> {balance_status}</li></ul></div>', unsafe_allow_html=True)
        if claim_rate < 40 or claim_rate > 60:
            st.warning("⚠️ Dataset shows class imbalance. Consider using resampling techniques or adjusting class weights.")
    st.markdown('</div>', unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Data file not found. Please ensure 'data/raw/train.csv' exists.")
    st.info("Expected path: data/raw/train.csv")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.exception(e)
# ===============================
# FOOTER
# ===============================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p style='margin: 0;'>Built with ❤️ using Streamlit & Plotly</p>
    <p style='margin: 5px 0 0 0;'>Data Science Project | GUVI Trainee</p>
</div>
""", unsafe_allow_html=True)