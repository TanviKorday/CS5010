
#coding = utf8
__author__ = 'Jilin Yan'

import sys, time

if __name__ == '__main__':

    notebook = file("./notebook.log", "w+")
    notebook_lines = ""
    
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
            output_line = "%s\tstart\t%d\t%s" % (time.strftime('%m/%d %H:%M', time.localtime(time.time())), question_num, comments)
            notebook_lines += output_line + "\n"
            while(True):
                print "--------------- stop or pause or resume ---------------"
                input_op = raw_input()
                if input_op == "stop" or input_op == "pause" or input_op == "resume":
                    output_line = "%s\t%s\t%d\t%s" % (time.strftime('%m/%d %H:%M', time.localtime(time.time())), input_op, question_num, comments)
                    notebook_lines += output_line + "\n"
                if input_op == "stop":
                    notebook_lines += "--------------- Split Line ---------------\n"
                    break
        elif first_op == "exit":
            notebook.writelines(notebook_lines)
            notebook.flush()
            notebook.close()
            exit(0)
