import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import fastf1
import fastf1.plotting
import io

# Page configuration
st.set_page_config(layout="wide", page_title="F1 Qualifying Analysis", page_icon="🏁")

# fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,color_scheme=None)

st.title("🏁 Qualifying results overview")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "qual_img_buf" not in st.session_state:
    st.session_state.qual_img_buf = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=3)
    grand_prix = st.text_input("Grand Prix (e.g., Spanish Grand Prix)", "Spanish Grand Prix")
    session_type = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=0)
    
    if st.button("Generate Plot"):
        with st.spinner("Fetching session data..."):
            progress_bar = st.progress(10)
            
            try:

                session = fastf1.get_session(year, grand_prix, session_type)
                session.load()
                progress_bar.progress(30)

                drivers = pd.unique(session.laps['Driver'])
                list_fastest_laps = []
                
                for drv in drivers:
                    drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
                    list_fastest_laps.append(drvs_fastest_lap)
                
                progress_bar.progress(50)
                fastest_laps = fastf1.core.Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
                pole_lap = fastest_laps.pick_fastest()
                fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']
                
                team_colors = [fastf1.plotting.get_team_color(lap['Team'], session=session) for _, lap in fastest_laps.iterlaps()]
                
                progress_bar.progress(70)
                # Create Matplotlib figure
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
                ax.set_yticks(fastest_laps.index)
                ax.set_yticklabels(fastest_laps['Driver'])
                ax.invert_yaxis()
                ax.set_axisbelow(True)
                ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
                
                lap_time_string = f"{pole_lap['LapTime'].seconds}.{pole_lap['LapTime'].microseconds//1000}"
                plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\nFastest Lap: {lap_time_string} ({pole_lap['Driver']})")
                
                progress_bar.progress(90)
                
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight")
                img_buf.seek(0)
                st.session_state.qual_img_buf = img_buf
                
                progress_bar.progress(100)
                st.success("Graph generated successfully! 🎉")
            
            except Exception as e:
                st.error(f"{e}")
                progress_bar.progress(0)

if st.session_state.qual_img_buf:
    with col_graph:
        st.image(st.session_state.qual_img_buf)
    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.qual_img_buf,
        file_name=f"Fastest_Laps_Qualifying_{year}.png",
        mime="image/png",
    )
