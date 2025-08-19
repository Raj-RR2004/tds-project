import os
import pandas as pd
import matplotlib.pyplot as plt
import base64
import io
import json
import duckdb
from sklearn.linear_model import LinearRegression
from utils import safe_json_dumps

def encode_plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return "data:image/png;base64," + encoded

def process_task(files: list[str]):
    # Ensure questions.txt exists
    q_file = [f for f in files if f.endswith("questions.txt")]
    if not q_file:
        return {"error": "questions.txt missing"}
    with open(q_file[0], "r") as f:
        instruction = f.read().strip()

    outputs = []
    plots = []

    for fpath in files:
        if fpath.endswith(".csv"):
            df = pd.read_csv(fpath)

            # Example analysis: correlation matrix
            corr = df.corr(numeric_only=True).to_dict()
            outputs.append({"correlation_matrix": corr})

            # Example regression if numeric columns exist
            if len(df.select_dtypes(include="number").columns) >= 2:
                cols = df.select_dtypes(include="number").columns[:2]
                X = df[[cols[0]]].dropna().values.reshape(-1, 1)
                y = df[cols[1]].dropna().values

                if len(X) > 1 and len(y) > 1:
                    model = LinearRegression()
                    model.fit(X, y)
                    y_pred = model.predict(X)

                    fig, ax = plt.subplots()
                    ax.scatter(X, y, label="Data")
                    ax.plot(X, y_pred, "r--", label="Regression line")
                    ax.set_xlabel(cols[0])
                    ax.set_ylabel(cols[1])
                    ax.legend()

                    plots.append(encode_plot_to_base64(fig))

        elif fpath.endswith(".json"):
            with open(fpath, "r") as jf:
                data = json.load(jf)
            outputs.append({"json_keys": list(data.keys())})

        elif fpath.endswith(".parquet"):
            df = pd.read_parquet(fpath)
            outputs.append({"parquet_shape": df.shape})

        elif fpath.endswith(".txt") and not fpath.endswith("questions.txt"):
            with open(fpath, "r") as tf:
                text_data = tf.read()
            outputs.append({"text_preview": text_data[:100]})

    response = {
        "instruction": instruction,
        "outputs": outputs,
        "plots": plots[:3]  # limit to 3 plots
    }
    return json.loads(safe_json_dumps(response))
