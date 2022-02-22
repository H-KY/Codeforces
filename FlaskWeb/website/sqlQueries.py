

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
                SELECT users.handle, users.rating, users.contribution, COUNT(*) as numfollowers
                FROM users JOIN friends ON users.handle = friends.handle2 
                WHERE users.handle LIKE '%(handle)s' AND users.rating %(rop)s %(rating)d AND users.contribution %(cntrop)s %(contribution)d AND users.country LIKE '%(country)s'
                GROUP BY users.handle
                HAVING COUNT(*) %(fcmp)s %(numfollowers)s
                ORDER BY users.rating DESC
                LIMIT %(length)d OFFSET %(offset)d;

            """

sql_num_followers = """
                SELECT COUNT(*)
                FROM friends
                WHERE friends.handle2 = '%(handle1)s';
            """

sql_check_follower = """
                SELECT friends.handle1, friends.handle2
                FROM friends
                WHERE friends.handle1 = '%(handle1)s' AND friends.handle2 = '%(handle2)s';
            """

sql_make_follower = """
                INSERT INTO friends VALUES ('%(handle1)s', '%(handle2)s');
            """


sql_make_unfollower = """
                DELETE FROM friends 
                WHERE friends.handle1 = '%(handle1)s' AND friends.handle2 = '%(handle2)s';
            """

sql_get_tags = """
                SELECT ARRAY_AGG(DISTINCT ptags)
                FROM problems, UNNEST(problems.tags) AS ptags;
            """

sql_search_problems = """
                SELECT *
                FROM problems
                WHERE problems.rating %(rop)s %(rating)d AND ARRAY %(ptags)s <@ problems.tags
                LIMIT %(length)d OFFSET %(offset)d;
            """
sql_search_problems_without_tags = """
                SELECT *
                FROM problems
                WHERE problems.rating %(rop)s %(rating)d 
                LIMIT %(length)d OFFSET %(offset)d;
            """


