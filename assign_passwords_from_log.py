#!/usr/bin/python

import argparse
import csv

def read_passwords(log_fh):
    result = []
    next_is_password = False
    for line in log_fh:
        line = line.strip()
        if line.startswith('*******'):
            next_is_password = True
        elif next_is_password:
            next_is_password = False
            if line.startswith('ec2-'):
                machine, password = line.split(' ', 1)
                result.append((machine, password))
    return result


def read_students(student_list_fh):
    students = []
    reader = csv.DictReader(student_list_fh)
    for record in reader:
        students.append((record['Email Address'], record['Student Name']))
    return students

def assign_machines(password_list, student_list):
    result = []
    for i in range(max(len(password_list), len(student_list))):
        machine = None
        password = None
        email = None
        name = None
        if len(password_list) > i:
            machine = password_list[i][0]
            password = password_list[i][1]
        if len(student_list) > i:
            email = student_list[i][0]
            name = student_list[i][1]
        result.append((machine, password, email, name))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('log', type=file)
    parser.add_argument('students_list', type=file)
    parser.add_argument('output_file', type=argparse.FileType('w'))

    args = parser.parse_args()

    passwords = read_passwords(args.log)
    students = read_students(args.students_list)
    result = assign_machines(passwords, students)
    writer = csv.writer(args.output_file)
    writer.writerow(('hostname', 'password', 'email', 'name'))
    for line in result:
        writer.writerow(line)
    args.output_file.close() 
