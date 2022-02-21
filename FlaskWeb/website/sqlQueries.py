

sql_user_with_handle = """
                        SELECT *
                        FROM users
                        WHERE users.handle = '%(handle)s';
                   """

sql_insert_user = """
                    INSERT INTO users VALUES %(user)s;
                  """


sql_update_user = """
                        UPDATE users
                        SET handle = '%(new_handle)s', firstname = '%(firstname)s', lastname = '%(lastname)s', country = '%(country)s', password = '%(password)s'  
                        WHERE handle = '%(old_handle)s';

                   """

sql_delete_user = """
                        DELETE FROM users
                               WHERE handle = '%(handle)s';
                  """

sql_top_x_rated_users = """
                        SELECT users.handle, users.rating
                        FROM users
                        ORDER BY users.rating DESC
                        LIMIT %(num)d;
                    """


sql_top_x_contributors_users = """
                        SELECT users.handle, users.contribution
                        FROM users
                        ORDER BY users.contribution DESC, users.rating DESC
                        LIMIT %(num)d;
                    """

sql_countries = """
                         SELECT DISTINCT users.country
                         FROM users
                         ORDER BY users.country;
                    """

sql_users = """
                SELECT users.handle, users.rating, users.contribution
                FROM users
                WHERE users.handle LIKE '%(handle)s' AND users.rating %(rop)s %(rating)d AND users.contribution %(cntrop)s %(contribution)d AND users.country LIKE '%(country)s'
                LIMIT 100;

            """
