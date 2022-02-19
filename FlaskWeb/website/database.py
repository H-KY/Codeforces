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
    logging.debug("Querying User with Handle %s:", handle)
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
    except Exception as e:
        logging.critical("Error querying the users table: %s",  e)
        return None

    assert len(result) <= 1
    if len(result) == 1:
        return result[0]
    else:
        return None

def db_insert_user(db, dbConn, user):
    logging.debug("Adding user: %s to users table", user.getStr() )
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
    logging.debug("Updating user with handle: %s", handle)
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
        logging.debug("Update query into users table was successful.")

def db_delete_user(db, dbConn, handle):
    logging.debug("Deleteing user: %s", handle)

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
        logging.debug("Deleting user was successful.")

def db_get_top_rated_users(db, dbConn, num):
    assert num >= 0
    logging.debug("Querying database for %d top rated users", num)

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
    except Exception as e:
        logging.critical("Error querying top rated users. Error: %s", e)
        return None

    return result

def db_get_top_contributors_users(db, dbConn, num):
    assert num >= 0
    logging.debug("Querying database for %d top contributors users", num)

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
    except Exception as e:
        logging.critical("Error querying top rated users. Error: %s", e)
        return None

    return result
