import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
import fastf1
import fastf1.plotting

st.set_page_config(layout="wide", page_title="F1 Lap Time Visualization", page_icon="🏎️")

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

st.title("🏎️ F1 Lap Time Visualization")

col_graph, col_input = st.columns([4, 1])

if "dscps_plot_image" not in st.session_state:
    st.session_state.dscps_plot_image = None
if "dscps_drivers" not in st.session_state:
    st.session_state.dscps_drivers = []
if 'session' not in st.session_state:
    st.session_state.session = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=5)
    grand_prix = st.text_input("Grand Prix (e.g., Azerbaijan)", "Azerbaijan")
    session_type = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=7)

    if st.button("Load Session"):
        with st.spinner("Loading session data..."):
            try:
                session = fastf1.get_session(year, grand_prix, session_type)
                session.load()
                st.session_state.session = session
                st.session_state.dscps_drivers = pd.unique(session.laps['Driver'])
                st.success("Session loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load session data: {e}")

    if st.session_state.session:
        drivers_selected = st.multiselect("Select Drivers", st.session_state.dscps_drivers, default=['PER', 'VER', 'RUS'])
        plot_option = st.radio("Plot Style", ["Basic Plot", "Sorted Legend", "Enhanced Style"])

        if st.button("Generate Plot"):
            session = st.session_state.session
            try:
                fig, ax = plt.subplots(figsize=(10, 6))

                my_styles = [
                    {'color': 'auto', 'linestyle': 'solid', 'linewidth': 5, 'alpha': 0.3},
                    {'color': 'auto', 'linestyle': 'solid', 'linewidth': 1, 'alpha': 0.7}
                ]

                for driver in drivers_selected:
                    laps = session.laps.pick_driver(driver).pick_quicklaps().reset_index()
                    if plot_option == "Enhanced Style":
                        style = fastf1.plotting.get_driver_style(driver, style=my_styles, session=session)
                    else:
                        style = fastf1.plotting.get_driver_style(driver, style=['color', 'linestyle'], session=session)
                    ax.plot(laps['LapNumber'], laps['LapTime'], **style, label=driver)

                ax.set_xlabel("Lap Number")
                ax.set_ylabel("Lap Time")

                if plot_option == "Sorted Legend":
                    fastf1.plotting.add_sorted_driver_legend(ax, session)
                else:
                    ax.legend()

                plt.suptitle(f"Lap Time Comparison\n{grand_prix} {year} {session_type}")

                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches="tight")
                buf.seek(0)
                st.session_state.dscps_plot_image = buf

                st.success("Plot generated successfully!")
            except Exception as e:
                st.error(f"Failed to generate plot: {e}")
                st.session_state.dscps_plot_image = None

if st.session_state.dscps_plot_image:
    with col_graph:
        st.image(st.session_state.dscps_plot_image, use_container_width=True)

    st.download_button(
        label="📥 Download Plot",
        data=st.session_state.dscps_plot_image,
        file_name=f"{grand_prix}_{year}_{session_type}_plot_styling.png",
        mime="image/png"
    )
