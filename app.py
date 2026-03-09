import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def apply_custom_css():
    """Apply custom CSS for professional styling."""
    st.markdown("""
        <style>
        /* Main page styling */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Header styling */
        h1 {
            color: #1e3a8a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
            padding-bottom: 20px;
            border-bottom: 3px solid #3b82f6;
        }
        
        h2, h3 {
            color: #1e40af;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            color: #1e40af;
            font-weight: 600;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 16px;
            color: #64748b;
            font-weight: 500;
        }
        
        /* Card-like containers */
        .css-1r6slb0 {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            border: 2px dashed #3b82f6;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            border: none;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #2563eb;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Info box styling */
        .stAlert {
            background-color: #dbeafe;
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
        }
        
        /* Divider */
        hr {
            margin: 30px 0;
            border: none;
            border-top: 2px solid #e2e8f0;
        }
        
        /* Section headers */
        .section-header {
            background: linear-gradient(90deg, #3b82f6 0%, #1e40af 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 20px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)


def configure_page():
    """Set page settings."""
    st.set_page_config(
        page_title="World Happiness Dashboard", 
        layout="wide",
        initial_sidebar_state="collapsed",
        page_icon="😊"
    )
    apply_custom_css()
    
    # Set plot style
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = '#f8f9fa'
    plt.rcParams['axes.edgecolor'] = '#cbd5e1'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9


def show_dataset_description():
    """Show dataset information."""
    st.markdown("""
    <div style="background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 30px;">
        <h3 style="color: #1e40af; margin-top: 0;">📊 World Happiness Report (2015-2019)</h3>
        <p style="color: #475569; font-size: 16px; line-height: 1.6;">
            This comprehensive dataset contains happiness scores and key factors including GDP per Capita,
            Social Support, Life Expectancy, Freedom, Generosity, and Government Corruption for countries worldwide.
        </p>
        <p style="color: #64748b; font-size: 14px; line-height: 1.6;">
            📈 Analyze global happiness trends and discover the factors that influence well-being across nations.
        </p>
    </div>
    """, unsafe_allow_html=True)


def standardize_columns(df):
    """Rename columns to standard format."""
    try:
        df.columns = df.columns.str.strip()
        df = df.rename(columns={
            "Score": "Happiness Score",
            "Economy (GDP per Capita)": "GDP",
            "GDP per Capita": "GDP",
            "Health (Life Expectancy)": "Life Expectancy",
            "Trust (Government Corruption)": "Corruption"
        })
        return df
    except:
        return df


def load_multiple_datasets():
    """Upload and merge multiple CSV files."""
    try:
        files = st.file_uploader(
            "Upload 2015-2019 CSV Files",
            type=["csv"],
            accept_multiple_files=True
        )

        if files:
            df_list = []
            for file in files:
                df = pd.read_csv(file)
                try:
                    year = int(file.name[:4])
                    df["Year"] = year
                except:
                    pass
                df = standardize_columns(df)
                df_list.append(df)

            combined = pd.concat(df_list, ignore_index=True)
            return combined

        return None

    except Exception as e:
        st.error(e)
        return None


def kpi_total_countries(df):
    """Total unique countries."""
    try:
        st.metric("Total Countries", df["Country"].nunique())
    except Exception as e:
        st.error(e)


def kpi_total_years(df):
    """Total years available."""
    try:
        st.metric("Total Years", df["Year"].nunique())
    except Exception as e:
        st.error(e)


def kpi_average_happiness(df):
    """Average happiness score."""
    try:
        st.metric("Average Happiness", round(df["Happiness Score"].mean(), 2))
    except Exception as e:
        st.error(e)


def kpi_happiest_country(df):
    """Happiest country overall."""
    try:
        row = df.loc[df["Happiness Score"].idxmax()]
        st.metric("Happiest Country", f"{row['Country']} ({round(row['Happiness Score'],2)})")
    except Exception as e:
        st.error(e)


def kpi_unhappiest_country(df):
    """Least happy country overall."""
    try:
        row = df.loc[df["Happiness Score"].idxmin()]
        st.metric("Unhappiest Country", f"{row['Country']} ({round(row['Happiness Score'],2)})")
    except Exception as e:
        st.error(e)


def kpi_gdp_vs_happiness(df):
    """GDP vs Happiness plot."""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x="GDP", y="Happiness Score", data=df, ax=ax, 
                       alpha=0.6, s=80, color="#3b82f6")
        ax.set_title("GDP vs Happiness Score", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("GDP per Capita", fontsize=11, fontweight='500')
        ax.set_ylabel("Happiness Score", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_yearly_trend(df):
    """Yearly happiness trend."""
    try:
        avg = df.groupby("Year")["Happiness Score"].mean()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=avg.index, y=avg.values, marker="o", ax=ax, 
                    linewidth=3, markersize=10, color="#10b981")
        ax.set_title("Average Happiness Score Trend Over Years", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("Year", fontsize=11, fontweight='500')
        ax.set_ylabel("Average Happiness Score", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_top_gdp(df):
    """Top 5 GDP countries."""
    try:
        top = df.sort_values("GDP", ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="GDP", y="Country", data=top, ax=ax, palette="viridis")
        ax.set_title("Top 5 Countries by GDP per Capita", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("GDP per Capita", fontsize=11, fontweight='500')
        ax.set_ylabel("Country", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_top_10_latest(df):
    """Top 10 happiest countries (latest year)."""
    try:
        year = df["Year"].max()
        top = df[df["Year"] == year].sort_values(
            "Happiness Score", ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(x="Happiness Score", y="Country", data=top, ax=ax, palette="rocket")
        ax.set_title(f"Top 10 Happiest Countries ({int(year)})", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("Happiness Score", fontsize=11, fontweight='500')
        ax.set_ylabel("Country", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_boxplot(df):
    """Happiness distribution by year."""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x="Year", y="Happiness Score", data=df, ax=ax, palette="Set2")
        ax.set_title("Happiness Score Distribution by Year", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("Year", fontsize=11, fontweight='500')
        ax.set_ylabel("Happiness Score", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_heatmap(df):
    """Correlation heatmap."""
    try:
        cols = ["Happiness Score", "GDP", "Social Support",
                "Life Expectancy", "Freedom",
                "Generosity", "Corruption"]
        corr = df[cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax, 
                   fmt=".2f", linewidths=0.5, cbar_kws={'label': 'Correlation'})
        ax.set_title("Correlation Matrix of Happiness Factors", fontsize=14, fontweight='bold', color='#1e40af', pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_rank_trend(df):
    """Rank trend for selected countries."""
    try:
        df2 = df.copy()
        df2["Rank"] = df2.groupby("Year")["Happiness Score"].rank(ascending=False)
        countries = ["India", "Finland", "United States"]
        data = df2[df2["Country"].isin(countries)]
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=data, x="Year", y="Rank", hue="Country", marker="o", ax=ax, linewidth=2.5, markersize=10)
        ax.invert_yaxis()
        ax.set_title("Happiness Rank Trend for Selected Countries", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("Year", fontsize=11, fontweight='500')
        ax.set_ylabel("Rank (Lower is Better)", fontsize=11, fontweight='500')
        ax.legend(title='Country', title_fontsize=10, fontsize=9, loc='best')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_country_count(df):
    """Countries reported per year."""
    try:
        count = df.groupby("Year")["Country"].count()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=count.index, y=count.values, ax=ax, palette="mako")
        ax.set_title("Number of Countries Reported per Year", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("Year", fontsize=11, fontweight='500')
        ax.set_ylabel("Number of Countries", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_freedom_vs_happiness(df):
    """Freedom vs Happiness plot."""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x="Freedom", y="Happiness Score", data=df, ax=ax, 
                       alpha=0.6, s=80, color="#10b981")
        ax.set_title("Freedom vs Happiness Score", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("Freedom", fontsize=11, fontweight='500')
        ax.set_ylabel("Happiness Score", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_corruption_vs_happiness(df):
    """Corruption vs Happiness plot."""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x="Corruption", y="Happiness Score", data=df, ax=ax, 
                       alpha=0.6, s=80, color="#f59e0b")
        ax.set_title("Government Corruption vs Happiness Score", fontsize=14, fontweight='bold', color='#1e40af')
        ax.set_xlabel("Corruption (Trust in Government)", fontsize=11, fontweight='500')
        ax.set_ylabel("Happiness Score", fontsize=11, fontweight='500')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def display_dashboard(df):
    """Display all KPIs."""
    # Key Metrics Section
    st.markdown("<div class='section-header'>📊 Key Metrics Overview</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_total_countries(df)
    with col2:
        kpi_total_years(df)
    with col3:
        kpi_average_happiness(df)
    
    col4, col5 = st.columns(2)
    with col4:
        kpi_happiest_country(df)
    with col5:
        kpi_unhappiest_country(df)
    
    st.markdown("---")
    
    # Trends Analysis
    st.markdown("<div class='section-header'>📈 Trends & Analysis</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        kpi_yearly_trend(df)
    with col2:
        kpi_boxplot(df)
    
    st.markdown("---")
    
    # Country Rankings
    st.markdown("<div class='section-header'>🏆 Country Rankings</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        kpi_top_10_latest(df)
    with col2:
        kpi_top_gdp(df)
    
    col3, col4 = st.columns(2)
    with col3:
        kpi_rank_trend(df)
    with col4:
        kpi_country_count(df)
    
    st.markdown("---")
    
    # Factor Analysis
    st.markdown("<div class='section-header'>🔍 Factor Analysis</div>", unsafe_allow_html=True)
    kpi_heatmap(df)
    
    col1, col2 = st.columns(2)
    with col1:
        kpi_gdp_vs_happiness(df)
    with col2:
        kpi_freedom_vs_happiness(df)
    
    kpi_corruption_vs_happiness(df)


def main():
    """Run the dashboard."""
    configure_page()
    
    # Header with icon
    st.markdown("""
        <h1 style='text-align: center;'>😊 World Happiness Dashboard</h1>
        <p style='text-align: center; color: #64748b; font-size: 18px; margin-bottom: 30px;'>
            Explore global happiness trends from 2015 to 2019
        </p>
    """, unsafe_allow_html=True)
    
    show_dataset_description()
    
    df = load_multiple_datasets()
    if df is not None:
        st.success(f"✅ Successfully loaded {len(df)} records from {df['Year'].nunique()} years!")
        display_dashboard(df)
    else:
        st.markdown("""
            <div style="background-color: #dbeafe; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0;">
                <h3 style="color: #1e40af; margin-top: 0;">📁 Upload Data Files</h3>
                <p style="color: #475569; font-size: 16px;">
                    Please upload all CSV files (2015-2019) to begin exploring the World Happiness data.
                </p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
