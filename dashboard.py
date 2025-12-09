import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.title("Gapminder Mini Dashboard")

file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
else:
    df = px.data.gapminder()
    df = df.rename(columns={
        "pop": "population",
        "gdpPercap": "gdp_cap",
        "lifeExp": "life_exp"
    })

st.write("Preview")
st.dataframe(df.head())

st.subheader("Continent Comparison")
grouped = df.groupby("continent").agg({
    "population": "sum",
    "gdp_cap": "mean",
    "life_exp": "mean"
}).reset_index()

fig_bar = px.bar(
    grouped,
    x="continent",
    y=["population", "gdp_cap", "life_exp"],
    barmode="group",
    title="Population, GDP per Capita & Life Expectancy"
)
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("GDP vs Life Expectancy")
scatter = (
    alt.Chart(df)
    .mark_circle(size=60)
    .encode(
        x="gdp_cap",
        y="life_exp",
        color="continent",
        tooltip=["country", "continent", "gdp_cap", "life_exp"]
    )
    .interactive()
)
st.altair_chart(scatter, use_container_width=True)

st.subheader("Population Trend")
trend = df.groupby(["year", "continent"])["population"].mean().reset_index()

fig_line = px.line(
    trend,
    x="year",
    y="population",
    color="continent",
    markers=True,
    title="Avg Population Trend by Continent"
)
st.plotly_chart(fig_line, use_container_width=True)