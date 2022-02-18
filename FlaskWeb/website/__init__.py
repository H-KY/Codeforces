parser = None

db = None
dbConn = None

login_manager = None

# Maintained for integrity
# Attributes of user should be passed using this class
class User:
    def __init__(self, user):
        (handle, firstname, lastname, country, rating, contribution, password) = user
        self.handle = handle
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.rating = rating
        self.contribution = contribution
        self.password = password
        self.authenticated = False
    
    def is_active(self):
        return True

    def get_id(self):
        return self.handle

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    
    def getStr(self):
        return "('%s', '%s', '%s', '%s', %s, %s, '%s')" % (self.handle, self.firstname, self.lastname, self.country, self.rating, self.contribution, str(self.password))
        

#Points to be noted 
#1. Database will return tuples
#2. If required tuples can be converted to the User class
#3. Database function doing insert will take these classes as input
