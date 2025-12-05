"""
Netflix Data Analysis Dashboard
A simple interactive frontend for exploring Netflix dataset insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import random
import matplotlib.pyplot as plt
try:
    from wordcloud import WordCloud  # Optional dependency
    HAS_WORDCLOUD = True
except Exception:
    HAS_WORDCLOUD = False

# Page configuration
st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Theme & Styling ---------------- #
def get_theme():
    theme_choice = st.session_state.get('theme', 'Light')
    if theme_choice == 'Dark':
        return {
            'bg': '#0f0f0f',
            'surface': '#141414',
            'card': '#1a1a1a',
            'text': '#e6e6e6',
            'muted': '#b3b3b3',
            'primary': '#E50914',
            'accent': '#b20710',
        }
    else:  # Light
        return {
            'bg': '#ffffff',
            'surface': '#f7f7f7',
            'card': '#ffffff',
            'text': '#111111',
            'muted': '#5c5c5c',
            'primary': '#E50914',
            'accent': '#b20710',
        }

def apply_base_css(t):
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        :root {{
            --bg: {t['bg']};
            --surface: {t['surface']};
            --card: {t['card']};
            --text: {t['text']};
            --muted: {t['muted']};
            --primary: {t['primary']};
            --accent: {t['accent']};
        }}
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        
        .main {{
            padding: 0rem 1.5rem;
            background: var(--bg);
            color: var(--text);
            animation: fadeIn 0.5s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, rgba(229,9,20,0.15), rgba(229,9,20,0.05));
            border: 2px solid rgba(229,9,20,0.25);
            padding: 32px 28px;
            border-radius: 20px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(229,9,20,0.1);
            transition: all 0.3s ease;
            animation: slideIn 0.6s ease-out;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(229,9,20,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        .hero:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 48px rgba(229,9,20,0.15);
            border-color: rgba(229,9,20,0.4);
        }}
        
        .hero h1 {{
            color: var(--primary);
            margin: 0 0 8px 0;
            font-weight: 800;
            letter-spacing: -0.5px;
            font-size: 2.5rem;
            position: relative;
            z-index: 1;
        }}
        
        .hero p {{
            color: var(--muted);
            margin: 0;
            font-size: 1.1rem;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }}
        
        /* Enhanced KPI Cards */
        .kpi {{
            background: var(--card);
            border: 1px solid rgba(229,9,20,0.1);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: slideIn 0.5s ease-out;
        }}
        
        .kpi::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .kpi:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(229,9,20,0.15);
            border-color: rgba(229,9,20,0.3);
        }}
        
        .kpi:hover::before {{
            transform: scaleX(1);
        }}
        
        .kpi .label {{
            color: var(--muted);
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .kpi .value {{
            color: var(--text);
            font-size: 32px;
            font-weight: 800;
            line-height: 1.2;
            background: linear-gradient(135deg, var(--text), var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Section Headers */
        .section-title {{
            color: var(--text);
            font-weight: 700;
            font-size: 1.5rem;
            margin: 24px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--primary);
            display: inline-block;
            position: relative;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 40%;
            height: 2px;
            background: var(--accent);
            animation: expandWidth 0.6s ease-out;
        }}
        
        @keyframes expandWidth {{
            from {{ width: 0; }}
            to {{ width: 40%; }}
        }}
        
        /* Sidebar Enhancement */
        [data-testid="stSidebar"] {{
            background: var(--surface);
            border-right: 1px solid rgba(229,9,20,0.1);
        }}
        
        [data-testid="stSidebar"] .stButton button {{
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(229,9,20,0.3);
        }}
        
        [data-testid="stSidebar"] .stButton button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(229,9,20,0.4);
        }}
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, rgba(229,9,20,0.1), rgba(229,9,20,0.05));
            border-bottom: 3px solid var(--primary);
        }}
        
        /* Metric Cards */
        [data-testid="stMetric"] {{
            background: var(--card);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid rgba(229,9,20,0.1);
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        
        /* Dataframe Styling */
        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        }}
        
        /* Info/Success/Warning boxes */
        .stAlert {{
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            animation: slideIn 0.4s ease-out;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .streamlit-expanderHeader:hover {{
            background: rgba(229,9,20,0.05);
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--surface);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--primary);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent);
        }}
        </style>
    """, unsafe_allow_html=True)

