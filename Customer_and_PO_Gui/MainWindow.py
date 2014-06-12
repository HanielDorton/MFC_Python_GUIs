from Tkinter import *
from tkMessageBox import showwarning, showinfo, askyesno
from tkFileDialog import asksaveasfilename
import csv
import pickle

class MainWindow(Frame):
    
    def __init__(self, root, master=None):
        
        Frame.__init__(self, master)
                
        global Current_View, Current_Filter, Active_Variable, Filter_Variable, View_Variable
        
        ### make header with top buttons###
        
        self.header = Frame(root, bd=2, relief=SUNKEN)
        self.header.pack(fill=None, expand=False)

        self.sep = Frame(self.header)
        self.sep.pack()

        Button_Inner_Padding = 20
        Button_Outer_Padding = 10

        View_Variable = StringVar(self.sep)
        View_Variable.set("Sales")
        View_Variable.trace("w", self.Draw_Tables)
        self.View_Menu = OptionMenu(self.sep, View_Variable, "Sales", "Purchases").pack(padx=Button_Outer_Padding, side=LEFT)

        Active_Variable = StringVar(self.sep)
        Active_Variable.set("Active")
        Active_Variable.trace("w", self.Draw_Tables)
        self.Active_Menu = OptionMenu(self.sep, Active_Variable, "Active", "History").pack(padx=Button_Outer_Padding, side=LEFT)

        Filter_Variable = StringVar(self.sep)
        Filter_Variable.set("")
        Filter_Variable.trace("w", self.Draw_Tables)
        self.Filter_Menu = OptionMenu(self.sep, Filter_Variable, "")
        self.Filter_Menu.pack(padx=Button_Outer_Padding, side=LEFT)
  
        self.Add_Row_Button = Button(self.sep, text="Add Row", padx=Button_Inner_Padding, command=self.Add_Row).pack(padx=Button_Outer_Padding, side=LEFT)
        self.Save_Button = Button(self.sep, text="Save", padx=Button_Inner_Padding, command=self.Save_Button).pack(padx=Button_Outer_Padding, side=LEFT)
        self.Export_Button = Button(self.sep, text="Export", padx=Button_Inner_Padding, command=self.Export_CVS).pack(padx=Button_Outer_Padding, side=LEFT)
        self.Quit_Button = Button(self.sep, text="Quit", padx=Button_Inner_Padding, command=self.On_Quit).pack(padx=Button_Outer_Padding, side=LEFT)

        ### make canvas/body frame for rows with scrollbar ###
        
        self.canvas = Canvas(root, borderwidth=0, background="#ffffff", width=990, height=600)
        self.body = Frame(self.canvas)
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side=LEFT, fill=None, expand=False,)
        self.canvas.create_window((4,4), window=self.body, anchor="nw", tags="self.body")
        self.body.bind("<Configure>", self.On_Frame_Configure)
        self.canvas.bind_all("<MouseWheel>", self.On_Mousewheel)

        
        ### Startup Default settings (active sales) ###
        
        Current_Filter = ""
        Current_View = ""
        self.Draw_Tables()
	
    def Draw_Tables(self, *args):
        
        global Current_View, Current_Filter, Last_Number

        ### First Saves all data if there is data and if isn't being filtered ###

        if Current_View:
            if not Current_Filter:
                self.Save_Pickle()
            self.Clear_Frames()

        ### Then updates all data variables and data iteself ###

        Current_View = View_Variable.get() + "_" + Active_Variable.get()
        self.data = pickle.load( open(Current_View + ".p", "rb"))
        Current_Filter = Filter_Variable.get()

        self.Filter_Menu['menu'].delete(0, 'end')

        ### make header row and filter data if needed ###

        if Current_View[:5] == "Sales":
            Filter_Choices = list(set([sale['Rep'] for sale in self.data]))
            self.columns= [['Customer',19],['Rep',7],['SO',4],['Signed',9],['POs',8],['Inventory',11],
                        ['DepinSF',11],['Job Done', 10],['Invoice',7],['Amount',14],['Date',12],['Last Billed',12],['Notes',35]]
            if Current_Filter:
                self.data = [item for item in self.data if item["Rep"] == Current_Filter]
            if Current_View[-6:] == "Active":
                Last_Number = int(self.data[-1]["SO"])+1
        else:
            Filter_Choices = list(set([sale['Company'] for sale in self.data]))
            self.columns= [["PO",21],["Company",18],["Rep",18],["Client",20],["Ordered",18],["Completed",18],["Notes",46]]
            if Current_Filter:
                self.data = [item for item in self.data if item["Company"] == Current_Filter]
            if Current_View[-6:] == "Active":
                Last_Number = int(self.data[-1]["PO"])+1

        Filter_Choices.insert(0, "")
        Filter_Choices = list(set(Filter_Choices))
        for filters in Filter_Choices:
            self.Filter_Menu['menu'].add_command(label=filters, command=lambda filters=filters: Filter_Variable.set(filters))

        self.separator = Frame(self.header)
        self.separator.pack(side=BOTTOM)
        for item in self.columns:
            self.key = Label(self.separator, text=item[0], width=int(item[1]*.88), relief=SUNKEN)
            self.key.pack(fill=None, expand=False, side=LEFT)
        self.lastkey = Label(self.separator,text="Side Menu", width=20, relief=SUNKEN)
        self.lastkey.pack(fill=None, expand=False, side=RIGHT)

        ### make rows and fill in with data (save references in self.rows) ###
        
        self.rows = []

        for row in self.data:        
            self.widgetrow = Frame(self.body, height=2, relief=SUNKEN)
            self.rows.append({})
            self.widgetrow.pack()
            for item in self.columns:
                    self.entry = Entry(self.widgetrow, width=item[1])
                    self.rows[-1][item[0]] = self.entry
                    self.entry.pack(fill=None, expand=False,side=LEFT)
                    self.entry.insert(0, row[item[0]])
                    

    def Export_CVS(self):
        
        file = asksaveasfilename(filetypes=[('CSV', '.csv')], initialfile='output.csv')
        try:
            
            f = open(file, "wb")
            headers=[head[0] for head in self.columns]
            csv_writer = csv.DictWriter(f, headers)
            csv_writer.writer.writerow(headers)
            csv_writer.writerows(self.data)
            f.close()
            showinfo("Success", "%s successfully created." % file)
        except:
            showinfo("Failure", "%s could not be created." % file)

    def Add_Row(self):
        
        global Last_Number
        if not Current_Filter and Current_View[-6:] == 'Active':
            self.widgetrow = Frame(self.body, height=2, relief=SUNKEN)
            self.rows.append({})
            self.widgetrow.pack()
            if Current_View[:5] == "Sales":
                keyword = "SO"
            else:
                keyword = "PO"            
            for item in self.columns:
                self.entry = Entry(self.widgetrow, width=item[1])
                self.rows[-1][item[0]] = self.entry
                self.entry.pack(fill=None, expand=False,side=LEFT)
                if item[0] == keyword:
                    self.entry.insert(0, Last_Number)
                    Last_Number += 1
        else:
            showwarning("Disabled",
                        "Adding Rows is only enabled on Active/Non-Filtered View.")
        
    def Save_Button(self):
        
        if Current_Filter:
            showwarning("Unable to Save",
                        "Save is disabled when list is filtered.")
        else:
            self.Draw_Tables()


    
    def Save_Pickle(self):
        
        if Current_Filter:
            showwarning("Unable to Save",
                        "Save is disabled when list is filtered.")
            return

        ### clear self.data and put all data from rows into it ###
        
        self.data = []
        for row in self.rows:
            self.data.append({})
            for item in row:
                self.data[-1][item] = row[item].get()
        
        ### dump data into  file                      ###
        ### also transfers completed items to history ###
                
        if Current_View[-6:] == "Active":
            Temp_History = []
            if Current_View[:5] == "Sales":
                Filter_Var = "Amount"
            else:
                Filter_Var = "Completed"
            for item in self.data:
                if item[Filter_Var] == "done":
                    Temp_History.append(item)
                    self.data.remove(item)
            if len(Temp_History)> 0:
                self.History = pickle.load( open(Current_View[:-7] +"_History.p", "rb"))
                for item in Temp_History:
                    self.History.append(item)
                pickle.dump(self.History, open(Current_View[:-7] + "_History.p", 'wb'))
        pickle.dump(self.data, open(Current_View + ".p", 'wb'))
                      
    def Clear_Frames(self):
        
        self.separator.pack_forget()
        self.separator.destroy()
        self.body.pack_forget()
        self.body.destroy()
        self.body = Frame(self.canvas)
        self.canvas.create_window((4,4), window=self.body, anchor="nw", tags="self.body")
        self.body.bind("<Configure>", self.On_Frame_Configure)

    def On_Quit(self):
        
        if Current_Filter:
            if askyesno("Verify Quit", "Unable to save when filtered by Rep. Continue without saving?") == False:
                return
        self.Save_Pickle()
        self.quit()


    ### functions for scrollbar ###
        
    def On_Frame_Configure(self, event):
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def On_Mousewheel(self, event):
        
        self.canvas.yview_scroll(-1*(event.delta/120), "units")
        


if __name__ == "__main__":
    root = Tk()
    root.title("Daniel's MFC Office Application")
    MainWindow(root)
    root.mainloop()
