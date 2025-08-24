from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

_forget_password_bg_image_ref = None

def create_forget_password_window(master, switch_to_signin_callback):
    global _forget_password_bg_image_ref

    forget_window = Toplevel(master)
    forget_window.title('Forgot Password')
    forget_window.geometry('500x550')
    forget_window.resizable(False, False)

    #Background Image Setup
    try:
        original_image = Image.open('app/abstract-digital-grid-black-background.jpg')
        resized_image = original_image.resize((500, 550), Image.LANCZOS)
        _forget_password_bg_image_ref = ImageTk.PhotoImage(resized_image)

        bgLabel = Label(forget_window, image=_forget_password_bg_image_ref)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Background image not found for forget password. Falling back to black.")
        forget_window.config(bg='black')
    except Exception as e:
        print(f"Error loading or resizing forget password background image: {e}")
        forget_window.config(bg='black')

    # Main frame 
    main_frame = Frame(forget_window, bg='black', padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

   
    request_reset_heading = Label(main_frame, text='Forgot Password?', font=('Microsoft Yahei UI Light', 18, 'bold'),
                                  bg='black', fg='white')
    request_reset_heading.pack(pady=(0, 15))

    request_instruction_label = Label(main_frame, text='Enter your username or email to reset your password.',
                                      font=('Microsoft Yahei UI Light', 10), bg='black', fg='white', wraplength=250)
    request_instruction_label.pack(pady=(0, 10))

    username_email_label = Label(main_frame, text='Username or Email:', font=('Microsoft Yahei UI Light', 10, 'bold'),
                                 bg='black', fg='white')
    username_email_label.pack(pady=(5, 0), anchor='w')

    username_email_entry = Entry(main_frame, width=30, font=('Microsoft Yahei UI Light', 10), bd=0,
                                 bg='white', fg='black', insertbackground='black')
    username_email_entry.pack(pady=5)

    request_reset_button = Button(main_frame, text='Request Reset', font=('Open Sans', 10, 'bold'),
                                  bd=0, bg='white', fg='black', activebackground='black',
                                  activeforeground='white', cursor='hand2')
    request_reset_button.pack(pady=20)

    set_password_heading = Label(main_frame, text='Set New Password', font=('Microsoft Yahei UI Light', 18, 'bold'),
                                 bg='black', fg='white')
    set_password_instruction_label = Label(main_frame, text='Enter and confirm your new password.',
                                           font=('Microsoft Yahei UI Light', 10), bg='black', fg='white', wraplength=250)
    
    new_password_label = Label(main_frame, text='New Password:', font=('Microsoft Yahei UI Light', 10, 'bold'),
                               bg='black', fg='white')
    new_password_entry = Entry(main_frame, width=30, font=('Microsoft Yahei UI Light', 10), bd=0,
                               bg='white', fg='black', show='*', insertbackground='black')
    
    confirm_password_label = Label(main_frame, text='Confirm New Password:', font=('Microsoft Yahei UI Light', 10, 'bold'),
                                  bg='black', fg='white')
    confirm_password_entry = Entry(main_frame, width=30, font=('Microsoft Yahei UI Light', 10), bd=0,
                                   bg='white', fg='black', show='*', insertbackground='black')
    
    set_new_password_button = Button(main_frame, text='Set New Password', font=('Open Sans', 10, 'bold'),
                                     bd=0, bg='white', fg='black', activebackground='black',
                                     activeforeground='white', cursor='hand2')

    back_button = Button(main_frame, text='Back to Login', font=('Open Sans', 9, 'underline'),
                         bd=0, bg='black', fg='blue', activebackground='black',
                         activeforeground='blue', cursor='hand2', command=lambda: [forget_window.destroy(), switch_to_signin_callback()])
    back_button.pack(pady=(10,0))


    # Functions to switch between views
    def show_request_reset_view():
        set_password_heading.pack_forget()
        set_password_instruction_label.pack_forget()
        new_password_label.pack_forget()
        new_password_entry.pack_forget()
        confirm_password_label.pack_forget()
        confirm_password_entry.pack_forget()
        set_new_password_button.pack_forget()
        back_button.pack_forget()

        request_reset_heading.pack(pady=(0, 15))
        request_instruction_label.pack(pady=(0, 10))
        username_email_label.pack(pady=(5, 0), anchor='w')
        username_email_entry.pack(pady=5)
        request_reset_button.pack(pady=20)
        back_button.pack(pady=(10,0))

    def show_set_password_view():
        request_reset_heading.pack_forget()
        request_instruction_label.pack_forget()
        username_email_label.pack_forget()
        username_email_entry.pack_forget()
        request_reset_button.pack_forget()
        back_button.pack_forget() 

        set_password_heading.pack(pady=(0, 15))
        set_password_instruction_label.pack(pady=(0, 10))
        new_password_label.pack(pady=(5, 0), anchor='w')
        new_password_entry.pack(pady=5)
        confirm_password_label.pack(pady=(5, 0), anchor='w')
        confirm_password_entry.pack(pady=5)
        set_new_password_button.pack(pady=20)
        back_button.pack(pady=(10,0)) 

    def process_request_reset():
        identifier = username_email_entry.get().strip()
        if not identifier:
            messagebox.showerror("Error", "Please enter your username or email address.")
            return
        
        con = None
        try:
            con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata',port=3306)
            mycursor = con.cursor()

            find_user_query = "SELECT username FROM data WHERE username = %s OR email = %s"
            mycursor.execute(find_user_query, (identifier, identifier))
            user_found = mycursor.fetchone()

            if user_found:
                messagebox.showinfo("Reset Process", "Correct entry, you can now set a new password.")
                show_set_password_view()
            else:
                messagebox.showinfo("Reset Process", "Wrong entry, you cannot set a new password.")
                username_email_entry.delete(0, END) 

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database or process request: {e}")
        finally:
            if con: 
                mycursor.close()
                con.close()

    def process_set_new_password():
        new_pass = new_password_entry.get()
        confirm_pass = confirm_password_entry.get()
        username_or_email_for_update = username_email_entry.get().strip()

        if not new_pass or not confirm_pass:
            messagebox.showerror("Error", "Please fill in both new password fields.")
            return
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New password and confirm password do not match.")
            return
        if len(new_pass) < 1:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        plain_new_password = new_pass

        con = None
        try:
            con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata')
            mycursor = con.cursor()
            update_query = "UPDATE data SET password = %s WHERE username = %s OR email = %s"
            mycursor.execute(update_query, (plain_new_password, username_or_email_for_update, username_or_email_for_update))
            con.commit()

            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", "Your password has been reset successfully. You can now log in with your new password.")
                forget_window.destroy()
                switch_to_signin_callback()
            else:
                messagebox.showerror("Error", "Failed to update password. User not found or no change occurred. Please try again.")

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not update password: {e}")
        finally:
            if con:
                mycursor.close()
                con.close()

    request_reset_button.config(command=process_request_reset)
    set_new_password_button.config(command=process_set_new_password)

    show_request_reset_view()

    forget_window.update_idletasks()
    forget_window.deiconify()

    return forget_window