import json
from bottle import Bottle, run

from db import Task, Resource

app = Bottle()


@app.route('/task')
def task_list():
    tasks = [task for task in Task.select().dicts()]
    return json.dumps({"task_list": tasks})


@app.route('/resource')
def resource_list():
    resources = [_ for _ in Resource.select().dicts()]
    return json.dumps({"resource": resources})

run(app, host='localhost', port=8080)
