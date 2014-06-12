from Tkinter import *
from SideMenu import SideMenu
from MainWindow import MainWindow

root = Tk()
root.resizable(0,0)
root.title("Daniel's MFC Office Application")
MainWindow(root)
SideMenu(root)
root.mainloop()
