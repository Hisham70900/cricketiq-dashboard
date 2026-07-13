import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Player Comparison",
    page_icon="👤",
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

st.title("👤 Player Comparison")

st.write(
    "Compare the batting performance of two players."
)

st.markdown("---")

# =====================================
# PLAYER SELECTION
# =====================================

players = sorted(df["batter"].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox(
        "🏏 Select Player 1",
        players,
        key="player1"
    )

with col2:
    player2 = st.selectbox(
        "🏏 Select Player 2",
        players,
        index=1,
        key="player2"
    )

# =====================================
# PLAYER STATS FUNCTION
# =====================================

def player_stats(player):

    data = df[df["batter"] == player]

    runs = int(data["runs_batter"].sum())
    balls = int(len(data))
    matches = int(data["match_id"].nunique())

    fours = int((data["runs_batter"] == 4).sum())
    sixes = int((data["runs_batter"] == 6).sum())

    strike_rate = 0

    if balls > 0:
        strike_rate = round((runs / balls) * 100, 2)

    return {
        "Runs": runs,
        "Balls": balls,
        "Matches": matches,
        "Fours": fours,
        "Sixes": sixes,
        "Strike Rate": strike_rate
    }

stats1 = player_stats(player1)
stats2 = player_stats(player2)

# =====================================
# PLAYER CARDS
# =====================================

left, right = st.columns(2)

with left:

    st.subheader(f"🏏 {player1}")

    c1, c2, c3 = st.columns(3)

    c1.metric("Runs", stats1["Runs"])
    c2.metric("Balls", stats1["Balls"])
    c3.metric("Strike Rate", stats1["Strike Rate"])

    c4, c5, c6 = st.columns(3)

    c4.metric("Fours", stats1["Fours"])
    c5.metric("Sixes", stats1["Sixes"])
    c6.metric("Matches", stats1["Matches"])

with right:

    st.subheader(f"🏏 {player2}")

    c1, c2, c3 = st.columns(3)

    c1.metric("Runs", stats2["Runs"])
    c2.metric("Balls", stats2["Balls"])
    c3.metric("Strike Rate", stats2["Strike Rate"])

    c4, c5, c6 = st.columns(3)

    c4.metric("Fours", stats2["Fours"])
    c5.metric("Sixes", stats2["Sixes"])
    c6.metric("Matches", stats2["Matches"])

st.markdown("---")

# =====================================
# COMPARISON TABLE
# =====================================

comparison = pd.DataFrame({
    "Metric": stats1.keys(),
    player1: stats1.values(),
    player2: stats2.values()
})

st.subheader("📋 Comparison Table")

left, right = st.columns([1, 2])

with left:

    st.dataframe(
        comparison,
        use_container_width=True,
        height=350
    )

    csv = comparison.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Comparison",
        csv,
        "player_comparison.csv",
        "text/csv"
    )

with right:

    chart = pd.DataFrame({
        "Player": [player1, player2],
        "Runs": [stats1["Runs"], stats2["Runs"]]
    })

    fig = px.bar(
        chart,
        x="Player",
        y="Runs",
        text="Runs",
        color="Runs",
        color_continuous_scale="Purples",
        title="🏏 Runs Comparison",
        height=550
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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# =====================================
# STRIKE RATE COMPARISON
# =====================================

sr_chart = pd.DataFrame({
    "Player": [player1, player2],
    "Strike Rate": [
        stats1["Strike Rate"],
        stats2["Strike Rate"]
    ]
})

fig2 = px.bar(
    sr_chart,
    x="Player",
    y="Strike Rate",
    text="Strike Rate",
    color="Strike Rate",
    color_continuous_scale="Blues",
    height=550
)

fig2.update_layout(
    plot_bgcolor="#162447",
    paper_bgcolor="#162447",
    font=dict(size=18, color="white"),
    margin=dict(l=20, r=20, t=20, b=20)
)


fig2.update_traces(textfont_size=16)

st.markdown(
    "<h2 style='color:white;'>⚡ Strike Rate Comparison</h2>",
    unsafe_allow_html=True
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.markdown("---")

st.caption(
    "Developed by Mohammad Hisham | Python • Streamlit • Pandas • Plotly"
)