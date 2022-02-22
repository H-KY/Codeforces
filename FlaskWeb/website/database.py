from posixpath import expanduser
import psycopg2
import logging
import sys
import website
from website.sqlQueries import *

def get_database_connection(host, port, name, user, password):
    logging.info("Connecting to database...")

    try:
        dbConn = psycopg2.connect(host=host, database=name, user=user, password=password, port=port)
        db = dbConn.cursor()
        logging.info("Connected to Database!")
    except:
        error = sys.exc_info()[0]
        logging.error("Connection to database failed with error: " + str(error))
        sys.exit(-1)
    return db, dbConn


def close_database_connection(db, dbConn):
    logging.info("Closing connection to database")

    if db is not None:
        db.close()
        logging.info("Communication cursor closed.")
    else:
        logging.warning("Trying to close a connection with NULL cursor")

    if dbConn is not None:
        dbConn.close()
        logging.info("Connection closed.")
    else:
        logging.warning("Trying to close a connection with NULL connection")

def db_get_user_with_handle(db, dbConn, handle):
    # Returns the user with handle=handle if user exists, else returns None
    logging.info("Querying User with Handle %s:", handle)
    if handle == "":
        logging.warning("Querying user with empty handle")
        return None
    if db == None:
        logging.critical("Querying with None db cursor!!")
        return None

    user_query = sql_user_with_handle % {'handle':handle}
    logging.debug(user_query)

    try:
        db.execute(user_query) 
        result = db.fetchall()
        logging.debug(result)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error querying the users table: %s",  e)
        dbConn.rollback()
        return None

    assert len(result) <= 1
    if len(result) == 1:
        return result[0]
    else:
        return None

def db_insert_user(db, dbConn, user):
    logging.info("Adding user: %s to users table", user.getStr() )
    assert len(user.handle) != 0
    assert len(user.firstname) != 0
    assert len(user.password) != 0

    if db == None:
        logging.critical("Inserting user with None db cursor!!")
        return 

    user_insert_query = sql_insert_user % {'user': user.getStr() }
    logging.debug("Insert query: %s", user_insert_query)
    try:
        db.execute(user_insert_query)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error inserting in the users table: %s",  e)
        dbConn.rollback()
    else:
        logging.debug("Insert query into users tables was successful")

def db_update_user(db, dbConn, handle, new_user):
    logging.info("Updating user with handle: %s", handle)
    logging.debug("New user attributes: %s", new_user.getStr())

    if db == None:
        logging.critical("Updating user with None db cursor!!")
        return 

    user_update_query = sql_update_user % {'old_handle': handle, 'new_handle': new_user.handle, 'firstname': new_user.firstname, 'lastname': new_user.lastname, 'country': new_user.country, 'password': new_user.password }

    logging.debug("Update user query: %s", user_update_query)
    try:
        db.execute(user_update_query)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error updating the users table: %s", e)
        dbConn.rollback()
    else:
        logging.info("Update query into users table was successful.")

def db_delete_user(db, dbConn, handle):
    logging.info("Deleteing user: %s", handle)

    if db == None:
        logging.critical("Updating user with None db cursor!!")
        return 

    user_delete_query = sql_delete_user % {'handle': handle}
    logging.debug("Delete user query: %s", user_delete_query)

    try:
        db.execute(user_delete_query)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error deleting the user from users table: %s", e)
        dbConn.rollback()
    else:
        logging.info("Deleting user was successful.")

def db_get_top_rated_users(db, dbConn, num):
    assert num >= 0
    logging.info("Querying database for %d top rated users", num)

    if db == None:
        logging.critical("Updating user with None db cursor!!")
        return 
    
    user_top_rated_query = sql_top_x_rated_users % {'num': num }
    logging.debug("User top rated query: %s", user_top_rated_query)
    try: 
        db.execute(user_top_rated_query)
        result = db.fetchall()
        logging.debug(result)
        assert len(result) <= num
        dbConn.commit()
    except Exception as e:
        logging.critical("Error querying top rated users. Error: %s", e)
        dbConn.rollback()
        return []

    return result

def db_get_top_contributors_users(db, dbConn, num):
    assert num >= 0
    logging.info("Querying database for %d top contributors users", num)

    if db == None:
        logging.critical("Updating user with None db cursor!!")
        return 
    
    user_top_contributors_query = sql_top_x_contributors_users % {'num': num }
    logging.debug("User top contributors query: %s", user_top_contributors_query)
    try: 
        db.execute(user_top_contributors_query)
        result = db.fetchall()
        logging.debug(result)
        assert len(result) <= num
        dbConn.commit()
    except Exception as e:
        logging.critical("Error querying top rated users. Error: %s", e)
        dbConn.rollback()
        return []

    return result

def db_get_countries(db, dbConn):
    logging.info("Querying database for coutries name")

    if db == None:
        logging.critical("Updating user with None db cursor!!")
        return 
    
    countries_query = sql_countries 
    logging.debug("Sql query for countries: %s", countries_query)

    try:
        db.execute(countries_query)
        result = db.fetchall()
        logging.debug(result)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error querying countries with prefix. Error %s", e)
        dbConn.rollback()
        return []
    return result


