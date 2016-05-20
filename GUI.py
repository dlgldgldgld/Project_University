# -*- coding: utf-8 -*-

from Tkinter import *

class ClearApp:
    def __init__(self, parent=0):
        self.mainWindow = Frame(parent)
        self.mainWindow.pack()

        self.entry = Entry(self.mainWindow)
        self.entry.insert(0,"")
        self.entry.pack(fill=X)

        fButtons = Frame(self.mainWindow,border=1,relief = "groove")
        b1 = Button(fButtons, text= "1", width = 3, height = 2, command = (lambda char = 1 : self.Enter_Index(char)))
        b2 = Button(fButtons, text= "2", width = 3, height = 2, command = (lambda char = 2 : self.Enter_Index(char)))
        b3 = Button(fButtons, text= "3", width = 3, height = 2, command = (lambda char = 3 : self.Enter_Index(char)))
        b4 = Button(fButtons, text= "+", width = 3, height = 2, command = (lambda char = '+' : self.Enter_Index(char)))


        b1.pack(side="left", padx=2,pady=2)
        b2.pack(side="left", padx=2,pady=2)
        b3.pack(side="left", padx=2,pady=2)
        b4.pack(side="left", padx=2,pady=2)
        fButtons.pack(fill=X)

        fButtons2 = Frame(self.mainWindow,border=1,relief = "groove")
        b1 = Button(fButtons2, text= "4", width = 3, height = 2, command = (lambda char = 4 : self.Enter_Index(char)))
        b2 = Button(fButtons2, text= "5", width = 3, height = 2, command = (lambda char = 5 : self.Enter_Index(char)))
        b3 = Button(fButtons2, text= "6", width = 3, height = 2, command = (lambda char = 6 : self.Enter_Index(char)))
        b4 = Button(fButtons2, text= "-", width = 3, height = 2, command = (lambda char = '-' : self.Enter_Index(char)))

        b1.pack(side="left", padx=2,pady=2)
        b2.pack(side="left", padx=2,pady=2)
        b3.pack(side="left", padx=2,pady=2)
        b4.pack(side="left", padx=2,pady=2)
        fButtons2.pack(fill=X)

        fButtons3 = Frame(self.mainWindow,border=1,relief = "groove")
        b1 = Button(fButtons3, text= "7", width = 3, height = 2, command = (lambda char = 7 : self.Enter_Index(char)))
        b2 = Button(fButtons3, text= "8", width = 3, height = 2, command = (lambda char = 8 : self.Enter_Index(char)))
        b3 = Button(fButtons3, text= "9", width = 3, height = 2, command = (lambda char = 9 : self.Enter_Index(char)))
        b4 = Button(fButtons3, text= "=", width = 3, height = 2, command = (lambda char = '=' : self.Enter_Index(char)))

        b1.pack(side="left", padx=2,pady=2)
        b2.pack(side="left", padx=2,pady=2)
        b3.pack(side="left", padx=2,pady=2)
        b4.pack(side="left", padx=2,pady=2)
        fButtons3.pack(fill=X)

        self.mainWindow.master.title("°è»ê±â")
    def Enter_Index(self,btn) :
        if btn=='=':
            ans = eval(self.entry.get())
            self.entry.delete(0,END)
            self.entry.insert(0,ans)
        else :
            self.entry.insert(END,btn)





app = ClearApp()
app.mainWindow.mainloop()
