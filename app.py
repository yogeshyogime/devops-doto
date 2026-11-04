import os
import time
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def query(sql, params=None, fetch=False):
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if fetch else None
    finally:
        conn.close()


def init_db():
    for _ in range(10):
        try:
            query("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title TEXT NOT NULL)")
            return
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("Database not reachable")


@app.get("/tasks")
def list_tasks():
    rows = query("SELECT id, title FROM tasks ORDER BY id", fetch=True)
    return jsonify([{"id": r[0], "title": r[1]} for r in rows])


@app.post("/tasks")
def add_task():
    rows = query(
        "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title",
        (request.json["title"],),
        fetch=True,
    )
    return jsonify({"id": rows[0][0], "title": rows[0][1]}), 201


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    query("DELETE FROM tasks WHERE id = %s", (task_id,))
    return "", 204


@app.get("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)