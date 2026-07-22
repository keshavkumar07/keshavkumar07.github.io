from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

from database import init_db
from recognizer import enroll_face, recognize_face

app = Flask(__name__)
init_db()


def get_stats():
    """Small dashboard stats. Wrapped defensively so a missing DB/folder
    never breaks the page — worst case the numbers show as 0."""
    stats = {"enrolled": 0, "today": 0, "total": 0}

    try:
        if os.path.isdir("Images"):
            stats["enrolled"] = len([
                d for d in os.listdir("Images")
                if os.path.isdir(os.path.join("Images", d))
            ])
    except Exception:
        pass

    try:
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance")
        stats["total"] = cursor.fetchone()[0]

        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE date=?", (today,))
        stats["today"] = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass

    return stats


@app.route("/")
def index():
    return render_template("index.html", stats=get_stats())


@app.route("/api/enroll", methods=["POST"])
def api_enroll():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "")
    images = payload.get("images", [])

    if not images:
        return jsonify(ok=False, message="No image was captured."), 400

    ok, message = enroll_face(name, images)
    return jsonify(ok=ok, message=message, stats=get_stats())


@app.route("/api/recognize", methods=["POST"])
def api_recognize():
    payload = request.get_json(silent=True) or {}
    image = payload.get("image")

    if not image:
        return jsonify(ok=False, message="No image was captured."), 400

    name, confidence, error = recognize_face(image)
    if error:
        return jsonify(ok=False, message=error, stats=get_stats())

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    cursor.execute("SELECT 1 FROM attendance WHERE name=? AND date=?", (name, date))
    already = cursor.fetchone()

    if already:
        conn.close()
        return jsonify(
            ok=True, already_marked=True, name=name,
            message=f"{name} is already marked present today.",
            stats=get_stats(),
        )

    cursor.execute(
        "INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
        (name, date, time_str),
    )
    conn.commit()
    conn.close()

    return jsonify(
        ok=True, already_marked=False, name=name,
        message=f"Attendance marked for {name}.",
        stats=get_stats(),
    )


@app.route("/api/records")
def api_records():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, date, time FROM attendance ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return jsonify(records=[
        {"id": r[0], "name": r[1], "date": r[2], "time": r[3]} for r in rows
    ])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
