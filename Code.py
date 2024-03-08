#Import all the required modules for this application

from tkinter import *
from tkinter import ttk
import sqlite3
import numpy as np
import scipy as sp
import babel.numbers
import matplotlib.pyplot as plt
import requests
import pycountry 
from tkinter import messagebox
from tkinter import filedialog
import os
from tkinter import PhotoImage,Image
from PIL import ImageTk
from tkPDFViewer import tkPDFViewer as pdf
from tkcalendar import Calendar
import json
from tkinter import font
from builtins import str
import requests
import bibtexparser
import re


#main Window creation

root=Tk()
root.title("My Own Space")
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the root window dimensions to match the screen size
root.geometry(f"{screen_width}x{screen_height}")

#multipage window creation, which is made available by the Notebook method in ttk.Notebook

nbook=ttk.Notebook(root)
nbook.pack()

#adding pages to the notebook interface

# To do frame
todo=ttk.Frame(nbook)
nbook.add(todo,text="To Do Lists",padding=10)














#my task frame
mytask=ttk.Frame(nbook)
nbook.add(mytask,text="My Own Tasks",padding=10)





















#Booklist Frame

booklist=ttk.Frame(nbook)
nbook.add(booklist,text="Booklist",padding=10)

def bookdatabase():
    """This is the function which is called in the begining of this frame. 
    This will try to create a database at the first run of the application.
    If the database is available from the beginning the will or on the second
    run this function will bypass the function creation.

    
    """
#Book Database
#creat the Book database or connect to one
    try:
        conn=sqlite3.connect("Book List.db")


        #create cursor
        c = conn.cursor()

        #creat table
        
        c.execute("""CREATE TABLE BookList(
            Book_Name text,
            Authors text,
            Publisher text,
            Book_Catagory text,
            price_tag text,
            ISBN text,
            Book_Subject text,
            Place text,
            Price int,
            Date text,
            DOI_Number text,
            Upload_Directory text,
            Borrowed text,
            Borrower_Name text,
            Borrow_return_date text
        )


            """)
        

        conn.commit()

        conn.close()
    except:
        pass

#database function calls, database created

bookdatabase()

#tkinter variable definition

catagory=StringVar()
yes_or_no=StringVar()
placedata=StringVar()
serial_number=StringVar()
borrow=StringVar()
searchnames=StringVar()
searchcatagories=StringVar()
searchbooksubjects=StringVar()
searchauthors=StringVar()

#Book catagories list and other list for combo box

catagories=['Academic','Science Fiction','Adventure','Detective','Travel','Teaching','Politics & Social Science','Thrillers/Suspence','Literary Fiction','law & Criminology','Business & Money','Humor & Entertainment','Motivational/Inspirational','Cooking','Art & Photography','Autobiography','Personal Development','Biography','Health & Fitness','Horror','Romance','Historic','Encyclopeida','Religious/Spirituality']
options=['Brought by Me','PDF Print','Gifted','Scan PDF/e-PDF']

# here all the functions are defined

def delete():
    """
    This fucntion is to delete data entries from the database
    by the defined oid ID number. This function will try to 
    connect to database and delete a single item. If multiple 
    item in treeview is selected or outofrange oid is given it will
    pass the function and reload the treeview.
    """
    deletebutton.config(activebackground="red")
    response=messagebox.askyesno("Delete From DataBase",message="Do you want to delete this item?")
    if response == True:
        try:
            conn = sqlite3.connect("Book List.db")
            c=conn.cursor()
            c.execute("DELETE FROM BookList WHERE oid="+str(serial_number.get()))
            conn.commit()
            conn.close()
            serial_no.delete(0,END)
            reload()
        except:
            reload()
    else:
        pass


def deleteall():
    pass

def treeselection(a):
    
    """
    When item from the treeview is selected, this function
    insert the oid ID of the selected item to database ID entry 
    widget for different perposes. 
    """
    try:
        serial_no.delete(0,END)
        serial_no.insert(0,tree.item(tree.selection())['text'])
    except:
        pass


def reload():
    """
    Reload the treeview.
    """
    for item in tree.get_children():
        tree.delete(item)
    conn=sqlite3.connect("Book List.db")
    c=conn.cursor()
    c.execute("SELECT *, oid FROM BookList")
    records=c.fetchall()

    for data in records:
        record=data
        tree.insert(parent='',index='end',text=record[15],value=(record[0],record[1],record[3],record[4],record[6],record[7],record[12],record[13],record[14]),tags=record[15])
        if int(record[15])%2==0:
            tree.tag_configure(record[15],background="#a4e1f5",foreground="#23077d")


    conn.commit()
    conn.close()

