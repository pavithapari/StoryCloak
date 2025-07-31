from flask import Blueprint

from flask import render_template, request,flash,redirect,url_for
from flask_login import current_user,login_required
from datetime import datetime
from app.posts.forms import PostForm
from app.models import PrivateNote
from app import db

notes = Blueprint('notes', __name__)

@notes.route('/show_notes')
@login_required
def show_notes():
    user=current_user
    notes=user.private_notes
    if notes is None:
        notes = []
    return render_template('notes.html',notes=notes,now=datetime.now(),user=user)

@notes.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = PrivateNote.query.get(note_id)
    if note is not None:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('notes.show_notes'))

@notes.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form= PostForm()
    note = PrivateNote.query.get(note_id)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes.show_notes'))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
        form.visibility.data='private'
    return render_template('create_post.html', form=form, now=datetime.now(),user=current_user)

@notes.route('/readmore/<int:note_id>')
def read_more(note_id):
    note=PrivateNote.query.get(note_id)
    return render_template('readmore_notes.html', note=note, now=datetime.now(), user=current_user)