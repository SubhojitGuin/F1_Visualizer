import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import fastf1
import fastf1.plotting
import pandas as pd
from matplotlib.collections import LineCollection
import matplotlib as mpl
import io

# Set page configuration
st.set_page_config(layout="wide", page_title="F1 Speed On Track Visualization", page_icon="🏁")

st.title("🏁 F1 Speed On Track Visualization")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

colormap = mpl.cm.plasma

if "session" not in st.session_state:
    st.session_state.session = None
    st.session_state.drivers = []
    st.session_state.svot_image = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2026)), index=3)
    wknd = st.number_input("Weekend Round", min_value=1, max_value=23, value=9)
    ses = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=0)

    if st.button("Load Session"):
        with st.spinner("Loading session data..."):
            try:
                session = fastf1.get_session(year, wknd, ses)
                session.load()
                st.session_state.session = session
                st.session_state.drivers = pd.unique(session.laps['Driver'])
                st.success("Session loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load session data: {e}")

    if st.session_state.session:
        driver = st.selectbox("Select Driver", st.session_state.drivers, key="driver")

        if st.button("Generate Plot"):
            session = st.session_state.session
            with st.spinner("Generating plot..."):
                try:
                    weekend = session.event
                    lap = session.laps.pick_driver(driver).pick_fastest()
                    x = lap.telemetry['X']
                    y = lap.telemetry['Y']
                    color = lap.telemetry['Speed']
                    points = np.array([x, y]).T.reshape(-1, 1, 2)
                    segments = np.concatenate([points[:-1], points[1:]], axis=1)
                    
                    # We create a plot with title and adjust some setting to make it look good.
                    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
                    fig.suptitle(f'{weekend.name} {year} - {driver} - Speed', size=24, y=0.97)

                    # Adjust margins and turn of axis
                    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
                    ax.axis('off')


                    # After this, we plot the data itself.
                    # Create background track line
                    ax.plot(lap.telemetry['X'], lap.telemetry['Y'],
                            color='black', linestyle='-', linewidth=16, zorder=0)

                    

                    # Create a continuous norm to map from data points to colors
                    norm = plt.Normalize(color.min(), color.max())
                    lc = LineCollection(segments, cmap=colormap, norm=norm,
                                        linestyle='-', linewidth=5)

                    # Set the values used for colormapping
                    lc.set_array(color)

                    # Merge all line segments together
                    line = ax.add_collection(lc)


                    # Finally, we create a color bar as a legend.
                    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
                    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
                    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap,
                                                    orientation="horizontal")
                    
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches="tight")
                    buf.seek(0)
                    st.session_state.svot_image = buf
                    st.success("Graph generated successfully! 🎉")
                except Exception as e:
                    st.error(f"Failed to generate plot: {e}")
                    st.session_state.svot_image = None

if st.session_state.svot_image:
    with col_graph:
        st.image(st.session_state.svot_image, use_container_width=True)
    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.svot_image,
        file_name=f"F1_{year}_{ses}_{driver}_speed_on_track.png",
        mime="image/png"
    )
