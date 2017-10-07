from tkinter import *
from gui import StegoGui

"Run stego app"
str = "zest"
str2 = str[-1]
r = 5
r = bin(r)[2:].zfill(8)
print("test:  " + str)
print("test2: " + str2)
print("rb = " + r)
root = Tk()
root.title("Stego Tool")
stegoGui = StegoGui(root)
stegoGui.mainloop()
