import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd
import io
import fastf1
import fastf1.plotting

# Set page configuration
st.set_page_config(layout="wide", page_title="F1 Strategy Visualization", page_icon="🏎️")

# Enable Matplotlib patches for plotting timedelta values and load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

st.title("🏎️ F1 Strategy Visualization")

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])

if "strategy_plot_img_buf" not in st.session_state:
    st.session_state.strategy_plot_img_buf = None

with col_input:
    st.write("### Select F1 Session")
    year = st.selectbox("Year", list(range(2018, 2025)), index=4)
    grand_prix = st.text_input("Grand Prix (e.g., Hungary)", "Hungary")
    session_type = st.selectbox("Session Type", ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'], index=7)

    if st.button("Generate Plot"):
        with st.spinner("Generating plot..."):
            progress_bar = st.progress(10)
            try:
                session = fastf1.get_session(year, grand_prix, session_type)
                session.load()
                laps = session.laps
                drivers = session.drivers
                drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]

                stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
                stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
                stints = stints.rename(columns={"LapNumber": "StintLength"})

                fig, ax = plt.subplots(figsize=(5, 10))

                for driver in drivers:
                    driver_stints = stints.loc[stints["Driver"] == driver]
                    previous_stint_end = 0
                    for idx, row in driver_stints.iterrows():
                        compound_color = fastf1.plotting.get_compound_color(row["Compound"], session=session)
                        plt.barh(
                            y=driver,
                            width=row["StintLength"],
                            left=previous_stint_end,
                            color=compound_color,
                            edgecolor="black",
                            fill=True
                        )
                        previous_stint_end += row["StintLength"]

                plt.title(f"{year} {grand_prix} Grand Prix Strategies")
                plt.xlabel("Lap Number")
                plt.grid(False)
                ax.invert_yaxis()
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                plt.tight_layout()

                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches="tight")
                buf.seek(0)

                st.session_state.strategy_plot_img_buf = buf

                progress_bar.progress(100)
                st.success("Graph generated successfully!")

            except Exception as e:
                st.error(f"Failed to generate plot: {e}")
                st.session_state.strategy_plot_img_buf = None

if st.session_state.strategy_plot_img_buf:
    with col_graph:
        st.image(st.session_state.strategy_plot_img_buf)

    st.download_button(
        label="📥 Download Graph",
        data=st.session_state.strategy_plot_img_buf,
        file_name=f"strategy_plot_{year}_{grand_prix}_{session_type}.png",
        mime="image/png"
    )
