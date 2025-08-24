from tkinter import *
import signup_module
import signin_module
import forget_password_module
import dashboard_module

class App:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()

        self.signup_window = None
        self.signin_window = None
        self.forget_password_window = None
        self.dashboard_window = None
        self.regular_user_welcome_window = None 

        self.show_signup_page()

    def _destroy_all_windows(self):
        if self.signup_window and self.signup_window.winfo_exists():
            self.signup_window.destroy()
        if self.signin_window and self.signin_window.winfo_exists():
            self.signin_window.destroy()
        if self.forget_password_window and self.forget_password_window.winfo_exists():
            self.forget_password_window.destroy()
        if self.dashboard_window and self.dashboard_window.winfo_exists():
            self.dashboard_window.destroy()
        if self.regular_user_welcome_window and self.regular_user_welcome_window.winfo_exists():
            self.regular_user_welcome_window.destroy()

    def show_signup_page(self):
        self._destroy_all_windows()
        self.signup_window = signup_module.create_signup_window(self.master, self.show_signin_page)
        self.signup_window.lift()
        self.signup_window.focus_set()

    def show_signin_page(self):
        self._destroy_all_windows()
        self.signin_window = signin_module.create_signin_window(
            self.master,
            self.show_signup_page,
            self.show_forget_password_page,
            self.show_dashboard_page, 
            self.show_regular_user_welcome_page 
        )
        self.signin_window.lift()
        self.signin_window.focus_set()

    def show_forget_password_page(self):
        self._destroy_all_windows()
        self.forget_password_window = forget_password_module.create_forget_password_window(self.master, self.show_signin_page)
        self.forget_password_window.lift()
        self.forget_password_window.focus_set()

    def show_dashboard_page(self):
        self._destroy_all_windows()
        self.dashboard_window = dashboard_module.create_dashboard_window(self.master, self.show_signin_page)
        self.dashboard_window.lift()
        self.dashboard_window.focus_set()

    def show_regular_user_welcome_page(self):
        self._destroy_all_windows()
        self.regular_user_welcome_window = Toplevel(self.master)
        self.regular_user_welcome_window.title("Welcome User!")
        self.regular_user_welcome_window.geometry("400x200")
        self.regular_user_welcome_window.grab_set()

        Label(self.regular_user_welcome_window, text="Welcome! You have successfully logged in as a regular user.",
              font=('Arial', 12)).pack(pady=20)
        Button(self.regular_user_welcome_window, text="Go to Login",
               command=lambda: [self.regular_user_welcome_window.destroy(), self.show_signin_page()]).pack(pady=10)

        self.regular_user_welcome_window.lift()
        self.regular_user_welcome_window.focus_set()

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()