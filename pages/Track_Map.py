import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import fastf1
import io

# Set page configuration
st.set_page_config(layout="wide", page_title="F1 Circuit Map Plot", page_icon="🏎️")

st.title("F1 Circuit Map Plot")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "circuit_map_img_buf" not in st.session_state:
    st.session_state.circuit_map_img_buf = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=5)
    gp = st.text_input("Grand Prix (e.g., Silverstone)", "Silverstone")
    session_type = st.selectbox("Session Type", ["R", "Q", "FP1", "FP2", "FP3"], index=1)

    if st.button("Generate Circuit Map"):
        with st.spinner("Loading session data..."):
            progress_bar = st.progress(10)
            try:
                session = fastf1.get_session(year, gp, session_type)
                session.load()
                progress_bar.progress(40)

                lap = session.laps.pick_fastest()
                pos = lap.get_pos_data()
                circuit_info = session.get_circuit_info()

                def rotate(xy, *, angle):
                    rot_mat = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
                    return np.matmul(xy, rot_mat)

                track = pos.loc[:, ('X', 'Y')].to_numpy()
                track_angle = circuit_info.rotation / 180 * np.pi
                rotated_track = rotate(track, angle=track_angle)

                fig, ax = plt.subplots(figsize=(8, 8))
                ax.plot(rotated_track[:, 0], rotated_track[:, 1])

                offset_vector = [500, 0]
                for _, corner in circuit_info.corners.iterrows():
                    txt = f"{corner['Number']}{corner['Letter']}"
                    offset_angle = corner['Angle'] / 180 * np.pi
                    offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
                    text_x = corner['X'] + offset_x
                    text_y = corner['Y'] + offset_y
                    text_x, text_y = rotate([text_x, text_y], angle=track_angle)
                    track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

                    ax.scatter(text_x, text_y, color='grey', s=140)
                    ax.plot([track_x, text_x], [track_y, text_y], color='grey')
                    ax.text(text_x, text_y, txt, va='center_baseline', ha='center', size='small', color='white')

                ax.set_title(session.event['Location'])
                ax.set_xticks([])
                ax.set_yticks([])
                ax.axis('equal')

                progress_bar.progress(80)

                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight")
                img_buf.seek(0)

                st.session_state.circuit_map_img_buf = img_buf

                progress_bar.progress(100)
                st.success("Circuit Map generated successfully! 🎉")

            except Exception as e:
                st.error(f"Failed to load session data: {e}")
                progress_bar.progress(0)

if st.session_state.circuit_map_img_buf:
    with col_graph:
        st.image(st.session_state.circuit_map_img_buf)
    st.download_button(
        label="📥 Download Circuit Map",
        data=st.session_state.circuit_map_img_buf,
        file_name=f"F1_Circuit_Map_{year}_{gp}.png",
        mime="image/png",
    )