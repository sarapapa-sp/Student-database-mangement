'''

About Project
About School management system manages the information the students like their name, Dob, streams, and other personal information. Regarding to the features included :

Taking personal information
Showing the information as a record
deleting the record
resting fields
deleting database
Project Prerequisites:
For the following projects, you need this prerequisites:

1. Tkinter – To create the GUI.
2. mysqlconnector – To connect the program to the database and store information in it.
3. TkCalender – To get the user to enter a date.
4. Datetime.date – To convert the date from the tree to a Datetime.date instance so that it can be set in.
5. Tkinter.messagebox – To show a display box, displaying some information or an error.
6. Tkinter.ttk – To create the tree where all the information will be displayed.

'''
import datetime
from tkinter import *
from tkcalendar import DateEntry
import tkinter.messagebox as mb
from tkinter import ttk
import mysql.connector
try:
    con=mysql.connector.connect(host='localhost',user='root',password='Sage',database='studentdatabase')
    cursor = con.cursor(buffered=True)

except:
    mb.showerror("Database Error!","Unable to connect to the database")
def add_record():

    '''
    TO add record to the database
    :return: true if data added successfully
    '''
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    name = name_strvar.get()
    email=email_strvar.get()
    contact=phone_strvar.get()
    gender=gender_strvar.get()
    DOB = dob.get_date()
    date = DOB.strftime("%m/%d/%Y")
    stream=stream_strvar.get()
    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror("Error ! ","Please fill all the fields ")
    else:
        try:
            cursor.execute('insert into studentdata (Name,Emailid,phoneno,gender,dob,stream_) values ("{}","{}","{}","{}","{}","{}")'.format(name,email,contact,gender,date,stream))
            con.commit()

            mb.showinfo('Data Added Successfully','Data has been successfully added for {} '.format(name))
        except Exception as e:
            mb.showerror('Wrong type','The type of data entered is wrong , Please try again\n {}'.format(e))

    clear_fields()
    display_record()

    mb.showinfo("Successful","Data was inserted successful for {}".format(name))
    return True

def clear_fields():
    '''
    To clear the fields in GUI
    :return:  true if cleared successfully
    '''
    for i in ["name_strvar","email_strvar","phone_strvar","gender_strvar","stream_strvar"]:
        exec("{}.set('')".format(i))
    dob.set_date(datetime.datetime.now().date())

    mb.showinfo("Cleared","All fields have been cleared")
    display_record()
    return True

def display_record():
    tree.delete(*tree.get_children())

    cursor.execute('SELECT * from studentdata;')
    data = cursor.fetchall()

    for records in data:
        tree.insert('',END,values=records)

def delete_record():
    if not tree.selection():
        mb.showerror("Error","No entry is selected")
    else:
        try:
            current_item = tree.focus()
            values=tree.item(current_item)
            selection = values["values"]

            cursor.execute('delete from studentdata where id={}'.format(selection[0]))
            con.commit()

            tree.delete(current_item)
        except Exception as e:
            mb.showerror("Error","Error while deleting the data of {} . Error is - {}".format(selection[1],e))
        else:
            mb.showinfo("Successful","Entry was deleted")

def view_record():
    if not tree.selection():
        mb.showerror("Error","No entry is selected")
    else:
        current_item = tree.focus()
        values= tree.item(current_item)
        value=values["values"]

        name_strvar.set(value[1])
        email_strvar.set(value[2])
        phone_strvar.set(value[3])
        gender_strvar.set(value[4])
        stream_strvar.set(value[6])

        new_date=datetime.date(int(value[5][6:]),int(value[5][:2]),int(value[5][3:5]))
        dob.set_date(new_date)


def reset_form():
    clear_fields()
    # delete_record()



main = Tk()

main.title("School Management System")
main.geometry("1250x800")

main.config(bg="green4")
main.resizable(0,0)