def namesearch(a,b,c):
    """
    This function search the database for book name with the similar name or word or 
    letter given in the book name search widget
    """
    conn=sqlite3.connect("Book List.db")
    c=conn.cursor()
    try:
        for item in tree.get_children():
            tree.delete(item)
        c.execute("""SELECT *, oid FROM BookList WHERE 
                  Book_Name LIKE ? 
                  AND Authors LIKE ?
                  AND Book_Catagory LIKE ?
                  AND Book_Subject LIKE ?
                  """, ('%'+str(searchnames.get())+'%','%'+str(searchauthors.get())+'%','%'+str(searchcatagories.get())+'%','%'+str(searchbooksubjects.get())+'%'))
        records=c.fetchall()
        for data in records:
            record=data
            tree.insert(parent='',index='end',text=record[15],value=(record[0],record[1],record[3],record[4],record[6],record[7],record[12],record[13],record[14]),tags=record[15])
            if int(record[15])%2==0:
                tree.tag_configure(record[15],background="#a4e1f5",foreground="#23077d")
    except:

        reload()
        pass   
    conn.commit()
    conn.close()


def catagorysearch(a,b,c):
    """
    This function search the database for catagory with the similar name or word or 
    letter given in the catagory search widget
    """
    conn=sqlite3.connect("Book List.db")
    c=conn.cursor()
    try:
        for item in tree.get_children():
            tree.delete(item)
        c.execute("""SELECT *, oid FROM BookList WHERE 
                  Book_Name LIKE ? 
                  AND Authors LIKE ?
                  AND Book_Catagory LIKE ?
                  AND Book_Subject LIKE ?
                  """, ('%'+str(searchnames.get())+'%','%'+str(searchauthors.get())+'%','%'+str(searchcatagories.get())+'%','%'+str(searchbooksubjects.get())+'%'))
        records=c.fetchall()
        for data in records:
            record=data
            tree.insert(parent='',index='end',text=record[15],value=(record[0],record[1],record[3],record[4],record[6],record[7],record[12],record[13],record[14]),tags=record[15])
            if int(record[15])%2==0:
                tree.tag_configure(record[15],background="#a4e1f5",foreground="#23077d")

    except:
        reload()
        pass   
    conn.commit()
    conn.close()



def authorsearch(a,b,c):
    """
    This function search the database for authors name with the similar name or word or 
    letter given in the authors search widget
    """
    conn=sqlite3.connect("Book List.db")
    c=conn.cursor()
    try:
        for item in tree.get_children():
            tree.delete(item)
        c.execute("""SELECT *, oid FROM BookList WHERE 
                  Book_Name LIKE ? 
                  AND Authors LIKE ?
                  AND Book_Catagory LIKE ?
                  AND Book_Subject LIKE ?
                  """, ('%'+str(searchnames.get())+'%','%'+str(searchauthors.get())+'%','%'+str(searchcatagories.get())+'%','%'+str(searchbooksubjects.get())+'%'))
        records=c.fetchall()
        for data in records:
            record=data
            tree.insert(parent='',index='end',text=record[15],value=(record[0],record[1],record[3],record[4],record[6],record[7],record[12],record[13],record[14]),tags=record[15])
            if int(record[15])%2==0:
                tree.tag_configure(record[15],background="#a4e1f5",foreground="#23077d")

    except:
        reload()
        pass   
    conn.commit()
    conn.close()



def booksubjectsearch(a,b,c):
    """
    This function search the database for the subjects with the similar name or word or 
    letter given in the subject search widget
    """
    conn=sqlite3.connect("Book List.db")
    c=conn.cursor()
    try:
        for item in tree.get_children():
            tree.delete(item)
        c.execute("""SELECT *, oid FROM BookList WHERE 
                  Book_Name LIKE ? 
                  AND Authors LIKE ?
                  AND Book_Catagory LIKE ?
                  AND Book_Subject LIKE ?
                  """, ('%'+str(searchnames.get())+'%','%'+str(searchauthors.get())+'%','%'+str(searchcatagories.get())+'%','%'+str(searchbooksubjects.get())+'%'))
        records=c.fetchall()
        for data in records:
            record=data
            tree.insert(parent='',index='end',text=record[15],value=(record[0],record[1],record[3],record[4],record[6],record[7],record[12],record[13],record[14]),tags=record[15])
            if int(record[15])%2==0:
                tree.tag_configure(record[15],background="#a4e1f5",foreground="#23077d")

    except:
        reload()
        pass   
    conn.commit()
    conn.close()


def entry_reload():
    """
    This function called when user make entry to the database
    with entry button press. 

    This function only calls other two function
    entry and reload at the same this.
    """
    entry()
    reload()

def update_reload():
    """
    This function called when user make updates to the database
    with update button press. 

    This function only calls other two function
    update and reload at the same this.
    """
    update()
    reload()

def button_color_picker(a):
    """
    This function helps to change the color of update buttons
    depending on the if the book is being issued or returned by the user.
    If Issued it will show red button upon activation of the update button.
    If returned it will be Green.
    """
    if borrow.get() == "Issue":
        updatebutton.config(activebackground="Red")
    if borrow.get() == "Return":
        updatebutton.config(activebackground="#95f587")

