import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
from matplotlib.collections import LineCollection
import fastf1
import io

# Page configuration
st.set_page_config(layout="wide", page_title="F1 Fastest Lap Visualization", page_icon="🏎️")

st.title("🏎️ Fastest Lap Gear Shift Visualization")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

# Initialize session state variables

if "flgs_img_buf" not in st.session_state:
    st.session_state.flgs_img_buf = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=3)
    grand_prix = st.text_input("Grand Prix (e.g., Austrian Grand Prix)", "Austrian Grand Prix")
    session_type = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=0)

    if st.button("Generate Plot"):
        with st.spinner("Fetching session data..."):
            progress_bar = st.progress(10)
            
            try:
                # Fetch session data
                session = fastf1.get_session(year, grand_prix, session_type)
                session.load()
                progress_bar.progress(30)

                # Extract fastest lap data
                lap = session.laps.pick_fastest()
                tel = lap.get_telemetry()
                progress_bar.progress(50)

                # Process telemetry data
                x = np.array(tel['X'].values)
                y = np.array(tel['Y'].values)
                progress_bar.progress(70)

                points = np.array([x, y]).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                gear = tel['nGear'].to_numpy().astype(float)

                # Create matplotlib figure
                fig, ax = plt.subplots(figsize=(16, 8))
                cmap = colormaps['Paired']
                lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
                lc_comp.set_array(gear)
                lc_comp.set_linewidth(4)

                ax.add_collection(lc_comp)
                ax.axis('equal')
                ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

                plt.suptitle(f"Fastest Lap Gear Shift Visualization\n{lap['Driver']} - {grand_prix} {session.event.year}")

                cbar = plt.colorbar(mappable=lc_comp, ax=ax, label="Gear", boundaries=np.arange(1, 10))
                cbar.set_ticks(np.arange(1.5, 9.5))
                cbar.set_ticklabels(np.arange(1, 9))

                progress_bar.progress(90)

                # Save figure for persistent display and download
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight")
                img_buf.seek(0)

                # # Store in session state
                # st.session_state.fig = fig
                st.session_state.flgs_img_buf = img_buf

                progress_bar.progress(100)
                st.success("Graph generated successfully! 🎉")

            except Exception as e:
                st.error(f"{e}")
                progress_bar.progress(0)

if st.session_state.flgs_img_buf:
        with col_graph:
            st.image(st.session_state.flgs_img_buf)

    # Download button (Remains visible)

        st.download_button(
            label="📥 Download Graph",
            data=st.session_state.flgs_img_buf,
            file_name=f"Fastest_Lap_Gearshift_{year}.png",
            mime="image/png",
        )

   


  
