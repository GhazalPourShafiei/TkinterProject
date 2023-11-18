#project for github

import sqlite3
import tkinter
from tkinter import messagebox

cnt = sqlite3.connect("uni.db")
#----------------CREATE TABLE-------------
# sql=''' CREATE TABLE students(
#         id INTEGER PRIMARY KEY ,
#         user VARCHAR(20) NOT NULL ,
#         password VARCHAR(30) NOT NULL,
#         Dars1 VARCHAR(20),
#         Dars2 VARCHAR(20),
#         Dars3 VARCHAR(20)
#         )'''
# cnt.execute(sql)
#
#---------------------------main win(def login, validate, submit, delete, logout)---------------------------    
def login():
    global session ,count,pw
    user=txt_user.get()
    pas=txt_pass.get()
    
    sql=''' SELECT * FROM students WHERE user=? and password=?'''
    result=cnt.execute(sql,(user,pas))
    rows=result.fetchall()
    
    if (len(rows)>0):
        lbl_msg.configure(text='welcome to your account!', fg='green',bg="aquamarine2")
        btn_login.configure(state='disable')
        btn_logout.configure(state='active',bg="cyan4")
        txt_user.delete(0,'end')
        txt_pass.delete(0,'end')
        session=user
        pw=pas
        count=0
        
    else:
        lbl_msg.configure(text='wrong Name or Password!' , fg='red',bg="aquamarine2")
        count+=1
        if count==3:
            lbl_msg.configure(text='Unfortunately,You have entered the wrong Name or Password more than three times!' , fg='red')
            btn_login.configure(state='disabled')
            
def validate(user,pas):
    if user=='' or pas=='':
        lbl_msg.configure(text='please fill the textbox',fg='red')
        return False
    if len(pas)<8:
        lbl_msg.configure(text='password length at least 8')
        return False
    
    if user.lower()=='admin':
        lbl_msg.configure(text='admin is restricted!',fg='red',bg="aquamarine2")
        return False
    
    return True

def submit():
    user=txt_user.get()
    pas=txt_pass.get()
    result=validate(user,pas)
    if result:
        sql=''' INSERT INTO students (user,password) 
        VALUES(?,?)'''
        
        cnt.execute(sql,(user,pas))
        cnt.commit()
        lbl_msg.configure(text='submit done!' , fg='green')
        txt_user.delete(0,'end')
        txt_pass.delete(0,'end')       
def delete():
    global session ,pw
    if session==False:
        lbl_msg.configure(text='please Login first!', fg='red')
        return
    confirm=messagebox.askyesno(message='are you sure to delete your account?')
    if confirm:
        if session=='admin':
            lbl_msg.configure(text='admin acc is not removable!', fg='red')
            return
        sql=''' DELETE FROM students WHERE user=? and password=?'''
        cnt.execute(sql,(session,pw))
        cnt.commit()
        lbl_msg.configure(text='your acc deleted!', fg='green')
        session=False
        btn_logout.configure(state='disabled')
        btn_login.configure(state='active')
        
  
def logout():
    global session
    session=False
    lbl_msg.configure(text='you are logout!', fg='green')
    btn_login.configure(state='active')
    btn_logout.configure(state='disabled')


#----------------------------Dars--------------------------
def Dars1():
    global txt , session ,pw
    sql=''' UPDATE students SET Dars1="Dars 1" WHERE user=? AND password=? '''
    cnt.execute(sql,(session,pw))
    cnt.commit()
        
    txt+=">> Dars 1 <<"
    lbl_selected.configure(text=txt ,fg="purple")
    btn_Dars1.configure(state="disabled")
       
def Dars2():
    global txt , session ,pw
    sql=''' UPDATE students SET Dars2="Dars 2" WHERE user=? AND password=? '''
    cnt.execute(sql,(session,pw))
    cnt.commit()
        
    txt+=">> Dars 2 << "
    lbl_selected.configure(text=txt ,fg="purple",bg="aquamarine2")
    btn_Dars2.configure(state="disabled")
        
def Dars3():
    global txt , session ,pw
    sql=''' UPDATE students SET Dars3="Dars 3" WHERE user=? AND password=? '''
    cnt.execute(sql,(session,pw))
    cnt.commit()
        
    txt+=">> Dars 3 <<"
    lbl_selected.configure(text=txt ,fg="purple")
    btn_Dars3.configure(state="disabled")  
    
def ok():
    global txt
    if txt=='':
        lbl_selected.configure(text="You have not selected any courses yet!",fg="red")
        return
    confirm=messagebox.askyesno(message='Do you approve of this function?')
    if confirm:
        global session , pw
        sql=''' SELECT * FROM students WHERE user=? and password=?'''
        result=cnt.execute(sql,(session,pw))
        rows=result.fetchall()
        print("a user with the following profile entered and selected:"+str(rows))
        print("These were the user's choices : " +txt)
        lbl_selected.configure(text="your selected courses were successfully registered : "+txt ,fg="green",bg="aquamarine2")
        lbl_choosed.configure(text='',bg="aquamarine2")
        btn_Dars1.configure(state="disabled")
        btn_Dars2.configure(state="disabled")
        btn_Dars3.configure(state="disabled")

        btn_ok.configure(state="disabled")

      
#---------------tkinter(win)-------------
session=False
win=tkinter.Tk()
win.configure(bg="aquamarine2", cursor="heart",bd=44)
win.title('university')
win.geometry('500x580')
#-------------------------tkinter(user, pass)------------------------
txt=''
count=0

lbl_user=tkinter.Label(win,text='Name: ',fg="darkgreen",bg="aquamarine2")
lbl_user.pack()

txt_user=tkinter.Entry(win,fg="cyan4")
txt_user.pack()

lbl_pass=tkinter.Label(win,text='Password: ',fg="darkgreen",bg="aquamarine2")
lbl_pass.pack()

txt_pass=tkinter.Entry(win,fg="cyan4")
txt_pass.pack()

lbl_msg=tkinter.Label(win, text='')
lbl_msg.pack()

#---tkinter(login, submit, delete, logout)---

btn_login=tkinter.Button(win,text='Login', command=login,bg="cyan4")
btn_login.pack()

btn_submit=tkinter.Button(win,text='submit' ,command=submit,bg="cyan4")
btn_submit.pack()

btn_delete=tkinter.Button(win,text='delete account' ,command=delete,bg="cyan4")
btn_delete.pack()

btn_logout=tkinter.Button(win,text='Logout' ,command=logout , state='disabled',bg="cyan4")
btn_logout.pack()

#--------------tkinter(Dars)----------------
lbl_select=tkinter.Label(win,text='Please choose your courses and finally click OK : ',fg="blue",bg="aquamarine2")
lbl_select.pack()
    
btn_Dars1=tkinter.Button(win,text='course 1' ,command=Dars1,bg="cyan4")
btn_Dars1.pack()
    
btn_Dars2=tkinter.Button(win,text='course 2' ,command=Dars2,bg="cyan4")
btn_Dars2.pack()
    
btn_Dars3=tkinter.Button(win,text='course 3' ,command=Dars3,bg="cyan4")
btn_Dars3.pack()
    
lbl_choosed=tkinter.Label(win,text='Selected courses : ',fg="purple",bg="aquamarine2")
lbl_choosed.pack()
    
lbl_selected=tkinter.Label(win, text='',bg="aquamarine2")
lbl_selected.pack()
    
btn_ok=tkinter.Button(win,text='OK' ,command=ok,bg="cyan4")
btn_ok.pack()

win.mainloop()
