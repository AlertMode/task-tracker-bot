from peewee import SqliteDatabase, AutoField, Model, CharField, DateField, IntegerField, ForeignKeyField, BooleanField

db = SqliteDatabase('task_tracker.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = CharField(null=False)
    date_of_registration = DateField(null=False)

class List(BaseModel):
    id = AutoField(primary_key=True, null=False)
    user_id = ForeignKeyField(User.id)
    name = CharField(null=False, unique=True)
    date_of_creation = DateField(null=False)

class Task(BaseModel):
    id = AutoField(primary_key=True, null=False)
    user_id = ForeignKeyField(User.id)
    list_id = ForeignKeyField(List.id)
    description = CharField(null=False)
    date_of_creation = DateField(null=False)
    date_of_completion = DateField()

db.create_tables([User, List, Task])