def entry():
    """
    This function connects to the database to add new entry to the database.
    This is called upon entry button activation via another function 
    entry_reload. Also delete all the entries in the entry widgets after wards
    """
    conn=sqlite3.connect("Book List.db")
    c=conn.cursor()
    c.execute("""INSERT INTO BookList VALUES(
              :Book_Name,
              :Authors,
              :Publisher,
              :Book_Catagory,
              :Price_tag,
              :ISBN,
              :Book_Subject,
              :Place,
              :Price,
              :Date,
              :DOI_Number,
              :Upload_Directory,
              :Borrowed,
              :Borrower_Name,
              :Borrow_return_date
              )""",
              {"Book_Name": bookname.get(),
               "Authors": authors.get(),
               "Publisher": publisher.get(),
               "Book_Catagory": typedata.get(),
               "Price_tag": book_print_type.get(),
               "ISBN": ISBNnumber.get(),
               "Book_Subject": topic.get(),
               "Place": place.get(),
               "Price": price.get(),
               "Date": calender.get_date(),
               "DOI_Number": doi.get(),
               "Upload_Directory": uploaddata.get(),
               "Borrowed": borrowed.get(),
               "Borrower_Name": isborrowed.get(),
               "Borrow_return_date": borrowcalender.get_date()
              }

    )
    conn.commit()
    conn.close()

    bookname.delete(0,END)
    authors.delete(0,END)
    publisher.delete(0,END)
    typedata.set("Academic")
    book_print_type.set("Brought by Me")
    ISBNnumber.delete(0,END)
    topic.delete(0,END)
    place.set("Home")
    price.delete(0,END)
    doi.delete(0,END)


def updatedata(a,b,c):
    """This function connects to the database to update an item to the database.
    This is called upon update button activation via another function 
    update_reload. Also delete all the entries in the entry widgets after wards
    """
    conn=sqlite3.connect("Book List.db")
    c=conn.cursor()
    try:
        c.execute("SELECT *, oid FROM BookList WHERE oid="+str(serial_number.get()))
        records=c.fetchall()
        data=records[0]
        borrowed.set(data[12])
        isborrowed.delete(0,END)
        isborrowed.insert(0,data[13])
        updatebutton.config(state=NORMAL)
        deletebutton.config(state=NORMAL)
    except:
        updatebutton.config(state=DISABLED)
        deletebutton.config(state=DISABLED)
    conn.commit()

    conn.close()

def update():
    try:
        conn=sqlite3.connect("Book List.db")
        c=conn.cursor()
        c.execute("""UPDATE BookList SET
                Borrowed = :Borrowed,
                Borrower_Name = :Borrower_Name,
                Borrow_return_date = :Borrow_return_date
                WHERE oid =:oid
                """,
                {
                    "Borrowed": borrowed.get(),
                    "Borrower_Name": isborrowed.get(),
                    "Borrow_return_date": borrowcalender.get_date(),
                    "oid": serial_number.get()
                })
        borrowed.set(" ")
        isborrowed.delete(0,END)
        serial_no.delete(0,END)
        conn.commit()
        conn.close()
    except:
        pass


#creation of all the important label frames which will contain 
#all the widgets

labelframe1=ttk.LabelFrame(booklist,text="Book DataBase Entry",padding=2)
labelframe1.grid(row=0,column=0,padx=5,pady=2,sticky=NW)

labelframe1_1=ttk.LabelFrame(labelframe1,padding=2)
labelframe1_1.grid(row=7,column=1,padx=5,pady=2,columnspan=2)

labelframe2=ttk.LabelFrame(booklist,text="Update DataBase Entry",padding=2)
labelframe2.grid(row=1,column=0,padx=5,pady=2,sticky=NW)

labelframe2_1=ttk.LabelFrame(labelframe2,padding=2)
labelframe2_1.grid(row=3,column=1,padx=5,pady=2,columnspan=2)

labelframe3=ttk.LabelFrame(booklist,text="Book List",padding=5)
labelframe3.grid(row=0,column=1,rowspan=2,padx=5,pady=5,sticky=NW)

labelframe3_1=ttk.LabelFrame(labelframe3)
labelframe3_1.grid(row=2,column=0,columnspan=10)

#creation of all the widgets


booklabel=ttk.Label(labelframe1,text="Book Name")
booklabel.grid(row=0,column=0,sticky=NW,padx=10,pady=5)

bookname=ttk.Entry(labelframe1,width=25)
bookname.grid(row=1,column=0,padx=10,pady=5,sticky=NW)


authorlabel=ttk.Label(labelframe1,text="Authors")
authorlabel.grid(row=0,column=1,sticky=NW,padx=10,pady=5)

authors=ttk.Entry(labelframe1,width=25)
authors.grid(row=1,column=1,padx=10,pady=5,sticky=NW)

publicationlabel=ttk.Label(labelframe1,text="Publisher")
publicationlabel.grid(row=0,column=2,sticky=NW,padx=10,pady=5)

