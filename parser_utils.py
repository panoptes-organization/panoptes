import os
import re
from pprint import pprint
from pandas.io.json import json_normalize
import datetime
import argparse
import sys

DATE = 'date'
LEVEL = 'level'
TYPE = 'type'
CLASS = 'class'
MESSAGE = 'message'

def match_date(line):
    match_this = ''
    matched = re.match(r'\[\w\w\w\s\w\w\w \d\d \d\d:\d\d:\d\d\s\d\d\d\d\]', line)
    if matched:
        # matches a date and adds it to match_this
        match_this = matched.group()
    else:
        match_this = 'NONE'
    return match_this


def generate_dicts(log_fh):
    current_dict = {}
    for line in log_fh:
        if line.startswith(match_date(line)):
            if current_dict:
                yield current_dict
            current_dict = {DATE: line.split('__')[0][1:25],
                            # TYPE: temp[0],
                            # CLASS: temp[1].split(' ')[2],
                            MESSAGE: ''}
        else:
            if DATE in current_dict:
                current_dict[MESSAGE] += line[:]
            else:
                pass

    yield current_dict


def structure_snakemake_logs(logs):
    """
    Takes as input a parced log dictionary.
    Returns a structured object for each entry.
    Two types of entries exist:
    - Submitted rules/jobs
    - Finished rules/jobs

    Returns list of structured entries
    """

    snakemake_log_objects = []

    for log in logs:

        if 'rule' in log['message']:

            print(log["message"])

            try:
                rule = re.search(r'rule (\w+):', log['message']).group(1)
            except:
                rule = None

            try:
                input = re.search(r'input:\s(.*)', log['message']).group(1).split(",")
            except Exception as e:
                input = None

            try:
                output = re.search(r'output:\s(.*)', log['message']).group(1).split(",")
            except:
                output = None

            try:
                log_c = re.search(r'log:\s(.*)', log['message']).group(1)
            except:
                log_c = None

            try:
                wildcards = re.search(r'wildcards:\s(.*)', log['message']).group(1).split(",")
            except Exception as e:
                wildcards = None

            try:
                jobid = re.search(r'jobid:\s(\d+)', log['message']).group(1)
            except Exception as e:
                jobid = None

            snakemake_log_objects.append({"job_type": 'submitted',
                                          "job_id": jobid,
                                          "rule": rule,
                                          "input": input,
                                          "output": output,
                                          "log": log_c,
                                          "wildcards": wildcards
                                          })

        elif "Finished job" in log['message']:
            try:
                job_id = re.search(r'Finished job (\d+)\.', log['message']).group(1)
                progress = re.search(r'(\d+) of (\d+) steps \((\d+%)\) done', log['message']).group(1,2,3)
                current_job = progress[0]
                total_jobs = progress[1]
                percent = progress[2]
            except Exception as e:
                current_job = None
                total_jobs = None
                percent = None

            snakemake_log_objects.append({"job_type": 'finished',
                                          "job_id": job_id,
                                          "current_job": current_job,
                                          "total_jobs": total_jobs,
                                          "percent": percent
                                          })

    return snakemake_log_objects

def main():
    """
        -import_file "example_files/example.log"
        -export_csv_file "exported_tabular.csv"

       :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-import_file', metavar='import_file', type=str,
                        help='Path to import the simulation json.')
    parser.add_argument('-export_csv_file', metavar='export_csv_file', type=str,
                        help='Path to export the results')
    args = parser.parse_args()

    import_file = args.import_file
    with open(import_file) as f:
        parced_logs = list(generate_dicts(f))

    pprint(parced_logs)

    print(structure_snakemake_logs(parced_logs))

    #data = parced_logs.jason_normalize()
    #data.to_csv('exported.csv')


if __name__ == '__main__':
    main()
