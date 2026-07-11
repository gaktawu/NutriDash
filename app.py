# =============================================================================
# NUTRIDASH - Indonesian Food Nutrition Analytics Dashboard
# Professional-grade Streamlit dashboard for nutrition data analysis
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os
import io

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="NutriDash - Indonesian Nutrition Analytics",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# DESIGN SYSTEM - Warm Professional Palette
# =============================================================================
COLORS = {
    "navy": "#1a2332",
    "navy_light": "#243447",
    "cream": "#f8f6f1",
    "cream_dark": "#efebde",
    "gold": "#c9a84c",
    "gold_light": "#dbc070",
    "text": "#2c3e50",
    "text_light": "#5d6d7e",
    "text_muted": "#95a5a6",
    "white": "#ffffff",
    "success": "#27ae60",
    "warning": "#e67e22",
    "danger": "#c0392b",
    "info": "#2980b9",
    "card_bg": "#ffffff",
    "border": "#e0dcd3",
    "sidebar_bg": "#1a2332",
}

CATEGORY_PALETTE = [
    "#c9a84c", "#1a2332", "#27ae60", "#e67e22", "#8e44ad",
    "#2980b9", "#c0392b", "#16a085", "#d35400", "#2c3e50",
    "#7f8c8d", "#27ae60", "#8e44ad", "#c9a84c", "#2980b9",
]

