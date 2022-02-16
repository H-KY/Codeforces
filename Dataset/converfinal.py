import csv 
import pandas as pd
import json
import ast
with open('file.csv', 'w') as f:
    with open('csvfile.csv', mode='r') as file:
        csvFile = csv.reader(file)
        i = 0
        writer= csv.writer(f)

        writer.writerow(['handle'   , 'firstName', 'lastName', 'country', 'rank', 'rating', 'contribution'])
        for lines in csvFile:
            if i!=0:
                x = ast.literal_eval(lines[1])
                # print(type(x['handle']))
                if 'firstName' in x and 'country' in x and 'lastName' in x and 'contribution' in x:
                    writer.writerow( [ x['handle'],x['firstName'],x['lastName'],x['country'], x['rating'], x['contribution'] ])
            i=1
