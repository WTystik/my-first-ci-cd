simport hashlib
import ipaddress
import subprocess
import sys

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    user_id = request.args.get("id", "1")
    return f"<h1>Hello, user #{escape(user_id)}!</h1>"


@app.route("/checksum")
def checksum():
    data = request.args.get("data", "")
    return hashlib.sha256(data.encode()).hexdigest()


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    try:
        ipaddress.ip_address(host)
    except ValueError:
        return "Invalid IP address", 400

    count_flag = "-n" if sys.platform == "win32" else "-c"

    try:
        result = subprocess.run(
            ["ping", count_flag, "1", host],
            shell=False,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return "Ping timed out", 504
    except FileNotFoundError:
        return "Ping executable not found", 503

    output = result.stdout.decode(errors="replace")
    return f"<pre>{escape(output)}</pre>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False)Ы