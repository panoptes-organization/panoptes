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
                current_dict[MESSAGE] += line[:-1]
            else:
                pass

    yield current_dict


def main():
    """
        -import_file "/home/giorgos/PycharmProjects/vzflow/example_files/example.log"
        -export_csv_file "/home/gkost/Documents/logs/exported_tabular.csv"

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

    #data = parced_logs.jason_normalize()
    #data.to_csv('exported.csv')


if __name__ == '__main__':
    main()
