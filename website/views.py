'''
This is going to hold pages the users can navigate to
'''
                                             #render template allows us to render the templates we've created to hold the pages (the different files containing the web pages)
from flask import Blueprint, render_template, flash, request, jsonify #Blueprint allows us to separate and organize our project, it has URLS defined in it 
from flask_login import login_required,  current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)




@views.route('/', methods=['GET','POST']) #this decorates a function to register it with a given URL 
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:     #ensure the note that's being deleted belongs to the useer trying to delete it
            db.session.delete(note)
            db.session.commit()
            flash('Note Deleted!', category='success')
    
    return jsonify({})