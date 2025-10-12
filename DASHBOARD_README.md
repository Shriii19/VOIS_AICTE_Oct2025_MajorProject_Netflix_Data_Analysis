# 🎬 Netflix Dashboard - Quick Start

## Installation & Run

### Step 1: Install Streamlit
```powershell
pip install streamlit plotly
```

### Step 2: Run the Dashboard
```powershell
streamlit run netflix_dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

---

## Features

✅ **Interactive Filters** - Filter by content type and year range  
✅ **Key Metrics** - Total titles, movies, TV shows, countries  
✅ **5 Analysis Tabs**:
  - 📊 Overview - Content distribution, ratings, durations
  - 🎭 Genres - Top genres, trends over time
  - 🌍 Geographic - Country distribution, world map
  - 📅 Temporal - Yearly/monthly trends
  - 🔍 Explore - Search & download filtered data

✅ **Visualizations** - Interactive Plotly charts  
✅ **Download** - Export filtered data as CSV  
✅ **Netflix Theme** - Red & black Netflix colors

---

## Troubleshooting

**Error: "streamlit: command not found"**
```powershell
pip install streamlit
```

**Port already in use**
```powershell
streamlit run netflix_dashboard.py --server.port 8502
```

**Data not loading**
- Ensure `Netflix Dataset.csv` is in the same folder
- Or have `outputs/cleaned_netflix.csv` from the Jupyter notebook

---

## Screenshot Preview

The dashboard includes:
- Netflix-branded header with logo
- Real-time filtering sidebar
- 4 key metrics cards
- 15+ interactive visualizations
- Data exploration and export

---

Enjoy exploring your Netflix data! 🚀
