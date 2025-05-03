from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

M3U_URL = "https://iptv-org.github.io/iptv/countries/pt.m3u"

def parse_m3u(url):
    response = requests.get(url)
    lines = response.text.splitlines()
    channels = []

    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            name = lines[i].split(",")[-1].strip()
            link = lines[i + 1].strip()
            channels.append({"name": name, "url": link})

    return channels

@app.route("/")
def index():
    channels = parse_m3u(M3U_URL)
    return render_template("index.html", channels=channels)

@app.route("/channels")
def channels():
    return jsonify(parse_m3u(M3U_URL))

if __name__ == "__main__":
    app.run(debug=True)
