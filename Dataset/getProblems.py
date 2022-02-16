import requests
import csv
import json
import sys
import ast
import pandas as pd


encoding = 'utf-8'

api_url = 'https://codeforces.com/api/problemset.problems'
response = requests.get(api_url)

f = csv.writer(open('problems1.csv', 'w'))

f.writerow(['problemId', 'name', 'contestId', 'index', 'rating', 'tags'])

def isInContest(problem):
    return 'contestId' in problem
def hasRating(problem):
    return 'rating' in problem

def hasIndex(problem):
    return 'index' in problem

def hasType(problem):
    return problem['type'] == 'PROGRAMMING'

def isValid(problem):
    return isInContest(problem) and hasRating(problem) and hasType(problem) and hasIndex(problem)


def removeQuote(s):
    s1 = s.replace('\"', '')
    s2 = s1.replace('\'', '')
    return s2
 

id = 0

i = 0

response = json.loads(response.text)
for lines in response['result']['problems']:
    if i != 0:
        x = lines
        if not isValid(x):
            continue
        id += 1
        f.writerow([id, removeQuote(x['name']), x['contestId'], x['index'], x['rating'], x['tags'] ])
    i = 1

