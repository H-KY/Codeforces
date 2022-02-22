import datetime
import logging

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
        self.numfollowers = None #Note: only non None for profile function other always null
    
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
        
class Problem:
    def __init__(self, problem):
        (problemId, name, constestId, problemIndex, rating, tags) = problem
        self.problemId = problemId
        (name, constestId, problemIndex, rating, tags) = problem
        self.name = name
        self.constestId = constestId
        self.problemIndex = problemIndex
        self.rating = rating
        self.tags = tags

        self.correct_submissions = 0


class Contest:
    def __init__(self, contest):
        (contestId, contestName, contestDate, problems, status, duration) = contest
        self.contestId = contestId
        self.contestName = contestName
        # self.contestDate = datetime.datetime(contestDate)
        self.contestDate = datetime.datetime.strptime(str(contestDate), '%Y-%m-%d')
        self.problems = problems
        self.status = status
        self.duration = duration
         
#Points to be noted 
#1. Database will return tuples
#2. If required tuples can be converted to the User class
#3. Database function doing insert will take these classes as input
