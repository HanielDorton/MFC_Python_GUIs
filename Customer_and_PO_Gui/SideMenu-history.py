from Tkinter import *
import subprocess


class SideMenu:
    def __init__(self, parent):
        f = Frame(parent, width=20)
        f.pack(fill=None, expand=False, side=RIGHT)

        ### Open Folders ###

        self.button = Button(text="Important Docs", command=self.open_docs).pack(padx=10, pady=10, side=BOTTOM)
        self.button = Button(text="   Downloads   ", command=self.open_downloads).pack(padx=10,side=BOTTOM)

    def open_downloads(self):
        subprocess.Popen("explorer c:\users\daniel\Desktop\Downloads")
        

    def open_docs(self):
        subprocess.Popen("explorer c:\Users\daniel\Desktop\MFC_Office\ImportantDocs")


if __name__ == '__main__':
	root = Tk()
	root.title("Daniel's MFC Office Application")
	app = SideMenu(root)
	root.mainloop()
