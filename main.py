import tkinter as tk
from ui.main_window import MainWindow
from tkinter import PhotoImage
from ui.login_ui import LoginWindow
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def start_main_app(user):
    login_root.destroy()  # close login window
    main_root = tk.Tk()

    # Set app icon
    icon_path = resource_path("assets/app_icon.png")
    icon = PhotoImage(file=icon_path)
    main_root.iconphoto(True, icon)
    main_root._icon_ref = icon  # prevent garbage collection

    # Launch main app with user info
    MainWindow(main_root, user)
    main_root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()

    # Set login window icon
    icon_path = resource_path("assets/app_icon.png")
    icon = PhotoImage(file=icon_path)
    login_root.iconphoto(True, icon)
    login_root._icon_ref = icon

    # Start login
    LoginWindow(login_root, on_login_success=start_main_app)
    login_root.mainloop()
