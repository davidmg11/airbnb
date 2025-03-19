import streamlit as st
import pandas as pd
import plotly.express as px

# 1º: Set up title with your name
st.title("David's Airbnb Dashboard")

# 2º: Load the CSV file
df = pd.read_csv("airbnb.csv").dropna(subset=["price", "number_of_reviews", "reviews_per_month", "room_type", "neighbourhood", "neighbourhood_group"])

# 3º: Sidebar for filtering data
st.sidebar.header("Filters")
neighborhood_group = st.sidebar.multiselect("Select Neighborhood Group", df["neighbourhood_group"].unique(), default=df["neighbourhood_group"].unique())
listing_type = st.sidebar.multiselect("Select Listing Type", df["room_type"].unique(), default=df["room_type"].unique())
max_price = st.sidebar.slider("Select Maximum Price", min_value=int(df["price"].min()), max_value=int(df["price"].max()), value=int(df["price"].max()/2))

filtered_df = df[(df["neighbourhood_group"].isin(neighborhood_group)) & 
                 (df["room_type"].isin(listing_type)) & 
                 (df["price"] <= max_price)]

# 4º: Create tabs for the dashboard
tab1, tab2 = st.tabs(["Graphs", "Detailed Analysis"])

# Tab 1: Graphs
with tab1:
    st.subheader("Listing Type and Number of People")
    fig1 = px.histogram(filtered_df, x="room_type", title="Distribution of Listing Types")
    st.plotly_chart(fig1)
    
    st.subheader("Price by Listing Type")
    fig2 = px.box(filtered_df, x="room_type", y="price", title="Price Distribution by Listing Type")
    st.plotly_chart(fig2)
    
    st.subheader("Top Neighborhoods by Reviews per Month")
    top_reviews = filtered_df.groupby("neighbourhood")["reviews_per_month"].mean().reset_index()
    fig3 = px.bar(top_reviews, x="neighbourhood", y="reviews_per_month", title="Average Reviews per Month by Neighborhood")
    st.plotly_chart(fig3)
    
    st.subheader("Number of Reviews vs. Price")
    fig4 = px.scatter(filtered_df, x="number_of_reviews", y="price", title="Number of Reviews vs. Price")
    st.plotly_chart(fig4)

# Tab 2: Detailed Analysis
with tab2:
    st.write("Detailed Analysis of Filtered Data")
    st.dataframe(filtered_df[["name", "neighbourhood", "price", "number_of_reviews", "reviews_per_month"]])

# 5º: Price Recommendation Simulator
st.sidebar.header("Price Recommendation Simulator")
sim_neigh = st.sidebar.selectbox("Neighborhood", df["neighbourhood"].unique())
sim_type = st.sidebar.selectbox("Room Type", df["room_type"].unique())
sim_people = st.sidebar.slider("Number of People", min_value=1, max_value=10, value=2)

recommended_price = df[(df["neighbourhood"] == sim_neigh) & (df["room_type"] == sim_type)]["price"].median()
st.sidebar.write(f"Suggested Price Range: ${recommended_price - 10} - ${recommended_price + 10}")
