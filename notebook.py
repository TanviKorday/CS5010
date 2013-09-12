
#coding = utf8
__author__ = 'Jilin Yan'

import sys, time

def timestamp():
    return time.strftime('%m/%d %H:%M', time.localtime(time.time()))

def loop(notebook):
    def write_log(txt):
        notebook.write(txt + "\n")
        notebook.flush()

    while(True):
        print "--------------- start -question -comments or exit ---------------"
        input_op = raw_input().split()
        first_op = input_op[0]
        if first_op == "start":
            if len(input_op) < 3:
                continue
            question_num = int(input_op[1])
            comments = input_op[2]
            for i in range (3, len(input_op)):
                comments += " " + input_op[i]

            write_log("%s\tstart\t%d\t%s" % (timestamp(), question_num, comments))

            while(True):
                print "--------------- stop or pause or resume ---------------"
                input_op = raw_input()
                if input_op == "stop" or input_op == "pause" or input_op == "resume":
                    write_log("%s\t%s\t%d\t%s" % (timestamp(), input_op, question_num, comments))
                    if input_op == "stop":
                        write_log("--------------- Split Line ---------------")
                        break

        elif first_op == "exit":
            exit(0)

if __name__ == '__main__':
    suffix = int(time.time())
    with open("./notebook_%s.log" % suffix, "w") as notebook:
        loop(notebook)



