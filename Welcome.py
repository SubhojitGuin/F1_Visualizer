import streamlit as st
from streamlit_javascript import st_javascript


st.set_page_config(page_title="F1 Car Stats Visualizer", page_icon="🏎️", layout="wide")

# Detect light or dark mode
# is_dark_mode = st.get_option("theme.base") == "dark"


# Get the current theme
st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")
print(st_theme)

# Store the theme in session state to trigger a refresh
if "theme" not in st.session_state:
    st.session_state.theme = st_theme
elif st.session_state.theme != st_theme:
    st.session_state.theme = st_theme
    st.rerun()  # Forces a refresh when theme changes

# Define colors based on theme
if st.session_state.theme == "dark":
    card_bg_color = "rgb(252, 250, 250)"
    card_text_color = "rgb(10, 10, 0)"
    card_shadow = "rgb(188, 59, 64)"
else:
    card_bg_color = "rgb(252, 250, 250)"
    card_text_color = "rgb(10, 10, 0)"
    card_shadow = "rgb(188, 59, 64)"


# # Custom CSS for Horizontal Card Slider with Light/Dark Mode Support
# card_bg_color = "rgb(174, 246, 244)"
# card_text_color = "rgb(10, 10, 0)" #if is_dark_mode else "#333333"
# card_shadow = "rgba(9, 131, 238, 1)"

st.markdown(
    f"""
    <style>
    .title {{ text-align: center; font-size: 36px; font-weight: bold; color: #ff1e00; margin-bottom: 20px; }}
    .description {{ text-align: center; font-size: 18px; color: #666; margin-bottom: 30px; }}
    .video-container {{ display: flex; justify-content: center; margin-bottom: 30px; }}
    .container {{ overflow: auto; display: flex; scroll-snap-type: x mandatory; width: 90%; margin: 0 auto; padding: 0 15px; }}
    .card {{ background: {card_bg_color}; box-shadow: 0 8px 32px 0 {card_shadow}; backdrop-filter: blur(7px); -webkit-backdrop-filter: blur(7px); border-radius: 10px; padding: 2rem; margin: 1rem; min-width: 300px; cursor: pointer; transition: transform 0.3s ease; color: {card_text_color}; text-align: center; }}
    .card:hover {{ transform: translateY(-5px); }}
    .container:hover > :not(:hover) {{ opacity: 0.2; }}
    .title-text {{ font-size: 16px; font-weight: bold; margin-top: 8px; }}
    .card-description {{ font-size: 12px; margin-top: 4px; }}
    .card-image {{ width: 60px; height: 60px; object-fit: contain; margin-bottom: 8px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">🏎️ F1 Car Stats Visualizer</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="description">Explore interactive visualizations of Formula 1 car statistics and race insights.</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="video-container">', unsafe_allow_html=True)
st.video("https://www.youtube.com/watch?v=L2bTZKHmDtE")
st.markdown('</div>', unsafe_allow_html=True)

# Page Names, Descriptions, and Icons
pages = [
    ("Draw_a_track_map_with_numbered_corners", "Track Map", "Visualize a track map with numbered corners", "🌄"),
    ("Driver_Laptimes_Distribution_Visualization", "Laptimes Distribution", "Analyze driver lap time distributions", "📉"),
    ("Driver_Laptimes_Scatterplot", "Laptimes Scatterplot", "Plot lap times on a scatter plot", "🔀"),
    ("Driver_specific_plot_styling", "Plot Styling", "Customize driver-specific plot styles", "🎨"),
    ("Fastest_lap_gear_shift", "Gear Shift Analysis", "Examine gear shifts during the fastest lap", "🚜"),
    ("Overlay_speed_traces_of_two_laps", "Speed Overlay", "Compare speed traces of two laps", "💨"),
    ("Plot_driver_standings_in_a_heatmap", "Standings Heatmap", "Visualize driver standings in a heatmap", "📊"),
    ("Plot_speed_traces_with_corner_annotations", "Speed + Corners", "Plot speed traces with corner data", "🏁"),
    ("Position_changes_during_a_race", "Position Changes", "Track position changes during a race", "🏎️"),
    ("Qualifying_results_overview", "Qualifying Results", "View qualifying results overview", "🏆"),
    ("Speed_visualization_on_track_map", "Speed on Track", "Visualize speed on the track map", "🚀"),
    ("Team_pace_comparison", "Team Pace Comparison", "Compare pace between teams", "💡"),
    ("Tyre_strategies_during_a_race", "Tyre Strategies", "Analyze tyre strategies during a race", "💧"),
]

st.markdown('<div class="container">', unsafe_allow_html=True)

for page, title, description, icon in pages:
    page_url = f"/{page}"
    card_html = f"""
    <a href="{page_url}" style="text-decoration: none; color: inherit;" target="_self">
        <div class="card">
            <div class="title-text">{icon} {title}</div>
            <div class="card-description">{description}</div>
        </div>
    </a>
    """
    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)