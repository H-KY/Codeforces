import requests
import csv
import json

api_url = 'https://codeforces.com/api/user.ratedList?activeOnly=true'


response = requests.get(api_url)



f = csv.writer(open('users.csv', 'w'))

f.writerow(['handle', 'firstName', 'lastName', 'country', 'rank', 'rating'])

for x in json.loads(response.text):
    print(x)
    break
    f.writerow([user['handle'], user['firstName'], user['lastName'], user['country'], str(user['rank']), str(user['rating'] )])

