from Tkinter import *
import tkFileDialog 
from main import get_result

class Stagegui(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.frame1 = Frame(self)
        self.frame1.pack(side=LEFT,fill=Y)
        self.frame2 = Frame(self)
        self.frame2.pack(side=LEFT,fill=Y)
        self.frame3 = Frame(self)
        self.frame3.pack(side=LEFT,fill=Y)
         
        self.parent = parent        
        self.centerWindow()
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("File dialog")
        self.pack(fill=BOTH, expand=1)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)        
        

        self.txt = Text(self.frame3,background='red')
        #self.txt.pack(side=RIGHT,fill=BOTH)
        self.listBox()
        #self.label()
    def onOpen(self):
      
        ftypes = [('csv files', '*.csv'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):
        data,result = get_result(filename)
        f = open(filename, "r")
        text = f.read()
        return text
    def centerWindow(self):
        w = 1024
        h = 768

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
    def listBox(self):
        self.list1 = Listbox(self.frame1)
        self.list1.pack(side=LEFT,fill=BOTH,padx=5) 
        self.list2 = Listbox(self.frame2)
        self.list2.pack(side=LEFT,fill=BOTH,padx=5)
    def label(self):
        self.label['text']='hi, this is just a test on how long this text can go hopefuloly not too long that can block the other two components.I am pretty happy that this actually only expand to here. that will be good enough for me i guess '
def main():
    root = Tk()
    ex = Stagegui(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