#TODO: complete function when more tables are added
def db_get_users_with(db, dbConn, country, handle, rcmp, rating, cntrcmp, contribution, fcmp, numfollowers, cnstcmp, numcontests, offset, length ):
    logging.info("Querying database for users with provided attributes")
    logging.debug("Handle: %s", handle)
    logging.debug("Country: %s", country)
    logging.debug("Rating: %s", rating)
    logging.debug("Contributions: %s", contribution)
    logging.debug("Numfriends: %s", numfollowers)
    logging.debug("Numcontest: %s", numcontests)
    logging.debug("rcmp: %s, cntrcmp: %s, fcmp: %s, cnstcmp: %s", rcmp, cntrcmp, fcmp, cnstcmp)
    
    cmp_to_op = { 'ge': '>=', 'gt': '>', 'lt': '<', 'le': '<='}

    def transform_handle(handle):
        t_handle = "%"
        for c in handle:
            t_handle += c
            t_handle += '%'
        return t_handle
    if country == "":
        country = "%"
    
    users_query = sql_users % {'handle': transform_handle(handle), 'rop': cmp_to_op[rcmp], 'cntrop': cmp_to_op[cntrcmp], 'rating': rating, 'contribution': contribution, 'country': country, 'numfollowers': numfollowers, 'fcmp': cmp_to_op[fcmp], 'length':length, 'offset': offset}
    try:
        logging.debug("Users search query: %s", users_query)
        db.execute(users_query)
        result = db.fetchall()
        logging.debug(result)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error querying database for users. Error %s", e)
        dbConn.rollback()
        return []
    return result

def db_get_num_followers(db, dbConn, handle):
    logging.info("Querying #num of followers of %s", handle)

    user_num_friend_query = sql_num_followers % {'handle1': handle}

    try:
        db.execute(user_num_friend_query)
        result = db.fetchall()
        logging.debug(result)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error querying database for friends of %s", handle)
        dbConn.rollback()
        return 0
    return result[0][0]
    

def db_is_follower(db, dbConn, handle1, handle2):

    logging.info("Check if %s is a follower of %s", handle1, handle2)
    user_follower_query = sql_check_follower % {'handle1': handle1, 'handle2': handle2}
    logging.debug("Query: %s", user_follower_query)
    try:
        db.execute(user_follower_query)
        result = db.fetchall()
        logging.debug(result)
        dbConn.commit()
    except Exception as e:
        logging.critical("Error querying database when checking follower. Error %s", e)
        dbConn.rollback()
        return False
    assert len(result) <= 1
    return (len(result) == 1)

def db_make_follower(db, dbConn, handle1, handle2):
    logging.info("Inserting into friends table: (%s, %s)", handle1, handle2)
    user_make_follower_query = sql_make_follower % {'handle1': handle1, 'handle2': handle2}
    logging.debug("Query: %s", user_make_follower_query)

    try:
        db.execute(user_make_follower_query)
        dbConn.commit()
    except Exception as e:
        logging.critical("Inserting into friends table unsuccesful. Error %s", e)
        dbConn.rollback()
        return False
    else:
        logging.info("Insertion is successful")
    return True

def db_make_unfollower(db, dbConn, handle1, handle2):
    logging.info("Deleting from friends table: (%s, %s)", handle1, handle2)
    user_make_unfollower_query = sql_make_unfollower % {'handle1': handle1, 'handle2': handle2}
    logging.debug("Query: %s", user_make_unfollower_query)

    try:
        db.execute(user_make_unfollower_query)
        dbConn.commit()
    except Exception as e:
        logging.critical("Deleting from friends table unsuccesful. Error %s", e)
        dbConn.rollback()
        return False
    else:
        logging.info("Deletion is successful")
    return True

def db_get_all_problem_tags(db, dbConn):
    logging.info("Querying database for all tags")
    problem_all_tag_query = sql_get_tags 
    logging.debug("Query %s", problem_all_tag_query)

    try:
        db.execute(problem_all_tag_query)
        result = db.fetchall()
        logging.debug(result)
        dbConn.commit()
    except Exception as e:
        logging.critical("Fetching tags unsuccesful. Error %s", e)
        dbConn.rollback()
        return []
    else:
        logging.info("Fetching tags successful")
    return result[0][0]

def db_get_problems_with(db, dbConn, rating, rcmp, tags, offset, length):
    logging.info("Querying database for problems with provided attributes")
    logging.debug("Rating: %s", rating)
    logging.debug("Rcmp: %s", rcmp)
    logging.debug("Tags: [")
    for tag in tags:
        logging.debug("%s,", tag)
    logging.debug("]")
    logging.debug("Offset: %s", offset)
    logging.debug("Length: %s", length)
    cmp_to_op = { 'ge': '>=', 'gt': '>', 'lt': '<', 'le': '<='}

    if '' in tags:
        tags.remove('') #remove this if present
    if len(tags) > 0:
        problem_search_query = sql_search_problems % {'rating':rating, 'rop':cmp_to_op[rcmp], 'ptags':str(tags), 'length':length, 'offset':offset }
    else:
        problem_search_query = sql_search_problems_without_tags % {'rating':rating, 'rop':cmp_to_op[rcmp], 'length':length, 'offset':offset }
    logging.debug(problem_search_query)
    try:
        db.execute(problem_search_query)
        result = db.fetchall()
        logging.debug(result)
        dbConn.commit()
    except Exception as e:
        logging.critical('Fetching problems was unsuccesful. Error %s', e)
        dbConn.rollback()
        return []
    else:
        logging.info('Fetching problems successful')
    return result
        



