import sys, os
sys.path.insert(0, os.path.abspath('.'))
from tkinter import Tk
from ui.customer_item_ui import CustomerItemUI
from tkinter import messagebox
# suppress message boxes for automation
messagebox.showinfo = lambda *a, **k: None
messagebox.showerror = lambda *a, **k: None

root = Tk()
root.withdraw()
win = CustomerItemUI(root)
win.show_full_form()

# Fill customer
win.name_entry.insert(0, "UI Item Test User")
win.phone_entry.insert(0, "5551234567")
win.remarks_entry.insert(0, "Added via UI automation")
win.date_entry.delete(0, 'end')
win.date_entry.insert(0, "2025-12-30")

# Fill item fields required for EMI
win.entries["Brand"].insert(0, "TestBrand")
win.entries["Model"].insert(0, "T1")
win.entries["Item Amount"].insert(0, "10000")
win.entries["Advance"].insert(0, "1000")
win.entries["Interest (%)"].insert(0, "12")
win.entries["Installments"].insert(0, "12")

# Calculate EMI then Save
win.calculate_emi()
win.save_all()
root.destroy()
print('saved')