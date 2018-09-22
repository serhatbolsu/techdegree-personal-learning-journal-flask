from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, Field, FormField, FieldList
from wtforms import Form as NoCsrfForm
from wtforms.validators import DataRequired, ValidationError, Regexp, InputRequired, Length
from wtforms.widgets.core import TextArea, TextInput, HiddenInput
from wtforms.fields.html5 import DateField


from models import Entry, Tag


def title_exist(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError("Entry with same title already exists.")


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
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


class TagForm(NoCsrfForm):
    tag = StringField('', validators=[InputRequired(), Length(max=256)])


class EntryEditForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_ ]+$', message=("Title should include ",
                                             "letters and numbers only"))
    ])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    timeSpent = IntegerField('Time Spent', validators=[DataRequired()])
    whatILearned = TextAreaField('What I Learned', widget=TextArea(), validators=[DataRequired()])
    ResourcesToRemember = TextAreaField('Resources To Remember', widget=TextArea(), validators=[DataRequired()])
    tags = FieldList(FormField(TagForm))
