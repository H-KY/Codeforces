from os import defpath
from flask import Blueprint, render_template, flash, request, redirect, jsonify
from flask.helpers import url_for
from flask_login import  current_user, logout_user, login_user, login_required
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

# @views.route('/profile/<handle>/home', methods=['GET', 'POST'])
# def profilehome(handle):
    # logging.debug("User: %s profile was requested", handle)
    # return render_template("profile_home.html", user=current_user)

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
    #TODO, pass both current_user and handle into the render_template
    logging.info("User: %s profile was requested", handle)
    
    profile_user = db_get_user_with_handle(website.db, website.dbConn, handle)
    if profile_user == None:
        return redirect(url_for('views.home'))
    
    profile_userObj = website.User(profile_user)
    profile_user_friends = db_get_num_followers(website.db, website.dbConn, handle)

    profile_userObj.numfollowers = profile_user_friends

    user_follows_profile = False
    if current_user.is_authenticated:
        user_follows_profile = db_is_follower(website.db, website.dbConn, current_user.handle, profile_userObj.handle) 

    return render_template("profile_home.html", user=current_user, profile_user = profile_userObj, user_follows_profile = user_follows_profile)


#TODO: make this user sepecific
user_attribute_store = dict()
#ideally we should not maintain this
#but kya kare itna atta nahi hai hume


@views.route('/users', methods=['GET', 'POST'])
def users():
    logging.info("Users search page request")
    #if request.method == 'POST':
    #no need to handle it separately

    if request.method == 'POST' or len(user_attribute_store) == 0:
        user_attribute_store['country'] = request.form.get('country', default = "", type=str)
        user_attribute_store['handle'] = request.form.get('handle', default = "", type=str) 
        user_attribute_store['rcmp'] = request.form.get('ratcmp', default="ge", type=str)
        user_attribute_store['rating'] = request.form.get('rating', default=0, type=int)
        user_attribute_store['ctrbcmp'] = request.form.get('ctrbcmp', default="ge", type=str)
        user_attribute_store['contributions'] = request.form.get('contribution', default=0, type=int)
        user_attribute_store['fcmp'] = request.form.get('fcmp', default="ge", type=str)
        user_attribute_store['numfollowers'] = request.form.get('numfollowers', default=0, type=int)
        user_attribute_store['cnstcmp'] = request.form.get('cnstcmp', default="ge", type=str)
        user_attribute_store['numcontests'] = request.form.get('numcontests', default=0, type=int)

    curr_page = request.args.get('pageNo', default=1, type=int)
    users_per_page = int(website.parser['users']['users_per_page'])
    users = db_get_users_with(website.db, website.dbConn, 
            user_attribute_store['country'],
            user_attribute_store['handle'],
            user_attribute_store['rcmp'],
            user_attribute_store['rating'],
            user_attribute_store['ctrbcmp'],
            user_attribute_store['contributions'],
            user_attribute_store['fcmp'],
            user_attribute_store['numfollowers'],
            user_attribute_store['cnstcmp'],
            user_attribute_store['numcontests'],
            (curr_page-1)*users_per_page, users_per_page+1)
    if curr_page != 1 and len(users) == 0:
        return redirect(url_for('views.users') + '?pageNo=1'  )

    first_page = (curr_page == 1)
    last_page = False

    if len(users) != users_per_page + 1:
        last_page = True
    else:
        users.pop()


    countries = db_get_countries(website.db, website.dbConn)

    return render_template("users.html", user = current_user, users= users, countries = countries, first_page = first_page, last_page =last_page, curr_page = curr_page)


#TODO make this separate for each user
problem_set_tag_store = dict()

