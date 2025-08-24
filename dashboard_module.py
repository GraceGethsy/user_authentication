from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql

_dashboard_bg_image_ref = None

def create_dashboard_window(master, switch_to_signin_callback):
    global _dashboard_bg_image_ref

    dashboard_window = Toplevel(master)
    dashboard_window.title('User Dashboard (Admin View)') 
    dashboard_window.geometry('800x600')
    dashboard_window.resizable(True, True)

    try:
        original_image = Image.open('app/abstract-digital-grid-black-background.jpg')
        resized_image = original_image.resize((800, 600), Image.LANCZOS)
        _dashboard_bg_image_ref = ImageTk.PhotoImage(resized_image)

        bgLabel = Label(dashboard_window, image=_dashboard_bg_image_ref)
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
        dashboard_window.bind('<Configure>', lambda event, img=original_image, label=bgLabel: resize_background(event, img, label))

    except FileNotFoundError:
        print("Background image not found for dashboard. Falling back to black.")
        dashboard_window.config(bg='black')
    except Exception as e:
        print(f"Error loading or resizing dashboard background image: {e}")
        dashboard_window.config(bg='black')

    def resize_background(event, original_img, label):
        new_width = event.width
        new_height = event.height
        if new_width > 0 and new_height > 0:
            try:
                global _dashboard_bg_image_ref
                resized_img = original_img.resize((new_width, new_height), Image.LANCZOS)
                _dashboard_bg_image_ref = ImageTk.PhotoImage(resized_img)
                label.config(image=_dashboard_bg_image_ref)
            except Exception as e:
                print(f"Error during background image resize: {e}")


    content_frame = Frame(dashboard_window, bg='black', bd=2, relief='groove')
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    heading = Label(content_frame, text='Registered Users (Admin View)', font=('Microsoft Yahei UI Light', 20, 'bold'),
                    bg='black', fg='white')
    heading.pack(pady=(10, 20))

    columns = ('ID', 'Email', 'Username', 'Password')
    tree = ttk.Treeview(content_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        if col == 'ID':
            tree.column(col, width=50, stretch=NO, anchor='center')
        elif col == 'Email':
            tree.column(col, width=200, stretch=YES)
        elif col == 'Username':
            tree.column(col, width=150, stretch=YES)
        elif col == 'Password ':
            tree.column(col, width=200, stretch=YES)

    scrollbar = Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill='both')

    def load_user_data():
        for item in tree.get_children():
            tree.delete(item)

        con = None
        try:
            con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata',port=3306)
            mycursor = con.cursor()

            select_query = "SELECT id, email, username, password FROM data"
            mycursor.execute(select_query)
            rows = mycursor.fetchall()

            for row in rows:
                tree.insert('', 'end', values=row)

        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not fetch data: {e}")
        finally:
            if con:
                mycursor.close()
                con.close()

    refresh_button = Button(content_frame, text='Refresh Data', font=('Open Sans', 10, 'bold'),
                            bd=0, bg='white', fg='black', activebackground='black',
                            activeforeground='white', cursor='hand2', command=load_user_data)
    refresh_button.pack(pady=(15, 5))

    logout_button = Button(content_frame, text='Logout', font=('Open Sans', 10, 'bold'),
                           bd=0, bg='red', fg='white', activebackground='darkred',
                           activeforeground='white', cursor='hand2',
                           command=lambda: [dashboard_window.destroy(), switch_to_signin_callback()])
    logout_button.pack(pady=10)

    load_user_data()

    dashboard_window.update_idletasks()
    dashboard_window.deiconify()

    return dashboard_window