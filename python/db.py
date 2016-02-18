from datetime import datetime
import configparser
import peewee
from playhouse.fields import PasswordField


try:
    config = configparser.ConfigParser()
    config.read("settings.conf")
    db_path = config['database']['path']
except:
    db_path = "dmhy.db"
    config['database'] = config.get('database', {})  # initialize if not exists
    config['database']['path'] = db_path
    with open('settings.conf', 'w') as configfile:
        config.write(configfile)

db = peewee.SqliteDatabase(db_path)


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
    download = peewee.BooleanField(default=False)
    last_update = peewee.DateTimeField(default=datetime.now(), formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = db


class Account(peewee.Model):
    username = peewee.CharField()
    password = PasswordField()
    token = peewee.CharField(default=None, null=True)

    class Meta:
        database = db

    @staticmethod
    def check_token(t):
        return Account.select().where(Account.token == t).exists()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Task, Resource, Account])
