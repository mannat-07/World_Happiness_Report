import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def configure_page():
    """Set page settings."""
    st.set_page_config(page_title="World Happiness Dashboard", layout="wide")


def show_dataset_description():
    """Show dataset information."""
    st.markdown("""
    ### World Happiness Report (2015-2019)

    This dataset contains happiness scores and factors like GDP,
    Social Support, Life Expectancy, Freedom, Generosity and Corruption.

    It helps understand global happiness trends and influencing factors.
    """)


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
        fig, ax = plt.subplots()
        sns.scatterplot(x="GDP", y="Happiness Score", data=df, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_yearly_trend(df):
    """Yearly happiness trend."""
    try:
        avg = df.groupby("Year")["Happiness Score"].mean()
        fig, ax = plt.subplots()
        sns.lineplot(x=avg.index, y=avg.values, marker="o", ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_top_gdp(df):
    """Top 5 GDP countries."""
    try:
        top = df.sort_values("GDP", ascending=False).head(5)
        fig, ax = plt.subplots()
        sns.barplot(x="GDP", y="Country", data=top, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_top_10_latest(df):
    """Top 10 happiest countries (latest year)."""
    try:
        year = df["Year"].max()
        top = df[df["Year"] == year].sort_values(
            "Happiness Score", ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(x="Happiness Score", y="Country", data=top, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_boxplot(df):
    """Happiness distribution by year."""
    try:
        fig, ax = plt.subplots()
        sns.boxplot(x="Year", y="Happiness Score", data=df, ax=ax)
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
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
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
        fig, ax = plt.subplots()
        sns.lineplot(data=data, x="Year", y="Rank", hue="Country", marker="o", ax=ax)
        ax.invert_yaxis()
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_country_count(df):
    """Countries reported per year."""
    try:
        count = df.groupby("Year")["Country"].count()
        fig, ax = plt.subplots()
        sns.barplot(x=count.index, y=count.values, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_freedom_vs_happiness(df):
    """Freedom vs Happiness plot."""
    try:
        fig, ax = plt.subplots()
        sns.scatterplot(x="Freedom", y="Happiness Score", data=df, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def kpi_corruption_vs_happiness(df):
    """Corruption vs Happiness plot."""
    try:
        fig, ax = plt.subplots()
        sns.scatterplot(x="Corruption", y="Happiness Score", data=df, ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(e)


def display_dashboard(df):
    """Display all KPIs."""
    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_total_countries(df)
    with col2:
        kpi_total_years(df)
    with col3:
        kpi_average_happiness(df)

    kpi_happiest_country(df)
    kpi_unhappiest_country(df)
    kpi_gdp_vs_happiness(df)
    kpi_yearly_trend(df)
    kpi_top_gdp(df)
    kpi_top_10_latest(df)
    kpi_boxplot(df)
    kpi_heatmap(df)
    kpi_rank_trend(df)
    kpi_country_count(df)
    kpi_freedom_vs_happiness(df)
    kpi_corruption_vs_happiness(df)


def main():
    """Run the dashboard."""
    configure_page()
    st.title("World Happiness Dashboard")
    show_dataset_description()
    df = load_multiple_datasets()
    if df is not None:
        display_dashboard(df)
    else:
        st.info("Upload all CSV files to continue.")


if __name__ == "__main__":
    main()
