from flask import Blueprint, render_template, flash, request, redirect
from flask.helpers import url_for
from flask_login import  current_user, logout_user, login_user
from website.database import *
from werkzeug.security import generate_password_hash
import website
import logging

views = Blueprint('views', __name__)

@website.login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # new_note = Note(data=note, user_id=current_user.id)
            # db.session.add(new_note)
            # db.session.commit()
            flash('Note Added!', category='success')

    return render_template("home.html", user=current_user) 

@views.route('/profile/<handle>', methods=['GET', 'POST'])
def profile(handle):
    logging.debug("User: %s profile was requested", handle)
    return render_template("home.html", user=current_user)


@views.route('/profile/<handle>/edit', methods=['GET', 'POST'])
def account(handle):

    logging.debug("User: %s, Request Type: %s, Page: edit profile", handle, request.method)

    user = get_user_with_handle(website.db, website.dbConn, handle)
    if not current_user.is_authenticated:
        logging.debug("Edit profile page for user: %s, was requrest without login", handle)
        return redirect(url_for('views.profile', handle=handle))
    elif user:
        userObj = website.User(user)
        logging.debug("User %s exists in database. Check authorization", userObj.handle)
            
        if current_user.handle != userObj.handle:
            logging.debug("User %s is not authorizaed to edit user %s, redirecting to view profile page", current_user.handle, userObj.handle)
            return redirect(url_for('views.profile', handle=handle))

    else:
        logging.debug("No such user exists, redirecting to home page")
        return redirect(url_for('views.home'))


    if request.method == 'POST':
        logging.debug("Received post request on edit profile page")
        new_firstname = request.form.get('firstname')
        new_lastname = request.form.get('lastname')
        new_handle = request.form.get('handle')
        new_country = request.form.get('country')
        new_password1 = request.form.get('password1')
        new_password2 = request.form.get('password2')
        
        if new_handle != "":
            userObj.handle = new_handle
        handle_already_exists = (None != get_user_with_handle(website.db, website.dbConn, new_handle))
        if handle_already_exists:
            logging.debug("User requested for an already in use handle")
            flash('Handle already taken by some other user', category='error')
            return render_template("profile_edit.html", user=current_user)

        if new_firstname != "":
            userObj.firstname = new_firstname
        if new_lastname != "":
            userObj.lastname = new_lastname
        if new_country != "":
            userObj.country = new_country
        if new_password1 != new_password2:
            logging.debug("User entered non-matching passwords")
            flash("Password don't match", category='error')
            return render_template("profile_edit.html", user=current_user)

        if new_password1 != "":
            logging.debug("User entered a new password")
            userObj.password = generate_password_hash(new_password1, method='sha256')

        update_user(website.db, website.dbConn, current_user.handle, userObj)
        flash('Profile Updated!', category='success')
        
        logout_user()
        login_user(userObj, remember=True)

        return redirect(url_for('views.profile', handle=handle))

    #handle get request here
    logging.debug("Authorization Successful, User %s is on edit profile page", userObj.handle)
    return render_template("profile_edit.html", user=current_user)
