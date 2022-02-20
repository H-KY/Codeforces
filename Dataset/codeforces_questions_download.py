import requests
from datetime import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from io import BytesIO
import os
import time

cwd = os.getcwd()
PATH = './problemSet'
try:
    os.mkdir('./problemSet')
except OSError as error: 
    print(error)

cf_contest_url = "https://codeforces.com/api/contest.list"
cf_problem_url = "https://codeforces.com/api/problemset.problems"
problem_domain = "https://codeforces.com/problemset/problem/{}/{}"
contest_date_limit = datetime(2000, 2, 1)
prepare_data = {}

# Assuming that CSV is in the same folder as this script
output_sheet_name = "Codeforces_Question_Details.csv"
csv_fieldnames = ["Contest Id", "Contest Name", "Contest Date",
                  "Problem Type", "Problem Name", "Rating", "Problem Location", "Tags"]

print('Fact: Firefox may take upto 30 seconds when started using selenium')
driver = webdriver.Firefox(executable_path='./geckodriver')


def prepare_contest_data():
    all_contest = requests.get(url=cf_contest_url).json()
    all_contest = all_contest["result"]
    for contest in all_contest:
        contest["cont_date"] = datetime.fromtimestamp(
            contest["startTimeSeconds"])
        if(contest["cont_date"] < contest_date_limit):
            continue
        prepare_data[contest["id"]] = {
            "Contest Id": contest["id"],
            "Contest Name": contest.get("name", ""),
            "Contest Date": contest["cont_date"].strftime("%d %b, %Y"),
            "problem_list": []
        }


def prepare_problem_data():
    all_problem = requests.get(url=cf_problem_url).json()
    all_problem = all_problem["result"]["problems"]
    for problem in all_problem:
        if problem["contestId"] not in prepare_data:
            continue

        created_problem_url = problem_domain.format(
            problem["contestId"], problem.get("index", ""))
        complete_tag_list = problem.get("tags", [])
        complete_tag_list = ' '.join(complete_tag_list)

        #getting questions
        driver.get(created_problem_url)
        if driver.current_url != created_problem_url:
            continue
        dir = PATH + '/' + str(problem["contestId"])
        if not os.path.isdir(dir):
            os.mkdir(dir)
        path = dir + '/' + problem.get("index", "") + ".png"
        driver.find_element_by_class_name('problem-statement').screenshot(path)


        problem_details = {
            "Problem Type": problem.get("index", ""),
            "Problem Name": problem.get("name", ""),
            "Rating": problem.get("rating", ""),
            "Problem Location": path,
            "Tags": complete_tag_list
        }
        prepare_data[problem["contestId"]
                     ]["problem_list"].append(problem_details)


def fill_csv_sheet():
    already_updated_contest = []
    with open(output_sheet_name, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        already_updated_contest = [int(line["Contest Id"]) for line in reader]

    with open(output_sheet_name, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames)
        for key, val in prepare_data.items():
            if int(key) in already_updated_contest:
                continue
            temp_row_data = {
                "Contest Id": val["Contest Id"],
                "Contest Name": val["Contest Name"],
                "Contest Date": val["Contest Date"]
            }
            for problem_xyz in val["problem_list"]:
                temp_row_data.update(problem_xyz)
                writer.writerow(temp_row_data)


def execute_script():
    csv_file = open(output_sheet_name, 'w')
    prepare_contest_data()
    prepare_problem_data()
    fill_csv_sheet()
    driver.quit()


execute_script()
