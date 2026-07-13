import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Match Insights",
    page_icon="📊",
    layout="wide"
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

st.title("📊 Match Insights")

st.write(
    "Explore match statistics, highest team scores, boundaries and overall insights."
)

st.markdown("---")

# =====================================
# DASHBOARD METRICS
# =====================================

total_runs = int(df["runs_batter"].sum())
total_wickets = int(df["bowler_wicket"].sum())
matches = int(df["match_id"].nunique())
players = int(df["batter"].nunique())

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Runs", total_runs)
c2.metric("🎯 Wickets", total_wickets)
c3.metric("🏟 Matches", matches)
c4.metric("👥 Players", players)

st.markdown("---")

# =====================================
# HIGHEST TEAM SCORES
# =====================================

highest_scores = (
    df.groupby(["match_id", "batting_team"])["runs_total"]
      .sum()
      .reset_index()
      .sort_values("runs_total", ascending=False)
      .head(10)
)

highest_scores.columns = ["Match", "Team", "Runs"]

fig1 = px.bar(
    highest_scores,
    x="Team",
    y="Runs",
    text="Runs",
    color="Runs",
    color_continuous_scale="Turbo",
    height=550
)

fig1.update_layout(
    title="",
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    margin=dict(l=20, r=20, t=20, b=20)
)

fig1.update_traces(textfont_size=16)

fig1.update_traces(textfont_size=16)

st.markdown(
    "<h2 style='color:white;'>🏏 Highest Team Scores</h2>",
    unsafe_allow_html=True
)

left, right = st.columns([1,2])

with left:

    st.dataframe(
        highest_scores,
        use_container_width=True,
        height=520
    )

    csv = highest_scores.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Highest Scores",
        csv,
        "highest_scores.csv",
        "text/csv"
    )

with right:

    st.plotly_chart(
       fig1,
       use_container_width=True,
    config={"displayModeBar": False}
    )

st.markdown("---")

# =====================================
# MOST SIXES
# =====================================

sixes = (
    df[df["runs_batter"] == 6]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Sixes")
)

fig2 = px.bar(
    sixes,
    x="batter",
    y="Sixes",
    text="Sixes",
    color="Sixes",
    color_continuous_scale="Sunset",
    height=550
)

fig2.update_layout(
    title="",
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    margin=dict(l=20, r=20, t=20, b=20)
)

fig2.update_traces(textfont_size=16)

st.markdown(
    "<h2 style='color:white;'>💥 Most Sixes</h2>",
    unsafe_allow_html=True
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.markdown("---")

# =====================================
# MOST FOURS
# =====================================

fours = (
    df[df["runs_batter"] == 4]
    .groupby("batter")
    .size()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Fours")
)

fig3 = px.bar(
    fours,
    x="batter",
    y="Fours",
    text="Fours",
    color="Fours",
    color_continuous_scale="Viridis",
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
    "<h2 style='color:white;'>🔥 Most Fours</h2>",
    unsafe_allow_html=True
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    config={"displayModeBar": False}
)
st.markdown("---")

# =====================================
# RUN DISTRIBUTION
# =====================================

run_distribution = (
    df.groupby("batting_team")["runs_batter"]
      .sum()
      .sort_values(ascending=False)
)

top10 = run_distribution.head(10)
others = run_distribution.iloc[10:].sum()

pie_df = top10.reset_index()

pie_df.columns = ["Team", "Runs"]

if others > 0:
    pie_df.loc[len(pie_df)] = ["Others", others]

fig4 = px.pie(
    pie_df,
    names="Team",
    values="Runs",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig4.update_layout(
    title="",
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    legend_font=dict(color="white", size=13),
    height=650,
    margin=dict(l=20, r=20, t=20, b=20)
)

fig4.update_traces(
    textinfo="percent",
    textfont_size=16,
    textposition="inside",
    hovertemplate="<b>%{label}</b><br>Runs=%{value:,}<br>%{percent}<extra></extra>"
)

st.markdown(
    "<h2 style='color:white;'>🏆 Overall Run Distribution</h2>",
    unsafe_allow_html=True
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.markdown("---")

st.caption(
    "Developed by Mohammad Hisham | Python • Streamlit • Pandas • Plotly"
)