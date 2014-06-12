import csv
import pickle


#This code takes the data from an excel spreadsheet saved as an csv
#uses the first row as the keys
#and makes a python dictionary of all the data

FILE = 'sales.csv'

Sales_Active = []

with open(FILE, mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if reader.line_num ==  1:
            headers = row
        else:
            Sales_Active.append(dict(zip(headers, row)))


#This is how to dump the list of dictionarys called sales into a pickled file


pickle.dump( Sales_Active, open("Sales_Active.p", 'wb'))


#Here's the code to unpickle the file back into a list object called sales:

"""
sales = pickle.load( open("sales.p", "rb"))
"""
