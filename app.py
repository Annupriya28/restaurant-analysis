import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data

df = pd.read_csv("cleaned_data/cleaned_zomato_data.csv")


# Clean column names
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# Debug line
st.write("Columns in the dataset:", df.columns.tolist())

# Now this will work
st.metric("Average Rating", round(df['aggregate_rating'].mean(), 2))


# Sidebar - Filters
st.sidebar.title("Filter Restaurants")
cities = df['city'].dropna().unique()
selected_city = st.sidebar.selectbox("Select City", sorted(cities))

cuisines = df['cuisines'].dropna().unique()
selected_cuisine = st.sidebar.selectbox("Select Cuisine", sorted(cuisines))

# Filtered Data
filtered_df = df[(df['city'] == selected_city) & (df['cuisines'].str.contains(selected_cuisine, case=False))]

# Title
st.title("🍽️ Restaurant Data Dashboard")

# Top Metrics
st.metric("Total Restaurants", df.shape[0])
st.metric("Total Votes", int(df['votes'].sum()))
st.metric("Average Rating", round(df['aggregate_rating'].mean(), 2))

# Chart 1: Top 10 Cities
st.subheader("🏙️ Top 10 Cities by Number of Restaurants")
top_cities = df['city'].value_counts().head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_cities.values, y=top_cities.index, ax=ax1, hue=None, legend=False)
st.pyplot(fig1)

# Chart 2: Top 10 Cuisines
st.subheader("🍜 Top 10 Most Common Cuisines")
top_cuisines = df['cuisines'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_cuisines.values, y=top_cuisines.index, ax=ax2, hue=None, legend=False)
st.pyplot(fig2)


# Chart 3: Online Delivery Pie
st.subheader("🛵 Online Delivery Availability")
delivery = df['has_online_delivery'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(delivery, labels=['No', 'Yes'], autopct='%1.1f%%', startangle=90, explode=(0, 0.1), shadow=True)
ax3.axis('equal')
st.pyplot(fig3)

# Table: Top Rated Restaurants
st.subheader("⭐ Top Rated Restaurants")
top_rated = df[df['aggregate_rating'] >= 4.5]
st.dataframe(top_rated[['restaurant_name', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']])

# Optional Scatter Plot
st.subheader("💸 Rating vs Cost Scatter Plot")
fig4, ax4 = plt.subplots()
sns.scatterplot(data=df, x='aggregate_rating', y='average_cost_for_two', hue='price_range', ax=ax4, palette='viridis')
st.pyplot(fig4)
