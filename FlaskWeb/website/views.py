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
    logging.info("Home page is requested") 

    num_top_rated = int(website.parser['home_page']['num_top_rated'])
    num_top_contributors = int(website.parser['home_page']['num_top_contributors'])
    top_rated_users = db_get_top_rated_users(website.db, website.dbConn, num_top_rated)
    top_contributors_users = db_get_top_contributors_users(website.db, website.dbConn, num_top_contributors)
    return render_template("home.html", user=current_user, top_rated_users = top_rated_users, top_contributors_users= top_contributors_users) 

@views.route('/profile/<handle>/home', methods=['GET', 'POST'])
def profilehome(handle):
    logging.debug("User: %s profile was requested", handle)
    return render_template("profile_home.html", user=current_user)

@views.route('/profile/<handle>/blog', methods=['GET', 'POST'])
def profileblog(handle):
    logging.debug("User: %s blogs was requested", handle)
    return render_template("profile_blog.html", user=current_user)

@views.route('/profile/<handle>/contest', methods=['GET', 'POST'])
def profilecontest(handle):
    logging.debug("User: %s contests was requested", handle)
    return render_template("profile_contest.html", user=current_user)

@views.route('/profile/<handle>/submission', methods=['GET', 'POST'])
def profilesubmission(handle):
    logging.debug("User: %s submission was requested", handle)
    return render_template("profile_submission.html", user=current_user)

@views.route('/profile/<handle>/friend', methods=['GET', 'POST'])
def profilefriend(handle):
    logging.debug("User: %s friends was requested", handle)
    return render_template("profile_friend.html", user=current_user)

@views.route('/profile/<handle>', methods=['GET', 'POST'])
def profile(handle):
    logging.info("User: %s profile was requested", handle)
    return render_template("home.html", user=current_user)


@views.route('/profile/<handle>/edit', methods=['GET', 'POST'])
def account(handle):

    logging.info("User: %s, Request Type: %s, Page: edit profile", handle, request.method)

    user = db_get_user_with_handle(website.db, website.dbConn, handle)
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
        logging.info("Received post request on edit profile page")
        new_firstname = request.form.get('firstname')
        new_lastname = request.form.get('lastname')
        new_handle = request.form.get('handle')
        new_country = request.form.get('country')
        new_password1 = request.form.get('password1')
        new_password2 = request.form.get('password2')
        
        if new_handle != "":
            userObj.handle = new_handle
        handle_already_exists = (None != db_get_user_with_handle(website.db, website.dbConn, new_handle))
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

        db_update_user(website.db, website.dbConn, current_user.handle, userObj)
        flash('Profile Updated!', category='success')
        
        logout_user()

        login_user(userObj, remember=True)

        return redirect(url_for('views.profile', handle=handle))

    #handle get request here
    logging.info("Authorization Successful, User %s is on edit profile page", userObj.handle)
    return render_template("profile_edit.html", user=current_user)

@views.route('/deleteProfile/<handle>', methods=['GET', 'POST'])
def delete_account(handle):
    #only post methods are accepted
    #delete the account of the user currently logged in
    #and then logout and redirect to home page
    
    logging.info("Got Account delete requres from user: %s", handle)
    assert db_get_user_with_handle(website.db, website.dbConn, current_user.handle) != None
    logging.info("Deleting user from database")
    db_delete_user(website.db, website.dbConn, current_user.handle)
    logging.info("Logging out user and redirecting to home page")
    logout_user()

    return redirect(url_for('views.home'))
    

