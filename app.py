from flask import (Flask, url_for, render_template, redirect, flash,
                   abort, g)

import models
import forms

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key = "dfşlj1*5u1qekfjqşeklfmqke-ekjr34éadfakjqşr134134kjfşkasdfjaşdf^^"


@app.route('/entry', methods=('GET', 'POST'))
def create_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        flash("Entry created", 'success')
        models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            timeSpent=form.timeSpent.data,
            whatILearned=form.whatILearned.data,
            ResourcesToRemember=form.ResourcesToRemember.data
        )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


# @app.route('/entries/<int:id>')
@app.route('/entries/<slug>')
def view_entry(slug=None):
    # if id:
    #     entry = models.Entry.select().where(models.Entry.id == id).get()
    #     render_template(url_for('entry_detail'), entry=entry)
    #     return render_template('detail.html', entry=entry)
    # elif slug:
    entry = models.Entry.select().where(models.Entry.slug == slug).get()
    return render_template('detail.html', entry=entry)


@app.route('/entries/edit/<slug>', methods=('GET', 'POST'))
def edit_entry(slug):
    entry = models.Entry.select().where(models.Entry.slug == slug).get()
    form = forms.EntryEditForm(obj=entry)
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.date = form.date.data
        entry.timeSpent = form.timeSpent.data
        entry.whatILearned = form.whatILearned.data
        entry.ResourcesToRemember = form.ResourcesToRemember.data
        entry.save()
        flash("Entry edit successful", 'successful')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/delete/<slug>', methods=('GET', 'POST'))
def delete_entry(slug):
    entry = models.Entry.select().where(models.Entry.slug == slug).get()
    if entry:
        entry.delete_instance()
        return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().order_by(models.Entry.date.desc())
    return render_template('index.html', entries=entries)


if __name__ == '__main__':
    models.initialize()
    try:
        models.Entry.create_entry(
            title="My first entry",
            date="10/30/1990",
            timeSpent=120,
            whatILearned=("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          "Nunc ut rhoncus felis, vel tincidunt neque."
                          "Cras egestas ac ipsum in posuere. Fusce suscipit, libero id malesuada placerat, "
                          "orci velit semper metus, quis pulvinar sem nunc vel augue. In ornare tempor metus, "
                          "sit amet congue justo porta et. Etiam pretium, sapien non fermentum consequat, "
                          "<a href="">dolor augue</a> gravida lacus, non accumsan. Vestibulum ut metus eleifend, "
                          "malesuada nisl at, scelerisque sapien."
                          "it is really hard to mention in here."),
            ResourcesToRemember="Teamtreehouse, beyin"
        )
    except ValueError:
        pass
    try:
        models.Tag.create(tag="BasicThings")
        models.Tag.create(tag="MyTag2")
        models.Tag.create(tag="MyTag3")
        models.Entry.get(models.Entry.slug == 'my-last-entry').tags.add(['BasicThings'])
        models.Entry.get(models.Entry.slug == 'my-last-entry').tags.add(['MyTag2', 'MyTag3'])
    except:
        pass

    app.run(debug=DEBUG, host=HOST, port=PORT)
