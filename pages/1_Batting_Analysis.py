import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="CricketIQ",
    page_icon="🏏",
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

st.title("🏏 Batting Analysis")

st.write(
    "Explore batting performance, top run scorers and detailed player statistics."
)

st.markdown("---")

# =====================================
# PLAYER SEARCH
# =====================================

players = sorted(df["batter"].dropna().unique())

selected_player = st.selectbox(
    "🔍 Search Player",
    players
)

# =====================================
# PLAYER STATISTICS
# =====================================

player_df = df[df["batter"] == selected_player]

runs = int(player_df["runs_batter"].sum())
balls = int(player_df["ball"].count())
matches = int(player_df["match_id"].nunique())

fours = int((player_df["runs_batter"] == 4).sum())
sixes = int((player_df["runs_batter"] == 6).sum())

strike_rate = 0

if balls > 0:
    strike_rate = round((runs / balls) * 100, 2)

st.subheader(f"📈 {selected_player} Statistics")

c1, c2, c3 = st.columns(3)

c1.metric("🏏 Runs", runs)
c2.metric("🏏 Balls", balls)
c3.metric("⚡ Strike Rate", strike_rate)

c4, c5, c6 = st.columns(3)

c4.metric("4️⃣ Fours", fours)
c5.metric("6️⃣ Sixes", sixes)
c6.metric("🏟 Matches", matches)

st.markdown("---")

# =====================================
# TOP BATTERS
# =====================================

top_n = st.slider(
    "Select Number of Top Batters",
    5,
    30,
    10,
    5
)

top_batsmen = (
    df.groupby("batter")["runs_batter"]
      .sum()
      .sort_values(ascending=False)
      .head(top_n)
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
    color_continuous_scale="Greens",
    title="",
    height=600
)

fig.update_layout(
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font_color="white",
    title_font_color="white",
    title_font_size=28,
    font=dict(size=18, color="white"),
)

fig.update_traces(textfont_size=16)

# =====================================
# TABLE + CHART
# =====================================

st.markdown(
    "<h2 style='color:white;'>🏏 Top Run Scorers</h2>",
    unsafe_allow_html=True
)

left, right = st.columns([1,2])

with left:

    st.dataframe(
        top_batsmen,
        use_container_width=True,
        height=520
    )

    csv = top_batsmen.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Batting Statistics",
        csv,
        "top_batters.csv",
        "text/csv"
    )

with right:

    st.plotly_chart(
        fig,
        use_container_width=True
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
    title="",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig2.update_layout(
    title=None,
    paper_bgcolor="#162447",
    plot_bgcolor="#162447",
    font=dict(size=18, color="white"),
    legend_font=dict(color="white"),
    height=600,
    margin=dict(l=20, r=20, t=20, b=20)
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
    use_container_width=True
)

st.markdown("---")

st.caption(
    "Developed by Mohammad Hisham | Python • Streamlit • Pandas • Plotly"
)