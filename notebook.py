#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, os, math, re
from types import ListType, StringType

NOTEBOOK_FILE = 'notebook.txt'
USERNAME_FILE = 'me'

problem_set = None
username = None

records = []


def timestamp():
    utc = time.time()
    date = time.strftime("%m/%d", time.localtime(utc))
    now = time.strftime("%H:%M", time.localtime(utc))

    return date, now, utc

def column_len(lines, index):
    length = 0
    for line in lines:
        if type(line) is ListType and len(line[index]) > length:
            length = len(line[index])

    return length + 2

def pretty_print(records):
    lines = [["Date", "Who", "Start", "Stop", "Interruptions", "Question", "TimeOnTask", "Comments"]]
    for record in records:
        if is_question_record(record):
            words = re.split(r"\s{2,}", record)
            if len(words) == 7:
                words[4:4] = [""]
            lines.append(words)
        elif is_commit_record(record):
            lines.append(record)

    output = ''
    for line in lines:
        if type(line) is ListType:
            index = 0
            for word in line:
                if index != 7:
                    output += ("%-" + str(column_len(lines, index)) + "s") % word
                else:
                    output += word
                index += 1
            output += "\n"
        elif type(line) is StringType:
            output += line + "\n"

    return output

def write_log():
    notebook_path = os.path.join(problem_set, NOTEBOOK_FILE)
    with open(notebook_path, 'w') as notebook:
        notebook.write(pretty_print(records))

def commit_to_git():
    date, now, utc = timestamp()
    records.append("========== committing to git %s ===========" % (date + ' ' + now))
    write_log()

def validate_yes_no(msg):
    return msg.upper() == 'Y'

def validate_integer(msg):
    try:
        value = int(msg)
        return True
    except:
        return False

def validate_non_empty(msg):
    return msg != ''

def work_on_question():
    question = prompt("Which question are you going to work on?", validate_integer)

    start_date, start_time, start_utc = timestamp()

    comment = prompt("What are you going to do?", validate_non_empty)

    prompt("Finished? [y/n]", validate_yes_no)
    stop_date, stop_time, stop_utc = timestamp()

    duration = int(math.ceil((stop_utc - start_utc) / 60))

    coworkers = prompt("Who is working with you? (split by ',')").split(',')
    if len(coworkers) == 1 and coworkers[0] == '':
        coworkers = [username]
    else:
        coworkers.insert(0, username)

    #TODO interruptions

    records.append(start_date + "  " +
                   ','.join(coworkers) + "  " +
                   start_time + "  " +
                   stop_time + "  " +
                   "    " +
                   question + "  " +
                   str(duration) + "  " +
                   comment)
    write_log()

def menu_loop():
    choice = prompt("Welcome! " + username + "\n" +
                    "Please choose an action:\n" +
                    "1. Start working on a question.\n" +
                    "2. Commit to git.\n" +
                    "3. Exit.")

    if choice == '1':
        work_on_question()
    elif choice == '2':
        commit_to_git()
    elif choice == '3':
        exit(0)
    else:
        print "invalid input"

def prompt(msg, validate_p = None):
    validate = False

    while not validate:
        print msg
        user_input = raw_input("> ").strip()

        if validate_p:
            validate = validate_p(user_input)
        else:
            validate = True

    return user_input

def username_exists():
    return os.path.isfile(USERNAME_FILE)

def ask_for_username():
    return prompt("May I have your name?", validate_non_empty)

def save_username(username):
    with open(USERNAME_FILE, 'w') as f:
        f.write(username)

def retrieve_username():
    with open(USERNAME_FILE, 'r') as f:
        return f.read()

def get_username():
    if username_exists():
        username = retrieve_username()
    else:
        username = ask_for_username()
        save_username(username)

    return username

def is_question_record(text):
    return text[0] <= '9' and text[0] >= '0'

def is_commit_record(text):
    return text[0] == '='

def parse_notebook(lines):
    for line in lines:
        if is_commit_record(line):
            records.append(line[0:-1])
        elif is_question_record(line):
            records.append(line[0:-1])

def get_problem_set():
    global problem_set

    ps_number = prompt("Which problem set do you want to work on?", validate_integer)
    while len(ps_number) < 2:
        ps_number = '0' + ps_number

    problem_set = "set" + ps_number

    # create problem set folder
    if not os.path.exists(problem_set):
        os.mkdir(problem_set)

    notebook_path = os.path.join(problem_set, NOTEBOOK_FILE)
    if os.path.exists(notebook_path):
        with open(notebook_path, 'r') as notebook:
            parse_notebook(notebook.readlines())

def main():
    global username
    username = get_username()
    get_problem_set()

    while True:
        menu_loop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt, SystemExit:
        print "\nprogram exit"
        exit(0)
