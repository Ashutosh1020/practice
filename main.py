import streamlit as st
import pandas as pd

from Processor import load_data, clean_data, generate_summary, incidents_by_category, incidents_by_time

# Load and preprocess data
file_path = "crime.csv"
df = clean_data(load_data(file_path))

# Streamlit app
st.title("Crime Data Analysis and Visualization")
st.sidebar.header("Filters")

# Sidebar filters
city_filter = st.sidebar.multiselect("City", options=df['city'].dropna().unique(), default=None)
state_filter = st.sidebar.multiselect("State", options=df['state'].dropna().unique(), default=None)

# Apply filters
filtered_df = df[(df['city'].isin(city_filter)) & (df['state'].isin(state_filter))] if city_filter or state_filter else df

# Summary statistics
st.header("Summary Statistics")
summary = generate_summary(filtered_df)
st.write(f"Total Incidents: {summary['total_incidents']}")
st.write(f"Most Common Incident: {summary['most_common_incident']}")
st.write(f"Peak Hour: {summary['peak_hour']}")
st.write(f"Peak Day: {summary['peak_day']}")

# Visualization: Incidents by Time
st.header("Incidents by Time")
hourly, daily = incidents_by_time(filtered_df)
st.bar_chart(hourly, use_container_width=True)
st.bar_chart(daily, use_container_width=True)

# Visualization: Incidents by Category
st.header("Incidents by Category")
category_counts = incidents_by_category(filtered_df)
st.bar_chart(category_counts, use_container_width=True)

# Geospatial Visualization
st.header("Geospatial Analysis")
map_data = filtered_df[['latitude', 'longitude']].dropna()
st.map(map_data)
