from bokeh.plotting import figure, output_file, show

from summary_db import SummaryDB
import pandas as pd
import numpy as np

db = SummaryDB()

df = db.get_df()

def plot_scores(df):
    df = df.dropna()
    date = df['date']
    rogue = df['rouge'].to_numpy()
    meteor = df['meteor'].to_numpy()

    graph = figure(title="Rouge and Meteor Scores Over Time")
    graph.line(date, rogue, legend_label="Rogue Score")
    graph.line(date, meteor, legend_label="Meteor Score", line_color="green")
    graph.legend.title = "Score Type"
    graph.legend.location = "top_left"

    show(graph)

if __name__ == "__main__":
    plot_scores(df)
