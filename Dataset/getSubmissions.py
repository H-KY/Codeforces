import requests
import csv
import os
import json
import sys
import ast


encoding = 'utf-8'

api_url = 'https://codeforces.com/api/user.status?handle='+sys.argv[1]+'&from=1&count=100000'
response = requests.get(api_url)

store_id = 0
authro = ''

# csv.field_size_limit(sys.maxsize)

# with open('problemset.problems', encoding=encoding) as inputfile:
    # df = pd.read_json(inputfile)

# df.to_csv('problems_int.csv', encoding=encoding, index=False)


f = csv.writer(open('submissions.csv', 'a'))

uf= open('Tables/users.csv', 'r')

user_dict = dict()

zz = 0
for line in uf:
    if zz != 0:
        zz = 1

#f.writerow(['problemId', 'name', 'contestId', 'rating', 'tags'])

def isInContest(submission):
    if 'contestId' not in submission:
        submission['contestId'] = -1
    return True

def checkUser(user):
    global authro
    authro = ''
    ss = "psql -d project -c \"SELECT * FROM users WHERE users.handle = '" + user['members'][0]['handle'] + "';\" -o tmp.txt"
    # print(ss)
    os.system(ss)
    num_lines = sum(1 for line in open('tmp.txt'))
    if num_lines >= 4:
        authro = user['members'][0]['handle']
        return True
    else:
        return False


def isNotinTeam(submission):
    arr = ['CONTESTANT','PRACTICE']
    # print(submission['ghost'])
    if 'teamId' not in submission and ('ghost' in submission and submission['ghost'] == False ) and submission['participantType'] in arr:
        #only one other is there
        assert len(submission['members']) == 1
        # print("YPE")
        return True
    return False

def removeQuote(s):
    s1 = s.replace('\"', '')
    s2 = s1.replace('\'', '')
    return s2
    


def checkProblem(problem):
    global store_id
    if 'rating' not in problem:
        return False
    store_id = -1
    ss = "psql -d project -c \"SELECT problems.problemid FROM problems WHERE problems.name = '" + removeQuote(problem['name']) + "' AND problems.rating = " + str(problem['rating']) + " ;\" -o tmp.txt"
    # print(ss)
    os.system(ss)
    num_lines = sum(1 for line in open('tmp.txt'))
    if num_lines >= 5:
        store_id = 3
        for line in open('tmp.txt'):
            store_id -= 1
            if store_id == 0:
                store_id = int(line.strip(' ').strip('\n'))
                break
        assert store_id != -1
        return True
    else:
        return False

def hasVerdit(submission):
    return 'verdict' in submission


def isValid(submission):
    return isInContest(submission) and isNotinTeam(submission['author'])  and checkProblem(submission['problem']) and checkUser(submission['author']) and hasVerdit(submission)

id = 0

# with open('problems_int.csv', mode='r') as file:
    # csvFile = csv.reader(file)
i = 0

response = json.loads(response.text)

# print(response['status'])
if response['status'] != 'OK':
    print("Error")
    exit()
else:
    print("Got response")

for lines in response['result']:
    if i != 0:
        #print(lines.decode(encoding))
        #x = json.loads(lines.decode(encoding))
        #x = ast.literal_eval(lines[1])
        x = lines
        #print(x)
        if not isValid(x):
            # print("HI")
            continue
        # print("yello")
        id += 1
        f.writerow([x['id'], x['contestId'], x['author']['participantType'], store_id, authro, x['programmingLanguage'] , x['verdict'], str(x['timeConsumedMillis']), str(x['memoryConsumedBytes']) ])
    i = 1

