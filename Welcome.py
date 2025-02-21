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
video_file = open("assets/Skyfall.mp4", "rb")
video_bytes = video_file.read()
st.video(video_bytes, start_time=75, autoplay=True, loop=True , muted = True)
st.markdown('</div>', unsafe_allow_html=True)

# Page Names, Descriptions, and Icons
pages = [
    ("Track_Map", "Track Map", "Visualize a track map with numbered corners", "🌄", "https://i.pinimg.com/originals/64/a8/08/64a8083d07b8c98923311cbc88fecafe.gif"),
    ("Laptimes_Distribution", "Laptimes Distribution", "Analyze driver lap time distributions", "📉", "https://i.pinimg.com/originals/f2/8b/62/f28b62e3c73e0991d51e6c0dcb412360.gif"),
    ("Laptimes_Scatterplot", "Laptimes Scatterplot", "Plot lap times on a scatter plot", "🔀", "https://media3.giphy.com/media/326d5iOUoYY8N6uFPm/giphy.gif?cid=6c09b952i2u8rsaik85mq657uu14gw3p7wy8qay51b2hruqn&ep=v1_gifs_search&rid=giphy.gif&ct=g"),
    ("Plot_Styling", "Plot Styling", "Customize driver-specific plot styles", "🎨", "https://i.makeagif.com/media/12-28-2020/pmz0zh.gif"),
    ("Gear_Shift_Analysis", "Gear Shift Analysis", "Examine gear shifts during the fastest lap", "🚜", "https://i.gifer.com/embedded/download/3UA6.gif"),
    ("Speed_Overlay", "Speed Overlay", "Compare speed traces of two laps", "💨", "https://wallpapercave.com/wp/wp2856136.gif"),
    ("Standings_Heatmap", "Standings Heatmap", "Visualize driver standings in a heatmap", "📊", "https://i.pinimg.com/originals/8d/ba/39/8dba397fbba5800b488b36659a87854c.gif"),
    ("Speed_+_Corners", "Speed + Corners", "Plot speed traces with corner data", "🏁", "https://i.makeagif.com/media/4-18-2017/zn-bXZ.gif"),
    ("Position_Changes", "Position Changes", "Track position changes during a race", "🏎️", "https://giffiles.alphacoders.com/144/14449.gif"),
    ("Qualifying_Results", "Qualifying Results", "View qualifying results overview", "🏆", "https://i.pinimg.com/originals/c9/bc/98/c9bc987940c4fca69fc9047ebbd61e9c.gif"),
    ("Speed_on_Track", "Speed on Track", "Visualize speed on the track map", "🚀", "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/045656e1-2048-4b39-9f99-ea5eb41d9651/dgr2gme-0a4fae1d-9c31-454d-8f36-b01ff59b8958.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzA0NTY1NmUxLTIwNDgtNGIzOS05Zjk5LWVhNWViNDFkOTY1MVwvZGdyMmdtZS0wYTRmYWUxZC05YzMxLTQ1NGQtOGYzNi1iMDFmZjU5Yjg5NTguZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.QM9Df82jqvMQ4E7Y7gjzlZeT0WFfwsiQsminKTGTQgk"),
    ("Team_Pace_Comparison", "Team Pace Comparison", "Compare pace between teams", "💡", "https://i.pinimg.com/originals/62/39/4d/62394d753859943e6a1a36443ef78795.gif"),
    ("Tyre_Strategies", "Tyre Strategies", "Analyze tyre strategies during a race", "💧", "https://i.pinimg.com/originals/41/7b/36/417b36f9e1c45c496505d5e45a20c1d9.gif"),
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