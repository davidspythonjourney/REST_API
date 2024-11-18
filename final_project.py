from flask import Flask, request, jsonify

app = Flask(__name__)
#change for pr
JSON_NUM = 0
tasks = {}

@app.route("/tasks", methods=["GET"])
def getTasks():
    return jsonify(tasks), 200

@app.route("/tasks/<task_id>", methods=["GET"])
def getTaskId(task_id):
    global tasks
    if task_id in tasks:
        return jsonify(tasks[task_id]), 200  
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>/completed", methods=["PUT"])
def completeTask(task_id):
    global tasks
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        #using kwargs here 
        return jsonify({"message": "Task marked as completed"}, **tasks[task_id]), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks", methods=["POST"])
def addTasks():
    global tasks, JSON_NUM
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
       return jsonify({"error": "Bad Request, data must include 'title' and 'description' "}), 400
    JSON_NUM += 1
    new_task = {str(JSON_NUM): {
        "completed": False,
        'description': data["description"],
        "id": JSON_NUM,
        'title': data["title"],
    }}
    tasks.update(new_task)
    return jsonify(new_task), 201

@app.route("/tasks/<task_id>", methods=["PUT"])
def updateTask(task_id):
    global tasks
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "Bad Request, data must include 'title' and 'description'"}), 400
    if task_id in tasks:
        tasks[task_id].update(data)
        return jsonify(tasks[task_id]), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>", methods=["DELETE"])
def deleteTask(task_id):
    global tasks
    if task_id in tasks:
        if tasks[task_id]["completed"] is True:
            del tasks[task_id]
            return jsonify({"message": "task deleted"}), 200
        else:   
          return jsonify({"error": "Task not completed"}), 404
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5050)