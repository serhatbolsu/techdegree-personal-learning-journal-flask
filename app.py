"""
Author: Serhat Bolsu
Date Created: Sept 22, 2017
Revision: 1.0
Title: Learning Journal with Flask
Description: Create a local web interface of a learning journal. The main
(index) page will list journal entry titles with a title and date. Each
journal entry title will link to a detail page that displays the title, date,
time spent, what you learned, and resources to remember. Include the ability
to add or edit journal entries. When adding or editing a journal entry, there
must be prompts for title, date, time spent, what you learned, resources to
remember. The results for these entries must be stored in a database and
displayed in a blog style website. The HTML/CSS for this site has been
supplied for you.
For each part choose from the tools we have covered in the courses so far.
Please don’t employ more advanced tools we haven’t covered yet, even if they
are right for the job. However, if you identify a place where a more advanced
tool is appropriate, please mention that in a code comment as you and your
mentor may want to discuss it later.
"""
from flask import (Flask, url_for, render_template, redirect, flash,
                   abort, g)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import models
import forms

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key = "dfşlj1*5u1qekfjqşeklfmqke-ekjr34éadfakjqşr134134kjfşkasdfjaşdf^^"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/entry', methods=('GET', 'POST'))
@login_required
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
@login_required
def view_entry(slug=None):
    # if id:
    #     entry = models.Entry.select().where(models.Entry.id == id).get()
    #     render_template(url_for('entry_detail'), entry=entry)
    #     return render_template('detail.html', entry=entry)
    # elif slug:
    entry = models.Entry.select().where(models.Entry.slug == slug).get()
    return render_template('detail.html', entry=entry)


@app.route('/entries/edit/<slug>', methods=('GET', 'POST'))
@login_required
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
        flash("Entry edited.", 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/delete/<slug>', methods=('GET', 'POST'))
@login_required
def delete_entry(slug):
    entry = models.Entry.select().where(models.Entry.slug == slug).get()
    if entry:
        entry.delete_instance()
        return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
@login_required
def index():
    entries = models.Entry.select().order_by(models.Entry.date.desc())
    return render_template('index.html', entries=entries)


# TODO: Not finished
@app.route('/tags/<slug>')
@login_required
def tag_entries(slug):
    tag = models.Tag.get(models.Tag.slug==slug)
    return render_template('index.html', entries=tag.entries)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email='serhat@email.com',
            password='1234',
            admin=True
        )
    except ValueError:
        pass
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
        models.Tag.create(name="BasicThings")
        models.Tag.create(name="MyTag2")
        models.Tag.create(name="MyTag3")
        models.Entry.get(models.Entry.slug == 'my-last-entry').tags.add(['BasicThings'])
        models.Entry.get(models.Entry.slug == 'my-first-entry').tags.add(['BasicThings'])
        models.Entry.get(models.Entry.slug == 'my-last-entry').tags.add(['MyTag2', 'MyTag3'])
    except:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
