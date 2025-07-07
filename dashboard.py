from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="frontend")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/report.json")
def report():
    return send_from_directory("backend/observer", "report.json")

if __name__ == "__main__":
    app.run(port=8080)

