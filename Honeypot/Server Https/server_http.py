from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Resursa secreta</h1><p>Asta e o pagina hostata pe Honeypot VM prin HTTPS.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4443, ssl_context=("server.crt", "server.key"))