publisher=ttk.Entry(labelframe1,width=25)
publisher.grid(row=1,column=2,padx=10,pady=5,sticky=NW)

typelabel=ttk.Label(labelframe1,text="Book Catagory")
typelabel.grid(row=2,column=0,sticky=NW,padx=10,pady=5)
# sets default as academic
typedata=ttk.Combobox(labelframe1,textvariable=catagory,values=catagories,width=20)
typedata.set("Academic")
typedata.grid(row=3,column=0,padx=10,pady=5,sticky=NW)

book_print_type_label=ttk.Label(labelframe1,text="Brought/ PDF Print")
book_print_type_label.grid(row=2,column=1,sticky=NW,padx=10,pady=5)
#sets default to Brought by Me
book_print_type=ttk.Combobox(labelframe1,width=20,textvariable=yes_or_no,values=options,state='readonly')
book_print_type.grid(row=3,column=1,padx=10,pady=5,sticky=NW)
book_print_type.set("Brought by Me")

ISBNlabel=ttk.Label(labelframe1,text="ISBN")
ISBNlabel.grid(row=2,column=2,sticky=NW,padx=10,pady=5)

ISBNnumber=ttk.Entry(labelframe1,width=25)
ISBNnumber.grid(row=3,column=2,padx=10,pady=5,sticky=NW)


topiclabel=ttk.Label(labelframe1,text="Book Subject")
topiclabel.grid(row=4,column=0,sticky=NW,padx=10,pady=5)

topic=ttk.Entry(labelframe1,width=25)
topic.grid(row=5,column=0,padx=10,pady=5,sticky=NW)

placelabel=ttk.Label(labelframe1,text="Place")
placelabel.grid(row=4,column=1,sticky=NW,padx=10,pady=5)
#set Defult as Home
place=ttk.Combobox(labelframe1,width=20,textvariable=placedata,values=['Home','Others','Computer/Hard Disk'],state='readonly')
place.set('Home')
place.grid(row=5,column=1,padx=10,pady=5,sticky=NW)


pricelabel=ttk.Label(labelframe1,text="Price")
pricelabel.grid(row=4,column=2,sticky=NW,padx=10,pady=5)

price=ttk.Entry(labelframe1,width=25)
price.grid(row=5,column=2,padx=10,pady=5,sticky=NW)

datelabel=ttk.Label(labelframe1,text="Date")
datelabel.grid(row=6,column=0,sticky=NW,padx=10,pady=5)

#creation of calender to select date
calender=Calendar(labelframe1,selectmode='day')
calender.grid(row=7,column=0)

doilabel=ttk.Label(labelframe1_1,text="DOI Number")
doilabel.grid(row=0,column=0,sticky=NW,padx=10,pady=5)

doi=ttk.Entry(labelframe1_1,width=25)
doi.grid(row=1,column=0,padx=10,pady=5,sticky=NW)

uploadlabel=ttk.Label(labelframe1_1,text="Upload PDF")
uploadlabel.grid(row=0,column=1,sticky=NW,padx=10,pady=5)

uploaddata=ttk.Entry(labelframe1_1,width=25)
uploaddata.grid(row=1,column=1,padx=10,pady=5,sticky=NW)
uploaddata.insert(0,"Put upload filedialog")
uploaddata.config(state=DISABLED)

entrybutton=Button(labelframe1_1,text="Entry",padx=10,pady=6,command=entry_reload,width=10,background="#95f587",font=30,borderwidth=5,activebackground="#e592e8")
entrybutton.grid(row=2,column=1,padx=10,pady=5)

serial_no_label=ttk.Label(labelframe2,text="DataBase Id / Serial No.")
serial_no_label.grid(row=0,column=0,sticky=NW,padx=10,pady=5)

serial_no=ttk.Entry(labelframe2,width=25,textvariable=serial_number)
serial_no.grid(row=1,column=0,padx=10,pady=5,sticky=NW)
#next line moniters any type of entry to the serial no widget
serial_number.trace_add("write", updatedata)

borrowedlabel=ttk.Label(labelframe2,text="Borrowed?")
borrowedlabel.grid(row=0,column=1,sticky=NW,padx=10,pady=5)

borrowed=ttk.Combobox(labelframe2,width=25,textvariable=borrow,values=["Issue","Return"],state='readonly')
borrowed.grid(row=1,column=1,padx=10,pady=5)
# depending os the combobox selection next line called the fucntion button_color_picker
borrowed.bind("<<ComboboxSelected>>", button_color_picker)


isborrowedlabel=ttk.Label(labelframe2,text="Issuer Name")
isborrowedlabel.grid(row=0,column=2,sticky=NW,padx=10,pady=5)

isborrowed=ttk.Entry(labelframe2,width=25)
isborrowed.grid(row=1,column=2,padx=10,pady=5,sticky=NW)



