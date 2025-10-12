# 🎬 Netflix Data Analysis

A comprehensive data analysis project exploring Netflix's content catalog with interactive visualizations, strategic insights, and an interactive dashboard.

![Netflix](https://img.shields.io/badge/Netflix-E50914?style=for-the-badge&logo=netflix&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Highlights](#analysis-highlights)
- [Dashboard Features](#dashboard-features)
- [Key Insights](#key-insights)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project provides an in-depth analysis of Netflix's content catalog, exploring patterns in:
- Content distribution (Movies vs TV Shows)
- Genre trends over time
- Geographic content contributions
- Temporal patterns in content additions
- Top directors and cast members
- Duration and rating distributions

The project includes both a detailed Jupyter notebook analysis and an interactive Streamlit dashboard for exploring the data.

## ✨ Features

### 📊 Data Analysis
- **Comprehensive EDA**: Exploratory data analysis with 15+ visualizations
- **Data Cleaning**: Handles missing values, parses dates, and normalizes text fields
- **Multi-dimensional Analysis**: Analyzes content across genres, countries, years, ratings, and more
- **Statistical Insights**: Provides descriptive statistics and distribution analyses

### 🎨 Interactive Dashboard
- **Real-time Filtering**: Filter by content type, year, rating, genre, and country
- **Dynamic Visualizations**: Interactive charts using Plotly
- **Key Metrics**: Overview of important statistics at a glance
- **Export Functionality**: Download filtered data as CSV
- **Search Feature**: Find specific titles quickly

### 📈 Strategic Insights
- Content strategy recommendations
- Market gap analysis
- Geographic expansion priorities
- Genre optimization suggestions

## 📁 Project Structure

```
Netflix_Data_Analysis/
│
├── netflix_analysis.ipynb          # Jupyter notebook with comprehensive analysis
├── netflix_dashboard.py            # Streamlit interactive dashboard
├── generate_presentation.py        # Script to generate presentation slides
├── Netflix Dataset.csv             # Original Netflix dataset
├── requirements.txt                # Python dependencies
│
├── outputs/
│   ├── cleaned_netflix.csv        # Cleaned and processed dataset
│   └── charts/                    # Generated visualization images
│
└── README.md                      # Project documentation (this file)
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository** (or download the project)
   ```bash
   git clone https://github.com/Shriii19/Netflix_Data_Analysis.git
   cd Netflix_Data_Analysis
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import streamlit, pandas, plotly; print('All packages installed successfully!')"
   ```

## 💻 Usage

### Running the Jupyter Notebook

1. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook netflix_analysis.ipynb
   ```

2. **Run all cells** to perform the complete analysis
   - The notebook will automatically load the dataset
   - Execute data cleaning and preprocessing
   - Generate visualizations
   - Save cleaned data to `outputs/cleaned_netflix.csv`

### Running the Interactive Dashboard

1. **Launch the Streamlit dashboard**
   ```bash
   streamlit run netflix_dashboard.py
   ```

2. **Access the dashboard** in your web browser (usually opens automatically at `http://localhost:8501`)

3. **Explore the features**:
   - Use sidebar filters to narrow down content
   - Switch between different analysis tabs
   - Download filtered data
   - Search for specific titles

### Generating Presentation

```bash
python generate_presentation.py
```

## 📊 Analysis Highlights

### 1. Content Distribution
- **Movies vs TV Shows**: Analyze the ratio and trends
- **Growth Over Time**: Track how the catalog has evolved
- **Content Quality**: Distribution of ratings and durations

### 2. Genre Analysis
- **Top 15 Genres**: Most popular content categories
- **Genre Trends**: How genre popularity has changed over time
- **Genre-Type Correlation**: Relationship between genres and content types

### 3. Geographic Distribution
- **Top 20 Countries**: Leading content producers
- **Regional Analysis**: Content distribution across continents
- **Market Penetration**: Identify underserved regions

### 4. Temporal Patterns
- **Year-over-Year Growth**: Content addition trends
- **Monthly Patterns**: Seasonal content release patterns
- **Peak Periods**: Identify high-activity periods

### 5. People & Talent
- **Top Directors**: Most prolific directors on Netflix
- **Featured Cast**: Most frequently appearing actors
- **Collaboration Networks**: Relationships between talent

## 🎨 Dashboard Features

### 📊 Overview Tab
- Content distribution pie chart
- Top ratings bar chart
- Duration distribution histogram
- Key metrics summary

### 🎭 Genres Tab
- Top 15 genres bar chart
- Genre trends over time line chart
- Genre statistics table

### 🌍 Geographic Tab
- Top 20 countries bar chart
- Global distribution choropleth map
- Country statistics table

### 📅 Temporal Tab
- Content added per year area chart
- Monthly addition patterns
- Year-over-year growth analysis

### 👥 Cast & Directors Tab
- Top directors visualization
- Most featured cast members
- Word cloud of content themes

### 🔍 Explore Data Tab
- Searchable data table
- Customizable row display
- CSV export functionality

## 🔍 Key Insights

### Strategic Recommendations

1. **Content Balance**
   - Increase TV Show production for better retention
   - Maintain optimal movie duration (90-120 minutes)

2. **Genre Focus**
   - Invest heavily in International Movies, Dramas, and Comedies
   - Diversify within popular genres for broader appeal

3. **Geographic Expansion**
   - Prioritize underrepresented markets (Latin America, Africa, Southeast Asia)
   - Increase local language original content

4. **Quality Over Quantity**
   - Focus on high-rated content in popular genres
   - Avoid single-season cancellations

5. **Competitive Strategy**
   - Fill content gaps compared to competitors
   - Increase original productions for exclusivity

### Data-Driven Findings

- **Peak Content Addition**: Identify years with maximum growth
- **Popular Genres**: Top 3-5 genres account for majority of content
- **Geographic Leaders**: USA, India, and UK are top content producers
- **Duration Sweet Spot**: Most successful movies are 90-120 minutes
- **Rating Patterns**: Family-friendly content dominates catalog

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib**: Static visualizations
- **Plotly**: Interactive visualizations
- **Streamlit**: Web dashboard framework
- **WordCloud**: Text visualization
- **Jupyter Notebook**: Interactive analysis environment

## 📸 Screenshots

### Dashboard Overview
*Interactive dashboard showing key metrics and content distribution*

### Genre Analysis
*Top genres and trends over time*

### Geographic Distribution
*Global map showing content by country*

### Temporal Trends
*Content addition patterns over years*

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions

- Add sentiment analysis of descriptions
- Implement recommendation system
- Add comparison with other streaming platforms
- Enhance visualizations with new chart types
- Improve data preprocessing pipeline
- Add unit tests

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

**Project Maintainer**: Shriii19

- GitHub: [@Shriii19](https://github.com/Shriii19)
- Repository: [Netflix_Data_Analysis](https://github.com/Shriii19/Netflix_Data_Analysis)

## 🙏 Acknowledgments

- **Netflix** for making their dataset publicly available
- **Streamlit** for the amazing dashboard framework
- **Plotly** for interactive visualization capabilities
- **Python community** for excellent data science libraries

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Netflix Technology Blog](https://netflixtechblog.com/)

## 🔄 Future Enhancements

- [ ] Add machine learning predictions for content success
- [ ] Implement NLP for description analysis
- [ ] Create competitor comparison dashboard
- [ ] Add user rating correlation analysis
- [ ] Build recommendation engine
- [ ] Deploy dashboard to cloud (Streamlit Cloud/Heroku)
- [ ] Add automated reporting feature
- [ ] Integrate real-time data updates

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ and Python

</div>
