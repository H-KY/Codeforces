

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
