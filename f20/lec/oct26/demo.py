from flask import Flask, Response, request
import pandas as pd
from matplotlib import pyplot as plt
from io import BytesIO
import random

values = [1,2,3]
app = Flask(__name__)

@app.route("/")
def home():
    #values.append(float(request.args["insert"]))
    html = """
    <html>
    <body>
    <h1>Errors over Time</h1>
    <img src="plot.svg">
    <h1>CDF</h1>
    <img src="dist.svg">
    </body>
    </html>
    """
    return html

@app.route("/upload", methods=["POST"])
def upload():
    uploads = str(request.get_data(), "utf-8").split(",")
    for x in uploads:
        values.append(float(x))
    print("input", request.data)
    return "True\n"

@app.route("/dist.svg")
def dist():
    # CDF (Cumulative Distribution Function)
    # 1) normalizes 0-to-100 instead of 0-to-N
    # 2) swaps the x and y axes
    fig, ax = plt.subplots(figsize=(3,2))
    s = pd.Series(sorted(values))
    rev = pd.Series(100 * (s.index+1) / len(s), index=s.values)
    
    rev.plot.line(ax=ax)
    ax.set_xlabel("Error #")
    ax.set_ylabel("% Less")
    plt.tight_layout()
    
    f = BytesIO()
    fig.savefig(f)
    plt.close()
    return Response(f.getvalue(),
                    headers={"Content-Type": "image/xml+svg"})

@app.route("/plot.svg")
def plot():
    fig, ax = plt.subplots(figsize=(3,2))
    pd.Series(values).plot.line(ax=ax)
    ax.set_xlabel("Time")
    ax.set_ylabel("Errors")
    plt.tight_layout()
    
    f = BytesIO()
    fig.savefig(f)
    plt.close()
    return Response(f.getvalue(),
                    headers={"Content-Type": "image/xml+svg"})

app.run("0.0.0.0", debug=True)
