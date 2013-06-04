from tkinter import *

vendorfile = "US4-1-13.csv"
usdict = {}

"""
usdict keys are skus corresponding to a list of:
[0] = string with extra quotes = description
[1] = list price as float
[2] = our price as float
[3] = company name
[4] = default multiplier
"""

with open(vendorfile, 'r') as f:
    for line in f:
        line = line.split(',"""",')
        usdict[line[0]] = [line[1], float(line[2]), float(line[3]), line[4], line[5].strip()]

salestaxfile = "salestax.csv"
salestaxdict = {}

"""
salestaxdict key is city corresponding to list of:
[0] is taxrate
[1] is county
"""

with open(salestaxfile, 'r') as f:
    for line in f:
        line = line.split(',"""",')
        salestaxdict[line[0].lower()] = [line[3], line[4].strip()]


def findsku(sku):
    '''give it a sku it returns the list of the five objects'''
    sku = sku.strip()
    if sku in usdict:
        result = usdict[sku]
        return result
    else:
        return ['',1,1,'',1]

def calculatesell(result):
    """returns either multiplier*ourcost if that is less than list*.9, else list*.9"""
    multiplier = result[2]*float(result[4])
    discounter = result[1]*.9
    if multiplier < discounter:
        return "{0:.2f}".format(multiplier)
    else:
        return "{0:.2f}".format(discounter)

def displayinfo(ignore):
    entry = entersku.entry.get().upper()
    result = findsku(entry)
    showprice = calculatesell(result)
    fields = {company : result[3][:-1] ,
              companysku : entry ,
              description : result[0].replace('"', '',) ,
              listprice: result[1] ,
              ourprice: result[2] ,
              sellprice: showprice , 
              multiplier: float(showprice)/result[2] }
    for field in fields:
        field.text.delete(1.0, END)
    if result[0] == '':
        return
    for field in fields:
        field.text.insert(INSERT, fields[field])
        
def changemultiplier(ignore):
    entry = float(changemulty.entry.get())
    if len(ourprice.text.get(1.0, END)) == 1:
        return
    mfccost = float(ourprice.text.get(1.0,END))
    newsellprice = mfccost * entry
    sellprice.text.delete(1.0, END)
    multiplier.text.delete(1.0, END)
    sellprice.text.insert(INSERT, newsellprice)
    multiplier.text.insert(INSERT, (float(newsellprice)/mfccost))

    
def getsalestax(ignore):
    entry = salestaxenter.entry.get().lower()
    if entry in salestaxdict:
        taxlist = salestaxdict[entry]
    else:
        taxlist = ['','']
    taxrate.text.delete(1.0, END)
    taxratecounty.text.delete(1.0, END)
    taxrate.text.insert(INSERT, taxlist[0])
    taxratecounty.text.insert(INSERT, taxlist[1])
    

root = Tk()
root.wm_title("MFC Vendor & Sales Tax App")

class MyFrames():
    def __init__ (self, parent):
        self.frame = Frame(root, bd=10)
        self.frame.pack(side = TOP)

class MyEntries():
    def __init__ (self, parent, text, functcall):
        self.label = Label(parent.frame, text=text)
        self.label.pack(side=LEFT)
        self.entry = Entry(parent.frame, bd=5)
        self.entry.pack(side=LEFT)
        self.button = Button(parent.frame, text="Search", command=lambda: functcall(0))
        self.entry.bind('<Return>', functcall)
        self.button.pack(side=LEFT)

class MyTextBoxes():
    def __init__ (self, parent, text, width):
        self.label = Label(parent.frame, text=text)
        self.label.pack(side=LEFT)
        self.text = Text(parent.frame, width=width, height=1)
        self.text.pack(side=LEFT)

        
'''Row 1'''
sku = MyFrames(root)
entersku = MyEntries(sku, "Enter Sku: ", displayinfo)
changemulty = MyEntries(sku, "Update", changemultiplier)
'''Row 2'''
vendor = MyFrames(root)
company = MyTextBoxes(vendor, "Vendor: ", 20)
companysku = MyTextBoxes(vendor, "   SKU: ", 10)
description = MyTextBoxes(vendor, "   Description: ", 30)
'''Row 3'''
prices = MyFrames(root)
listprice = MyTextBoxes(prices, "List Price: ", 8)
ourprice = MyTextBoxes(prices, "   MFC's Cost: ", 8)
sellprice = MyTextBoxes(prices, "   Sell Price: ", 8)
multiplier = MyTextBoxes(prices, "   Multiplier: ", 4)
'''Row 4'''
salestax = MyFrames(root)
salestaxenter = MyEntries(salestax, "Current Sales Tax rate by City: ", getsalestax)
taxrate = MyTextBoxes(salestax, "   Tax Rate: ", 4)
taxratecounty = MyTextBoxes(salestax, "   District: ", 20)

root.mainloop()
