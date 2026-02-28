from flask import Flask, redirect, url_for, render_template_string
import time
import threading

app = Flask(__name__)

# 🔁 Toggle: exponential backoff
use_backoff = False

# 📊 Live metrics (reset every second)
metrics = {
    "requests": 0,
    "retries": 0,
    "latency": 0.0
}

lock = threading.Lock()

HTML = """
<!doctype html>
<meta http-equiv="refresh" content="1">

<title>Retry Storm Visualizer</title>

<h2>Retry Storm Lab</h2>

<p>
<b>Exponential Backoff:</b>
<span style="color:{{ 'green' if backoff else 'red' }}">
{{ 'ENABLED' if backoff else 'DISABLED' }}
</span>
</p>

<form method="post" action="/toggle">
<button>{{ 'Disable Backoff' if backoff else 'Enable Backoff' }}</button>
</form>

<hr>

<h3>Live Metrics (last ~1s)</h3>
<ul>
  <li>Requests/sec: {{ req }}</li>
  <li>Retries/sec: {{ retries }}</li>
  <li>Avg Latency: {{ latency }} ms</li>
</ul>

<h1 style="color:{{ color }}">{{ state }}</h1>
"""

def simulated_db_call():
    # 🔴 Injected latency (300ms)
    time.sleep(0.3)
    return "OK"

@app.route("/")
def handler():
    start = time.time()

    with lock:
        metrics["requests"] += 1

    base_delay = 0.1  # 100ms

    for attempt in range(3):
        try:
            return simulated_db_call()
        except Exception:
            with lock:
                metrics["retries"] += 1

            if use_backoff:
                time.sleep(base_delay * (2 ** attempt))
            # else: immediate retry → retry storm

    return "FAILED", 500

@app.route("/ui")
def ui():
    with lock:
        req = metrics["requests"]
        retries = metrics["retries"]
        latency = metrics["latency"]

        # reset per-second counters
        metrics["requests"] = 0
        metrics["retries"] = 0

    cascading = retries > req

    return render_template_string(
        HTML,
        backoff=use_backoff,
        req=req,
        retries=retries,
        latency=round(latency, 1),
        state="CASCADING FAILURE 🔴" if cascading else "STABLE 🟢",
        color="red" if cascading else "green"
    )

@app.route("/toggle", methods=["POST"])
def toggle():
    global use_backoff
    use_backoff = not use_backoff
    return redirect(url_for("ui"))

def latency_estimator():
    while True:
        time.sleep(1)
        with lock:
            # latency worsens as retries increase
            metrics["latency"] = 300 + metrics["retries"] * 50

threading.Thread(target=latency_estimator, daemon=True).start()

app.run(host="0.0.0.0", port=8080)
