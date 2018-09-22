import datetime

from peewee import *
from flask_peewee.utils import slugify

DATABASE = PostgresqlDatabase('serhatbolsu', user='serhatbolsu',autorollback=True)


class Entry(Model):
    title = CharField()
    date = DateField()
    timeSpent = IntegerField()
    whatILearned = TextField()
    ResourcesToRemember = TextField()
    slug = CharField(unique=True)

    class Meta:
        database = DATABASE
        ordering = ('-date',)

    @classmethod
    def create_entry(cls, title, date, timeSpent, whatILearned, ResourcesToRemember):
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    date=date,
                    timeSpent=timeSpent,
                    whatILearned=whatILearned,
                    ResourcesToRemember=ResourcesToRemember,
                    slug=slugify(title))
        except IntegrityError:
            raise ValueError("Entry already exist")


class Tag(Model):
    tag = CharField(max_length=50, primary_key=True)
    entries = ManyToManyField(Entry, backref='tags')

    def __repr__(self):
        return '<%s>' % self.tag

    class Meta:
        database = DATABASE



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tag, Tag.entries.get_through_model()], safe=True)
