from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

#ADMIN CREDENTIALS 
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpassword123"

_signin_bg_image_ref = None

def create_signin_window(master, switch_to_signup_callback, switch_to_forget_password_callback,
                         switch_to_admin_dashboard_callback, switch_to_regular_user_success_callback):
    global _signin_bg_image_ref

    login_window = Toplevel(master)
    login_window.title('Login Page')
    login_window.geometry('800x600')
    login_window.resizable(False, False)

    try:
        original_image = Image.open('app/abstract-digital-grid-black-background.jpg')
        resized_image = original_image.resize((800, 600), Image.LANCZOS)
        _signin_bg_image_ref = ImageTk.PhotoImage(resized_image)

        bgLabel = Label(login_window, image=_signin_bg_image_ref)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Background image not found for signin. Falling back to black.")
        login_window.config(bg='black')
    except Exception as e:
        print(f"Error loading or resizing signin background image: {e}")
        login_window.config(bg='black')

    #FUNCTIONALITY PART
    def user_enter(event):
        if usernameEntry.get() == 'Username':
            usernameEntry.delete(0, END)
            usernameEntry.config(fg='white')

    def password_enter(event):
        if passwordEntry.get() == 'Password':
            passwordEntry.delete(0, END)
            passwordEntry.config(show='*', fg='white')

    def login_user():
        username = usernameEntry.get()
        password = passwordEntry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # ADMIN LOGIN CHECK 
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            messagebox.showinfo("Admin Login", "Admin login successful! Redirecting to User Data.")
            login_window.destroy()
            switch_to_admin_dashboard_callback()
            return 
        
        entered_password_plain = password

        con = None
        try:
            con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata',port=3306)
            mycursor = con.cursor()

            query = "SELECT password FROM data WHERE username = %s OR email = %s"
            mycursor.execute(query, (username, username))
            result = mycursor.fetchone()

            if result:
                stored_password_plain = result[0]
                if entered_password_plain == stored_password_plain:
                    messagebox.showinfo("Login Success", "Login successfull!")
                    login_window.destroy()
                    switch_to_regular_user_success_callback()
                else:
                    messagebox.showerror("Login Failed", "Invalid username/email or password.")
            else:
                messagebox.showerror("Login Failed", "Invalid username/email or password.")

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database or perform login: {e}")
        finally:
            if con:
                mycursor.close()
                con.close()


    # --- GUI PART ---
    login_frame = Frame(login_window, bg='black', padx=30, pady=30)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    heading = Label(login_frame, text='USER LOGIN', font=('Microsoft Yahei UI Light', 23, 'bold'),
                    bg='black', fg='white')
    heading.pack(pady=(0, 20))

    usernameEntry = Entry(login_frame, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'),
                          bd=0, bg='black', fg='grey', insertbackground='white')
    usernameEntry.pack(pady=5)
    usernameEntry.insert(0, 'Username')
    usernameEntry.bind('<FocusIn>', user_enter)
    Frame(login_frame, width=250, height=2, bg='white').pack()

    passwordEntry = Entry(login_frame, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'),
                          bd=0, bg='black', fg='grey', insertbackground='white')
    passwordEntry.pack(pady=15)
    passwordEntry.insert(0, 'Password')
    passwordEntry.bind('<FocusIn>', password_enter)
    Frame(login_frame, width=250, height=2, bg='white').pack()

    forgetButton = Button(login_frame, text='Forgot Password?', bd=0, bg='black', fg='white', activebackground='black',
                          cursor='hand2', font=('Microsoft Yahei UI Light', 9, 'bold'), activeforeground='white',
                          command=lambda: [login_window.destroy(), switch_to_forget_password_callback()])
    forgetButton.pack(pady=(5, 20), anchor='e')

    loginButton = Button(login_frame, text='Login', font=('Open Sans', 16, 'bold'), cursor='hand2', bd=0, width=19,
                         fg='black', bg='white', activeforeground='black', activebackground='white',
                         command=login_user)
    loginButton.pack(pady=10)

    signupLabel = Label(login_frame, text='Dont have an account?', font=('Open Sans', 9, 'bold'), bg='black', fg='white')
    signupLabel.pack(pady=(10, 0))

    newaccountButton = Button(login_frame, text='Create new one', font=('Open Sans', 9, 'bold underline'), cursor='hand2', bd=0,
                              fg='blue', bg='black', activeforeground='blue', activebackground='black', command=switch_to_signup_callback)
    newaccountButton.pack()

    login_window.update_idletasks()
    login_window.deiconify()

    return login_window