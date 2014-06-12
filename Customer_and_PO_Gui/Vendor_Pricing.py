from Tkinter import *
import pickle


class Vendor_Pricing:    
    def __init__(self, parent):
        self.Vendors = ['Cherryman_Amber',
                        'DMI_Fairplex   ',
                        'Friant_Gitana  ',

                        ]
        # cost, sell
        self.Vendor_Info = {
            'DMI_Fairplex   ':         [.224, 2],
            'Cherryman_Amber':      [.232, 1.75],
            'Friant_Gitana  ':        [.25, 1.85],
            
        }

        Button_Inner_Padding = 20
        Button_Outer_Padding = 10

        ## Main Frames ##
        
        self.f = Frame(parent, width=20)
        self.f.pack(fill=None, expand=False, side=BOTTOM)

        self.header = Frame(self.f, bd=2)
        self.header.pack(fill=None, expand=False)

        self.body = Frame(self.f, bd=2)
        self.body.pack(side=BOTTOM)

        ## Vendor Option Menu ##

        self.Vendor_Label = Label(self.header, text="Vendor: ").pack(side=LEFT)
        self.Vendor_Variable = StringVar(self.header)
        self.Vendor_Variable.set("Cherryman_Amber")
        self.Vendor_Menu = apply(OptionMenu, (self.header, self.Vendor_Variable) + tuple(self.Vendors))
        self.Vendor_Menu.pack(padx=10, side=LEFT)

        ## Save and Clear Buttons ##

        self.Clear_Button = Button(self.header, text="Clear", padx=Button_Inner_Padding, command=self.Clear_Rows).pack(padx=Button_Outer_Padding, side=RIGHT)
        self.Calculate_Button = Button(self.header, text="Calculate", padx=Button_Inner_Padding, command=self.Calculate_Sell)
        self.Calculate_Button.pack(padx=Button_Outer_Padding, side=RIGHT)


        ## Initial Set-up ##

        self.Clear_Rows()

        #self.columns = [['sell', 15], ['description', 25]]
        
    def Clear_Rows(self):
        self.body.pack_forget()
        self.body.destroy()
        self.body = Frame(self.f, bd=2)
        self.body.pack(side=BOTTOM)
        self.rows = {}
        for i in range(10):
            self.widgetrow = Frame(self.body, height=2, relief=SUNKEN)
            #self.rows.append(self.widgetrow)
            self.widgetrow.pack()
            self.sku = Entry(self.widgetrow, width=20)
            self.sku.pack(fill=None, expand=False,side=LEFT)
            self.list = Entry(self.widgetrow, width=10)
            self.list.pack(fill=None, expand=False,side=LEFT)
            self.cost = Entry(self.widgetrow, width=10)
            self.cost.pack(fill=None, expand=False,side=LEFT)
            self.sell = Entry(self.widgetrow, width=10)
            self.sell.pack(fill=None, expand=False,side=LEFT)
            self.rows[self.widgetrow] = [self.sku, self.list, self.cost, self.sell]

    def Calculate_Sell(self):
        Current_Vendor = self.Vendor_Variable.get()
        Current_Cost_Multiplier = float(self.Vendor_Info[Current_Vendor][0])
        Current_Sell_Multiplier = float(self.Vendor_Info[Current_Vendor][1])
        self.data = pickle.load( open("Data\\" + Current_Vendor.strip()+".p", "rb"))
        #print(self.data)
        for i in self.rows:
            sku = self.rows[i][0].get()
            cost = self.rows[i][1].get()
            #print(sku, cost)
            try:
                if self.data[sku]:
                    self.rows[i][1].delete(0, END)
                    self.rows[i][1].insert(0, self.data[sku][0])
                    self.rows[i][2].delete(0, END)
                    self.rows[i][2].insert(0, self.data[sku][1])
                    self.rows[i][3].delete(0, END)
                    self.rows[i][3].insert(0, float(self.data[sku][1])*Current_Sell_Multiplier)

            except:
                try:
                    self.rows[i][2].delete(0, END)
                    self.rows[i][2].insert(0, float(self.rows[i][1].get()) * Current_Cost_Multiplier)
                except:
                    pass
            
            
        
            
        




if __name__ == '__main__':
	root = Tk()
	root.resizable(0,0)
	root.title("Daniel's MFC Office Application")
	app = Vendor_Pricing(root)
	root.mainloop()
