from flask import Flask, jsonify
import random
import time

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(message="hello from the observability lab")


@app.get("/slow")
def slow():
    time.sleep(random.uniform(0.2, 1.0))
    return jsonify(message="slow request complete")


@app.get("/error")
def error():
    return jsonify(error="intentional learning error"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

