

sql_user_with_handle = """
                        SELECT *
                        FROM users
                        WHERE users.handle = '%(handle)s';
                   """

sql_insert_user = """
                    INSERT INTO users VALUES %(user)s
                  """