# =============================================================================
# CUSTOM CSS - Professional Typography & Layout
# =============================================================================
# PERBAIKAN: Menghapus CSS agresif seperti [class*="css"] dan selector * # agar tidak merusak layout icon Plotly dan icon full-screen bawaan Streamlit
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background-color: {COLORS['cream']};
        color: {COLORS['text']};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['sidebar_bg']};
        border-right: none;
    }}
    /* Hanya targetkan tulisan Markdown di sidebar, jangan elemen Selectbox/Input */
    [data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS['white']} !important;
    }}

    /* Typography */
    h1 {{
        font-weight: 800 !important;
        font-size: 2rem !important;
        letter-spacing: -0.02em !important;
        color: {COLORS['navy']} !important;
        margin-bottom: 0.25rem !important;
    }}
    h2 {{
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        letter-spacing: -0.01em !important;
        color: {COLORS['navy']} !important;
        margin-top: 1.5rem !important;
    }}
    h3 {{
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        color: {COLORS['text']} !important;
    }}

    /* KPI Cards */
    .kpi-container {{
        background: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}
    .kpi-container:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-1px);
    }}
    .kpi-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {COLORS['text_muted']};
        margin-bottom: 0.5rem;
    }}
    .kpi-value {{
        font-size: 2rem;
        font-weight: 800;
        color: {COLORS['navy']};
        line-height: 1;
    }}
    .kpi-delta {{
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }}
    .kpi-delta.positive {{ color: {COLORS['success']}; }}
    .kpi-delta.negative {{ color: {COLORS['danger']}; }}

    /* Tables */
    .data-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
    }}
    .data-table thead th {{
        background-color: {COLORS['navy']};
        color: {COLORS['white']};
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        padding: 0.75rem 1rem;
        text-align: left;
    }}
    .data-table tbody td {{
        padding: 0.65rem 1rem;
        border-bottom: 1px solid {COLORS['border']};
    }}
    .data-table tbody tr:nth-child(even) {{
        background-color: {COLORS['cream']};
    }}

    /* Food Cards */
    .food-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }}
    .food-card {{
        background: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 1rem;
        transition: all 0.2s ease;
    }}
    .food-card:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: {COLORS['gold']};
    }}
    .food-category-badge {{
        display: inline-block;
        background: {COLORS['cream_dark']};
        color: {COLORS['text_light']};
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }}
    .food-name {{
        font-weight: 700;
        font-size: 0.9rem;
        color: {COLORS['navy']};
        margin-bottom: 0.5rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}
    .food-macro {{
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        padding-top: 0.5rem;
        border-top: 1px solid {COLORS['border']};
    }}
    .food-macro-value {{
        font-weight: 700;
        color: {COLORS['navy']};
    }}

    /* Rank List */
    .rank-item {{
        display: flex;
        align-items: center;
        background: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }}
    .rank-number {{
        font-size: 1.25rem;
        font-weight: 800;
        color: {COLORS['gold']};
        width: 2rem;
    }}
    .rank-info {{ flex: 1; }}
    .rank-name {{
        font-weight: 600;
        font-size: 0.85rem;
        color: {COLORS['navy']};
    }}
    .rank-score {{
        font-weight: 700;
        font-size: 0.9rem;
        color: {COLORS['success']};
    }}

    /* Prediction Result Box */
    .prediction-box {{
        background: linear-gradient(135deg, {COLORS['navy']} 0%, {COLORS['navy_light']} 100%);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: {COLORS['white']};
    }}
    .prediction-value {{
        font-size: 3rem;
        font-weight: 800;
        color: {COLORS['white']};
    }}

    /* Goal Badges */
    .goal-badge {{
        display: inline-flex;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
    }}
    .goal-cutting {{ background: #e8f5e9; color: #27ae60; }}
    .goal-bulking {{ background: #fff3e0; color: #e67e22; }}
    .goal-balanced {{ background: #e3f2fd; color: #2980b9; }}

    /* Streamlit Overrides - Diperhalus agar tidak merusak fungsi tombol bawaan */
    .stButton > button {{
        background-color: {COLORS['navy']} !important;
        color: {COLORS['white']} !important;
        border-radius: 8px !important;
    }}

    .sidebar-metric {{
        background: {COLORS['navy_light']};
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }}
    .sidebar-metric-label {{
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        color: {COLORS['text_muted']};
    }}
    .sidebar-metric-value {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {COLORS['gold_light']};
    }}

    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }}
    .section-header-text {{
        font-weight: 700;
        font-size: 1.1rem;
        color: {COLORS['navy']};
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# PLOTLY DEFAULT LAYOUT
# =============================================================================
PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color=COLORS["text"], size=12),
    paper_bgcolor=COLORS["white"],
    plot_bgcolor=COLORS["cream"],
    margin=dict(t=50, l=10, r=10, b=10),
    title_font=dict(size=14, color=COLORS["navy"], family="Inter, sans-serif"),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=COLORS["border"],
        borderwidth=1,
    ),
    colorway=CATEGORY_PALETTE,
)

# =============================================================================
# DATA LOADING & PREPROCESSING
# =============================================================================
@st.cache_data(show_spinner="Memuat dataset nutrisi...")
def load_and_preprocess_data(file_path):
    df_raw = pd.read_csv(file_path)
    df = df_raw.dropna().copy()
    df = df.drop_duplicates().reset_index(drop=True)

    name_candidates = ["nama", "nama_makanan", "makanan", "menu", "title", "item"]
    name_col = next((col for col in df.columns if col.lower() in name_candidates), None)
    if not name_col:
        name_col = next((col for col in df.columns if df[col].dtype == "object" and col not in ["keyword", "url"]), "keyword")

    df["display_name"] = df[name_col]

    anomalous = ((df["kalori"] > 20) & (df["lemak"] == 0) & (df["karbo"] == 0) & (df["protein"] == 0))
    df = df.loc[~anomalous].reset_index(drop=True)

    numeric_cols = ["kalori", "lemak", "karbo", "protein", "lemak_jenuh", "kolesterol_mg", "sodium_mg", "serat_g", "gula_g"]
    available_numeric = [c for c in numeric_cols if c in df.columns]
    
    if available_numeric:
        has_negative = (df[available_numeric] < 0).any(axis=1)
        df = df.loc[~has_negative].reset_index(drop=True)

    df["protein_per_kalori"] = df["protein"] / (df["kalori"] + 1)
    df["protein_pct"] = (df["protein"] * 4) / (df["kalori"] + 1) * 100

    return df_raw, df

@st.cache_resource(show_spinner="Melatih model regresi...")
def train_model(df):
    # PERBAIKAN: Mencegah KeyError jika dataset CSV tidak memiliki kolom-kolom ini
    NUM_FEATURES = ["kalori", "lemak_jenuh", "gula_g", "serat_g"]
    for col in NUM_FEATURES:
        if col not in df.columns:
            df[col] = 0.0  # Isi dengan nilai default aman jika data tidak tersedia
            
    df_enc = pd.get_dummies(df, columns=["keyword"], prefix="kw", drop_first=True)
    TARGET = "protein"
    dummy_cols = [c for c in df_enc.columns if c.startswith("kw_")]

    X = df_enc[NUM_FEATURES + dummy_cols]
    y = df_enc[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    return model, X.columns, X_test, y_test, y_pred, r2, mae, rmse, df_enc

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def render_kpi_card(label, value, delta=None, delta_pos=True):
    delta_html = ""
    if delta:
        cls = "positive" if delta_pos else "negative"
        icon = "&#9650;" if delta_pos else "&#9660;"
        delta_html = f'<div class="kpi-delta {cls}">{icon} {delta}</div>'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_section_header(icon, text):
    st.markdown(f"""
    <div class="section-header">
        <div class="section-header-icon">{icon}</div>
        <div class="section-header-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def render_food_grid(df, limit=12):
    cards = []
    for i, (_, row) in enumerate(df.head(limit).iterrows()):
        protein_per_cal = row.get("protein_per_kalori", row["protein"] / (row["kalori"] + 1))
        if protein_per_cal > 0.08:
            badge = '<span class="goal-badge goal-cutting">High Protein</span>'
        elif row["kalori"] > 400:
            badge = '<span class="goal-badge goal-bulking">High Calorie</span>'
        else:
            badge = '<span class="goal-badge goal-balanced">Balanced</span>'

        cards.append(f"""
        <div class="food-card">
            <div class="food-category-badge">{row['keyword']}</div>
            <div class="food-name" title="{row['display_name']}">{row['display_name']}</div>
            {badge}
            <div class="food-macro">
                <span><span style="color:{COLORS['text_muted']}">Cal</span> <b>{row['kalori']:.0f}</b></span>
                <span><span style="color:{COLORS['text_muted']}">Pro</span> <b style="color:{COLORS['success']}">{row['protein']:.1f}g</b></span>
                <span><span style="color:{COLORS['text_muted']}">Fat</span> <b>{row['lemak']:.1f}g</b></span>
            </div>
        </div>
        """)
    st.markdown(f'<div class="food-grid">{"" .join(cards)}</div>', unsafe_allow_html=True)

def render_rank_list(df, col, label, top_n=10, ascending=False, unit="g"):
    top = df.nlargest(top_n, col) if not ascending else df.nsmallest(top_n, col)
    rows = []
    for i, (_, row) in enumerate(top.iterrows(), 1):
        rows.append(f"""
        <div class="rank-item">
            <div class="rank-number">{i:02d}</div>
            <div class="rank-info">
                <div class="rank-name" title="{row['display_name']}">{row['display_name']}</div>
                <div style="font-size: 0.75rem; color:{COLORS['text_light']};">{row['keyword']} &middot; {row['kalori']:.0f} kcal</div>
            </div>
            <div class="rank-score">{row[col]:.2f}{unit}</div>
        </div>
        """)
    st.markdown("" .join(rows), unsafe_allow_html=True)

def render_data_table(df, cols, rename_map=None, limit=100):
    display_df = df[cols].head(limit).copy()
    if rename_map:
        display_df = display_df.rename(columns=rename_map)

    headers = "" .join(f"<th>{c}</th>" for c in display_df.columns)
    rows_html = []
    for _, row in display_df.iterrows():
        cells = []
        for col, val in row.items():
            if isinstance(val, (int, float, np.floating, np.integer)):
                cells.append(f'<td class="num" style="text-align:right;">{val:,.1f}</td>')
            else:
                cells.append(f"<td>{val}</td>")
        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    st.markdown(f"""
    <table class="data-table">
        <thead><tr>{headers}</tr></thead>
        <tbody>{'' .join(rows_html)}</tbody>
    </table>
    """, unsafe_allow_html=True)

# =============================================================================
# MAIN APPLICATION
# =============================================================================
path_file = "Data-Nutrisi.csv"

if not os.path.exists(path_file):
    st.error("File `Data-Nutrisi.csv` tidak ditemukan. Pastikan file berada di direktori yang sama dengan app.py")
    st.stop()

df_raw, df = load_and_preprocess_data(path_file)
model, feature_cols, X_test, y_test, y_pred, r2, mae, rmse, df_enc = train_model(df)

# ---- Sidebar ----
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:2rem;">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🥗</div>
        <div style="font-size:1.3rem; font-weight:800; color:{COLORS['white']};">NutriDash</div>
        <div style="font-size:0.75rem; color:{COLORS['text_muted']}; margin-top:0.25rem;">Indonesian Nutrition Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sidebar-metric"><div class="sidebar-metric-label">Total Foods</div><div class="sidebar-metric-value">{df.shape[0]:,}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric"><div class="sidebar-metric-label">Categories</div><div class="sidebar-metric-value">{df["keyword"].nunique()}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric"><div class="sidebar-metric-label">Avg Protein</div><div class="sidebar-metric-value">{df["protein"].mean():.1f}g</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")

    st.markdown("##### ⚙️ Filters")
    selected_categories = st.multiselect("Kategori Makanan:", options=sorted(df["keyword"].unique()), default=[])
    
    # PERBAIKAN: Validasi maximum value slider untuk menghindari crash
    max_cal = int(df["kalori"].max()) if df["kalori"].max() > 0 else 1
    cal_min, cal_max = st.slider("Rentang Kalori:", 0, max_cal, (0, max_cal))
    
    max_pro = float(df["protein"].max()) if df["protein"].max() > 0 else 1.0
    protein_min = st.slider("Protein Minimum (g):", 0.0, max_pro, 0.0, 0.5)

    st.markdown("---")
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download CSV",
        data=csv_buffer.getvalue(),
        file_name="filtered_nutrition_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ---- Apply Filters ----
filtered_df = df.copy()
if selected_categories:
    filtered_df = filtered_df[filtered_df["keyword"].isin(selected_categories)]
filtered_df = filtered_df[
    (filtered_df["kalori"] >= cal_min) &
    (filtered_df["kalori"] <= cal_max) &
    (filtered_df["protein"] >= protein_min)
].reset_index(drop=True)

# ---- Header ----
col_title, col_info = st.columns([3, 1])
with col_title:
    st.title("Indonesian Food Nutrition Analytics")
    st.markdown(f"""
    <p style="color:{COLORS['text_light']}; font-size:0.95rem; margin-top:0.25rem;">
        Eksplorasi <strong>{df.shape[0]:,}</strong> data nutrisi makanan Indonesia dari FatSecret. 
        Analisis protein, prediksi kandungan gizi, dan temukan makanan terbaik.
    </p>
    """, unsafe_allow_html=True)
with col_info:
    if filtered_df.shape[0] != df.shape[0]:
        st.markdown(f"""
        <div style="text-align:right; padding-top:1rem;">
            <div style="font-size:0.75rem; color:{COLORS['text_muted']}; font-weight:600;">Data Terfilter</div>
            <div style="font-size:1.5rem; font-weight:800; color:{COLORS['navy']};">{filtered_df.shape[0]:,}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='border:none; height:1px; background:#e0dcd3; margin:1rem 0;'>", unsafe_allow_html=True)

# ---- KPI Section ----
if not filtered_df.empty:
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1: render_kpi_card("Rata-rata Protein", f"{filtered_df['protein'].mean():.1f}g")
    with kpi2: render_kpi_card("Rata-rata Kalori", f"{filtered_df['kalori'].mean():.0f} kcal")
    with kpi3: render_kpi_card("Protein Tertinggi", f"{filtered_df['protein'].max():.1f}g")
    with kpi4: render_kpi_card("High Protein %", f"{(filtered_df['protein_per_kalori'] > 0.05).mean() * 100:.1f}%")
    with kpi5: render_kpi_card("Kategori", f"{filtered_df['keyword'].nunique()}")

# ---- Main Tabs ----
tab_overview, tab_explorer, tab_viz, tab_model, tab_predict, tab_meal, tab_compare = st.tabs([
    "📊 Overview", "🔍 Data Explorer", "📈 Visualisasi", "🧠 Model Prediksi", 
    "🔮 Kalkulator Protein", "🍽️ Meal Planner", "⚖️ Bandingkan"
])

# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================
with tab_overview:
    if filtered_df.empty:
        st.warning("Tidak ada data yang cocok dengan filter di sidebar.")
    else:
        col_left, col_right = st.columns([2, 1])
        with col_left:
            render_section_header("📈", "Distribusi Protein per Kategori (Top 10)")
            top10_cat = filtered_df["keyword"].value_counts().nlargest(10).index
            cat_protein = filtered_df[filtered_df["keyword"].isin(top10_cat)].groupby("keyword").agg(
                {"protein": "mean", "kalori": "mean"}
            ).reset_index().sort_values("protein", ascending=True)

            fig = go.Figure()
            fig.add_trace(go.Bar(y=cat_protein["keyword"], x=cat_protein["protein"], orientation='h', name='Avg Protein', marker_color=COLORS["gold"], text=cat_protein["protein"].round(1), textposition='outside'))
            fig.add_trace(go.Bar(y=cat_protein["keyword"], x=cat_protein["kalori"]/20, orientation='h', name='Avg Calorie (/20)', marker_color=COLORS["navy"], opacity=0.6))
            fig.update_layout(**PLOTLY_LAYOUT, barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            render_section_header("🏆", "Top 10 Protein Efficiency")
            render_rank_list(filtered_df.nlargest(10, "protein_per_kalori"), "protein_per_kalori", "g/kcal", top_n=10, unit=" g/kcal")

        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("🍽️", "Rekomendasi Berdasarkan Tujuan")
        goal_col1, goal_col2, goal_col3 = st.columns(3)
        with goal_col1:
            st.markdown("#### 🥗 Cutting / Defisit")
            render_food_grid(filtered_df[(filtered_df["kalori"] < 200) & (filtered_df["protein_per_kalori"] > 0.06)].nlargest(6, "protein_per_kalori"), limit=6)
        with goal_col2:
            st.markdown("#### 💪 Bulking / Surplus")
            render_food_grid(filtered_df[(filtered_df["kalori"] > 300) & (filtered_df["protein"] > 15)].nlargest(6, "protein"), limit=6)
        with goal_col3:
            st.markdown("#### ⚖️ Balanced")
            render_food_grid(filtered_df[(filtered_df["kalori"].between(200, 350)) & (filtered_df["protein"].between(8, 25))].nlargest(6, "protein_per_kalori"), limit=6)

# =============================================================================
# TAB 2: DATA EXPLORER
# =============================================================================
with tab_explorer:
    col_search, col_view = st.columns([3, 1])
    with col_search:
        search = st.text_input("Cari nama makanan...", placeholder="Contoh: Ayam, Ikan Bakar...")
    with col_view:
        view_mode = st.radio("Tampilan:", ["Grid", "Tabel"], horizontal=True)

    results = filtered_df[filtered_df["display_name"].str.contains(search, case=False, na=False)] if search else filtered_df
    st.markdown(f"**{results.shape[0]}** makanan ditemukan")

    if results.empty:
        st.info("Tidak ada hasil.")
    elif view_mode == "Grid":
        render_food_grid(results, limit=24)
    else:
        render_data_table(results, cols=["display_name", "keyword", "kalori", "protein", "lemak", "karbo"], limit=50)

# =============================================================================
# TAB 3: VISUALISASI
# =============================================================================
with tab_viz:
    viz1, viz2 = st.columns(2)
    with viz1:
        render_section_header("📈", "Scatter: Kalori vs Protein")
        if not filtered_df.empty:
            fig = px.scatter(filtered_df, x="kalori", y="protein", color="keyword", hover_data=["display_name"], color_discrete_sequence=CATEGORY_PALETTE)
            fig.update_layout(**PLOTLY_LAYOUT, height=420)
            st.plotly_chart(fig, use_container_width=True)
    with viz2:
        render_section_header("🔥", "Heatmap Korelasi")
        corr_cols = [c for c in ["kalori", "lemak", "karbo", "protein", "lemak_jenuh", "serat_g", "gula_g"] if c in filtered_df.columns]
        if len(corr_cols) >= 2:
            fig = px.imshow(filtered_df[corr_cols].corr(), text_auto=".2f", aspect="auto", color_continuous_scale=[COLORS["danger"], COLORS["cream"], COLORS["success"]], zmin=-1, zmax=1)
            fig.update_layout(**PLOTLY_LAYOUT, height=420)
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 4: MODEL PERFORMANCE
# =============================================================================
with tab_model:
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1: render_kpi_card("R² Score", f"{r2:.4f}")
    with col_m2: render_kpi_card("MAE", f"{mae:.2f} g")
    with col_m3: render_kpi_card("RMSE", f"{rmse:.2f} g")

    st.markdown("""
    <div style="background:#e3f2fd; border-left:4px solid #2980b9; padding:1rem; border-radius:0 8px 8px 0; margin:1rem 0;">
        <strong>Interpretasi:</strong> Model Multiple Linear Regression memprediksi kandungan protein berdasarkan kalori, makro, dan kategori.
    </div>
    """, unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig = go.Figure(go.Scatter(x=y_test, y=y_pred, mode='markers', marker=dict(color=COLORS['gold'])))
        fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], mode='lines', line=dict(color=COLORS['danger'], dash='dash')))
        fig.update_layout(**PLOTLY_LAYOUT, height=400, title="Actual vs Predicted Protein (g)")
        st.plotly_chart(fig, use_container_width=True)
    with col_chart2:
        coef_df = pd.DataFrame({"Fitur": feature_cols, "Koefisien": model.coef_})
        cat_coef = coef_df[coef_df["Fitur"].str.startswith("kw_")].copy()
        cat_coef["Kategori"] = cat_coef["Fitur"].str.replace("kw_", "")
        top_bottom = pd.concat([cat_coef.sort_values("Koefisien", ascending=False).head(10), cat_coef.sort_values("Koefisien", ascending=False).tail(10)])
        fig = go.Figure(go.Bar(y=top_bottom["Kategori"], x=top_bottom["Koefisien"], orientation='h'))
        fig.update_layout(**PLOTLY_LAYOUT, height=400, title="Bobot Kategori (Koefisien ML)")
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 5: PREDICTION
# =============================================================================
with tab_predict:
    col_input, col_result = st.columns([2, 1])
    with col_input:
        render_section_header("🎛️", "Parameter Input")
        c1, c2 = st.columns(2)
        with c1:
            in_kalori = st.number_input("Kalori (kcal):", min_value=0.0, value=300.0, step=10.0)
            in_lemak_jenuh = st.number_input("Lemak Jenuh (g):", min_value=0.0, value=2.0, step=0.5)
        with c2:
            in_gula = st.number_input("Gula (g):", min_value=0.0, value=3.0, step=0.5)
            in_serat = st.number_input("Serat (g):", min_value=0.0, value=1.0, step=0.5)
        in_kategori = st.selectbox("Kategori Makanan:", sorted(df["keyword"].unique()))
        predict_btn = st.button("Jalankan Estimasi Protein", use_container_width=True)

    with col_result:
        if predict_btn:
            input_dict = {col: 0.0 for col in feature_cols}
            input_dict["kalori"], input_dict["lemak_jenuh"], input_dict["gula_g"], input_dict["serat_g"] = in_kalori, in_lemak_jenuh, in_gula, in_serat
            if f"kw_{in_kategori}" in input_dict: input_dict[f"kw_{in_kategori}"] = 1.0

            pred_result = max(0.0, model.predict(pd.DataFrame([input_dict])[feature_cols])[0])
            st.markdown(f"""
            <div class="prediction-box">
                <div style="font-size: 0.75rem; color:{COLORS['gold_light']};">ESTIMASI PROTEIN</div>
                <div class="prediction-value">{pred_result:.2f}<span style="font-size: 1rem;"> g</span></div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# TAB 6: MEAL PLANNER
# =============================================================================
with tab_meal:
    render_section_header("🍽️", "Meal Planner & Nutrition Calculator")
    # PERBAIKAN: Menambahkan parameter unsafe_allow_html=True yang terlupa pada baris di bawah ini
    st.markdown(f"""
    <p style="color:{COLORS['text_light']}; font-size:0.9rem; margin-bottom:1rem;">
        Pilih makanan untuk menyusun kombinasi hidangan. Dashboard akan menghitung total nutrisi secara otomatis.
    </p>
    """, unsafe_allow_html=True) 

    meal_categories = st.multiselect("Filter kategori:", options=sorted(filtered_df["keyword"].unique()), default=sorted(filtered_df["keyword"].unique())[:5] if not filtered_df.empty else [])

    if meal_categories and not filtered_df.empty:
        meal_df = filtered_df[filtered_df["keyword"].isin(meal_categories)]
        col_pick1, col_pick2, col_pick3 = st.columns(3)
        with col_pick1: item1 = st.selectbox("Hidangan 1:", [""] + meal_df["display_name"].tolist())
        with col_pick2: item2 = st.selectbox("Hidangan 2:", [""] + meal_df["display_name"].tolist())
        with col_pick3: item3 = st.selectbox("Hidangan 3:", [""] + meal_df["display_name"].tolist())

        selected_items = [i for i in [item1, item2, item3] if i]
        if selected_items:
            totals = meal_df[meal_df["display_name"].isin(selected_items)][["kalori", "protein", "lemak", "karbo"]].sum()
            st.markdown("<hr>", unsafe_allow_html=True)
            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1: render_kpi_card("Total Kalori", f"{totals['kalori']:.0f} kcal")
            with mc2: render_kpi_card("Total Protein", f"{totals['protein']:.1f}g")
            with mc3: render_kpi_card("Total Lemak", f"{totals['lemak']:.1f}g")
            with mc4: render_kpi_card("Total Karbo", f"{totals['karbo']:.1f}g")

            fig = go.Figure(data=[go.Pie(labels=["Lemak", "Karbo", "Protein"], values=[totals["lemak"] * 9, totals["karbo"] * 4, totals["protein"] * 4], hole=0.55, marker_colors=[COLORS["gold"], COLORS["navy"], COLORS["success"]])])
            fig.update_layout(**PLOTLY_LAYOUT, height=300)
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 7: COMPARE
# =============================================================================
with tab_compare:
    render_section_header("⚖️", "Perbandingan Makanan")
    # PERBAIKAN: Menambahkan parameter unsafe_allow_html=True yang terlupa
    st.markdown(f"""
    <p style="color:{COLORS['text_light']}; font-size:0.9rem; margin-bottom:1rem;">
        Bandingkan profil nutrisi beberapa makanan secara berdampingan.
    </p>
    """, unsafe_allow_html=True)

    if not filtered_df.empty:
        food_options = filtered_df["display_name"].tolist()
        food1 = st.selectbox("Makanan 1:", food_options, key="cmp1")
        food2 = st.selectbox("Makanan 2:", food_options, index=min(1, len(food_options)-1), key="cmp2")

        if food1 and food2:
            d1 = filtered_df[filtered_df["display_name"] == food1].iloc[0]
            d2 = filtered_df[filtered_df["display_name"] == food2].iloc[0]

            comp_metrics = ["kalori", "protein", "lemak", "karbo"]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=[d1[m] for m in comp_metrics] + [d1[comp_metrics[0]]], theta=comp_metrics + [comp_metrics[0]], fill='toself', name=d1['display_name'][:30], line=dict(color=COLORS['gold'])))
            fig.add_trace(go.Scatterpolar(r=[d2[m] for m in comp_metrics] + [d2[comp_metrics[0]]], theta=comp_metrics + [comp_metrics[0]], fill='toself', name=d2['display_name'][:30], line=dict(color=COLORS['navy'])))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True)), **PLOTLY_LAYOUT, height=500)
            st.plotly_chart(fig, use_container_width=True)