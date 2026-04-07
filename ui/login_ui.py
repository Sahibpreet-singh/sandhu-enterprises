import tkinter as tk
from tkinter import messagebox

SUPERADMIN_PASSWORD = "9246"  # you can load this from DB later

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login - Sandhu Enterprises")
        self.root.geometry("400x200")
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Superadmin Password (optional):").pack(pady=20)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        password = self.password_entry.get()

        if password == SUPERADMIN_PASSWORD:
            user_role = "superadmin"
        elif password == "":
            user_role = "admin"
        else:
            messagebox.showerror("Error", "Incorrect superadmin password")
            return

        # Successful login
        self.on_login_success({"role": user_role})