borrowdatelabel=ttk.Label(labelframe2,text="Borrow/Return Date")
borrowdatelabel.grid(row=2,column=0,sticky=NW,padx=10,pady=5)


borrowcalender=Calendar(labelframe2,selectmode='day')
borrowcalender.grid(row=3,column=0)

updatebutton=Button(labelframe2_1,text="Update",padx=10,pady=10,command=update_reload,width=10,background="Blue",fg='white',font=30,borderwidth=5,state=DISABLED)
updatebutton.grid(row=1,column=0,padx=20,pady=20)

openbutton=Button(labelframe2_1,text="Open",padx=10,pady=10,command=update,width=10,background="Blue",fg='white',font=30,borderwidth=5)
openbutton.grid(row=0,column=0,padx=20,pady=20)

deletebutton=Button(labelframe2_1,text="Delete",state=DISABLED,padx=10,pady=10,command=delete,width=10,background="Blue",fg='white',font=30,borderwidth=5)
deletebutton.grid(row=0,column=1,padx=20,pady=20)

deleteallbutton=Button(labelframe2_1,text="Delete All",padx=10,pady=10,command=deleteall,width=10,background="Blue",fg='white',font=30,borderwidth=5)
deleteallbutton.grid(row=1,column=1,padx=20,pady=20)



#name search
searchnamelable=ttk.Label(labelframe3,text="Search by Name")
searchnamelable.grid(row=0,column=0,sticky=NW,padx=5,pady=5)

