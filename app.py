import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from utils import load_data

# =====================================
# PAGE CONFIGURATION
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

logo = Image.open("assets/logo.png")

# =====================================
# SIDEBAR
# =====================================

st.sidebar.image(logo, width=120)

st.sidebar.title("🏏 Cricket Analytics")

st.sidebar.markdown("""
### Navigation

🏠 Dashboard

🏏 Batting Analysis

🎯 Bowling Analysis

🏆 Team Analysis

👤 Player Comparison

📅 Season Analysis

🏟 Venue Analysis

📊 Match Insights
""")

st.sidebar.markdown("---")

st.sidebar.success("Built using Python & Streamlit")

# =====================================
# HERO SECTION
# =====================================

col1, col2 = st.columns([1, 4])

with col1:
    st.image(logo, width=150)

with col2:
    st.markdown(
        """
        <div style="padding-top:15px;">
            <div style="
                color:white;
                font-size:64px;
                font-weight:800;
                line-height:1.1;
            ">
            🏏 CricketIQ
            </div>

            <div style="
                color:white;
                font-size:32px;
                font-weight:600;
                margin-top:10px;
            ">
            Interactive IPL Cricket Analytics Dashboard
            </div>

            <div style="
                color:#D9D9D9;
                font-size:22px;
                margin-top:12px;
            ">
            Built using Python • Pandas • Plotly • Streamlit
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================
# DASHBOARD METRICS
# =====================================

total_runs = int(df["runs_batter"].sum())
total_wickets = int(df["bowler_wicket"].sum())
total_players = int(df["batter"].nunique())
total_matches = int(df["match_id"].nunique())

c1,c2,c3,c4 = st.columns(4)

c1.metric("🏏 Total Runs", f"{total_runs:,}")
c2.metric("🎯 Wickets", total_wickets)
c3.metric("👥 Players", total_players)
c4.metric("🏟 Matches", total_matches)

st.markdown("---")

# =====================================
# TEAM OVERVIEW
# =====================================

st.subheader("🏆 Team Overview")

teams = sorted(df["batting_team"].dropna().unique())

selected_team = st.selectbox(
    "Select Team",
    teams
)

team_df = df[df["batting_team"] == selected_team]

left,right = st.columns([1,2])

with left:

    summary = pd.DataFrame({
        "Statistic":[
            "Runs",
            "Wickets",
            "Matches",
            "Players"
        ],
        "Value":[
            int(team_df["runs_batter"].sum()),
            int(team_df["bowler_wicket"].sum()),
            int(team_df["match_id"].nunique()),
            int(team_df["batter"].nunique())
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        height=260
    )

with right:

    top_players = (
        team_df.groupby("batter")["runs_batter"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_players,
        x="batter",
        y="runs_batter",
        text="runs_batter",
        color="runs_batter",
        color_continuous_scale="Blues",
        title=f"Top Batters - {selected_team}",
        height=500
    )

    fig.update_layout(
        plot_bgcolor="#162447",
        paper_bgcolor="#162447",
        font_color="white",
        title_font_color="white",
        title_font_size=28,
        font=dict(size=18, color="white"),
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# =====================================
# TEAM DISTRIBUTION
# =====================================

team_runs = (
    df.groupby("batting_team")["runs_batter"]
      .sum()
      .reset_index()
)

fig2 = px.bar(
    team_runs,
    x="batting_team",
    y="runs_batter",
    text="runs_batter",
    color="runs_batter",
    color_continuous_scale="Blues",
    title="🏏 Runs by Team",
    height=550
)

fig2.update_layout(
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font_color="white",
    height=600,
    title_font_size=28,
    title_font_color="white",   # <-- Add this line
    font=dict(size=18, color="white"),
    legend_font=dict(color="white"),
    margin=dict(l=20, r=20, t=70, b=20)
)

fig2.update_traces(textfont_size=14)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("---")

# =====================================
# SEASON OVERVIEW
# =====================================

season_runs = (
    df.groupby("season")["runs_batter"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    season_runs,
    x="season",
    y="runs_batter",
    markers=True,
    title="📈 Runs Across Seasons"
)

fig3.update_layout(
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font_color="white",
    height=500,
    title_font_size=24,
    font=dict(size=16)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("---")

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;'>

### 🏏 CricketIQ

Interactive Cricket Analytics Dashboard

Developed by <b>Mohammad Hisham</b>

Python • Pandas • Plotly • Streamlit

</div>
""",
unsafe_allow_html=True
)