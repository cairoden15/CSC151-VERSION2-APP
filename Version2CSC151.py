from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import tkinter.messagebox
import os
import sqlite3




class sis(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        all_frame = tk.Frame(self)
        all_frame.pack(side="top", fill="both", expand = True)
        all_frame.rowconfigure(0, weight=1)
        all_frame.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Students, Home, Courses):
            frame = F(all_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show(Home)
    def show(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()



class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        leftcolor = tk.Label(self, height = 1260, width =550, bg = "Forest green")
        leftcolor.place(x=0, y=0)
        label = tk.Label(self, text="STUDENT INFORMATION SYSTEM", bg= "yellow", fg= "black", relief=GROOVE,font=("times new roman",30,"bold"))
        label.place(x=350,y=20)

        
        
        course = tk.Button(self, text="COURSES",font=("times new roman",20,"bold"),height = 1, width = 20,relief=GROOVE, bg="yellow", fg="black", command=lambda: controller.show(Courses))
        course.place(x=500,y=200)
        
        
        students = tk.Button(self, text="STUDENTS",font=("times new roman",20,"bold"), height = 1, width = 20,relief=GROOVE, bg="yellow", fg="black", command=lambda: controller.show(Students))
        students.place(x=500,y=400)
        

        
        



        
        
  
class Courses(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        leftcolor = tk.Label(self, height = 1260, width =550, bg = "Forest Green")
        leftcolor.place(x=0, y=0)
        self.controller = controller
        self.controller.title("Student Information System")
        
        label = tk.Label(self, text="Courses",bg= "yellow", fg= "black",bd=0, font=("times new roman",40,"bold"))
        label.place(x=500,y=20)
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def tablec():
            conn = sqlite3.connect("Students.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS COURSES (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def add_course():
            if Course_Code.get() == "" or Course_Name.get() == "" : 
                tkinter.messagebox.showinfo("Course/s", "Fill in the box")
            else:
                conn = sqlite3.connect("Students.db")
                c = conn.cursor()         
                c.execute("INSERT INTO COURSES(Course_Code,Course_Name) VALUES (?,?)",(Course_Code.get(),Course_Name.get()))        
                conn.commit()           
                conn.close()
                Course_Code.set('')
                Course_Name.set('') 
                tkinter.messagebox.showinfo("Course/s", "Course Added Successfully!")
                display_course()
              
        def display_course():
            self.course_list.delete(*self.course_list.get_children())
            conn = sqlite3.connect("Students.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM COURSES")
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def update_course():
            for selected in self.course_list.selection():
                conn = sqlite3.connect("Students.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE COURSES SET Course_Code=?, Course_Name=? WHERE Course_Code=?", (Course_Code.get(),Course_Name.get(), self.course_list.set(selected, '#1')))  
                conn.commit()
                tkinter.messagebox.showinfo("Course/s", "Course Updated Successfully!")
                display_course()
                clear()
                conn.close()
                
        def edit_course():
            x = self.course_list.focus()
            if x == "":
                tkinter.messagebox.showerror("Course/s", "Select a course!")
                return
            values = self.course_list.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def delete_course(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Info", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Students.db")
                    cur = con.cursor()
                    x = self.course_list.selection()[0]
                    id_no = self.course_list.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM COURSES WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.course_list.delete(x)
                    tkinter.messagebox.showinfo("Course/s", "Course deleted!")
                    display_course()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Course/s", "This course has students!")
                
        def search_course():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("Students.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM COURSES WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.course_list.delete(*self.course_list.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
        
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.course_list.selection()[0]
            values = self.course_list.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])

        home = tk.Button(self, text="HOME",font=("times new roman",18,"bold"), height = 1, width = 12,relief=GROOVE, bg="yellow", fg="black", command=lambda: controller.show(Home))
        home.place(x=20,y=30)
        
        
        course = tk.Button(self, text="COURSES",font=("times new roman",18,"bold"), height = 1, width = 12,relief=GROOVE, bg="yellow", fg="black", command=lambda: controller.show(Courses))
        course.place(x=20,y=100)
        course.config(cursor= "hand2")
        
        student = tk.Button(self, text="STUDENTS",font=("times new roman",18,"bold"), height = 1, width = 12,relief=GROOVE, bg="yellow", fg="black", command=lambda: controller.show(Students))
        student.place(x=20,y=170)
        
        
        self.lblccode = Label(self, font=("times new roman",17,"bold"), text="Course Code:", bg= "yellow", fg= "black",bd=0, relief=GROOVE)
        self.lblccode.place(x=20,y=330)
        self.txtccode = Entry(self, font=("times new roman",17,"bold"), textvariable=Course_Code, width=35)
        self.txtccode.place(x=20,y=380)

        self.lblcname = Label(self, font=("times new roman",17,"bold"), text="Course Name:",bg= "yellow", fg= "black",bd=0, relief=GROOVE, padx=5, pady=5)
        self.lblcname.place(x=20,y=230)
        self.txtcname = Entry(self, font=("times new roman",17,"bold"), textvariable=Course_Name, width=35)
        self.txtcname.place(x=20,y=280)
        
        self.SearchBar = Entry(self, font=("times new roman",15,"bold"), textvariable=SearchBar_Var, bd=3, width=20)
        self.SearchBar.place(x=780,y=102)
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1215,y=140,height=290)

        self.course_list = ttk.Treeview(self, columns=("Course Code","Course Name"), height = 13, yscrollcommand=scrollbar.set)

        self.course_list.heading("Course Code", text="Course Code", anchor=W)
        self.course_list.heading("Course Name", text="Course Name",anchor=W)
        self.course_list['show'] = 'headings'

        self.course_list.column("Course Code", width=200, anchor=W, stretch=False)
        self.course_list.column("Course Name", width=430, stretch=False)
        
        self.course_list.bind("<Double-1> ", OnDoubleclick)


        self.course_list.place(x=575,y=140)
        scrollbar.config(command=self.course_list.yview)

      

    
            
        ## Buttons

        self.adds = Button(self, text="Add", font=("times new roman",18,"bold"),bd=0,  width = 10, bg="yellow", fg="black",command=add_course)
        self.adds.place(x=20,y=500)
        

        self.update = Button(self, text="Update", font=("times new roman",18,"bold"),bd=0,  width = 10, bg="yellow", fg="black", command=update_course) 
        self.update.place(x=220,y=500)
        

        self.clear = Button(self, text="Clear", font=("times new roman",18,"bold"),bd=0,  width = 10, bg="yellow", fg="black", command=clear)
        self.clear.place(x=420,y=500)
        


        self.delete = Button(self, text="Delete", font=("times new roman",17,"bold"),bd=0,  width = 10, bg="yellow", fg="black", command=delete_course)
        self.delete.place(x=620,y=500)
        

        self.search = Button(self, text="Search", font=("times new roman",14,"bold"),bd=0,  width = 10, bg="yellow", fg="black", command=search_course)
        self.search.place(x=1000,y=100)
        

        self.display = Button(self, text="Display", font=("times new roman",14,"bold"),bd=0,  width = 10, bg="yellow", fg="black", command=display_course)
        self.display.place(x=1120,y=101)
        
        
        tablec()
        display_course()



class Students(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        leftcolor = tk.Label(self, height = 1260, width =550, bg = "Forest Green")
        leftcolor.place(x=0, y=0)
        self.controller = controller
        self.controller.title("Student Information System")
        
        label = tk.Label(self, text="STUDENT INFORMATION SYSTEM",bg= "yellow", fg= "black", relief=GROOVE, font=("times new roman",30,"bold"))
        label.place(x=320,y=20)
        
       
        
        course = tk.Button(self, text="COURSES",font=("times new roman",18,"bold"), height = 1, width = 12,relief=GROOVE, bg="yellow", fg="black", command=lambda: controller.show(Courses))
        course.place(x=900,y=465)
        course.config(cursor= "hand2")
        
        student = tk.Button(self, text="STUDENTS",font=("times new roman",18,"bold"), height = 1, width = 12,relief=GROOVE, bg="yellow", fg="black", command=lambda: controller.show(Students))
        student.place(x=650,y=465)
        student.config(cursor= "hand2")
        
        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()
        

        def tables():
            conn = sqlite3.connect("Students.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def add_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information", "Fill in the box")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("Student Information", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("Student Information", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("Student Information", "ID Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("Student Information", "Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("Student Information", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("Students.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO students(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("Student Information", "Student Added Successfully!")
                                    conn.commit() 
                                    clear()
                                    display_stud()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("Students.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM students")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    if ID in ids:
                                       tkinter.messagebox.showerror("Student Information", "ID already exists")
                                    else: 
                                       tkinter.messagebox.showerror("Student Information", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("Student Information", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("Student Information", "Invalid ID")
                 
        def update_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("Students.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE students SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("Student Information", "Student record updated!")
                    display_stud()
                    clear()
                    conn.close()
        
        def delete_stud():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Information", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Students.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM students WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("Student Information", "Student record deleted successfully!")
                    display_stud()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def search_stud():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("Students.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("Student Information", "Invalid ID")           
                
        def display_stud():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("Students.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def edit_stud():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information", "Select a record")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])

        

        self.lblid = Label(self, font=("times new roman",14,"bold"), text="ID Number:", bg= "yellow", fg= "black" )
        self.lblid.place(x=40,y=144)
        self.txtid = Entry(self, font=("times new roman",14,"bold"), textvariable=Student_ID, width=27)
        self.txtid.place(x=210,y=150)

        self.lblname = Label(self, font=("times new roman",14,"bold"), text="Name:", bg= "yellow", fg= "black")
        self.lblname.place(x=40,y=195)
        self.txtname = Entry(self, font=("times new roman",14,"bold"), textvariable=Student_Name, width=27)
        self.txtname.place(x=210,y=200)
        
        self.lblc = Label(self, font=("times new roman",14,"bold"), text="Course:", bg= "yellow", fg= "black")
        self.lblc.place(x=40,y=240)
        self.txtc = Entry(self,font=("times new roman",14,"bold"), textvariable=Course_Code, width=27)
        self.txtc.place(x=210,y=246)

        self.lblyear = Label(self,font=("times new roman",14,"bold"), text="Year Level:", bg= "yellow", fg= "black")
        self.lblyear.place(x=40,y=295)
        self.txtyear = ttk.Combobox(self, value=["1st Year", "2nd Year", "3rd Year", "4th Year"], state="readonly", font=("times new roman",14,"bold"), textvariable=Student_YearLevel, width=26)
        self.txtyear.place(x=210,y=305)
        
        self.lblgender = Label(self, font=("times new roman",14,"bold"), text="Gender:", bg= "yellow", fg= "black")
        self.lblgender.place(x=40,y=350)
        self.txtgender = ttk.Combobox(self, value=["Male", "Female"], font=("times new roman",14,"bold"), state="readonly", textvariable=Student_Gender, width=26)
        self.txtgender.place(x=210,y=356)

        self.SearchBar = Entry(self, font=("times new roman",14,"bold"), textvariable=SearchBar_Var, bd=1, width=34)
        self.SearchBar.place(x=750,y=105)

        ## Treeview

        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1230,y=140,height=305)
        

        self.studentlist = ttk.Treeview(self, columns=("ID Number", "Name", "Course", "Year Level", "Gender"), height = 14, yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID Number", text="ID Number", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course", text="Course",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID Number", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)
        
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        
        

        self.studentlist.place(x=590,y=140)
        scrollbar.config(command=self.studentlist.yview)
        
        ## Buttons
        
        self.add = Button(self, text="ADD", font=("times new roman",16,"bold"), bg= "yellow", fg= "black", padx= 20,bd=0, command=add_stud)
        self.add.place(x=35,y=408)
        self.add.config(cursor= "hand2")

        self.update = Button(self, text="UPDATE", font=("times new roman",16,"bold"), bg= "yellow", fg= "black",padx= 10,bd=0, command=update_stud)
        self.update.place(x=175,y=408)
        self.update.config(cursor= "hand2")

        self.clear = Button(self, text="CLEAR", font=("times new roman",16,"bold"), bg= "yellow", fg= "black", padx= 10,bd=0,command=clear)
        self.clear.place(x=330,y=408)
        self.clear.config(cursor= "hand2")

        self.delete = Button(self, text="DELETE", font=("times new roman",16,"bold"), bg= "yellow", fg= "black",padx= 6,bd=0, command=delete_stud)
        self.delete.place(x=460,y=408)
        self.delete.config(cursor= "hand2")

        self.search = Button(self, text="SEARCH", font=("times new roman",14,"bold"),bd=0, bg= "yellow", fg="black", command=search_stud)
        self.search.place(x=1060,y=100)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="DISPLAY", font=("times new roman",14,"bold"),  bd=0, bg= "yellow", fg="black",command = display_stud)
        self.display.place(x=1160,y=100)
        self.display.config(cursor= "hand2")

        
        tables()
        display_stud()



root = sis()
root.geometry("1260x550")

root.mainloop()
