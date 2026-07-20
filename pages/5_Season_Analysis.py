import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Season Analysis",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# LOAD CSS
# =====================================

def load_css():
    with open("style.css") as f:
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

st.title("📅 Season Analysis")

st.write(
    "Explore season-wise statistics, top batters and overall performance."
)

st.markdown("---")

# =====================================
# SELECT SEASON
# =====================================

seasons = sorted(df["season"].dropna().unique())

selected_season = st.selectbox(
    "📅 Select Season",
    seasons
)

season_df = df[df["season"] == selected_season]

# =====================================
# SEASON METRICS
# =====================================

total_runs = int(season_df["runs_batter"].sum())
total_wickets = int(season_df["bowler_wicket"].sum())
matches = int(season_df["match_id"].nunique())
players = int(season_df["batter"].nunique())

st.subheader(f"📊 {selected_season} Season Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Runs", total_runs)
c2.metric("🎯 Wickets", total_wickets)
c3.metric("🏟 Matches", matches)
c4.metric("👥 Players", players)

st.markdown("---")

# =====================================
# TOP BATTERS
# =====================================

top_batsmen = (
    season_df.groupby("batter")["runs_batter"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_batsmen.columns = ["Player", "Runs"]

# =====================================
# BAR CHART
# =====================================

fig = px.bar(
    top_batsmen,
    x="Player",
    y="Runs",
    text="Runs",
    color="Runs",
    color_continuous_scale="Tealgrn",
    height=550
)

fig.update_layout(
    title="",
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(
        tickfont=dict(size=14, color="white")
    ),
    yaxis=dict(
        tickfont=dict(size=14, color="white")
    )
)

fig.update_traces(textfont_size=16)

# =====================================
# TABLE + CHART
# =====================================

st.markdown(
    "<h2 style='color:white;'>🏆 Top Batters</h2>",
    unsafe_allow_html=True
)

left, right = st.columns([1, 2])

with left:

    st.dataframe(
        top_batsmen,
        use_container_width=True,
        height=520
    )

    csv = top_batsmen.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Season Statistics",
        csv,
        "season_statistics.csv",
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
    top_batsmen,
    names="Player",
    values="Runs",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig2.update_layout(
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font_color="white",
    height=600,
    title_font_size=28,
    font=dict(size=18),
    margin=dict(l=20, r=20, t=70, b=20)
)

fig2.update_traces(
    textfont_size=16,
    textinfo="percent+label"
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
# TOP WICKET TAKERS
# =====================================

top_bowlers = (
    season_df.groupby("bowler")["bowler_wicket"]
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
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font_color="white",
    title_font_size=28,
    font=dict(size=18),
    margin=dict(l=20, r=20, t=70, b=20)
)

fig3.update_traces(textfont_size=16)

st.markdown(
    "<h2 style='color:white;'>🎯 Top Wicket Takers</h2>",
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