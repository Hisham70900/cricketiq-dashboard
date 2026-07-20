import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Bowling Analysis",
    page_icon="🎯",
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

st.title("🎯 Bowling Analysis")

st.write(
    "Explore bowling performance, top wicket takers and detailed bowler statistics."
)

st.markdown("---")

# =====================================
# SEARCH BOWLER
# =====================================

bowlers = sorted(df["bowler"].dropna().unique())

selected_bowler = st.selectbox(
    "🔍 Search Bowler",
    bowlers
)

# =====================================
# BOWLER STATISTICS
# =====================================

bowler_df = df[df["bowler"] == selected_bowler]

wickets = int(bowler_df["bowler_wicket"].sum())
balls = int(len(bowler_df))
runs_conceded = int(bowler_df["runs_total"].sum())

economy = 0
if balls > 0:
    economy = round((runs_conceded / balls) * 6, 2)

dot_balls = int((bowler_df["runs_total"] == 0).sum())

st.subheader(f"📈 {selected_bowler} Statistics")

c1, c2, c3 = st.columns(3)

c1.metric("🎯 Wickets", wickets)
c2.metric("🏏 Balls", balls)
c3.metric("📊 Economy", economy)

c4, c5 = st.columns(2)

c4.metric("⚪ Dot Balls", dot_balls)
c5.metric("🏃 Runs Conceded", runs_conceded)

st.markdown("---")

# =====================================
# TOP BOWLERS
# =====================================

top_n = st.slider(
    "Select Number of Top Bowlers",
    5,
    30,
    10,
    5
)

top_bowlers = (
    df.groupby("bowler")["bowler_wicket"]
      .sum()
      .sort_values(ascending=False)
      .head(top_n)
      .reset_index()
)

top_bowlers.columns = ["Bowler", "Wickets"]

# =====================================
# BAR CHART
# =====================================
fig = px.bar(
    top_bowlers,
    x="Bowler",
    y="Wickets",
    text="Wickets",
    color="Wickets",
    color_continuous_scale="Reds",
    title="🎯 Top Wicket Takers",   # ← Add this line here
    height=600
)

fig.update_layout(
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    title=dict(
        text="🎯 Top Wicket Takers",
        font=dict(size=28, color="white"),
        x=0.5,
        xanchor="center"
    ),
    height=600,
    margin=dict(
        l=20,
        r=20,
        t=120,   # Increased from 80 to 120
        b=20
    )
)

fig.update_traces(textfont_size=16)

# =====================================
# TABLE + CHART
# =====================================

st.markdown(
    "<h2 style='color:white;'>🏆 Top Wicket Takers</h2>",
    unsafe_allow_html=True
)

left, right = st.columns([1, 2])

with left:

    st.dataframe(
        top_bowlers,
        use_container_width=True,
        height=520
    )

    csv = top_bowlers.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Bowling Statistics",
        csv,
        "top_bowlers.csv",
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
    top_bowlers,
    names="Bowler",
    values="Wickets",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Bold
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
    textfont_size=16,
    textinfo="percent+label"
)

st.markdown(
    "<h2 style='color:white;'>🥧 Wicket Distribution</h2>",
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