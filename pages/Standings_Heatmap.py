import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.io import show
from fastf1.ergast import Ergast
import io

# Page configuration
st.set_page_config(layout="wide", page_title="F1 Heatmap Visualization", page_icon="🏎️")
st.title("🏎️ F1 Season Points Heatmap")

# Initialize session state variables
if "race_results" not in st.session_state:
    st.session_state.race_results = None

if "heatmap_img_buf" not in st.session_state:
    st.session_state.heatmap_img_buf = None

# Create two columns: Graph (Left) | User Input (Right)
col_graph, col_input = st.columns([4, 1])
with col_input:
    st.write("### Select F1 Season")
    year = st.selectbox("Year", list(range(2018, 2025)), index=4)

    if st.button("Generate Visualization"):
        with st.spinner("Fetching race data..."):
            try:
                # Fetch race results
                ergast = Ergast()
                races = ergast.get_race_schedule(year)
                results = []
                
                for rnd, race in races['raceName'].items():
                    temp = ergast.get_race_results(season=year, round=rnd + 1).content[0]
                    sprint = ergast.get_sprint_results(season=year, round=rnd + 1)
                    
                    if sprint.content and sprint.description['round'][0] == rnd + 1:
                        temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
                        temp['points'] = temp['points_x'] + temp['points_y']
                        temp.drop(columns=['points_x', 'points_y'], inplace=True)
                    
                    temp['round'] = rnd + 1
                    temp['race'] = race.removesuffix(' Grand Prix')
                    temp = temp[['round', 'race', 'driverCode', 'points']]
                    results.append(temp)
                
                results = pd.concat(results)
                races = results['race'].drop_duplicates()
                results = results.pivot(index='driverCode', columns='round', values='points')
                results['total_points'] = results.sum(axis=1)
                results = results.sort_values(by='total_points', ascending=False)
                results.drop(columns='total_points', inplace=True)
                results.columns = races
                
                # Store results in session state
                st.session_state.race_results = results
                st.success("Graph generated successfully! 🎉")

            except Exception as e:
                st.error(f"Error fetching data: {e}")

# Visualization Section
if st.session_state.race_results is not None:
    with col_graph:
        fig = px.imshow(
            st.session_state.race_results,
            text_auto=True,
            aspect='auto',
            color_continuous_scale=[[0, 'rgb(198, 219, 239)'],
                                    [0.25, 'rgb(107, 174, 214)'],
                                    [0.5, 'rgb(33, 113, 181)'],
                                    [0.75, 'rgb(8, 81, 156)'],
                                    [1, 'rgb(8, 48, 107)']],
            labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'}
            )
        fig.update_xaxes(title_text='')
        fig.update_yaxes(title_text='', tickmode='linear')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False,
            xaxis=dict(side='top'),
            margin=dict(l=0, r=0, b=0, t=0)
        )

        st.plotly_chart(fig , use_container_width=True)

        st.download_button(
        label="📥 Download Graph",
        data=fig.to_image(format="png"),
        file_name=f"Heatmap_{year}.png",
        mime="image/png"
    )
