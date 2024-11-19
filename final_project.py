from flask import Flask, request, jsonify

app = Flask(__name__)
#change for pr
json_task_num = 0
tasks = {}


def dataCheck(data: dict):
    if not data or "title" not in data or "description" not in data:
        return False
    return True
      

@app.route("/tasks", methods=["GET"])
def getTasks():
    return jsonify(tasks), 200

@app.route("/tasks/<task_id>", methods=["GET"])
def getTaskId(task_id):
    global tasks
    if task_id in tasks:
        return jsonify({task_id: tasks[task_id]}), 200  
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>/completed", methods=["GET"])
def completeTask(task_id):
    global tasks
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        #using kwargs here 
        response = {"message": "Task marked as completed", **tasks[task_id]}
        return jsonify(response), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks", methods=["POST"])
def addTasks():
    global tasks, json_task_num
    data = request.get_json()
    if not dataCheck(data):
        return jsonify({"error": "Bad Request, data must include 'title' and 'description'"}), 400
    json_task_num += 1
    new_task = {str(json_task_num): {
        "completed": False,
        'description': data["description"],
        "id": json_task_num,
        'title': data["title"],
    }}
    tasks.update(new_task)
    return jsonify(new_task), 201

@app.route("/tasks/<task_id>", methods=["PUT"])
def updateTask(task_id):
    global tasks
    data = request.get_json()
    if not dataCheck(data):
        return jsonify({"error": "Bad Request, data must include 'title' and 'description'"}), 400
    if task_id in tasks:
        tasks[task_id].update(data)
        return jsonify(tasks[task_id]), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>", methods=["DELETE"])
def deleteTask(task_id):
    global tasks, json_task_num
    if task_id in tasks:
        if tasks[task_id]["completed"] is True:
            del tasks[task_id]
            json_task_num -= 1
            return jsonify({"message": "task deleted"}), 200
        else:   
          return jsonify({"error": "Task not completed"}), 404
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5050)
