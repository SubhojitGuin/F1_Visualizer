import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import fastf1
import fastf1.plotting
import io

# Page configuration
st.set_page_config(layout="wide", page_title="Plot Speed Traces with corner annotations", page_icon="🏁")

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                          color_scheme='fastf1')


st.title("🏁 Plot Speed Traces with corner annotations Overview")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "pstc_img_buf" not in st.session_state:
    st.session_state.pstc_img_buf = None

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

                fastest_lap = session.laps.pick_fastest()
                car_data = fastest_lap.get_car_data().add_distance()

                circuit_info = session.get_circuit_info()
                
                progress_bar.progress(70)
                # Create Matplotlib figure

                team_color = fastf1.plotting.get_team_color(fastest_lap['Team'],
                                            session=session)
                fig, ax = plt.subplots()
                ax.plot(car_data['Distance'], car_data['Speed'],
                        color=team_color, label=fastest_lap['Driver'])

                # Draw vertical dotted lines at each corner that range from slightly below the
                # minimum speed to slightly above the maximum speed.
                v_min = car_data['Speed'].min()
                v_max = car_data['Speed'].max()
                ax.vlines(x=circuit_info.corners['Distance'], ymin=v_min-20, ymax=v_max+20,
                        linestyles='dotted', colors='grey')

                # Plot the corner number just below each vertical line.
                # For corners that are very close together, the text may overlap. A more
                # complicated approach would be necessary to reliably prevent this.
                for _, corner in circuit_info.corners.iterrows():
                    txt = f"{corner['Number']}{corner['Letter']}"
                    ax.text(corner['Distance'], v_min-30, txt,
                            va='center_baseline', ha='center', size='small')

                ax.set_xlabel('Distance in m')
                ax.set_ylabel('Speed in km/h')
                ax.legend()

                # Manually adjust the y-axis limits to include the corner numbers, because
                # Matplotlib does not automatically account for text that was manually added.
                ax.set_ylim([v_min - 40, v_max + 20])
                                    
                progress_bar.progress(90)
                
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight")
                img_buf.seek(0)
                st.session_state.pstc_img_buf = img_buf
                
                progress_bar.progress(100)
                st.success("Graph generated successfully! 🎉")
            
            except Exception as e:
                st.error(f"{e}")
                progress_bar.progress(0)

if st.session_state.pstc_img_buf:
    with col_graph:
        st.image(st.session_state.pstc_img_buf)
    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.pstc_img_buf,
        file_name=f"Plot_Speed_Traces_with_corner_annotations{year}.png",
        mime="image/png",
    )
