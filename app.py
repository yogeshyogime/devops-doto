from flask import Flask, jsonify, request

app = Flask(__name__)
tasks = []
next_id = 1

@app.get("/tasks")
def list_tasks():
    return jsonify(tasks)

@app.post("/tasks")
def add_task():
    global next_id
    task = {"id": next_id, "title": request.json["title"]}
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return "", 204

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)