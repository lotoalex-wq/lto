from flask import Flask, render_template, redirect, url_for, flash
import subprocess
import os

app = Flask(__name__)
app.secret_key = "secret_key"

HISTORY_FILE = "participation_history.txt"

@app.route("/")
def index():
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = f.read().splitlines()
    return render_template("index.html", history=history)

@app.route("/run-bot")
def run_bot():
    try:
        result = subprocess.run(["python3", "bot_v3.py"], capture_output=True, text=True, timeout=60)
        output = result.stdout + "\n" + result.stderr
        flash(output, "info")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)