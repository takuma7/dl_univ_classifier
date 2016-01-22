# -*- coding: utf-8 -*-

import sys
import csv
import os
import json
from pprint import pprint
from itertools import groupby

files = [
        'asunaro.json',
        'gokakuo.json',
        'seisekiup.json',
        'tomonokai.json',
        'toshin.json',
        'umaster.json',
        'yotsuya.json'
        ]

universities = {}
with open("data/universities.csv", 'r') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        universities[(row[0].decode('utf-8'))] = {
                    'name-utf8': row[0],
                    'str_id': row[1],
                    'int_id': i
                }
        i += 1

students = []

for file in files:
    with open(file) as data_file:
        data = json.load(data_file)
        print('%s:\t%d' % (file, len(data)))
        students += data

print("\n")
print("%d students" % len(students))

m_students = []
f_students = []

for student in students:
    if student['gender'] == 'm':
        m_students.append(student)
    elif student['gender'] == 'f':
        f_students.append(student)
    else:
        print('invalid gender: %s' % student['gender'])

print('\tmale:\t%d' % len(m_students))
print('\tfemale:\t%d' % len(f_students))

with open('labeled_data_m.txt', 'w') as f:
    for m_student in m_students:
        path = m_student['images'][0]['path']
        faces_path = 'images/' + path.replace('full', 'faces')
        if os.path.isfile(faces_path):
            f.write("{path} {label}\n".format(
                path=faces_path,
                label=universities[m_student['university']]['int_id']))

with open('labeled_data_f.txt', 'w') as f:
    for f_student in f_students:
        path = f_student['images'][0]['path']
        faces_path = 'images/' + path.replace('full', 'faces')
        if os.path.isfile(faces_path):
            f.write("{path} {label}\n".format(
                path=faces_path,
                label=universities[f_student['university']]['int_id']))

m_students_by_univ = {}
f_students_by_univ = {}

for m_student in m_students:
    if m_student['university'] not in m_students_by_univ:
        if m_student['university'] in universities:
            m_students_by_univ[m_student['university']] = [m_student]
    else:
        m_students_by_univ[m_student['university']].append(m_student)

for f_student in f_students:
    if f_student['university'] not in f_students_by_univ:
        if f_student['university'] in universities:
            f_students_by_univ[f_student['university']] = [f_student]
    else:
        f_students_by_univ[f_student['university']].append(f_student)

print('male students:')
for k, v in m_students_by_univ.iteritems():
    print(u'\t' + k + u': ' + (str(len(v))).encode('utf-8'))

print('female students:')
for k, v in f_students_by_univ.iteritems():
    print(u'\t' + k + u': ' + (str(len(v))).encode('utf-8'))

