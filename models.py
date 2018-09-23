import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *
from flask_peewee.utils import slugify

DATABASE = SqliteDatabase('app.db')


# DATABASE = PostgresqlDatabase('serhatbolsu', user='serhatbolsu', autorollback=True)


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
                inst = cls.create(
                    title=title,
                    date=date,
                    timeSpent=timeSpent,
                    whatILearned=whatILearned,
                    ResourcesToRemember=ResourcesToRemember,
                    slug=slugify(title))
        except IntegrityError:
            raise ValueError("Entry already exist")
        else:
            return inst

    def create_and_add_tags(self, tags):
        with DATABASE.transaction():
            for tag in tags:
                try:
                    tag.save(force_insert=True)
                except IntegrityError:
                    pass
            self.tags.add(tags)


class Tag(Model):
    name = CharField(max_length=50, primary_key=True)
    entries = ManyToManyField(Entry, backref='tags')
    slug = CharField()

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag %s>' % self.name

    def __str__(self):
        return self.name

    class Meta:
        database = DATABASE


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Tag, Tag.entries.get_through_model()], safe=True)
