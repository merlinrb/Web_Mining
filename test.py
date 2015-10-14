__author__ = 'NLP-PC'
import csv
with open('test.txt', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for l in reader:
        print(l)