searchname=ttk.Entry(labelframe3,width=15,textvariable=searchnames)
searchname.grid(row=1,column=0,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search name entry widget
searchnames.trace_add("write",namesearch)

#author search
searchauthorlable=ttk.Label(labelframe3,text="Search by Author's First Name")
searchauthorlable.grid(row=0,column=1,sticky=NW,padx=5,pady=5)

searauthor=ttk.Entry(labelframe3,width=25,textvariable=searchauthors)
searauthor.grid(row=1,column=1,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search authors entry widget
searchauthors.trace_add("write",authorsearch)


#catagory Search 

searchcatagorylable=ttk.Label(labelframe3,text="Search by Catagory")
searchcatagorylable.grid(row=0,column=2,sticky=NW,padx=5,pady=5)

searchcatagory=ttk.Entry(labelframe3,width=15,textvariable=searchcatagories)
searchcatagory.grid(row=1,column=2,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search catagory entry widget
searchcatagories.trace_add("write",catagorysearch)

#Book subject search

searbooksubjectlable=ttk.Label(labelframe3,text="Search by Subject")
searbooksubjectlable.grid(row=0,column=3,sticky=NW,padx=5,pady=5)

searchbooksubject=ttk.Entry(labelframe3,width=15,textvariable=searchbooksubjects)
searchbooksubject.grid(row=1,column=3,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search subjects entry widget
searchbooksubjects.trace_add("write",booksubjectsearch)

#tree view create

tree=ttk.Treeview(labelframe3_1,height=30,selectmode=EXTENDED)
tree.pack(side=LEFT)
#next line moniters the selection in the treeview.
#if item selected in the treeview, next line binds that event to
#the created virtual event and called the treeselection function
tree.bind('<<TreeviewSelect>>',treeselection)

treescrollbar=ttk.Scrollbar(labelframe3_1,orient=VERTICAL,command=tree.yview)
treescrollbar.pack(side=RIGHT,fill=Y)
tree.config(yscrollcommand=treescrollbar.set)



# Define ur columns of treeview
tree["columns"]= ("Book Name","Authors","Book Catagory","Price Tag","Book Subject","Place","Issued/Returned","Issuer Name","Issue/Return Date")


#check boxes



#format our column(styling)
tree.column('#0',width=40)
tree.heading('#0',text="Database ID",anchor=W)

for col in tree["columns"]:
    tree.column(col,anchor=NW,width=82)
    tree.heading(col,text=col,anchor=W)

#connects to the databse to show data from the database
conn=sqlite3.connect("Book List.db")
c=conn.cursor()
c.execute("SELECT *, oid FROM BookList")
records=c.fetchall()
#for loop runs through each item of the database and put up on the tree

for data in records:
    record=data
    tree.insert(parent='',index='end',text=record[15],value=(record[0],record[1],record[3],record[4],record[6],record[7],record[12],record[13],record[14]),tags=record[15])
    if int(record[15])%2==0:
        tree.tag_configure(record[15],background="#a4e1f5",foreground="#23077d")

conn.commit()
conn.close()

'''
Learning Treeview
#create heading

tree.heading('#0',text='label',anchor=W)
tree.heading('Book Name',text='Book Names',anchor=W)
tree.heading('Authors',text='Authors',anchor=W)



#add data
#providing iid is optional. tree view makes its own.
#so we can input the database id
tree.insert(parent='',index='end',iid=0,text='Parent',values=("Name","Debdip"))
tree.insert(parent='',index='end',iid=1,text='child',values=("Name","Debdip"))


#add child

tree.insert(parent='',index='end',iid=2,text='',values=("Name2","Debdip1"))
tree.move('2','0','0')
tree.insert(parent='0',index='end',iid=2,text='',values=("Name3","Debdip4"))
'''

#adds new page paper to the window
paper=ttk.Frame(nbook)
nbook.add(paper,text="Paper",padding=10)




#paper database
def paperdatabase():
    try:
        conn = sqlite3.connect("Article DataBase.db")
        c = conn.cursor()

        c.execute("""CREATE TABLE Articles(
                Title text,
                Authors text,
                Journal text,
                Volume text,
                Number text,
                Pages text,
                DOI text,
                URL text,
                First_link text,
                Year text,
                Abstract text,
                Tag text,
                Detail text,
                BibTex text
                )""")
        conn.commit()
        conn.close()
    except:
        pass


paperdatabase()

def load():
    for item in papertree.get_children():
        papertree.delete(item)
    conn=sqlite3.connect("Article DataBase.db")
    c=conn.cursor()
    c.execute("SELECT *,oid FROM Articles")
    datas=c.fetchall()
    for data in datas:
        papertree.insert(parent='',index='end',text=data[14],values=(data[0],data[1],data[2],data[9],data[11]),tags=data[14])
        if int(data[14])%2==0:
            papertree.tag_configure(data[14],background="#b9f0c7",foreground="Black")
        elif int(data[14])%3==0:
            papertree.tag_configure(data[14],background="#b9f0c7",foreground="Black")
        elif int(data[14])%3==0 and int(data[14])%2==0:
            papertree.tag_configure(data[14],background="#f0b9d4",foreground="Black")
        else:
            papertree.tag_configure(data[14],background="#c3b9f0",foreground="Black")
    conn.commit()
    conn.close()


def paperdatabaseentry():
    authornames=""
    i=0
    for items in item["message"]["author"]:
        authornames = authornames + item["message"]["author"][i]["given"] + " " + item["message"]["author"][i]["family"] + ", "
        i=i+1
    #abstract=item['message']['abstract'][41:-9]
    conn=sqlite3.connect("Article DataBase.db")
    c=conn.cursor()
    c.execute("""INSERT INTO Articles (Title, Authors, Journal, Volume, Number, Pages, DOI, URL, First_Link, Year, Abstract, Tag, Detail, BibTex) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(item['message']['title'][0],authornames,item['message']['container-title'][0],item['message']['volume'],item['message']['issue'],item['message'].get('article-number',' '),item['message']['DOI'],item['message']['URL'],item['message']['resource']['primary']['URL'],item['message']['published-online']['date-parts'][0][0],abstract,papertype.get(),paperdetailtext.get("1.0",END),bib)) 
    conn.commit()
    conn.close()
    load()










#variable definition
searchpapernames=StringVar()
searchpaperauthors=StringVar()
searchjournals=StringVar()
searchyears=StringVar()
searchtags=StringVar()
searchqualifications=StringVar()
searchdois=StringVar()
papertype=StringVar()
namecheck=StringVar()




#got this code from the github repository of doi2bib pylibrery


bare_url = "http://api.crossref.org/"





def get_bib(doi):
    """
    Parameters
    ----------

        doi: str

    Returns
    -------

        found: bool
        bib: str
    """
    url = "{}works/{}/transform/application/x-bibtex"
    url = url.format(bare_url, doi)
    r = requests.get(url)
    found = False if r.status_code != 200 else True
    bib = r.content
    bib = str(bib, "utf-8")

    return found, bib


def get_json(doi):
    """
    Parameters
    ----------
        doi: str

    Returns
    -------

        found: bool
        item: dict
            Response from crossref
    """

    url = "{}works/{}"
    url = url.format(bare_url, doi)
    r = requests.get(url)
    found = False if r.status_code != 200 else True
    item = r.json()

    return found, item

def get_bib_from_doi(doi, abbrev_journal=True, add_abstract=False):
    """
    Parameters
    ----------

        doi: str
        abbrev_journal: bool
            If True try to abbreviate the journal name
    Returns
    -------

        found: bool
        bib: str
            The bibtex string
    """
    found, bib = get_bib(doi)
    if found and abbrev_journal:

        found, item = get_json(doi)
        if found:
            abbreviated_journal = item["message"]["short-container-title"]
            if add_abstract and "abstract" in item["message"].keys():
                abstract = item["message"]["abstract"][41:-9]
                bi = bibtexparser.loads(bib)
                bi.entries[0]["abstract"] = abstract
                bib = bibtexparser.dumps(bi)
            if add_abstract and "article-number" in item["message"].keys():
                pages = item["message"]["article-number"]
                bi = bibtexparser.loads(bib)
                bi.entries[0]["pages"] = pages
                bib = bibtexparser.dumps(bi)

            if len(abbreviated_journal) > 0:
                abbreviated_journal = abbreviated_journal[0].strip()
                bib = re.sub(
                    r"journal = \{[^>]*?\}",
                    "journal = {" + abbreviated_journal + "}",
                    bib)

    return found, bib

#Function Definition



def search():
    doi=searchdois.get()
    global bib
    found, bib = get_bib_from_doi(doi, abbrev_journal=True, add_abstract=True)
    global abstract
    global item
    founds, item = get_json(doi)
    try:
        titles=item["message"]['title'][0]
        abstract=item["message"]['abstract'][41:-9]
        papertitlelable.config(text="")
        paperabstractlable.config(text="")
        papertitlelable.config(text=titles,wraplength=690,font=my_font1)
        paperabstractlable.config(text=abstract,wraplength=690,font=my_font2)
        paperdatabaseentry()
    except:
        abstract=''
        titles=item["message"]['title'][0]
        papertitlelable.config(text="")
        paperabstractlable.config(text="")
        papertitlelable.config(text=titles,wraplength=690,font=my_font1)
        paperdatabaseentry()
    #papertitlelable.config(text="")
    #paperabstractlable.config(text="")



def paperupdate():
    pass

def paperdelete():
    pass


def paperview():
    pass


def citecopy():
    pass

def papernamesearch():
    pass




def paperauthorsearch():
    pass




def journalsearch():
    pass




def yearsearch():
    pass




def tagsearch():
    pass



def qualificationsearch():
    pass


#creation of all the important label frames which will contain 
#all the widgets

labelframe4=ttk.LabelFrame(paper,text="DOI Entry",padding=2)
labelframe4.grid(row=0,column=0,padx=5,pady=0,sticky=NW)

labelframe4_1=ttk.LabelFrame(labelframe4,padding=5)
labelframe4_1.grid(row=7,column=1,padx=5,pady=5,columnspan=2)

labelframe5=ttk.LabelFrame(paper,text="Update Details and Citation Details",padding=2)
labelframe5.grid(row=1,column=0,padx=5,pady=0,sticky=SW)

labelframe5_1=ttk.LabelFrame(labelframe5,padding=5)
labelframe5_1.grid(row=3,column=1,padx=5,pady=5,columnspan=2)

labelframe6=ttk.LabelFrame(paper,text="Paper DataBase",padding=2)
labelframe6.grid(row=0,column=1,rowspan=2,padx=5,pady=5)

labelframe6_1=ttk.LabelFrame(labelframe6)
labelframe6_1.grid(row=2,column=0,columnspan=10)



#Entry Via DOI Entry

searchdoi=ttk.Entry(labelframe4,width=84,textvariable=searchdois)
searchdoi.grid(row=0,column=0,padx=5,pady=5,sticky=SW,columnspan=5)


searchbutton=ttk.Button(labelframe4,width=22,text="Entry",command=search,padding=5)
searchbutton.grid(row=0,column=5,padx=5,pady=5,sticky=NW)


#check box for Treeview

#font style definition
my_font1 = font.Font(family='Helvetica', size=16, weight='bold')
my_font2 = font.Font(family='Times New Roman', size=12)
#Paper Title show

papertitlelable=ttk.Label(labelframe4)
papertitlelable.grid(row=1,column=0,columnspan=6,sticky=NW,pady=2)



#abstract show 

paperabstractlable=ttk.Label(labelframe4)
paperabstractlable.grid(row=2,column=0,columnspan=6,sticky=NW,pady=2)






#Enter Detailed survey of the paper or any details you waht to input
paperdetailtextlabel=ttk.Label(labelframe5,text="Enter Detailed Survay in words")
paperdetailtextlabel.grid(row=0,column=0,columnspan=3,sticky=NW)
paperdetailtext=Text(labelframe5,height=13,width=66)
paperdetailtext.grid(row=1,column=0,columnspan=3,rowspan=6,pady=10)

papertagstype=["PhD","Masters","Internship-OIST","Chanakya Fellowship"]

papertagtypes=ttk.Combobox(labelframe5,textvariable=papertype,values=papertagstype)
papertagtypes.grid(row=1,column=3,padx=5,pady=1)


uploadpaper=ttk.Entry(labelframe5,width=24)
uploadpaper.grid(row=2,column=3,padx=5,pady=5)
uploadpaper.insert(0,"Put upload filedialog")
uploadpaper.config(state=DISABLED)

paperupdatebutton=ttk.Button(labelframe5,width=22,text="Update",command=paperupdate,padding=5)
paperupdatebutton.grid(row=6,column=3,padx=5,pady=1)



paperdeletebutton=ttk.Button(labelframe5,width=22,text="Delete",command=paperdelete,padding=5)
paperdeletebutton.grid(row=3,column=3,padx=5,pady=1)



paperviewbutton=ttk.Button(labelframe5,width=22,text="View Paper",command=paperview,padding=5)
paperviewbutton.grid(row=4,column=3,padx=5,pady=1)


copybutton=ttk.Button(labelframe5,width=22,text="Copy BixTex",command=citecopy,padding=5)
copybutton.grid(row=5,column=3,padx=5,pady=1)



 

#name search
searchpapernamelable=ttk.Label(labelframe6,text="Search by Name")
searchpapernamelable.grid(row=0,column=0,sticky=NW,padx=5,pady=5)

searchpapername=ttk.Entry(labelframe6,width=15,textvariable=searchpapernames)
searchpapername.grid(row=1,column=0,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search name entry widget
searchpapernames.trace_add("write",papernamesearch)

#author search
searchpaperauthorlable=ttk.Label(labelframe6,text="Search by Author's First Name")
searchpaperauthorlable.grid(row=0,column=1,sticky=NW,padx=5,pady=5)

searchpaperauthor=ttk.Entry(labelframe6,width=25,textvariable=searchpaperauthors)
searchpaperauthor.grid(row=1,column=1,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search authors entry widget
searchpaperauthors.trace_add("write",paperauthorsearch)


#journal Search 

searchjournallable=ttk.Label(labelframe6,text="Search by Journal")
searchjournallable.grid(row=0,column=2,sticky=NW,padx=5,pady=5)

searchjournal=ttk.Entry(labelframe6,width=15,textvariable=searchjournals)
searchjournal.grid(row=1,column=2,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search catagory entry widget
searchjournals.trace_add("write",journalsearch)

#year search

searchyearlable=ttk.Label(labelframe6,text="Search by Year")
searchyearlable.grid(row=0,column=3,sticky=NW,padx=5,pady=5)

searchyear=ttk.Entry(labelframe6,width=15,textvariable=searchyears)
searchyear.grid(row=1,column=3,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search subjects entry widget
searchyears.trace_add("write",yearsearch)

#tag Search 

searchtaglable=ttk.Label(labelframe6,text="Search by Tag")
searchtaglable.grid(row=0,column=4,sticky=NW,padx=5,pady=5)

searchtag=ttk.Entry(labelframe6,width=15,textvariable=searchtags)
searchtag.grid(row=1,column=4,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search catagory entry widget
searchtags.trace_add("write",tagsearch)

#qualification Search 

searchqualificationlable=ttk.Label(labelframe6,text="Search by Entry Type")
searchqualificationlable.grid(row=0,column=5,sticky=NW,padx=5,pady=5)

searchqualification=ttk.Entry(labelframe6,width=15,textvariable=searchqualifications)
searchqualification.grid(row=1,column=5,padx=5,pady=5,sticky=NW)
#traces any chenges or entry to search catagory entry widget
searchqualifications.trace_add("write",qualificationsearch)





#treeview creation
papertree=ttk.Treeview(labelframe6_1,height=30,selectmode=EXTENDED)
papertree.pack(side=LEFT)
#next line moniters the selection in the treeview.
#if item selected in the treeview, next line binds that event to
#the created virtual event and called the treeselection function
tree.bind('<<TreeviewSelect>>')

papertreescrollbar=ttk.Scrollbar(labelframe6_1,orient=VERTICAL,command=papertree.yview)
papertreescrollbar.pack(side=RIGHT,fill=Y)
papertree.config(yscrollcommand=papertreescrollbar.set)

papertree["column"]=("Title","Authors","Journal","Year","Tags")



papertree.column("#0",width=80)
papertree.heading("#0",text="DataBase ID",anchor=W)

papertree.column("Title",width=220)
papertree.heading("Title",text="Title",anchor=W)

papertree.column("Authors",width=120)
papertree.heading("Authors",text="Authors",anchor=W)

papertree.column("Journal",width=130)
papertree.heading("Journal",text="Journal",anchor=W)

papertree.column("Year",width=70)
papertree.heading("Year",text="Year",anchor=W)

papertree.column("Tags",width=120)
papertree.heading("Tags",text="Tags",anchor=W)


conn=sqlite3.connect("Article DataBase.db")
c=conn.cursor()
c.execute("SELECT *,oid FROM Articles")


datas=c.fetchall()

for data in datas:
    papertree.insert(parent='',index='end',text=data[14],values=(data[0],data[1],data[2],data[9],data[11]),tags=data[14])
    if int(data[14])%2==0:
        papertree.tag_configure(data[14],background="#b9f0c7",foreground="Black")
    elif int(data[14])%3==0:
        papertree.tag_configure(data[14],background="#b9f0c7",foreground="Black")
    elif int(data[14])%3==0 and int(data[14])%2==0:
        papertree.tag_configure(data[14],background="#f0b9d4",foreground="Black")
    else:
        papertree.tag_configure(data[14],background="#c3b9f0",foreground="Black")
conn.commit()
conn.close()



#add new window expenditure analysis to the page



expence=ttk.Frame(nbook)
nbook.add(expence,text="Expenditure Analysis",padding=10)




#the loop is the main loop which help the app to see and monitor any changes in the app

root.mainloop()
