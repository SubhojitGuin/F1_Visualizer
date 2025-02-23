import streamlit as st
import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting
import io

# Set page configuration
st.set_page_config(layout="wide", page_title="F1 Driver Position Plot", page_icon="🏎️")

# Set up FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

st.title("F1 Driver Position Plot")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

# Initialize session state variables
if "pcdr_img_buf" not in st.session_state:
    st.session_state.pcdr_img_buf = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=3)
    gp = st.text_input("Grand Prix (e.g., Monaco)", "Monaco")
    identifier = st.selectbox("Session Type", ["R", "Q", "FP1", "FP2", "FP3"], index=0)

    if st.button("Generate Plot"):
        with st.spinner("Loading session data..."):
            progress_bar = st.progress(10)
            try:
                session = fastf1.get_session(year, gp, identifier)
                session.load(telemetry=False, weather=False)
                progress_bar.progress(40)

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

                progress_bar.progress(80)
                
                # Save figure for persistent display and download
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight")
                img_buf.seek(0)

                # Store in session state
                st.session_state.pcdr_img_buf = img_buf

                progress_bar.progress(100)
                st.success("Graph generated successfully! 🎉")
            
            except Exception as e:
                st.error(f"Failed to load session data: {e}")
                progress_bar.progress(0)


if st.session_state.pcdr_img_buf:
    with col_graph:
            st.image(st.session_state.pcdr_img_buf)
    # Download button (Remains visible)
    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.pcdr_img_buf,
        file_name=f"F1_Driver_Position_{year}.png",
        mime="image/png",
    )