def style_fig(fig, t):
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor=t['card'],
        plot_bgcolor=t['card'],
        font=dict(color=t['text'], family='Inter, system-ui, -apple-system', size=12),
        legend=dict(
            title_text='',
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=11),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        title_font=dict(size=18, color=t['text'], family='Inter'),
        hoverlabel=dict(
            bgcolor=t['card'],
            font_size=12,
            font_family='Inter'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        transition_duration=500
    )
    # Add subtle grid
    fig.update_xaxes(gridcolor='rgba(229,9,20,0.1)', gridwidth=1)
    fig.update_yaxes(gridcolor='rgba(229,9,20,0.1)', gridwidth=1)
    return fig

theme = get_theme()
apply_base_css(theme)

# Load data function with caching
@st.cache_data
def load_data():
    """Load and prepare Netflix dataset"""
    try:
        # Try to load cleaned data first
        if os.path.exists('outputs/cleaned_netflix.csv'):
            df = pd.read_csv('outputs/cleaned_netflix.csv')
            df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        else:
            # Load original data
            df = pd.read_csv('Netflix Dataset.csv')
            df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
            
            # Preserve original 'type' (often Movie/TV Show in some datasets, but sometimes genres)
            original_type = df['type'].copy() if 'type' in df.columns else None

            # Map columns safely
            if 'release_date' in df.columns and 'date_added' not in df.columns:
                df = df.rename(columns={'release_date': 'date_added'})
            if 'category' in df.columns:
                df['type'] = df['category']  # Movie / TV Show
            # Ensure genres column exists
            if 'listed_in' not in df.columns:
                if original_type is not None and original_type.dtype == object:
                    df['listed_in'] = original_type
                else:
                    df['listed_in'] = ''
            
            # Dates
            df['date_added'] = pd.to_datetime(df.get('date_added'), errors='coerce')
            df['year_added'] = df['date_added'].dt.year
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data()

