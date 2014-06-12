import csv
import pickle


#This code takes the data from an excel spreadsheet saved as an csv
#uses the first row as the keys
#and makes a python dictionary of all the data

FILE = 'salestax.csv'

Sales_Tax = {}

with open(FILE, mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        row[0] = row[0].strip()
        row[0] = row[0].lower()
        Sales_Tax[row[0]] = [row[1], row[2]]

for i in Sales_Tax:
    print(i, Sales_Tax[i])


#This is how to dump the list of dictionarys called sales into a pickled file


pickle.dump( Sales_Tax, open("Sales_Tax.p", 'wb'))


#Here's the code to unpickle the file back into a list object called sales:

"""
sales = pickle.load( open("sales.p", "rb"))
"""
