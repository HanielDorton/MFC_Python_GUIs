import csv
import pickle


#This code takes the data from an excel spreadsheet saved as an csv
#uses the first row as the keys
#and makes a python dictionary of all the data


NAME = "Cherryman_Amber"

FILE = NAME + ".csv"

current_dict = {}

with open(FILE, mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        current_dict[row[0].strip().lower()] = [row[1], row[2], row[3]]
    


#This is how to dump the list of dictionarys called sales into a pickled file


pickle.dump( current_dict, open(NAME + ".p", 'wb'))


#Here's the code to unpickle the file back into a list object called sales:

"""
sales = pickle.load( open("sales.p", "rb"))
"""
