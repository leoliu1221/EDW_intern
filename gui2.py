from Tkinter import *
import tkFileDialog 
from get_data_breast import get_format_data
import json


class Stagegui(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.frameTop = Frame(self)
        
        
        self.searchButton = Button(self.frameTop,text='search')
        self.searchButton.config(height=1)
        self.searchButton.config(command=self.searchtxt)
        #self.search.bind('<Return>',self.search)
        self.searchButton.pack(side=RIGHT,fill=X,expand=NO,padx=5)
        print 'finished linking button'

        self.search = Entry(self.frameTop,bg='white')
        self.search.pack(side=RIGHT,fill=BOTH,expand=YES)    
        self.search.config(width=9)
        self.frameTop.pack(side=TOP,expand=NO,fill=BOTH,pady=1)
        
        self.frame1 = Frame(self)
        self.frame1.pack(side=LEFT,fill=BOTH)
        self.frame2 = Frame(self)
        self.frame2.pack(side=LEFT,fill=BOTH,expand=YES)
        self.frame3 = Frame(self)
        self.frame3.pack(side=LEFT,fill=BOTH,expand=YES)

        self.parent = parent        
        self.centerWindow()
        self.initUI()

    def onselect1(self,evt):
        w = evt.widget
        
        if len(w.curselection())==0:
            return
        index = int(w.curselection()[0])
        value = int(w.get(index))
        #result is documentid -> datapoints, 'content'
        #datapoints -> key:value
        #'content'-> ABCDEFG   
        #A -> 'adlkajfejlkaljekflea'
        temp = self.result[value].items()
        #print 'temp is: ' + str(temp)
        temp2 = []

        for k,v in temp:
            if k!='content':
                if len(self.result[value][k])>=1:
                    temp2.append(str(k)+':'+str(self.result[value][k][0]))
            else:
                for contentKey,contentC in self.result[value][k].items():
                    temp2.append(str(k)+'|'+str(contentKey)+':'+str(contentC))
        self.clear_listbox(self.list2)
        self.insert_to_listbox(temp2,self.list2)
        print 'onselect1: ', value
        text = self.data[value][1]
        self.clear_text(self.txt)
        self.insert_to_text(text,self.txt)
        
    def onselect2(self,evt):
        w = evt.widget
        if len(w.curselection())==0:
            return
            
        index = w.curselection()[0]
        value = w.get(index)
        k= value.split(':')[0]
        v = value.split(':')[1]
        
        index1 = self.list1.curselection()[0]
        row_num = int(self.list1.get(index1))
        #now value1 is our row selection. 
        
        
        if not k.startswith('content'):
            text = self.result[row_num][k][1].replace('._',':')
        else:
            text = v;

        #print 'text',text,'index',index
        print 'you selected item %s' % str(value)
        print 'text is:',text
        self.searchtxt(text)
        
    def initUI(self):
      
        self.parent.title("staging GUI")
        
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        fileMenu.add_command(label="Export to csv",command=self.onExport)
        menubar.add_cascade(label="File", menu=fileMenu)        
        
        self.listBox()
        self.textBox()
        self.pack(fill=BOTH, expand=YES)
    def onExport(self):
        fTypes=[('csv files', '*.csv'), ('All files', '*')]
        dlg = tkFileDialog.SaveAs(self,filetypes = fTypes)
        fl = dlg.show()
        if fl!='':
            if '.csv' not in fl:
                fl+='.csv'
            try:
                from file_utilities import exportFile
                exportFile(fileName=fl,data=self.data,result=self.result,pGroup=self.pGroup)
            except AttributeError:
                print 'please at least run once to save results'
           

        

    def onOpen(self):
        ftypes = [('csv files', '*.csv'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.readFile(fileName=fl)
            #self.txt.insert(END, text)
    def rerun(self):
        t1,t2,t3 = self.read_thresholds()
        try:
            self.readFile(data=self.data,t1=t1,t2=t2,t3=t3)
        except AttributeError:
            print 'no data defined. Cannot run. Please specify the input file'
    def readFile(self, fileName=None):
        if fileName is not None:
            self.clear_listbox(self.list1)
            self.clear_listbox(self.list2)
            self.clear_text(self.txt)
        #data is the original data, result is the result after processing for each row, pGroup is the pId grouping information. 
        # I am being lazy here. Did not change much of the code but want to achieve the same result
            print 'reading from ',fileName
            self.data,self.result = get_format_data(fileName=fileName) 
            print 'read file finished, len of data:', len(self.data), 'len of result ',len(self.result.keys())
            self.insert_to_listbox(self.result.keys(),self.list1)

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

        
        self.list1 = Listbox(self.frame1)
        self.list1.pack(side=LEFT,fill=BOTH,padx=5) 
        scrollbar1 = Scrollbar(self.frame1)
        scrollbar1.pack(side=RIGHT,fill=Y)
        self.list1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=self.list1.yview)
        self.list1.config(width=5)
        self.list1.bind('<<ListboxSelect>>',self.onselect1)
        self.list1.config(exportselection=False)
        #self.list1.insert(END,1) 
        self.list2 = Listbox(self.frame2)
        self.list2.pack(side=LEFT,fill=BOTH,padx=5,expand=YES)
        self.list2.config(width=30)
        scrollbar2 = Scrollbar(self.frame2)
        scrollbar2.pack(side=RIGHT,fill=Y)
        self.list2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=self.list2.yview)
        self.list2.bind('<<ListboxSelect>>',self.onselect2)
        self.list2.config(exportselection=False)
        #self.list2.insert(END,1) 
    def insert_to_listbox(self,data,lBox):
        for item in data:
            lBox.insert(END,str(item))
    def clear_listbox(self,lBox):
        #lBox.delete(0,last=lBox.size()-1)
        lBox.delete(0,END)
    def insert_to_text(self,data,txt,block=True):
        
        if block:
            txt.config(state=NORMAL)
            for item in data:
                txt.insert(END,str(item))
            txt.config(state=DISABLED)
        else:
            txt.config(state=NORMAL)
            for item in data:
                txt.insert(END,str(item))
    def clear_text(self,txt):
        txt.config(state=NORMAL)
        txt.delete(1.0, END)
        txt.config(state=DISABLED)        
    def search2(self):
        print 'in search2'
    def get_text(self,txt):
        return txt.get('1.0',END)[:-1]
    def searchtxt(self,s=None):
        self.txt.config(state=NORMAL)
        self.txt.tag_remove('found', '1.0', END)
        if s == None:
            s = self.search.get()
            print 's is: ['+s+']'
            print s==''
        
        if not s=='':
            idx = '1.0'
            while 1:
                s = s.replace('\n','')
                idx = self.txt.search(re.escape(s), idx, nocase=1, stopindex=END,regexp=True)
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

