import pandas as pd
import plotly.express as px

# Read the dataset
df = pd.read_csv("data/matches.csv", low_memory=False)

# Calculate total runs scored by each batter
top_batsmen = (
    df.groupby("batter")["runs_batter"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("Top 10 Run Scorers")
print(top_batsmen)

# Convert Series to DataFrame
top_batsmen_df = top_batsmen.reset_index()

# Rename columns
top_batsmen_df.columns = ["Batter", "Runs"]

# Create bar chart
fig = px.bar(
    top_batsmen_df,
    x="Batter",
    y="Runs",
    title="Top 10 Run Scorers",
    text="Runs"
)

# Display chart
fig.show()

print("\nTop 10 Wicket Takers")

top_bowlers = (
    df.groupby("bowler")["bowler_wicket"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print(top_bowlers)