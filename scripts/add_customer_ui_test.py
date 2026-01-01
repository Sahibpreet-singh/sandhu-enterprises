from tkinter import Tk
from ui.customer_ui import AddCustomerWindow
from tkinter import messagebox
# suppress message boxes for automation
messagebox.showinfo = lambda *a, **k: None
messagebox.showerror = lambda *a, **k: None

root = Tk()
root.withdraw()
win = AddCustomerWindow(root)

# Fill form
win.name_entry.insert(0, "UI Test User")
win.phone_entry.insert(0, "1234567890")
win.remarks_entry.insert(0, "Added via UI automation")
win.date_entry.delete(0, 'end')
win.date_entry.insert(0, "2025-12-31")

# Save (calls add_customer and closes window)
win.save_customer()
root.destroy()
print('saved')
