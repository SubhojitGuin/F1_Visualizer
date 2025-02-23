import seaborn as sns
from matplotlib import pyplot as plt
import streamlit as st
import fastf1
import fastf1.plotting
import io


# Page Configuration
st.set_page_config(layout="wide", page_title="F1 Driver Laptimes Distibution", page_icon="🏎️")

# FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

st.title("🏎️ F1 Driver Laptimes Distibution")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "dldv_img_buf" not in st.session_state:
    st.session_state.dldv_img_buf = None

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

                point_finishers = session.drivers[:10]
                driver_laps = session.laps.pick_drivers(point_finishers).pick_quicklaps()
                driver_laps = driver_laps.reset_index()
                progress_bar.progress(50)

                finishing_order = [session.get_driver(i)["Abbreviation"] for i in point_finishers]

                # create the figure
                fig, ax = plt.subplots(figsize=(10, 5))

                # Seaborn doesn't have proper timedelta support,
                # so we have to convert timedelta to float (in seconds)
                driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

                sns.violinplot(data=driver_laps,
                            x="Driver",
                            y="LapTime(s)",
                            hue="Driver",
                            inner=None,
                            density_norm="area",
                            order=finishing_order,
                            palette=fastf1.plotting.get_driver_color_mapping(session=session)
                            )

                sns.stripplot(data=driver_laps,
                            x="Driver",
                            y="LapTime(s)",
                            order=finishing_order,
                            hue="Compound",
                            palette=fastf1.plotting.get_compound_mapping(session=session),
                            hue_order=["SOFT", "MEDIUM", "HARD"],
                            linewidth=0,
                            size=4,
                            )

                ax.set_xlabel("Driver")
                ax.set_ylabel("Lap Time(s)")
                ax.invert_yaxis()
                plt.suptitle(f"{year} {grand_prix} Grand Prix Lap Time Distributions")
                plt.grid(color='w', which='major', axis='both')
                sns.despine(left=True, bottom=True)
                plt.tight_layout()

                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches="tight")
                buf.seek(0)

                st.session_state.dldv_img_buf = buf

                progress_bar.progress(100)
                st.success("Graph generated successfully!")

            except Exception as e:
                st.error(f"Failed to generate plot: {e}")
                st.session_state.dldv_img_buf = None

if st.session_state.dldv_img_buf:
    with col_graph:
        st.image(st.session_state.dldv_img_buf, use_container_width=True)

    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.dldv_img_buf,
        file_name=f"{grand_prix}_{year}_{session_type}_laptimes_distribution.png",
        mime="image/png"
    )