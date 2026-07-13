import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Venue Analysis",
    page_icon="🏟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# LOAD CSS
# =====================================

def load_css():
    with open(".streamlit/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# =====================================
# LOAD DATA
# =====================================

df = load_data()

# =====================================
# TITLE
# =====================================

st.title("🏟 Venue Analysis")

st.write(
    "Explore venue-wise batting and bowling performance."
)

st.markdown("---")

# =====================================
# VENUE SELECTION
# =====================================

venues = sorted(df["venue"].dropna().unique())

selected_venue = st.selectbox(
    "🏟 Select Venue",
    venues
)

venue_df = df[df["venue"] == selected_venue]

# =====================================
# VENUE METRICS
# =====================================

runs = int(venue_df["runs_batter"].sum())
wickets = int(venue_df["bowler_wicket"].sum())
matches = int(venue_df["match_id"].nunique())
players = int(venue_df["batter"].nunique())

st.subheader(f"📊 {selected_venue}")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Runs", runs)
c2.metric("🎯 Wickets", wickets)
c3.metric("🏟 Matches", matches)
c4.metric("👥 Players", players)

st.markdown("---")

# =====================================
# TOP BATTERS
# =====================================

top_players = (
    venue_df.groupby("batter")["runs_batter"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_players.columns = ["Player", "Runs"]

# =====================================
# BAR CHART
# =====================================

fig = px.bar(
    top_players,
    x="Player",
    y="Runs",
    text="Runs",
    color="Runs",
    color_continuous_scale="Earth",
    height=550
)

fig.update_layout(
    title="",
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    margin=dict(l=20, r=20, t=20, b=20)
)

fig.update_traces(textfont_size=16)

# =====================================
# TABLE + CHART
# =====================================

st.markdown(
    "<h2 style='color:white;'>🏏 Top Batters</h2>",
    unsafe_allow_html=True
)

left, right = st.columns([1,2])

with left:

    st.dataframe(
        top_players,
        use_container_width=True,
        height=520
    )

    csv = top_players.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Venue Statistics",
        csv,
        "venue_statistics.csv",
        "text/csv"
    )

with right:

    st.plotly_chart(
       fig,
       use_container_width=True,
       config={"displayModeBar": False}
    )  

st.markdown("---")

# =====================================
# DONUT CHART
# =====================================

fig2 = px.pie(
    top_players,
    names="Player",
    values="Runs",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig2.update_layout(
    title="",
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    legend_font=dict(color="white"),
    height=600,
    margin=dict(l=20, r=20, t=20, b=20)
)

fig2.update_traces(
    textinfo="percent+label",
    textfont_size=16
)
st.markdown(
    "<h2 style='color:white;'>🥧 Run Distribution</h2>",
    unsafe_allow_html=True
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.markdown("---")

# =====================================
# TOP BOWLERS
# =====================================

top_bowlers = (
    venue_df.groupby("bowler")["bowler_wicket"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_bowlers.columns = ["Bowler", "Wickets"]

fig3 = px.bar(
    top_bowlers,
    x="Bowler",
    y="Wickets",
    text="Wickets",
    color="Wickets",
    color_continuous_scale="Reds",
    height=550
)

fig3.update_layout(
    title="",
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    margin=dict(l=20, r=20, t=20, b=20)
)

fig3.update_traces(textfont_size=16)

st.markdown(
    "<h2 style='color:white;'>🎯 Top Bowlers</h2>",
    unsafe_allow_html=True
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.markdown("---")

st.caption(
    "Developed by Mohammad Hisham | Python • Streamlit • Pandas • Plotly"
)