import streamlit as st
import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting

# Set page configuration
st.set_page_config(layout="wide")

# Set up FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

st.title("F1 Driver Position Plot")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(1950, 2026)), index=list(range(1950, 2026)).index(2024))
    gp = st.text_input("Grand Prix (e.g., Monaco)", "Monaco")
    identifier = st.selectbox("Session Type", ["R", "Q", "FP1", "FP2", "FP3"], index=0)

    if st.button("Generate Plot"):
        with st.spinner("Loading session data..."):
            try:
                session = fastf1.get_session(year, gp, identifier)
                session.load(telemetry=False, weather=False)

                fig, ax = plt.subplots(figsize=(10, 6))

                for drv in session.drivers:
                    drv_laps = session.laps.pick_driver(drv)
                    abb = drv_laps['Driver'].iloc[0]
                    style = fastf1.plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=session)

                    ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)

                ax.set_ylim([20.5, 0.5])
                ax.set_yticks([1, 5, 10, 15, 20])
                ax.set_xlabel('Lap')
                ax.set_ylabel('Position')
                ax.legend(bbox_to_anchor=(1.0, 1.02))
                plt.tight_layout()

                with col_graph:
                    st.pyplot(fig)

            except Exception as e:
                st.error(f"Failed to load session data: {e}")