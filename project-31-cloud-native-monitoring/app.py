import psutil
import os
from flask import Flask, render_template

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH", 1024 * 1024))

@app.route("/")
def index():
    cpu_metric = psutil.cpu_percent()
    mem_metric = psutil.virtual_memory().percent
    Message = None
    if cpu_metric > 80 or mem_metric > 80:
        Message = "High CPU or Memory Detected, scale up!!!"
    return render_template("index.html", cpu_metric=cpu_metric, mem_metric=mem_metric, message=Message)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

if __name__=='__main__':
    app.run(
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
        host='0.0.0.0',
        port=int(os.environ.get("PORT", "5000")),
    )
