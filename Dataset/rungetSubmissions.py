import os
import requests
import csv
import os
import json
import sys
import ast
import time

f = csv.writer(open('submissions.csv', 'a'))

uf= open('Tables/users.csv', 'r')

user_dict = set()

store_id = 0
authro = ''

worked = 0


zz = 0
for line in uf:
    if zz != 0:
        user_dict.add(line.split(',')[0])
    zz = 1

problems_dict = dict()
pf = open('Tables/problems.csv', 'r')
zz = 0
for line in pf:
    if zz != 0:
        xx = line.split(',')
        problems_dict[(xx[1],xx[2],xx[3])] = xx[0]
    zz = 1


def isInContest(submission):
    if 'contestId' not in submission:
        submission['contestId'] = -1
    return True

def checkUser(user):
    global authro, user_dict
    authro = ''
    if user['members'][0]['handle'] in user_dict:
        authro = user['members'][0]['handle']
        return True
    else:
        return False
    
def isNotinTeam(submission):
    arr = ['CONTESTANT','PRACTICE']
    if 'teamId' not in submission and ('ghost' in submission and submission['ghost'] == False ) and submission['participantType'] in arr:
        assert len(submission['members']) == 1
        return True
    return False

def removeQuote(s):
    s1 = s.replace('\"', '')
    s2 = s1.replace('\'', '')
    return s2
    


def checkProblem(problem):
    global store_id,problems_dict
    if 'rating' not in problem or 'contestId' not in problem or 'name' not in problem:
        return False
    store_id = -1
    ra = problem['name']
    rb = str(problem['contestId'])
    rc = str(problem['rating'])

    zz = (removeQuote(ra),rb,rc) 
    if  zz in problems_dict:
        store_id = problems_dict[zz]
        return True
    else:
        return False

def hasVerdit(submission):
    return 'verdict' in submission


def isValid(submission):
    return isInContest(submission) and isNotinTeam(submission['author'])  and checkProblem(submission['problem']) and checkUser(submission['author']) and hasVerdit(submission)




def check_for_handle(__handle):
    global store_id,authro, worked
    worked = 0

    encoding = 'utf-8'

    api_url = 'https://codeforces.com/api/user.status?handle='+__handle+'&from=1&count=100000'
    response = requests.get(api_url)

    response = json.loads(response.text)

    if response['status'] != 'OK':
        print("Error")
        exit()
    else:
        worked = 1
        print("Got response")

    i = 0
    for lines in response['result']:
        if i != 0:
            x = lines
            if not isValid(x):
                continue
            f.writerow([x['id'], x['contestId'], x['author']['participantType'], store_id, authro, x['programmingLanguage'] , x['verdict'], str(x['timeConsumedMillis']), str(x['memoryConsumedBytes']) ])
        i = 1



f1 = open('users.csv', 'r')

id = 0
for line in f1:
    id += 1
    if id <= 10192:
        continue
    while worked == 0:
        check_for_handle(line.strip())
    worked = 0
    print("Processed: " , id)

