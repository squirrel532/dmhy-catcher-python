from datetime import datetime
import peewee

db = peewee.SqliteDatabase('dmhy.db')


class Task(peewee.Model):
    tid = peewee.PrimaryKeyField()
    alias = peewee.CharField()
    keyword = peewee.CharField()
    status = peewee.BooleanField(default=True)
    last_update = peewee.DateTimeField(default=datetime.now(), formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = db


class Resource(peewee.Model):
    task = peewee.ForeignKeyField(Task, related_name='resources')
    title = peewee.TextField()
    magnet_link = peewee.TextField(default="")
    last_update = peewee.DateTimeField(default=datetime.now(), formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = db

if __name__ == '__main__':
    db.connect()
    db.create_tables([Task, Resource])
