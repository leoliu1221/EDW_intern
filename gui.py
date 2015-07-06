from Tkinter import *
import tkFileDialog 
from main import get_result

class Stagegui(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.frameTop = Frame(self)
        
        self.search = Text(self.frameTop,bg='white',wrap=WORD)
        self.search.pack(side=LEFT,fill=BOTH,expand=YES)
        self.search.config(height=1)      
        self.searchButton = Button(self.frameTop,text='search')
        self.searchButton.config(height=1)
        self.searchButton.config(command=self.searchtxt)
        #self.search.bind('<Return>',self.search)
        print 'finished linking button'
        self.searchButton.pack(side=LEFT,fill=X,expand=YES,padx=5)
        self.frameTop.pack(side=TOP,expand=NO,fill=BOTH,pady=1)
        
        
        self.frameP = Frame(self)
        self.frameP.pack(side=LEFT,fill=BOTH)
        self.frame1 = Frame(self)
        self.frame1.pack(side=LEFT,fill=BOTH)
        self.frame2 = Frame(self)
        self.frame2.pack(side=LEFT,fill=BOTH,expand=YES)
        self.frame3 = Frame(self)
        self.frame3.pack(side=LEFT,fill=BOTH,expand=YES)

        self.parent = parent        
        self.centerWindow()
        self.initUI()
    def onselectP(self,evt):
        w = evt.widget
        if len(w.curselection()):
            return
        index = int(w.curselection()[0])
        value = int(w.get(index))
        temp = self.pGroup[value].keys()
        self.clear_listbox(self.list1)
        self.insert_to_listbox(temp,self.list1)
        print 'onselect1: ', value
        text = self.data[value]
        self.clear_text(self.txt)
        self.insert_to_text(text,self.txt)
    def onselect1(self,evt):
        w = evt.widget
        
        if len(w.curselection())==0:
            return
        index = int(w.curselection()[0])
        value = int(w.get(index))
        temp = self.result[value]['stage'].items()
        print 'temp is: ' + str(temp)
        temp2 = []
        for item in temp:
            print 'start printing items'
            print 'item1',item[0]
            print 'item2',item[1]
        temp2 = [(str(item[0]) + ' ' + str(item[1][0][0]) + ' ID: ' +str(value)+' L#: '+ str(item[1][0][1])+ ' T: '+ str(item[1][0][2])) for item in temp]
        self.clear_listbox(self.list2)
        self.insert_to_listbox(temp2,self.list2)
        print 'onselect1: ', value
        text = self.data[value]
        self.clear_text(self.txt)
        self.insert_to_text(text,self.txt)
        
    def onselect2(self,evt):
        w = evt.widget
        if len(w.curselection())==0:
            return
        index = w.curselection()[0]
        value = w.get(index)
        index = value.split()[3]
        lineNum = int(value.split()[5])
        note = value.split()[7]
        text = ''
        if note == 'p':
            start = lineNum-1
            end = lineNum+1
            lines = self.data[int(index)][3].split('.')
            if len(lines)>end:
                end = len(lines)
            if start<0:
                start = 0
            text = lines[start:end]
        if note == 'pa':
            start = lineNum-1
            end = lineNum+2
            lines = self.data[int(index)][5].split('.')
            if len(lines)>end:
                end = len(lines)
            if start<0:
                start = 0
            text = lines[start:end]
        print 'text',text,'index',index
        print 'you selected item %s' % str(value)
        self.clear_text(self.txt)
        self.insert_to_text(text,self.txt)
        
    def initUI(self):
      
        self.parent.title("staging GUI")
        
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)

        menubar.add_cascade(label="File", menu=fileMenu)        
        
        self.listBox()
        self.textBox()
        self.pack(fill=BOTH, expand=YES)
        
    def onOpen(self):
        ftypes = [('csv files', '*.csv'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            text = self.readFile(fl)
            #self.txt.insert(END, text)

    def readFile(self, filename):
        self.clear_listbox(self.listP)
        self.clear_listbox(self.list1)
        self.clear_listbox(self.list2)
        self.clear_text(self.txt)
        #data is the original data, result is the result after processing for each row, pGroup is the pId grouping information. 
        # I am being lazy here. Did not change much of the code but want to achieve the same result
        self.data,self.result,self.pGroup = get_result(filename)
        print 'read file finished, len of data:', len(self.data), 'len of result ',len(self.result.keys())
        self.insert_to_listbox(self.pGroup.keys(),self.listP)
         
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
    
    def textBox(self):
        self.txt = Text(self.frame3,bg='white',wrap=WORD)
        self.txt.pack(side=LEFT,fill=BOTH,expand=YES)
        scrollbar3 = Scrollbar(self.frame3)
        scrollbar3.pack(side=RIGHT,fill=Y)
        self.txt.config(yscrollcommand=scrollbar3.set)
        scrollbar3.config(command=self.txt.yview)
        self.txt.config(state=DISABLED)
        #self.search = Text(self.frameTop,bg='white',wrap=WORD)
        #self.search.pack(side=TOP,fill=BOTH)
        #self.search.config(height=1)

    def listBox(self):
        self.listP = Listbox(self.frameP)
        self.listP.pack(side=LEFT,fill=BOTH,padx=3)
        self.listP.config(width=7)
        scrollbarP = Scrollbar(self.frameP)
        scrollbarP.pack(side=RIGHT,fill=BOTH,padx=3)
        self.listP.config(yscrollcommand=scrollbarP.set)
        scrollbarP.config(command=self.listP.yview)
        self.listP.bind('<<ListboxSelect>>',self.onselectP)
        self.list1 = Listbox(self.frame1)
        self.list1.pack(side=LEFT,fill=BOTH,padx=5) 
        scrollbar1 = Scrollbar(self.frame1)
        scrollbar1.pack(side=RIGHT,fill=Y)
        self.list1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=self.list1.yview)
        self.list1.config(width=5)
        self.list1.bind('<<ListboxSelect>>',self.onselect1)
        #self.list1.insert(END,1) 
        self.list2 = Listbox(self.frame2)
        self.list2.pack(side=LEFT,fill=BOTH,padx=5,expand=YES)
        self.list2.config(width=30)
        scrollbar2 = Scrollbar(self.frame2)
        scrollbar2.pack(side=RIGHT,fill=Y)
        self.list2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=self.list2.yview)
        self.list2.bind('<<ListboxSelect>>',self.onselect2)
        #self.list2.insert(END,1) 
    def insert_to_listbox(self,data,lBox):
        for item in data:
            lBox.insert(END,str(item))
    def clear_listbox(self,lBox):
        #lBox.delete(0,last=lBox.size()-1)
        lBox.delete(0,END)
    def insert_to_text(self,data,txt):
        txt.config(state=NORMAL)
        for item in data:
            txt.insert(END,str(item))
        txt.config(state=DISABLED)
    def clear_text(self,txt):
        txt.config(state=NORMAL)
        txt.delete(1.0, END)
        txt.config(state=DISABLED)        
    def search2(self):
        print 'in search2'
    def searchtxt(self):
        self.txt.config(state=NORMAL)
        self.txt.tag_remove('found', '1.0', END)
        s = self.search.get('1.0',END)[:-1]
        print 's is: ['+s+']'
        print s==''
        
        if not s=='':
            idx = '1.0'
            while 1:
                idx = self.txt.search(s, idx, nocase=1, stopindex=END)
                print idx
                
                if not idx:
                    break
                lastidx = '%s+%dc' % (idx, len(s))
                
                self.txt.tag_add('found', idx, lastidx)
            
                idx = lastidx
            self.txt.tag_config('found', foreground='white',background='black')
        self.txt.config(state=DISABLED)

def main():
    root = Tk()
    ex = Stagegui(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

