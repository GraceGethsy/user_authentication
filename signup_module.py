from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql

_signup_bg_image_ref = None

def create_signup_window(master, switch_to_signin_callback):
    global _signup_bg_image_ref 

    signup_window = Toplevel(master) 
    signup_window.title('Signup Page')
    signup_window.geometry('800x600') 
    signup_window.resizable(False, False) 

    # Background Image Setup
    try:
        original_image = Image.open('app/abstract-digital-grid-black-background.jpg')
       
        resized_image = original_image.resize((800, 600), Image.LANCZOS)
        _signup_bg_image_ref = ImageTk.PhotoImage(resized_image)

        bgLabel = Label(signup_window, image=_signup_bg_image_ref)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1) 
    except FileNotFoundError:
        print("Background image not found for signup. Please check the path: app/abstract-digital-grid-black-background.jpg")
        signup_window.config(bg='black') 
    except Exception as e:
        print(f"Error loading or resizing signup background image: {e}")
        signup_window.config(bg='black')

    #Frame for form elements 
    frame = Frame(signup_window, bg='black')
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def clear():
        emailEntry.delete(0,END)
        usernameEntry.delete(0,END)
        passwordEntry.delete(0,END)
        confirmpasswordEntry.delete(0,END)
        check.set(0)

    def connect_database():
        if emailEntry.get()=='' or usernameEntry.get()=='' or passwordEntry.get()=='' or confirmpasswordEntry.get()=='':
            messagebox.showerror('Error','All fields are required')
        elif passwordEntry.get() != confirmpasswordEntry.get():
            messagebox.showerror('Error','Password mismatch')
        elif check.get()==0:
            messagebox.showerror('Error', f'Database connectivity issue:\n{e}')
        else:
            try:
                con = pymysql.connect(host='localhost',user='root',password='1234',port=3306)
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error','Database connectivity issue,Please Try again')
                return
            
            query= 'create database IF NOT EXISTS userdata'
            mycursor.execute(query)
            query= 'use userdata'
            mycursor.execute(query)
            query='create table  IF NOT EXISTS  data(id int auto_increment primary key not null,email varchar(50),username varchar(100),password varchar(250))'
            mycursor.execute(query)

            query= 'select * from data where username=%s'
            mycursor.execute(query,(usernameEntry.get()))

            row=mycursor.fetchone()
            if row!=None:
                messagebox.showerror('Error','Username already exists')
           
            else:
              query= 'insert into data(email,username,password) values(%s,%s,%s)'
              mycursor.execute(query,(emailEntry.get(),usernameEntry.get(),passwordEntry.get()))
              con.commit()
              con.close()
              messagebox.showinfo('Success','Registration is successful')
              clear()
              signup_window.destroy()
              switch_to_signin_callback()

    #GUI Elements 
    heading = Label(frame,text='CREATE AN ACCOUNT',font=('Microsoft Yahei UI Light', 22,'bold')
                    ,bg='black',fg='white')
    heading.grid(row=0,column=0, columnspan=2, pady=(0, 20))

    emailLabel= Label(frame,text='Email',font=('Microsoft Yahei UI Light', 10,'bold'),bg='black',fg='white')
    emailLabel.grid(row=1,column=0,sticky='w',pady=(10,0))
    emailEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light', 10,'bold'),bg='white',fg='black', insertbackground='black')
    emailEntry.grid(row=2,column=0,sticky='w')

    usernameLabel= Label(frame,text='Username',font=('Microsoft Yahei UI Light', 10,'bold'),bg='black',fg='white')
    usernameLabel.grid(row=3,column=0,sticky='w',pady=(10,0))
    usernameEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light', 10,'bold'),bg='white',fg='black', insertbackground='black')
    usernameEntry.grid(row=4,column=0,sticky='w')

    passwordLabel= Label(frame,text='Password',font=('Microsoft Yahei UI Light', 10,'bold'),bg='black',fg='white')
    passwordLabel.grid(row=5,column=0,sticky='w',pady=(10,0))
    passwordEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light', 10,'bold'),bg='white',fg='black', show='*', insertbackground='black')
    passwordEntry.grid(row=6,column=0,sticky='w')

    confirmpasswordLabel= Label(frame,text='Confirm Password',font=('Microsoft Yahei UI Light', 10,'bold'),bg='black',fg='white')
    confirmpasswordLabel.grid(row=7,column=0,sticky='w',pady=(10,0))
    confirmpasswordEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light', 10,'bold'),bg='white',fg='black', show='*', insertbackground='black')
    confirmpasswordEntry.grid(row=8,column=0,sticky='w')
    
    check = IntVar()
    termscond=Checkbutton(frame,text='I agree to the Terms & Conditions',font=('Microsoft Yahei UI Light', 10,'bold'),bg='black',fg='white',
                          activebackground='black',activeforeground='white',cursor='hand2', selectcolor='black',variable=check)
    termscond.grid(row=9,column=0,sticky='w',pady=(10,0))

    signup_button = Button(frame,text='Signup',font=('Microsoft Yahei UI Light', 10,'bold'),bd=0,bg='white',
                           fg='black', activebackground='black',activeforeground='white',width=27,command=connect_database)
    signup_button.grid(row=10,column=0,sticky='w',pady=(10,0))

    alreadyaccount= Label(frame,text='Already have account?',font=('Microsoft Yahei UI Light', 8,'bold'),bg='black',fg='white')
    alreadyaccount.grid(row=11,column=0,sticky='w',pady=(10,0))

    loginButton=Button(frame,text='Login',font=('Open Sans',8,'bold underline'),cursor='hand2',bd=0,
                        fg='blue',bg='black', activebackground='blue',activeforeground='black',command=switch_to_signin_callback)
    
    loginButton.grid(row=11, column=1, sticky='w', pady=(10,0))


    signup_window.update_idletasks()
    signup_window.deiconify() 

    return signup_window