if df is not None:
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="hero">', unsafe_allow_html=True)
        st.markdown("<h1>🎬 Netflix Data Analysis Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p>Interactive insights into Netflix's content strategy</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
    
    # Sidebar
    st.sidebar.header("📊 Filters & Options")
    # Theme toggle
    st.sidebar.selectbox("Theme", ["Light", "Dark"], index=(0 if st.session_state.get('theme','Light')=='Light' else 1), key='theme')
    # Apply theme if changed
    theme = get_theme()
    apply_base_css(theme)
    
    # Defaults and Reset
    def compute_defaults():
        defaults = {}
        defaults['content_type'] = list(df['type'].unique()) if 'type' in df.columns else []
        if 'year_added' in df.columns and df['year_added'].notna().any():
            defaults['year_range'] = (int(df['year_added'].min()), int(df['year_added'].max()))
        else:
            defaults['year_range'] = (2008, 2021)
        defaults['ratings'] = sorted(df['rating'].dropna().unique().tolist()) if 'rating' in df.columns else []
        defaults['genres'] = sorted(df['listed_in'].dropna().str.split(', ').explode().unique().tolist())[:20] if 'listed_in' in df.columns else []
        defaults['countries'] = sorted(df['country'].dropna().str.split(', ').explode().value_counts().head(15).index.tolist()) if 'country' in df.columns else []
        return defaults

    defaults = compute_defaults()
    if st.sidebar.button("↺ Reset Filters"):
        st.session_state['content_type'] = defaults['content_type']
        st.session_state['year_range'] = defaults['year_range']
        st.session_state['selected_ratings'] = defaults['ratings']
        st.session_state['selected_genres'] = []
        st.session_state['selected_countries'] = []
        st.experimental_rerun()

    # Sidebar filters grouped in expanders
    with st.sidebar.expander("Content"):
        content_type = st.multiselect(
            "Select Content Type",
            options=defaults['content_type'],
            default=st.session_state.get('content_type', defaults['content_type']),
            key='content_type'
        )

    with st.sidebar.expander("Time Range"):
        if 'year_added' in df.columns:
            year_range = st.slider(
                "Year Added Range",
                min_value=defaults['year_range'][0],
                max_value=defaults['year_range'][1],
                value=st.session_state.get('year_range', defaults['year_range']),
                key='year_range'
            )
    
    # Additional filters
    with st.sidebar.expander("Genres & Ratings"):
        if 'rating' in df.columns:
            all_ratings = defaults['ratings']
            selected_ratings = st.multiselect(
                "Select Ratings",
                options=all_ratings,
                default=st.session_state.get('selected_ratings', all_ratings),
                key='selected_ratings'
            )
        else:
            selected_ratings = []
    
        if 'listed_in' in df.columns:
            all_genres = defaults['genres']
            selected_genres = st.multiselect(
                "Select Genres",
                options=all_genres,
                default=st.session_state.get('selected_genres', []),
                key='selected_genres'
            )
        else:
            selected_genres = []
    
    with st.sidebar.expander("Countries"):
        if 'country' in df.columns:
            top_countries = defaults['countries']
            selected_countries = st.multiselect(
                "Select Countries",
                options=top_countries,
                default=st.session_state.get('selected_countries', []),
                key='selected_countries'
            )
        else:
            selected_countries = []
    
    # Fun Facts Section
    st.sidebar.markdown("---")
    st.sidebar.header("💡 Did You Know?")
    
    # Safe utilities
    def safe_mode(series):
        try:
            m = series.mode(dropna=True)
            return m.iloc[0] if not m.empty else 'N/A'
        except Exception:
            return 'N/A'

    unique_countries = df['country'].dropna().str.split(', ').explode().nunique() if 'country' in df.columns else 0
    max_year = df['year_added'].dropna().max() if 'year_added' in df.columns else None
    latest_year_count = int(len(df[df['year_added'] == max_year])) if max_year == max_year and pd.notna(max_year) else 0
    common_rating = safe_mode(df['rating']) if 'rating' in df.columns else 'N/A'
    common_genre = safe_mode(df['listed_in'].dropna().str.split(', ').explode()) if 'listed_in' in df.columns else 'N/A'
    avg_movie_mins = None
    if 'duration' in df.columns and 'type' in df.columns:
        try:
            avg_movie_mins = df[df['type']=='Movie']['duration'].str.extract(r'(\d+)')[0].astype(float).mean()
        except Exception:
            avg_movie_mins = None
    usa_titles = len(df[df['country'].str.contains('United States', na=False)]) if 'country' in df.columns else 0
    # Growth between earliest and latest counts
    if 'year_added' in df.columns and df['year_added'].notna().any():
        earliest_year = df['year_added'].dropna().min()
        e_cnt = len(df[df['year_added'] == earliest_year])
        l_cnt = len(df[df['year_added'] == max_year]) if pd.notna(max_year) else 0
        growth_pct = ((l_cnt - e_cnt) / e_cnt * 100) if e_cnt else None
    else:
        growth_pct = None
    top_director_titles = None
    if 'director' in df.columns and df['director'].notna().any():
        vc = df['director'].dropna().str.split(', ').explode().value_counts()
        top_director_titles = int(vc.iloc[0]) if len(vc) else None

    fun_facts = []
    fun_facts.append(f"🎬 Netflix has content from {unique_countries} countries!")
    if pd.notna(max_year):
        fun_facts.append(f"📺 The platform added {latest_year_count} titles in {int(max_year)}!")
    if common_rating != 'N/A':
        fun_facts.append(f"⭐ '{common_rating}' is the most common rating!")
    if common_genre != 'N/A':
        fun_facts.append(f"🎭 '{common_genre}' is the top genre!")
    if avg_movie_mins and not pd.isna(avg_movie_mins):
        fun_facts.append(f"🎥 Average movie duration is {avg_movie_mins:.0f} minutes!")
    fun_facts.append(f"� USA produces {usa_titles} titles!")
    if growth_pct is not None:
        fun_facts.append(f"📈 Latest vs earliest year: {growth_pct:+.0f}% change")
    if top_director_titles:
        fun_facts.append(f"🎬 Top director has {top_director_titles} titles!")
    if not fun_facts:
        fun_facts.append("Explore the data to discover insights!")
    
    if st.sidebar.button("🔄 Refresh Fun Fact"):
        st.session_state.fun_fact_index = random.randint(0, len(fun_facts) - 1)
    
    if 'fun_fact_index' not in st.session_state:
        st.session_state.fun_fact_index = random.randint(0, len(fun_facts) - 1)
    
    st.sidebar.info(fun_facts[st.session_state.fun_fact_index])
    
    # Filter data
    if 'type' in df.columns and content_type:
        filtered_df = df[df['type'].isin(content_type)]
    else:
        filtered_df = df.copy()
    
    if 'year_added' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['year_added'] >= year_range[0]) & 
            (filtered_df['year_added'] <= year_range[1])
        ]
    
    # Apply additional filters
    if selected_ratings and 'rating' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['rating'].isin(selected_ratings)]
    
    if selected_genres and 'listed_in' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['listed_in'].str.contains('|'.join(selected_genres), na=False)]
    
    if selected_countries and 'country' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['country'].str.contains('|'.join(selected_countries), na=False)]
    
    # Key Metrics
    st.markdown('<h3 class="section-title">📈 Key Metrics</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    total_titles = f"{len(filtered_df):,}"
    movies = len(filtered_df[filtered_df['type'] == 'Movie']) if 'type' in filtered_df.columns else 0
    tv_shows = len(filtered_df[filtered_df['type'] == 'TV Show']) if 'type' in filtered_df.columns else 0
    countries = filtered_df['country'].dropna().str.split(', ').explode().nunique() if 'country' in filtered_df.columns else 0
    with col1:
        st.markdown(f"<div class='kpi'><div class='label'>Total Titles</div><div class='value'>📚 {total_titles}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='kpi'><div class='label'>Movies</div><div class='value'>🎞️ {movies:,}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='kpi'><div class='label'>TV Shows</div><div class='value'>📺 {tv_shows:,}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='kpi'><div class='label'>Countries</div><div class='value'>🌍 {countries:,}</div></div>", unsafe_allow_html=True)
    
    # Summary Statistics Cards
    st.markdown('<h3 class="section-title">📊 Summary Statistics</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if 'duration' in filtered_df.columns and 'type' in filtered_df.columns:
            avg_duration = filtered_df[filtered_df['type']=='Movie']['duration'].str.extract(r'(\d+)')[0].astype(float).mean()
            st.metric("Avg Movie Length", f"{avg_duration:.0f} min")
    
    with col2:
        if 'listed_in' in filtered_df.columns:
            top_genre = filtered_df['listed_in'].dropna().str.split(', ').explode().mode()[0]
            st.metric("Top Genre", f"{top_genre[:15]}...")
    
    with col3:
        if 'country' in filtered_df.columns:
            top_country = filtered_df['country'].dropna().str.split(', ').explode().mode()[0]
            st.metric("Top Country", top_country)
    
    with col4:
        if 'rating' in filtered_df.columns:
            top_rating = filtered_df['rating'].mode()[0]
            st.metric("Common Rating", top_rating)
    
    with col5:
        if 'year_added' in filtered_df.columns:
            growth = len(filtered_df[filtered_df['year_added'] == filtered_df['year_added'].max()])
            st.metric("Latest Year Adds", f"{growth:,}")
    
    st.markdown("---")
    
    # Main content - Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", 
        "🎭 Genres", 
        "🌍 Geographic", 
        "📅 Temporal",
        "👥 Cast & Directors", 
        "🔍 Explore Data"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("Content Distribution Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'type' in filtered_df.columns:
                # Movies vs TV Shows pie chart
                type_counts = filtered_df['type'].value_counts()
                fig = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Movies vs TV Shows Distribution",
                    color_discrete_sequence=['#E50914', '#564d4d']
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(style_fig(fig, theme), use_container_width=True)
        
        with col2:
            if 'rating' in filtered_df.columns:
                # Top ratings bar chart
                rating_counts = filtered_df['rating'].value_counts().head(10)
                fig = px.bar(
                    x=rating_counts.values,
                    y=rating_counts.index,
                    orientation='h',
                    title="Top 10 Content Ratings",
                    labels={'x': 'Count', 'y': 'Rating'},
                    color=rating_counts.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(style_fig(fig, theme), use_container_width=True)
        
        # Duration analysis
        if 'duration' in filtered_df.columns and 'type' in filtered_df.columns:
            st.subheader("Duration Analysis")
            
            # Parse duration for movies
            movies_df = filtered_df[filtered_df['type'] == 'Movie'].copy()
            if len(movies_df) > 0:
                movies_df['duration_minutes'] = movies_df['duration'].str.extract('(\d+)').astype(float)
                
                fig = px.histogram(
                    movies_df,
                    x='duration_minutes',
                    nbins=30,
                    title="Movie Duration Distribution (minutes)",
                    labels={'duration_minutes': 'Duration (minutes)', 'count': 'Number of Movies'},
                    color_discrete_sequence=['#E50914']
                )
                st.plotly_chart(style_fig(fig, theme), use_container_width=True)
    
    # Tab 2: Genres
    with tab2:
        st.header("Genre Analysis")
        
        if 'listed_in' in filtered_df.columns:
            # Explode genres
            genres_df = filtered_df['listed_in'].dropna().str.split(', ').explode()
            genre_counts = genres_df.value_counts().head(15)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.bar(
                    x=genre_counts.values,
                    y=genre_counts.index,
                    orientation='h',
                    title="Top 15 Genres",
                    labels={'x': 'Number of Titles', 'y': 'Genre'},
                    color=genre_counts.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(style_fig(fig, theme), use_container_width=True)
            
            with col2:
                st.subheader("Genre Statistics")
                st.dataframe(
                    pd.DataFrame({
                        'Genre': genre_counts.index,
                        'Count': genre_counts.values
                    }).reset_index(drop=True),
                    hide_index=True,
                    height=400
                )
            
            # Genre trends over time
            if 'year_added' in filtered_df.columns:
                st.subheader("Genre Trends Over Time")
                
                # Create exploded dataframe with year
                temp_df = filtered_df[['listed_in', 'year_added']].dropna()
                temp_df = temp_df.assign(genre=temp_df['listed_in'].str.split(', ')).explode('genre')
                
                # Get top 5 genres
                top_genres = temp_df['genre'].value_counts().head(5).index
                temp_df = temp_df[temp_df['genre'].isin(top_genres)]
                
                # Count by year and genre
                genre_time = temp_df.groupby(['year_added', 'genre']).size().reset_index(name='count')
                
                fig = px.line(
                    genre_time,
                    x='year_added',
                    y='count',
                    color='genre',
                    title='Top 5 Genre Trends Over Time',
                    labels={'year_added': 'Year', 'count': 'Number of Titles'},
                    markers=True
                )
                st.plotly_chart(style_fig(fig, theme), use_container_width=True)
    
    # Tab 3: Geographic
    with tab3:
        st.header("Geographic Distribution")
        
        if 'country' in filtered_df.columns:
            # Explode countries
            countries_df = filtered_df['country'].dropna().str.split(', ').explode()
            country_counts = countries_df.value_counts().head(20)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.bar(
                    x=country_counts.values,
                    y=country_counts.index,
                    orientation='h',
                    title="Top 20 Content Producing Countries",
                    labels={'x': 'Number of Titles', 'y': 'Country'},
                    color=country_counts.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Country Statistics")
                st.dataframe(
                    pd.DataFrame({
                        'Country': country_counts.index,
                        'Titles': country_counts.values
                    }).reset_index(drop=True),
                    hide_index=True,
                    height=500
                )
            
            # World map
            st.subheader("Global Distribution Map")
            country_df = pd.DataFrame({
                'country': country_counts.index,
                'count': country_counts.values
            })
            
            fig = px.choropleth(
                country_df,
                locations='country',
                locationmode='country names',
                color='count',
                title='Netflix Content by Country',
                color_continuous_scale='Reds',
                labels={'count': 'Number of Titles'}
            )
            st.plotly_chart(style_fig(fig, theme), use_container_width=True)
    
    # Tab 4: Temporal
    with tab4:
        st.header("Temporal Analysis")
        
        if 'year_added' in filtered_df.columns and 'type' in filtered_df.columns:
            # Content added per year
            year_type = filtered_df.groupby(['year_added', 'type']).size().reset_index(name='count')
            year_type = year_type.dropna()
            
            fig = px.area(
                year_type,
                x='year_added',
                y='count',
                color='type',
                title='Content Added Per Year by Type',
                labels={'year_added': 'Year', 'count': 'Number of Titles'},
                color_discrete_sequence=['#E50914', '#564d4d']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Monthly trends
            if 'date_added' in filtered_df.columns:
                st.subheader("Monthly Addition Patterns")
                monthly_df = filtered_df.copy()
                monthly_df['month'] = monthly_df['date_added'].dt.month_name()
                monthly_counts = monthly_df['month'].value_counts()
                
                # Reorder by month
                month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']
                monthly_counts = monthly_counts.reindex([m for m in month_order if m in monthly_counts.index])
                
                fig = px.bar(
                    x=monthly_counts.index,
                    y=monthly_counts.values,
                    title='Content Added by Month',
                    labels={'x': 'Month', 'y': 'Number of Titles'},
                    color=monthly_counts.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(style_fig(fig, theme), use_container_width=True)
    
    # Tab 5: Cast & Directors
    with tab5:
        st.header("👥 Top Cast & Directors")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎬 Most Prolific Directors")
            if 'director' in filtered_df.columns:
                directors_df = filtered_df['director'].dropna().str.split(', ').explode()
                top_directors = directors_df.value_counts().head(15)
                
                fig = px.bar(
                    x=top_directors.values,
                    y=top_directors.index,
                    orientation='h',
                    title="Top 15 Directors by Number of Titles",
                    labels={'x': 'Number of Titles', 'y': 'Director'},
                    color=top_directors.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(style_fig(fig, theme), use_container_width=True)
                
                # Directors table
                st.dataframe(
                    pd.DataFrame({
                        'Director': top_directors.index,
                        'Titles': top_directors.values
                    }).reset_index(drop=True),
                    hide_index=True,
                    height=300
                )
        
        with col2:
            st.subheader("⭐ Most Featured Cast Members")
            if 'cast' in filtered_df.columns:
                cast_df = filtered_df['cast'].dropna().str.split(', ').explode()
                top_cast = cast_df.value_counts().head(15)
                
                fig = px.bar(
                    x=top_cast.values,
                    y=top_cast.index,
                    orientation='h',
                    title="Top 15 Cast Members by Appearances",
                    labels={'x': 'Number of Appearances', 'y': 'Cast Member'},
                    color=top_cast.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Cast table
                st.dataframe(
                    pd.DataFrame({
                        'Cast Member': top_cast.index,
                        'Appearances': top_cast.values
                    }).reset_index(drop=True),
                    hide_index=True,
                    height=300
                )
        
        # Word Cloud from Descriptions
        st.subheader("☁️ Content Themes Word Cloud")
        if HAS_WORDCLOUD and 'description' in filtered_df.columns:
            descriptions_text = ' '.join(filtered_df['description'].dropna().astype(str))
            
            if descriptions_text:
                try:
                    wordcloud = WordCloud(
                        width=1200, 
                        height=400, 
                        background_color='black',
                        colormap='Reds',
                        max_words=100,
                        relative_scaling=0.5,
                        min_font_size=10
                    ).generate(descriptions_text)
                    
                    fig, ax = plt.subplots(figsize=(15, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    plt.tight_layout(pad=0)
                    st.pyplot(fig)
                    
                    st.caption("Word cloud generated from content descriptions showing popular themes and keywords")
                except Exception as e:
                    st.warning(f"Could not generate word cloud: {e}")
        elif not HAS_WORDCLOUD:
            st.info("Install the 'wordcloud' package to enable this visualization.")
    
    # Tab 6: Explore Data
    with tab6:
        st.header("Explore Raw Data")
        
        # Search functionality
        search_term = st.text_input("🔍 Search titles", "")
        
        if search_term:
            search_results = filtered_df[
                filtered_df['title'].str.contains(search_term, case=False, na=False)
            ]
            st.write(f"Found {len(search_results)} results")
            display_df = search_results
        else:
            display_df = filtered_df
        
        # Display options
        col1, col2 = st.columns([1, 3])
        with col1:
            rows_to_show = st.selectbox("Rows to display", [10, 25, 50, 100], index=1)
        
        # Display dataframe
        st.dataframe(
            display_df.head(rows_to_show),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f'netflix_filtered_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: gray;'>
            <p>Netflix Data Analysis Dashboard | Built with Streamlit & Plotly</p>
            <p>Data Source: Netflix Dataset (7,789+ titles)</p>
        </div>
    """, unsafe_allow_html=True)
    
else:
    st.error("❌ Could not load data. Please ensure 'Netflix Dataset.csv' or 'outputs/cleaned_netflix.csv' exists.")
    st.info("💡 Place your Netflix dataset in the same directory as this script.")
