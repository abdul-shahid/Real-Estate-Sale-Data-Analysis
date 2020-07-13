#!/usr/bin/env python
# coding: utf-8


import pickle
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly as plt
import plotly.graph_objects as go


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

    # Group by city and date and get the median sale price
    sold_prices_by_city_month = df.groupby(['City','Sold Date'])['Sold Price'].median()
    cities = [o[0] for o in sold_prices_by_city_month.index]
    dates = [o[1] for o in sold_prices_by_city_month.index]
    dff = pd.DataFrame()
    dff["Median Sale Price"] = sold_prices_by_city_month
    dff['City'] = cities
    dff['Date'] = dates

    # Line Chart: Date vs Median Sale price
    fig = px.line(dff, x="Date", y="Median Sale Price", color="City", title="Median Sale Price Over Time")
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

    # Median Price vs City
    city_df = df.groupby(['City'])['Sold Price'].median()
    fig = px.bar(city_df, x=city_df.index, y="Sold Price", color=city_df.index,
        title="Median Sale Price per City", labels={
            "x": "City",
            "Sold Price": "Median Sale Price"
        })
    st.write(fig)

    # Median Price vs Building Type
    dff = pd.DataFrame()
    sold_price_by_building = df.groupby(['City', 'Building Type'])['Sold Price'].median()
    dff["Median Sale Price"] = sold_price_by_building
    dff["City"] = [o[0] for o in sold_price_by_building.index]
    dff["Building Type"] = [o[1] for o in sold_price_by_building.index]
    fig = px.bar(dff, x="Building Type", y="Median Sale Price",
         color="City", barmode="group", title="Median Sale Price by Building Type")
    st.write(fig)

    # Number of Units sold
    sold_count_df = pd.DataFrame()
    fig = px.histogram(df, x="City", color="City", title="Units Sold per City")
    st.write(fig)


# Hide streamlit menu
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
