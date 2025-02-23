import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
import fastf1
import fastf1.plotting
import seaborn as sns

# Set page configuration
st.set_page_config(layout="wide", page_title="F1 Team Pace Comparison", page_icon="🏎️")

# Enable Matplotlib patches for plotting timedelta values and load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

st.title("🏎️ F1 Team Pace Comparison")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "team_pace_img_buf" not in st.session_state:
    st.session_state.team_pace_img_buf = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=3)
    grand_prix = st.text_input("Grand Prix (e.g., Spanish Grand Prix)", "Spanish Grand Prix")
    session_type = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=0)

    if 'session' not in st.session_state:
        st.session_state.session = None

    if st.button("Generate Plot"):
        with st.spinner("Loading session data..."):
            progress_bar = st.progress(10)

            try:
                progress_bar.progress(25)
                session = fastf1.get_session(year, grand_prix, session_type)
                session.load()
                progress_bar.progress(50)
                st.session_state.session = session
                progress_bar.progress(100)
                st.success("Session loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load session data: {e}")

    if st.session_state.session:
        # if st.button("Generate Plot"):
            session = st.session_state.session

            with st.spinner("Generating plot..."):
                progress_bar = st.progress(10)
                try:
                    laps = session.laps.pick_quicklaps()
                    transformed_laps = laps.copy()
                    transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

                    team_order = (
                        transformed_laps[["Team", "LapTime (s)"]]
                        .groupby("Team")
                        .median()["LapTime (s)"]
                        .sort_values()
                        .index
                    )
                    
                    team_palette = {team: fastf1.plotting.get_team_color(team, session=session)
                                    for team in team_order}

                    fig, ax = plt.subplots(figsize=(15, 10))
                    sns.boxplot(
                        data=transformed_laps,
                        x="Team",
                        y="LapTime (s)",
                        hue="Team",
                        order=team_order,
                        palette=team_palette,
                        whiskerprops=dict(color="white"),
                        boxprops=dict(edgecolor="white"),
                        medianprops=dict(color="grey"),
                        capprops=dict(color="white"),
                    )

                    plt.title(f"{session.event['EventName']} {session.event.year} Team Pace Comparison")
                    plt.grid(visible=False)
                    ax.set(xlabel=None)
                    plt.tight_layout()

                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches="tight")
                    buf.seek(0)

                    st.session_state.team_pace_img_buf = buf
                    progress_bar.progress(100)
                    st.success("Graph generated successfully! 🎉")
                except Exception as e:
                    st.error(f"Failed to generate plot: {e}")
                    st.session_state.team_pace_img_buf = None
                    progress_bar.progress(0)

if st.session_state.team_pace_img_buf:
    with col_graph:
        st.image(st.session_state.team_pace_img_buf, use_container_width=True)
    
    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.team_pace_img_buf,
        file_name=f"{grand_prix}_{year}_{session_type}_team_pace.png",
        mime="image/png"
    )
