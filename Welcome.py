import streamlit as st

# Set the title of the app
st.title("F1 Car Stats Visualizer")

# Add a sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.selectbox("Select a page", ["Home", "Car Stats"])

# Home page content

st.header("Welcome to the F1 Car Stats Visualizer")
st.write("""
This application allows you to explore various statistics of Formula 1 cars.
Use the navigation menu to select different pages and view the stats.
""")

video_url = "https://www.youtube.com/watch?v=L2bTZKHmDtE"

st.video(video_url)