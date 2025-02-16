import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
import fastf1
import fastf1.plotting

# Set page configuration
st.set_page_config(layout="wide")

# Enable Matplotlib patches for plotting timedelta values and load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

st.title("F1 Fastest Lap Speed Comparison")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "fig" not in st.session_state:
    st.session_state.fig = None
if "img_buf" not in st.session_state:
    st.session_state.img_buf = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2026)), index=3)
    grand_prix = st.text_input("Grand Prix (e.g., Spanish Grand Prix)", "Spanish Grand Prix")
    session_type = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=0)

    # Initialize session state
    if 'session' not in st.session_state:
        st.session_state.session = None
        st.session_state.drivers = []
        st.session_state.plot_image = None

    if st.button("Load Session"):
        with st.spinner("Loading session data..."):
            try:
                session = fastf1.get_session(year, grand_prix, session_type)
                session.load()
                st.session_state.session = session
                st.session_state.drivers = pd.unique(session.laps['Driver'])
                st.success("Session loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load session data: {e}")

    if st.session_state.session:
        driver1 = st.selectbox("Driver 1", st.session_state.drivers, key="driver1")
        driver2 = st.selectbox("Driver 2", st.session_state.drivers, key="driver2")

        if st.button("Generate Plot"):
            session = st.session_state.session

            with st.spinner("Generating plot..."):
                try:
                    lap1 = session.laps.pick_driver(driver1).pick_fastest()
                    lap2 = session.laps.pick_driver(driver2).pick_fastest()

                    tel1 = lap1.get_car_data().add_distance()
                    tel2 = lap2.get_car_data().add_distance()

                    color1 = fastf1.plotting.get_team_color(lap1['Team'], session=session)
                    color2 = fastf1.plotting.get_team_color(lap2['Team'], session=session)

                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(tel1['Distance'], tel1['Speed'], color=color1, label=driver1)
                    ax.plot(tel2['Distance'], tel2['Speed'], color=color2, label=driver2)

                    ax.set_xlabel('Distance in m')
                    ax.set_ylabel('Speed in km/h')
                    ax.legend()

                    plt.suptitle(f"Fastest Lap Comparison\n{session.event['EventName']} {session.event.year} {session_type}")

                    # Convert plot to image for download
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)

                    st.session_state.plot_image = buf

                    with col_graph:
                        st.pyplot(fig)

                except Exception as e:
                    st.error(f"Failed to generate plot: {e}")

    if st.session_state.plot_image:
        st.download_button(
            label="Download Plot as PNG",
            data=st.session_state.plot_image,
            file_name=f"{grand_prix}_{year}_{session_type}_comparison.png",
            mime="image/png"
        )
