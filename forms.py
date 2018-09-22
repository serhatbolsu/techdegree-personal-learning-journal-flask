from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Regexp, Length, Email, EqualTo
from wtforms.widgets.core import TextArea
from wtforms.fields.html5 import DateField


from models import Entry, Tag


def title_exist(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError("Entry with same title already exists.")


class TagField(StringField):
    def _value(self):
        if self.data:
            # Display tags as a comma-separated list.
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')

        # Filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tags if name.strip()]

        # Query the database and retrieve any tags we have already saved.
        existing_tags = Tag.select().where(Tag.name.in_(tag_names))

        # Determine which tag names are new.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tag(name=name) for name in new_names]

        # Return all the existing tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_ ]+$', message=("Title should include ",
                                             "letters and numbers only")),
        title_exist])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    timeSpent = IntegerField('Time Spent', validators=[DataRequired()])
    whatILearned = TextAreaField('What I Learned', widget=TextArea(), validators=[DataRequired()])
    # TODO: Use ListWidget to show a a list
    ResourcesToRemember = TextAreaField('Resources To Remember', widget=TextArea(), validators=[DataRequired()])
    tags = TagField('Tags', description="Separate Multiple tags with commans.")


class EntryEditForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_ ]+$', message=("Title should include ",
                                             "letters and numbers only"))
    ])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    timeSpent = IntegerField('Time Spent', validators=[DataRequired()])
    whatILearned = TextAreaField('What I Learned', widget=TextArea(), validators=[DataRequired()])
    ResourcesToRemember = TextAreaField('Resources To Remember', widget=TextArea(), validators=[DataRequired()],
                                        description="Enter each resource on a new line")
    tags = TagField('Tags', description="Separate Multiple tags with commans.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )