import string
import random
import json
import hashlib
import threading
from bottle import Bottle, run, request

from db import Task, Resource, Account
from worker import run_task
from dmhy import dmhy

app = Bottle()


@app.route('/task')
def task_list():
    tasks = [task for task in Task.select().dicts()]
    return json.dumps({"task_list": tasks}, ensure_ascii=False)


@app.route('/resource')
def resource_list():
    resources = [_ for _ in Resource.select().dicts()]
    return json.dumps({"resource": resources}, ensure_ascii=False)


@app.route('/search')
def search():
    keyword = request.query.get('q', '')
    res = [{"title": topic.title, "last_update": topic.date} for topic in dmhy.Search(keyword)]
    return json.dumps({"resource": res}, ensure_ascii=False)


@app.route('/run')
def crawler():
    td = threading.Thread(target=run_task)
    td.start()
    return "Start running"


@app.post('/login')
def do_login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        user = Account.select().where(Account.username == username).get()
        if hashlib.sha256(password).hexdigest() == user.password:
            user.token = ''.join(random.choice(string.hexdigest) for _ in range(24))
            user.save()
            return json.dumps({"status": True, "token": user.token})
        else:
            raise Exception
    except:
        return json.dumps({"status": False, "message": "authentication failed"})

run(app, host='localhost', port=8080)
