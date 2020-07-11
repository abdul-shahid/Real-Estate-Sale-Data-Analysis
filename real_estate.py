#!/usr/bin/env python
# coding: utf-8


import pickle
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly as plt


with open("allListings3.obj", "rb") as f:
    df = pickle.load(f)

st.title("Real Estate Sales in Ontario (2020)")
st.markdown(
"""
This is a demo of interacting with sold listings in Ontario from January 2020 - July 2020
""")
# map of all sales
st.map(df)

# Create a multi-select dropdown with sorted list of cities
cities = sorted(list(set([city for city in df["City"]])))
selected = set(st.multiselect("Cities", cities, default=["Toronto", "Brampton"]))

if len(selected) > 0:
    # filter by selected cities
    df = df[df["City"].isin(selected)]
    # Show price slider and Filter by selected price
    m, mm = min(df["Sold Price"]), max(df["Sold Price"])
    sp, ssp = st.slider("Sold Price", m, mm, (m,mm))
    df = df[((df["Sold Price"] >= sp) & (df["Sold Price"] <= ssp))]

    # Scatter plot: difference vs list price
    df["Difference"] = df["Sold Price"] - df["List Price"]
    fig = px.scatter(df, x="List Price", y="Difference", color="City",
        trendline="ols", hover_data=['Sold Price', 'List Price'],
        title="List Price vs Difference in Sold Price and List Price")
    fig.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white')
    st.write(fig)

    # Box plot: Sale price vs Building Type
    fig = px.box(df, x="Building Type", y="Sold Price",
        color="City", hover_data=['Sold Price'], title="Sale Price by Building Type")
    fig.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white')
    st.write(fig)

    # Group by city and date and get the average sale price
    sold_prices_by_city_month = df.groupby(['City','Sold Date'])['Sold Price'].mean()
    cities = [o[0] for o in sold_prices_by_city_month.index]
    dates = [o[1] for o in sold_prices_by_city_month.index]
    dff = pd.DataFrame()
    dff["Average Sale Price"] = sold_prices_by_city_month
    dff['City'] = cities
    dff['Date'] = dates

    # Line Chart: Date vs average Sale price
    fig = px.line(dff, x="Date", y="Average Sale Price", color="City")
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    )
)
    st.write(fig)
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
