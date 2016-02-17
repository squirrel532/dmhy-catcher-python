import configparser

import transmissionrpc

from db import Task, Resource
from dmhy import dmhy


def run_task():
    try:
        config = configparser.ConfigParser()
        config.read("settings.conf")
        bt_host = config['transmission']['host']
        bt_port = config['transmission']['port']
        bt_username = config['transmission']['username']
        bt_password = config['transmission']['password']
    except:
        print('Configuration error!')
        return

    for task in Task.select().where(Task.status == True):
        for topic in dmhy.Search(task.keyword):
            if not Resource.select().where(
                    Resource.magnet_link == topic.magnet).exists():
                # add this topic to database
                res = Resource.create(task=task, title=topic.title, magnet_link=topic.magnet)
                res.save()
                # transmission rpc
                try:
                    bt = transmissionrpc.Client(address=bt_host, port=bt_port,
                                                user=bt_username, password=bt_password)
                    bt.add_torrent(topic.magnet)
                except:
                    print('Error adding magnet link')
                    pass
                else:
                    res.download = True
                    res.save()


if __name__ == '__main__':
    run_task()