@views.route('/problemSet', methods=['GET', 'POST'])
def problemSet():

    if request.method == 'POST' or len(problem_set_tag_store) == 0:
        problem_set_tag_store['rating'] = request.form.get('rating', default=0, type=int)
        problem_set_tag_store['rcmp'] = request.form.get('rcmp', default="ge", type=int)
        problem_set_tag_store['tags'] = request.form.getlist('tags')

    curr_page = request.args.get('pageNo', default = 1, type=int)
    problems_per_page = int(website.parser['users']['problems_per_page'])

    logging.debug("Rating: %s", problem_set_tag_store['rating'])
    logging.debug("Tags: [")
    for tag in problem_set_tag_store['tags']:
        logging.debug("%s,", tag)
    logging.debug("]")


    problems = db_get_problems_with(website.db, website.dbConn, 
            problem_set_tag_store['rating'], 
            problem_set_tag_store['rcmp'],
            problem_set_tag_store['tags'],
            (curr_page-1)*problems_per_page, problems_per_page+1)
            

    if curr_page != 1 and len(problems) == 0:
        return redirect(url_for('views.problemSet') + '?pageNo=1'  )

    first_page = (curr_page == 1)
    last_page = False
    if len(problems) != problems_per_page + 1:
        last_page = True
    else:
        problems.pop()

    for (idx, problem) in enumerate(problems):
        problems[idx] = website.Problem(problem)

    all_tags = db_get_all_problem_tags(website.db, website.dbConn)

    # all_tags = db_get_all_problem_tags(website.db, website.dbConn)
    return render_template("problemSet.html", user = current_user, all_tags = all_tags, problems = problems, curr_page=curr_page, first_page=first_page, last_page=last_page)



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
    event = db_delete_user(website.db, website.dbConn, current_user.handle)

    if event:
        flash('Deletion of account successful.', category='success')

        logging.info("Logging out user and redirecting to home page")
        logout_user()
    else:
        flash('Error in deleting account.' , category='error')



    return redirect(url_for('views.home'))

@views.route('/follow/<handle>', methods=['GET'])
@login_required
def make_follower(handle):
    logging.info("User %s request to become follower of %s", current_user.handle, handle)
    
    is_follower = db_is_follower(website.db, website.dbConn, current_user.handle, handle)
    assert not is_follower
    
    event = db_make_follower(website.db, website.dbConn, current_user.handle, handle)
    if event:
        flash('You have become a follower of ' + handle, category='success')
    else:
        flash('Some error occured' + handle, category='error')

    return jsonify({})

@views.route('/unfollow/<handle>', methods=['GET'])
@login_required
def make_unfollower(handle):
    logging.info("User %s request to unfollower of %s", current_user.handle, handle)
    
    is_follower = db_is_follower(website.db, website.dbConn, current_user.handle, handle)
    assert is_follower
    
    event = db_make_unfollower(website.db, website.dbConn, current_user.handle, handle)
    if event:
        flash('You have unfollowed ' + handle, category='success')
    else:
        flash('Some error occured' + handle, category='error')

    return jsonify({})

@views.route('/contest/<id>/problem/<index>', methods=['GET'])
def problem(id, index):
    logging.info("Problem with index: %s in contest: %d is requested", index, int(id))


    contest = db_get_contest(website.db, website.dbConn, int(id))
    if contest == None:
        return redirect(url_for('views.home'))

    problem = db_get_problem(website.db, website.dbConn, int(id), index)
    if problem == None:
        #TODO redirect to contest
        return redirect(url_for('views.home'))

    return render_template("problem.html", problem = website.Problem(problem), user=current_user, contest = website.Contest(contest))

@views.route('/contests')
def contestlist():
    logging.info("Contest page is requested")
    ongoing_contests = db_get_ongoing_contests(website.db, website.dbConn)
    for (idx,contest) in enumerate(ongoing_contests):
        ongoing_contests[idx] = website.Contest(contest)

    curr_page = request.args.get('pageNo', default=1, type=int)
    contest_per_page = int(website.parser['contest']['contest_per_page'])

    first_page = (curr_page == 1)
    last_page = False
    finished_contests = db_get_finished_contests(website.db, website.dbConn, (curr_page-1)*contest_per_page, contest_per_page+1)

    if len(finished_contests) != contest_per_page + 1:
        last_page = True
    else:
        finished_contests.pop()

    for (idx,contest) in enumerate(finished_contests):
        finished_contests[idx] = website.Contest(contest)

    upcoming_contests = db_get_upcoming_contests(website.db,website.dbConn)
    for (idx,contest) in enumerate(upcoming_contests):
        upcoming_contests[idx] = website.Contest(contest)

    recent_contests = []
    if current_user.is_authenticated:
        recent_contests = db_get_recent_contests(website.db, website.dbConn, current_user.handle)
        for (idx, contest) in enumerate(recent_contests):
            recent_contests[idx] = website.Contest(contest)
    
    return render_template("contests.html", user=current_user, ongoing_contests=ongoing_contests, finished_contests=finished_contests, upcoming_contests=upcoming_contests, recent_contests=recent_contests,  first_page=first_page, last_page=last_page, curr_page=curr_page)


