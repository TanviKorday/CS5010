#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, os, math

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

def write_log():
    global problem_set

    notebook_path = os.path.join(problem_set, NOTEBOOK_FILE)
    with open(notebook_path, 'w') as notebook:
        notebook.write("Date  Who       Start Stop  Interruptions Question TimeOnTask    Comments\n")
        for record in records:
            notebook.write(record + "\n")

def commit_to_git():
    date, now, utc = timestamp()
    records.append("========== committing to git %s ===========" % (date + ' ' + now))
    write_log()

def work_on_question():
    question = prompt("Which question are you going to work on?")

    start_date, start_time, start_utc = timestamp()

    prompt("Finished?")
    stop_date, stop_time, stop_utc = timestamp()

    duration = int(math.ceil((stop_utc - start_utc) / 60))

    comment = prompt("What have you done?")

    coworkers = prompt("Who is working with you?")

    #TODO interruptions

    records.append(start_date + "  " +
                   username + ", " + coworkers + "  " +
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

def prompt(msg):
    print msg
    return raw_input("> ").strip()

def username_exists():
    return os.path.isfile(USERNAME_FILE)

def ask_for_username():
    return prompt("May I have your name?")

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

    ps_number = prompt("Which problem set do you want to work on?")
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
