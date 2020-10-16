from matplotlib import pyplot as plt
from flask import Flask, request
from io import StringIO
import pandas as pd

guesses_df = pd.DataFrame()

app = Flask(__name__)

def get_ax():
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return ax

@app.route('/plot.svg')
def show_plot():
    ax = get_ax()
    
    if len(guesses_df):
        ax = guesses_df.plot.scatter(x="x", y="actual", c="black", s=60, ax=ax, zorder=1, label="actual")
        ax = guesses_df.plot.scatter(x="x", y="y", c="red", s=20, ax=ax, zorder=2, label="guess")

    # "save" to a string in the SVG format
    f = StringIO()
    ax.get_figure().savefig(f, format="svg")
    svg_data = f.getvalue()

    html = "<html><body><h1>Guess that function</h1>{}</body></html>"
    return html.format(svg_data)

def f(x):
    return -abs(x)

@app.route('/guess', methods=["POST"])
def guess():
    parts = request.get_data(as_text=True).split(",")
    x = float(parts[0])
    y = float(parts[1])
    actual = f(x)
    
    # record guess
    idx = len(guesses_df)
    guesses_df.loc[idx, "x"] = x
    guesses_df.loc[idx, "y"] = y
    guesses_df.loc[idx, "actual"] = actual
    
    if actual == y:
        return "perfect"
    return "f({}) is {}, not {}".format(x, actual, y)

if __name__ == '__main__':
    app.run(host="0.0.0.0")