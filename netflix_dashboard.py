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

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .stMetric label {
        color: #000000 !important;
        font-weight: 600;
    }
    .stMetric .css-1xarl3l {
        color: #000000 !important;
    }
    [data-testid="stMetricValue"] {
        color: #E50914 !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-size: 14px !important;
    }
    h1 {
        color: #E50914;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .netflix-header {
        background-color: #000000;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

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
    st.markdown('<div class="netflix-header">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎬 Netflix Data Analysis Dashboard")
        st.markdown("**Interactive insights into Netflix's content strategy**")
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("📊 Filters & Options")
    
    # Sidebar filters
    content_type = st.sidebar.multiselect(
        "Select Content Type",
        options=df['type'].unique() if 'type' in df.columns else [],
        default=df['type'].unique() if 'type' in df.columns else []
    )
    
    if 'year_added' in df.columns:
        year_range = st.sidebar.slider(
            "Year Added Range",
            min_value=int(df['year_added'].min()) if df['year_added'].notna().any() else 2008,
            max_value=int(df['year_added'].max()) if df['year_added'].notna().any() else 2021,
            value=(int(df['year_added'].min()) if df['year_added'].notna().any() else 2008, 
                   int(df['year_added'].max()) if df['year_added'].notna().any() else 2021)
        )
    
    # Additional filters
    if 'rating' in df.columns:
        all_ratings = df['rating'].dropna().unique()
        selected_ratings = st.sidebar.multiselect(
            "Select Ratings",
            options=sorted(all_ratings),
            default=sorted(all_ratings)
        )
    else:
        selected_ratings = []
    
    if 'listed_in' in df.columns:
        all_genres = df['listed_in'].dropna().str.split(', ').explode().unique()
        selected_genres = st.sidebar.multiselect(
            "Select Genres",
            options=sorted(all_genres)[:20],  # Top 20 for performance
            default=[]
        )
    else:
        selected_genres = []
    
    if 'country' in df.columns:
        all_countries = df['country'].dropna().str.split(', ').explode().unique()
        top_countries = df['country'].dropna().str.split(', ').explode().value_counts().head(15).index.tolist()
        selected_countries = st.sidebar.multiselect(
            "Select Countries",
            options=sorted(top_countries),
            default=[]
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
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Titles", f"{len(filtered_df):,}")
    
    with col2:
        if 'type' in filtered_df.columns:
            movies = len(filtered_df[filtered_df['type'] == 'Movie'])
            st.metric("Movies", f"{movies:,}")
    
    with col3:
        if 'type' in filtered_df.columns:
            tv_shows = len(filtered_df[filtered_df['type'] == 'TV Show'])
            st.metric("TV Shows", f"{tv_shows:,}")
    
    with col4:
        if 'country' in filtered_df.columns:
            countries = filtered_df['country'].dropna().str.split(', ').explode().nunique()
            st.metric("Countries", f"{countries:,}")
    
    # Summary Statistics Cards
    st.header("📊 Summary Statistics")
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
                st.plotly_chart(fig, use_container_width=True)
        
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
                st.plotly_chart(fig, use_container_width=True)
        
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
                st.plotly_chart(fig, use_container_width=True)
    
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
                st.plotly_chart(fig, use_container_width=True)
            
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
                st.plotly_chart(fig, use_container_width=True)
    
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
            st.plotly_chart(fig, use_container_width=True)
    
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
                st.plotly_chart(fig, use_container_width=True)
    
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
                st.plotly_chart(fig, use_container_width=True)
                
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
