import streamlit as st
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import io
import fastf1
import fastf1.plotting

# Set page configuration
st.set_page_config(layout="wide", page_title="F1 Laptimes Visualization", page_icon="🏎️")

# Enable Matplotlib patches for plotting timedelta values and load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

st.title("🏎️ F1 Laptimes Visualization")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "laptime_plot_img_buf" not in st.session_state:
    st.session_state.laptime_plot_img_buf = None
if "dlc_drivers" not in st.session_state:
    st.session_state.dlc_drivers = []

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=5)
    grand_prix = st.text_input("Grand Prix (e.g., Azerbaijan)", "Azerbaijan")
    session_type = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=7)

    if st.button("Load Session"):
        with st.spinner("Loading session data..."):
            progress_bar = st.progress(10)
            try:
                race = fastf1.get_session(year, grand_prix, session_type)
                race.load()
                progress_bar.progress(50)

                st.session_state.session = race
                st.session_state.dlc_drivers = pd.unique(race.laps['Driver'])

                progress_bar.progress(100)
                st.success("Session loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load session data: {e}")
                st.session_state.session = None

    if st.session_state.get("session"):
        driver = st.selectbox("Driver", st.session_state.dlc_drivers)

        if st.button("Generate Plot"):
            with st.spinner("Generating plot..."):
                progress_bar = st.progress(10)
                try:
                    race = st.session_state.session
                    driver_laps = race.laps.pick_driver(driver).pick_quicklaps().reset_index()

                    fig, ax = plt.subplots(figsize=(8, 8))
                    sns.scatterplot(
                        data=driver_laps,
                        x="LapNumber",
                        y="LapTime",
                        ax=ax,
                        hue="Compound",
                        palette=fastf1.plotting.get_compound_mapping(session=race),
                        s=80,
                        linewidth=0,
                        legend='auto'
                    )

                    ax.set_xlabel("Lap Number")
                    ax.set_ylabel("Lap Time")
                    ax.invert_yaxis()
                    plt.suptitle(f"{driver} Laptimes in the {year} {grand_prix} Grand Prix")
                    plt.grid(color='w', which='major', axis='both')
                    sns.despine(left=True, bottom=True)
                    plt.tight_layout()

                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches="tight")
                    buf.seek(0)

                    st.session_state.laptime_plot_img_buf = buf

                    progress_bar.progress(100)
                    st.success("Graph generated successfully!")

                except Exception as e:
                    st.error(f"Failed to generate plot: {e}")
                    st.session_state.laptime_plot_img_buf = None

if st.session_state.laptime_plot_img_buf:
    with col_graph:
        st.image(st.session_state.laptime_plot_img_buf, use_container_width=True)

    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.laptime_plot_img_buf,
        file_name=f"{driver}_{grand_prix}_{year}_{session_type}_laptimes.png",
        mime="image/png"
    )
