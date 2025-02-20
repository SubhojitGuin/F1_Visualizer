import streamlit as st

st.set_page_config(page_title="F1 Car Stats Visualizer", page_icon="🏎️", layout="wide")

card_shadow = "rgba(31, 38, 135, 0.37)"

st.markdown(
    f"""
    <style>
    .title {{ text-align: center; font-size: 36px; font-weight: bold; color: #ff1e00; margin-bottom: 20px; }}
    .description {{ text-align: center; font-size: 18px; color: #666; margin-bottom: 30px; }}
    .video-container {{ display: flex; justify-content: center; margin-bottom: 30px; }}
    .container {{ overflow: auto; display: flex; scroll-snap-type: x mandatory; width: 90%; margin: 0 auto; padding: 0 15px; }}
    .card {{
        background-size: cover;
        background-position: center;
        box-shadow: 0 8px 32px 0 {card_shadow};
        backdrop-filter: blur(7px);
        -webkit-backdrop-filter: blur(7px);
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem;
        min-width: 300px;
        cursor: pointer;
        transition: transform 0.3s ease;
        color: white;
        text-align: center;
        position: relative;
    }}
    .card:hover {{ transform: translateY(-5px); }}
    .container:hover > :not(:hover) {{ opacity: 0.2; }}
    .card-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
    }}
    .title-text {{ font-size: 18px; font-weight: bold; margin-top: 8px; position: relative; z-index: 1; }}
    .card-description {{ font-size: 14px; margin-top: 4px; position: relative; z-index: 1; }}
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
    ("Draw_a_track_map_with_numbered_corners", "Track Map", "Visualize a track map with numbered corners", "🌄", "https://cdni.autocarindia.com/ExtraImages/20201008073109_Nanoli-speedway-Pune-track.jpg"),
    ("Driver_Laptimes_Distribution_Visualization", "Laptimes Distribution", "Analyze driver lap time distributions", "📉", "https://via.placeholder.com/300?text=Track+Map"),
    ("Driver_Laptimes_Scatterplot", "Laptimes Scatterplot", "Plot lap times on a scatter plot", "🔀", "https://via.placeholder.com/300?text=Track+Map"),
    ("Driver_specific_plot_styling", "Plot Styling", "Customize driver-specific plot styles", "🎨", "https://via.placeholder.com/300?text=Track+Map"),
    ("Fastest_lap_gear_shift", "Gear Shift Analysis", "Examine gear shifts during the fastest lap", "🚜", "https://via.placeholder.com/300?text=Track+Map"),
    ("Overlay_speed_traces_of_two_laps", "Speed Overlay", "Compare speed traces of two laps", "💨", "https://via.placeholder.com/300?text=Track+Map"),
    ("Plot_driver_standings_in_a_heatmap", "Standings Heatmap", "Visualize driver standings in a heatmap", "📊", "https://via.placeholder.com/300?text=Track+Map"),
    ("Plot_speed_traces_with_corner_annotations", "Speed + Corners", "Plot speed traces with corner data", "🏁", "https://via.placeholder.com/300?text=Track+Map"),
    ("Position_changes_during_a_race", "Position Changes", "Track position changes during a race", "🏎️", "https://via.placeholder.com/300?text=Track+Map"),
    ("Qualifying_results_overview", "Qualifying Results", "View qualifying results overview", "🏆", "https://via.placeholder.com/300?text=Track+Map"),
    ("Speed_visualization_on_track_map", "Speed on Track", "Visualize speed on the track map", "🚀", "https://via.placeholder.com/300?text=Track+Map"),
    ("Team_pace_comparison", "Team Pace Comparison", "Compare pace between teams", "💡", "https://via.placeholder.com/300?text=Track+Map"),
    ("Tyre_strategies_during_a_race", "Tyre Strategies", "Analyze tyre strategies during a race", "💧", "https://via.placeholder.com/300?text=Track+Map"),
]

st.markdown('<div class="container">', unsafe_allow_html=True)

for page, title, description, icon, image_url in pages:
    page_url = f"/{page}"
    card_html = f"""
    <a href="{page_url}" style="text-decoration: none; color: inherit;" target="_self">
        <div class="card" style="background-image: url('{image_url}');">
            <div class="card-overlay"></div>
            <div class="title-text">{icon} {title}</div>
            <div class="card-description">{description}</div>
        </div>
    </a>
    """
    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)