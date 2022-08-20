from tkinter import *
# Create object
from tkinter import filedialog

import parser.xml_parser

root = Tk()
root.geometry("600x600")


def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    # OptionMenu(root, StringVar(root), parser.xml_parser.loadMetaData(filename)).pack()
    print(parser.xml_parser.loadMetaData(filename))


Button(root, text="Upload", command=UploadAction).pack(side=TOP)
root.mainloop()
