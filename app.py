from flask import Flask, render_template, request
import pandas as pd
from engine import calculate_interest

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    file = request.files["excel_file"]
    df = pd.read_excel(file)

    result = calculate_interest(df)
    result = result.applymap(
        lambda x: f"{int(x):,}" if isinstance(x, (int, float)) else x
    )

    return render_template(
        "index.html",
        tables=result.to_html(index=False)
    )

if __name__ == "__main__":
    app.run(debug=True)
