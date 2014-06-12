import csv
import pickle

name = 'Cherryman_Amber'

new_list = {}

pickle.dump(new_list, open("%s.p" % name, 'wb'))
