from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pymysql

class ConnectorDB:
    def __init__(self,root):
        self.root = root
        tittlespace = " "
        self.root.title(102 * tittlespace + "Student Database")
        self.root.geometry("804x630+300+0")
        self.root.resizable(width=False, height=False)

        mainFrame = Frame(self.root, bd=10, width=770, height=630, relief=RIDGE, bg='cadet blue')
        mainFrame.grid()

        titleFrame = Frame(mainFrame, bd=7, width=760, height=100, relief=RIDGE)
        titleFrame.grid(row=0, column=0)
        topFrame3 = Frame(mainFrame, bd=5, width=770, height=500, relief=RIDGE)
        topFrame3.grid(row=1, column=0)

        leftFrame = Frame(topFrame3, bd=5, width=770, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        leftFrame.pack(side=LEFT)
        leftFrame1 = Frame(leftFrame, bd=5, width=600, height=180, padx=12, pady=9, relief=RIDGE)
        leftFrame1.pack(side=TOP)

        rightFrame1 = Frame(topFrame3, bd=5, width=100, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        rightFrame1.pack(side=RIGHT)
        rightFrame1a = Frame(rightFrame1, bd=5, width=90, height=300, padx=2, pady=2, relief=RIDGE)
        rightFrame1a.pack(side=TOP)

        # -----------------------------------------------
        
        studentId= StringVar()
        firstName= StringVar()
        surname= StringVar()
        address= StringVar()
        mobile= StringVar()
        gender= StringVar()

        def iExit():
            iExit=tkinter.messagebox.askyesno("Student Database", "Confirm if you wna t to exit")
            if iExit>0:
                root.destroy()
                return
            
        def reset():
            self.entStId.delete(0, END)
            self.entFirstName.delete(0, END)
            self.entSurname.delete(0, END)
            self.entAddress.delete(0, END)
            self.entMobile.delete(0, END)
            gender.set('')


        def addData():
            if studentId.get() == '' or firstName.get()=='' or surname.get()=='':
                tkinter.messagebox.showerror("Student Database", "Enter Correct Details")
            else:
                sqlCon = pymysql.connect(host='localhost', user='root', password='1999', database='student_registration')
                cursor = sqlCon.cursor()
                cursor.execute("insert into basicInfo (studentId, firstName, surname, address, mobile, gender) values(%s, %s, %s, %s, %s, %s)",
                               (
                                  int(studentId.get()),
                                  firstName.get(),
                                  surname.get(),
                                  address.get(),
                                  mobile.get(),
                                  gender.get()
                               ))
                sqlCon.commit()
                sqlCon.close()
                tkinter.messagebox.showinfo("Student Database", "Record Entered Successfully")

        
        def displayData():
            sqlCon = pymysql.connect(host='localhost', user='root', password='1999', database='student_registration')
            cursor = sqlCon.cursor()
            cursor.execute('select * from basicInfo')
            result = cursor.fetchall()
            if len(result) !=0:
                self.studentRecords.delete(*self.studentRecords.get_children())
                for row in result:
                    self.studentRecords.insert('', END, values=row)                   
            sqlCon.commit()
            sqlCon.close()
        

        def showData(event):
            viewInfo = self.studentRecords.focus()
            learnData = self.studentRecords.item(viewInfo)
            row = learnData['values']
            studentId.set(row[0]),
            firstName.set(row[1]),
            surname.set(row[2]),
            address.set(row[3]),
            mobile.set(row[4]),
            gender.set(row[5])


        def update():
            sqlCon = pymysql.connect(host='localhost', user='root', password='1999', database='student_registration')
            cursor = sqlCon.cursor()
            cursor.execute("update basicInfo set firstName=%s, surname=%s, address=%s, mobile=%s, gender=%s WHERE studentId=%s",
                    (
                        firstName.get(),
                        surname.get(),
                        address.get(),
                        mobile.get(),
                        gender.get(),
                        int(studentId.get())
                    ))
            sqlCon.commit()
            displayData()
            sqlCon.close()
            tkinter.messagebox.showinfo("Student Database", "Record Updated Successfully")


        def deleteEntry():
            sqlCon = pymysql.connect(host='localhost', user='root', password='1999', database='student_registration')
            cursor = sqlCon.cursor()
            cursor.execute("delete from basicInfo where studentId=%s", int(studentId.get()))
            sqlCon.commit()
            displayData()
            sqlCon.close()
            tkinter.messagebox.showinfo("Student Database", "Record Successfully Deleted")
            reset()



        def searchEntry():
            try:
                sqlCon = pymysql.connect(host='localhost', user='root', password='1999', database='student_registration')
                cursor = sqlCon.cursor()
                cursor.execute("SELECT * FROM basicInfo WHERE studentId=%s", (studentId.get(),))
                row = cursor.fetchone() 
                if row: 
                    studentId.set(row[0])
                    firstName.set(row[1])
                    surname.set(row[2])
                    address.set(row[3])
                    mobile.set(row[4])
                    gender.set(row[5])
                else:
                    tkinter.messagebox.showinfo("Student Database", "No Such Record Found")
                    reset()
            except Exception as e:
                print("Error:", e)
                tkinter.messagebox.showinfo("Student Database", "Error Occurred. Please try again.")
            finally:
                sqlCon.close()







        # -----------------------------------------------

        self.lblTitle=Label(titleFrame, font=('arial', 30, 'bold'), text="Student Registration Database", bd=7)
        self.lblTitle.grid(row=0,column=0,padx=90)

        self.lblStId=Label(leftFrame1, font=('arial', 12, 'bold'), text="Student Id", bd=7)
        self.lblStId.grid(row=0,column=0, sticky=W, padx=5)
        self.entStId=Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=studentId)
        self.entStId.grid(row=0,column=1, sticky=W, padx=5)

        self.lblFirstName=Label(leftFrame1, font=('arial', 12, 'bold'), text="First Name", bd=7)
        self.lblFirstName.grid(row=1,column=0, sticky=W, padx=5)
        self.entFirstName=Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=firstName)
        self.entFirstName.grid(row=1,column=1, sticky=W, padx=5)


        self.lblSurname=Label(leftFrame1, font=('arial', 12, 'bold'), text="Surname", bd=7)
        self.lblSurname.grid(row=2,column=0, sticky=W, padx=5)
        self.entSurname=Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=surname)
        self.entSurname.grid(row=2,column=1, sticky=W, padx=5)

        self.lblAddress=Label(leftFrame1, font=('arial', 12, 'bold'), text="Address", bd=7)
        self.lblAddress.grid(row=3,column=0, sticky=W, padx=5)
        self.entAddress=Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=address)
        self.entAddress.grid(row=3,column=1, sticky=W, padx=5)

        self.lblMobile=Label(leftFrame1, font=('arial', 12, 'bold'), text="Mobile", bd=7)
        self.lblMobile.grid(row=4,column=0, sticky=W, padx=5)
        self.entMobile=Entry(leftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left', textvariable=mobile)
        self.entMobile.grid(row=4,column=1, sticky=W, padx=5)

        self.lblGender=Label(leftFrame1, font=('arial', 12, 'bold'), text="Gender", bd=7)
        self.lblGender.grid(row=5,column=0, sticky=W, padx=5)
        self.cboGender=ttk.Combobox(leftFrame1, font=('arial', 12, 'bold'), width=43, state='readonly', textvariable=gender)
        self.cboGender['values']=['', 'Female', 'Male']
        self.cboGender.current(0)
        self.cboGender.grid(row=5,column=1)

        # ---------------------------Table Treeview-------------------------
        scroll_y=Scrollbar(leftFrame, orient= VERTICAL)

        self.studentRecords= ttk.Treeview(leftFrame, height=12,columns=('stId', 'firstName', 'surname', 'address', 'mobile', 'gender'),
                                          yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.studentRecords.heading('stId', text="Student ID")
        self.studentRecords.heading('firstName', text="First Name")
        self.studentRecords.heading('surname', text="Surname")
        self.studentRecords.heading('address', text="Address")
        self.studentRecords.heading('mobile', text="Mobile")
        self.studentRecords.heading('gender', text="Gender")

        self.studentRecords['show']='headings'

        self.studentRecords.column('stId', width=70)
        self.studentRecords.column('firstName', width=100)
        self.studentRecords.column('surname', width=100)
        self.studentRecords.column('address', width=100)
        self.studentRecords.column('mobile', width=70)
        self.studentRecords.column('gender', width=70)

        self.studentRecords.pack(fill=BOTH, expand=1)
        self.studentRecords.bind("<ButtonRelease-1>", showData)

        # --------------------------------------------------------
        self.btnAddNew = Button(rightFrame1a, font=('arial', 16, 'bold'), text="Add New", bd=4, pady=1, padx=24,
                                width=8, height=2, command=addData).grid(row=0,column=0, padx=1)
        self.btnDisplay = Button(rightFrame1a, font=('arial', 16, 'bold'), text="Display", bd=4, pady=1, padx=24,
                                width=8, height=2, command=displayData).grid(row=1,column=0, padx=1)
        self.btnUpdate = Button(rightFrame1a, font=('arial', 16, 'bold'), text="Update", bd=4, pady=1, padx=24,
                                width=8, height=2, command=update).grid(row=2,column=0, padx=1)
        self.btnDelete = Button(rightFrame1a, font=('arial', 16, 'bold'), text="Delete", bd=4, pady=1, padx=24,
                                width=8, height=2, command=deleteEntry).grid(row=3,column=0, padx=1)
        self.btnSearch = Button(rightFrame1a, font=('arial', 16, 'bold'), text="Search", bd=4, pady=1, padx=24,
                                width=8, height=2, command=searchEntry).grid(row=4,column=0, padx=1)
        self.btnAddReset = Button(rightFrame1a, font=('arial', 16, 'bold'), text="Reset", bd=4, pady=1, padx=24,
                                width=8, height=2, command=reset).grid(row=5,column=0, padx=1)
        self.btnAddExit = Button(rightFrame1a, font=('arial', 16, 'bold'), text="Exit", bd=4, pady=1, padx=24,
                                width=8, height=2, command=iExit).grid(row=6,column=0, padx=1)

        # --------------------------------------------------------

if __name__=='__main__':
    root = Tk()
    application = ConnectorDB(root)
    root.mainloop()


