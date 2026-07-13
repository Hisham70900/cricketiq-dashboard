import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Team Analysis",
    page_icon="🏆",
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

st.title("🏆 Team Analysis")
st.write("Explore team performance, top batters and bowling statistics.")

st.markdown("---")

# =====================================
# TEAM SELECTION
# =====================================

teams = sorted(df["batting_team"].dropna().unique())

selected_team = st.selectbox(
    "🏏 Select Team",
    teams
)

team_df = df[df["batting_team"] == selected_team]

# =====================================
# TEAM METRICS
# =====================================

runs = int(team_df["runs_batter"].sum())
wickets = int(team_df["bowler_wicket"].sum())
matches = int(team_df["match_id"].nunique())
players = int(team_df["batter"].nunique())

st.subheader(f"📈 {selected_team} Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Runs", runs)
c2.metric("🎯 Wickets", wickets)
c3.metric("🏟 Matches", matches)
c4.metric("👥 Players", players)

st.markdown("---")

# =====================================
# TOP BATTERS
# =====================================

top_batsmen = (
    team_df.groupby("batter")["runs_batter"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_batsmen.columns = ["Player", "Runs"]

fig = px.bar(
    top_batsmen,
    x="Player",
    y="Runs",
    text="Runs",
    color="Runs",
    color_continuous_scale="Oranges",
    height=500
)

fig.update_layout(
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    margin=dict(l=20, r=20, t=20, b=20)
)

fig.update_traces(textfont_size=16)

st.markdown(
    """
    <div style="padding-left:15px;">
        <h2 style="color:white;">🏏 Top Batters</h2>
    </div>
    """,
    unsafe_allow_html=True
)

left, right = st.columns([1, 2])

with left:

    st.dataframe(
        top_batsmen,
        use_container_width=True,
        height=500
    )

    csv = top_batsmen.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Team Statistics",
        csv,
        "team_statistics.csv",
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
# RUN DISTRIBUTION
# =====================================

fig2 = px.pie(
    top_batsmen,
    names="Player",
    values="Runs",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig2.update_layout(
    paper_bgcolor="#162447",
    plot_bgcolor="#162447",
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
    team_df.groupby("bowler")["bowler_wicket"]
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
    height=500
)

fig3.update_layout(
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