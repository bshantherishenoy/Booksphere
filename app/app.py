from flask import Flask, jsonify
import socket

app = Flask(__name__)

books = [
    {"id": 1, "name": "Atomic Habits"},
    {"id": 2, "name": "Deep Work"}
]


@app.route("/")
def home():
    return "Booksphere App Running"


@app.route("/books")
def get_books():
    return jsonify(books)


@app.route("/hostname")
def get_hostname():
    hostname = socket.gethostname()
    return f"Hostname: {hostname}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
