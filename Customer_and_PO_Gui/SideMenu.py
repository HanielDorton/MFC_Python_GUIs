from Tkinter import *
import subprocess
import pickle


class SideMenu:
    def __init__(self, parent):
        f = Frame(parent, width=20)
        f.pack(fill=None, expand=False, side=RIGHT)


        ### Open Folders ###

        self.button = Button(text="Important Docs", command=self.open_docs).pack(padx=10, pady=10, side=BOTTOM)
        self.button = Button(text="   Downloads   ", command=self.open_downloads).pack(padx=10,side=BOTTOM)

         ### Sales Tax ###

        self.Sales_Tax = pickle.load( open("Sales_Tax.p", "rb"))

        self.Tax_County = Text(width=15,height=1)
        self.Tax_County.pack(pady=10, side=BOTTOM)
        self.Tax_Rate = Text(width=4, height=1)
        self.Tax_Rate.pack(padx=10, pady=10, side=BOTTOM)
        self.Sales_Tax_Button = Button(text="Search", command=self.Get_Sales_Tax).pack(side=BOTTOM)
        self.Sales_Tax_Entry = Entry(width=15, bd=5)
        self.Sales_Tax_Entry.pack(pady=10, side=BOTTOM)
        self.Sales_Tax_Entry.bind('<Return>', lambda _:self.Get_Sales_Tax())
        self.Sales_Tax_Title = Label(text="Sales Tax Search").pack(side=BOTTOM)



        

    def Get_Sales_Tax(self):
        entry = self.Sales_Tax_Entry.get().lower()
        if entry in self.Sales_Tax:
            Current_Tax = self.Sales_Tax[entry]
        else:
            Current_Tax = ['','']
        self.Tax_Rate.delete(1.0, END)
        self.Tax_County.delete(1.0, END)
        self.Tax_Rate.insert(INSERT, Current_Tax[0])
        self.Tax_County.insert(INSERT, Current_Tax[1])

    def open_downloads(self):
        subprocess.Popen("explorer c:\users\daniel\Desktop\Downloads")
        

    def open_docs(self):
        subprocess.Popen("explorer c:\Users\daniel\Desktop\MFC_Office\ImportantDocs")


if __name__ == '__main__':
	root = Tk()
	root.title("Daniel's MFC Office Application")
	app = SideMenu(root)
	root.mainloop()
