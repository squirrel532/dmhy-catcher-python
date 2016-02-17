from db import Task, Resource
from dmhy import dmhy


def run_task():
    for task in Task.select().where(Task.status == True):
        for topic in dmhy.Search(task.keyword):
            if not Resource.select().where(
                    Resource.magnet_link == topic.magnet).exists():
                # transmission rpc
                # add this topic to database
                res = Resource.create(task=task, title=topic.title, magnet_link=topic.magnet)
                res.save()

if __name__ == '__main__':
    run_task()
