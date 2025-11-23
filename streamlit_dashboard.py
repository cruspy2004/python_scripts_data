import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd

# Page configuration
st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

# Title
st.title("📊 Interactive Data Visualization Dashboard")
st.markdown("**Student Name:** Muhammad Haadhee Sheeraz Mian | **Reg No:** 478359")
st.markdown("---")

# Load gapminder dataset
@st.cache_data
def load_data():
    df = px.data.gapminder()
    return df

df = load_data()

# Sidebar for filtering
st.sidebar.header("Filter Options")
year_filter = st.sidebar.slider("Select Year", 
                                 int(df['year'].min()), 
                                 int(df['year'].max()), 
                                 int(df['year'].max()))

# Filter data by year
df_filtered = df[df['year'] == year_filter]

# Calculate continent-wise aggregated data
continent_data = df_filtered.groupby('continent').agg({
    'pop': 'sum',
    'gdpPercap': 'mean',
    'lifeExp': 'mean'
}).reset_index()

continent_data.columns = ['Continent', 'Total Population', 'Avg GDP per Capita', 'Avg Life Expectancy']

# Section 1: Bar Chart - Continent-Wise Comparison
st.header("1️⃣ Continent-Wise Comparison")
st.markdown(f"### Data for Year: **{year_filter}**")

# Create tabs for different metrics
tab1, tab2, tab3 = st.tabs(["📈 Population", "💰 GDP per Capita", "🏥 Life Expectancy"])

with tab1:
    fig_pop = px.bar(continent_data, 
                     x='Continent', 
                     y='Total Population',
                     title=f'Total Population by Continent ({year_filter})',
                     color='Continent',
                     text='Total Population')
    fig_pop.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_pop.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_pop, use_container_width=True)

with tab2:
    fig_gdp = px.bar(continent_data, 
                     x='Continent', 
                     y='Avg GDP per Capita',
                     title=f'Average GDP per Capita by Continent ({year_filter})',
                     color='Continent',
                     text='Avg GDP per Capita')
    fig_gdp.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
    fig_gdp.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_gdp, use_container_width=True)

with tab3:
    fig_life = px.bar(continent_data, 
                      x='Continent', 
                      y='Avg Life Expectancy',
                      title=f'Average Life Expectancy by Continent ({year_filter})',
                      color='Continent',
                      text='Avg Life Expectancy')
    fig_life.update_traces(texttemplate='%{text:.2f} years', textposition='outside')
    fig_life.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_life, use_container_width=True)

st.markdown("---")

# Section 2: Scatter Plot - GDP per Capita vs Life Expectancy (Altair)
st.header("2️⃣ GDP per Capita vs Life Expectancy")
st.markdown(f"### Scatter Plot for Year: **{year_filter}**")

# Create Altair scatter plot
scatter = alt.Chart(df_filtered).mark_circle(size=100).encode(
    x=alt.X('gdpPercap:Q', title='GDP per Capita', scale=alt.Scale(type='log')),
    y=alt.Y('lifeExp:Q', title='Life Expectancy (years)'),
    color=alt.Color('continent:N', title='Continent'),
    size=alt.Size('pop:Q', title='Population', scale=alt.Scale(range=[50, 1000])),
    tooltip=['country', 'gdpPercap', 'lifeExp', 'pop', 'continent']
).properties(
    width=800,
    height=500,
    title=f'GDP per Capita vs Life Expectancy ({year_filter})'
).interactive()

st.altair_chart(scatter, use_container_width=True)

st.markdown("---")

# Section 3: Line Chart - Population Trend by Continent (Plotly)
st.header("3️⃣ Population Trend by Continent")
st.markdown("### Historical Population Growth")

# Calculate continent-wise population over time
continent_trend = df.groupby(['year', 'continent'], as_index=False)['pop'].sum()

# Create line chart
fig_trend = px.line(continent_trend, 
                    x='year', 
                    y='pop',
                    color='continent',
                    title='Population Trend by Continent Over Time',
                    labels={'year': 'Year', 'pop': 'Total Population', 'continent': 'Continent'},
                    markers=True)

fig_trend.update_traces(line=dict(width=3))
fig_trend.update_layout(
    height=500,
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# Additional insights section
st.header("📌 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Highest Life Expectancy",
        value=f"{df_filtered['lifeExp'].max():.1f} years",
        delta=f"{df_filtered[df_filtered['lifeExp'] == df_filtered['lifeExp'].max()]['country'].values[0]}"
    )

with col2:
    st.metric(
        label="Highest GDP per Capita",
        value=f"${df_filtered['gdpPercap'].max():.0f}",
        delta=f"{df_filtered[df_filtered['gdpPercap'] == df_filtered['gdpPercap'].max()]['country'].values[0]}"
    )

with col3:
    st.metric(
        label="Total World Population",
        value=f"{df_filtered['pop'].sum()/1e9:.2f}B",
        delta=f"Year {year_filter}"
    )

# Footer
st.markdown("---")
st.markdown("### 📊 Data Source: Gapminder Dataset")
st.markdown("*This dashboard demonstrates interactive data visualization using Plotly, Altair, and Streamlit.*")
