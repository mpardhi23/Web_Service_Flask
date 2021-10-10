from flask import Flask
from flask import jsonify
from flask import request
import logging
import os

app = Flask(__name__)

if not os.path.exists('log'):
    os.mkdir('log')
logging.basicConfig(filename='log/task_manager.log', level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s %(filename)s:%(message)s')

taskDB = [
    {
        'id': '101',
        'title': 'Design the solution',
        'due_date': '21/09/2021',
        'status': 'Done'
    },
    {
        'id': '102',
        'title': 'Define the server configuration',
        'due_date': '21/10/2021',
        'status': 'Open'
    }
]


@app.route('/taskdb/tasks', methods=['GET'])
def getAllTasks():
    """Returns all tasks list
        :returns: a list of tasks
    """
    logging.info("Retrieved Task Data : {}".format(taskDB))
    return jsonify({'tasks': taskDB})


@app.route('/taskdb/tasks/<taskId>', methods=['GET'])
def getTask(taskId):
    """Return a task from taskDB
        :param taskId: id of the task
        :returns: a task on successful query
    """
    task_data = [task for task in taskDB if (task['id'] == taskId)]
    logging.info("Retrieved Task Data for taskId {} : {}".format(taskId,
                                                                 task_data))
    return jsonify({'tasks': task_data})


@app.route('/taskdb/tasks/<taskId>', methods=['PUT'])
def updateTask(taskId):
    """Modify a task
        :param taskId: id of the task
        :returns: a task list with updated task data
    """
    task = [t1 for t1 in taskDB if (t1['id'] == taskId)]

    if 'title' in request.json:
        task[0]['title'] = request.json['title']

    if 'due_date' in request.json:
        task[0]['due_date'] = request.json['due_date']

    if 'status' in request.json:
        task[0]['status'] = request.json['status']

    logging.info("Updated Task Data for taskId {} : {}".format(taskId,
                                                               task[0]))
    return jsonify({'tasks': task[0]})


@app.route('/taskdb/tasks', methods=['POST'])
def createTask():
    """Create a task
        :param taskId: id of the task
        :param title: title of the task
        :param due_date: date for completion of task
        :param status: status of task
        :returns: newly created task details
    """
    task_data = {
        'id': request.json['id'],
        'title': request.json['title'],
        'due_date': request.json['due_date'],
        'status': request.json['status']
    }
    taskDB.append(task_data)
    logging.info("Created new Task Data with task data {}".format(task_data))
    return jsonify(task_data)


@app.route('/taskdb/tasks/<taskId>', methods=['DELETE'])
def deleteTask(taskId):
    """Delete a task from taskDB
        :param taskId: id of the task
        :returns: task data after deleting task
    """
    task = [t for t in taskDB if (t['id'] == taskId)]

    if len(task) == 0:
        abort(404)

    taskDB.remove(task[0])
    logging.info("Deleted Task Data for taskId {}".format(taskId))
    return jsonify({'response': 'Success'})


if __name__ == '__main__':
    app.run()
