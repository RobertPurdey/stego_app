from tkinter import *
from gui import StegoGui

"Run stego app"
root = Tk()
root.title("Stego Tool")
stegoGui = StegoGui(root)
root.resizable(width=False, height=False)
stegoGui.mainloop()