# Variables
name_strvar = StringVar()
email_strvar = StringVar()
phone_strvar = StringVar()
gender_strvar = StringVar()

stream_strvar = StringVar()

# Placing components in the main window
Label(main,text="Student Database Management System",bg="green4",font=("Arial",14)).pack(side=TOP , fill=X)

left_frame = Frame(main,bg="MediumSpringGreen")
left_frame.place(x=0,y=30,relheight=1,relwidth=0.2)

center_frame = Frame(main,bg="PaleGreen")
center_frame.place(relx=0.2,y=30,relheight=1,relwidth=0.2)

right_frame = Frame(main,bg="Olivedrab1")
right_frame.place(relx=0.4,y=30,relheight=1,relwidth=0.6)

#placing widgets in left frame
Label(left_frame,text="Name",bg="MediumSpringGreen").place(relx=0.3,rely=0.05)
Label(left_frame,text="Email Id",bg="MediumSpringGreen").place(relx=0.275,rely=0.18)
Label(left_frame,text="Contact No.",bg="MediumSpringGreen").place(relx=0.25,rely=0.31)
Label(left_frame,text="Gender",bg="MediumSpringGreen").place(relx=0.275,rely=0.44)
Label(left_frame,text="Date of Birth",bg="MediumSpringGreen").place(relx=0.25,rely=0.58)
Label(left_frame,text="Stream",bg="MediumSpringGreen").place(relx=0.275,rely=0.7)

Entry(left_frame,width=22,textvariable=name_strvar).place(x=20,rely=0.1)
Entry(left_frame,width=22,textvariable=email_strvar).place(x=20,rely=0.23)
Entry(left_frame,width=22,textvariable=phone_strvar).place(x=20,rely=0.36)
# Entry(left_frame,width=22,textvariable=stream_strvar).place(x=20,rely=0.75)
OptionMenu(left_frame,stream_strvar,"B.Com","B.Tech","B.Sc").place(x=40,rely=0.75,relwidth=0.5)
OptionMenu(left_frame,gender_strvar,"Male","Female").place(x=40,rely=0.49,relwidth=0.5)

dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)
Button(left_frame,text="Add Record",width=18,command=add_record).place(x=30,rely=0.85)

#placing the widgets in center frame
Button(center_frame,text="Delete Record",width=15,command=delete_record).place(relx=0.25,rely=0.30)
Button(center_frame,text="Reset Form",width=15,command=reset_form).place(relx=0.25,rely=0.40)
Button(center_frame,text="View Record",width=15,command=view_record).place(relx=0.25,rely=0.50)

#placing the widgets in right frame
Label(right_frame,text="Student Records",bg="Olivedrab1",font=("Arial",14)).pack(side=TOP,fill=X)

tree=ttk.Treeview(right_frame,height=160,selectmode=BROWSE,columns=('Student ID','Student Name','Student Mail','Student Contact','Gender','DOB','Stream'))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set,xscrollcommand=X_scroller.set)
tree.heading('Student ID',text="ID",anchor=CENTER)
tree.heading('Student Name',text='Name',anchor=CENTER)
tree.heading('Student Mail',text='Email',anchor=CENTER)
tree.heading('Student Contact',text='Contact',anchor=CENTER)
tree.heading('Gender',text='Gender',anchor=CENTER)
tree.heading('DOB',text='DOB',anchor=CENTER)
tree.heading('Stream',text='Stream',anchor=CENTER)
# tree.heading('',text='',anchor=CENTER)
tree.column('#0',width=0,stretch=NO)
tree.column('#1',width=40,stretch=NO)
tree.column('#2',width=200,stretch=NO)
tree.column('#3',width=140,stretch=NO)
tree.column('#4',width=80,stretch=NO)
tree.column('#5',width=80,stretch=NO)
tree.column('#6',width=80,stretch=NO)
tree.column('#7',width=120,stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.921, relx=0)

display_record()

main.update()
main.mainloop()
