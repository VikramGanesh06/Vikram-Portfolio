from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from html import escape
import sqlite3
import os

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

def init_db():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required."}), 400

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Message sent successfully!"}), 200

@app.route("/messages", methods=["GET"])
def get_messages():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message FROM contacts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Messages</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0b0b0f;
                color: white;
                padding: 30px;
            }
            h1 {
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background: #111;
                border-radius: 12px;
                overflow: hidden;
            }
            th, td {
                padding: 14px 16px;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                text-align: left;
                vertical-align: top;
            }
            th {
                background: #1a1a1f;
                color: #fff;
            }
            tr:hover {
                background: rgba(255,255,255,0.03);
            }
            .num {
                width: 60px;
                color: #aaa;
            }
            .email {
                color: #7cc0ff;
            }
            .message {
                max-width: 420px;
                line-height: 1.5;
            }
        </style>
    </head>
    <body>
        <h1>Contact Form Responses</h1>
        <table>
            <tr>
                <th>No.</th>
                <th>Name</th>
                <th>Email</th>
                <th>Message</th>
            </tr>
    """

    for index, row in enumerate(rows, start=1):
        name = escape(row[1])
        email = escape(row[2])
        message = escape(row[3])

        html += f"""
            <tr>
                <td class="num">{index}</td>
                <td>{name}</td>
                <td class="email">{email}</td>
                <td class="message">{message}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    init_db()
    app.run()