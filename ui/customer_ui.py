import tkinter as tk
from tkinter import messagebox, ttk
from models.customer_model import insert_customer, add_customer
from models.address_model import get_all_addresses, add_address
from models.village_model import get_all_villages, add_village
from datetime import date, datetime


def today_str():
    return date.today().isoformat()


class AddCustomerWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Add Customer")
        self.win.geometry("400x400")

        tk.Label(self.win, text="Name").pack()
        self.name_entry = tk.Entry(self.win)
        self.name_entry.pack()

        tk.Label(self.win, text="Phone").pack()
        self.phone_entry = tk.Entry(self.win)
        self.phone_entry.pack()

        tk.Label(self.win, text="Address").pack()
        # editable so typing shows suggestions
        self.address_cb = ttk.Combobox(self.win, width=40, state="normal")
        self.address_cb.pack()
        tk.Button(self.win, text="Add Address", command=self.add_address_dialog).pack(pady=2)

        tk.Label(self.win, text="Village").pack()
        self.village_cb = ttk.Combobox(self.win, width=40, state="normal")
        self.village_cb.pack()
        tk.Button(self.win, text="Add Village", command=self.add_village_dialog).pack(pady=2)

        # store full lists for filtering
        self.address_full = []
        self.village_full = []

        self.load_address_village()

        # local filter function for suggestions
        def _filter(cb, full_list):
            val = cb.get()
            if not val:
                cb['values'] = full_list
                return
            val_l = val.strip().lower()
            matches = [s for s in full_list if val_l in s.lower()]
            cb['values'] = matches
            if matches:
                try:
                    cb.event_generate('<Down>')
                except Exception:
                    pass

        # bind key release to filter suggestions
        self.address_cb.bind('<KeyRelease>', lambda e: _filter(self.address_cb, self.address_full))
        self.village_cb.bind('<KeyRelease>', lambda e: _filter(self.village_cb, self.village_full))

        tk.Label(self.win, text="Remarks").pack()
        self.remarks_entry = tk.Entry(self.win)
        self.remarks_entry.pack()

        tk.Label(self.win, text="Entry Date (YYYY-MM-DD)").pack()
        self.date_entry = tk.Entry(self.win)
        self.date_entry.insert(0, today_str())
        self.date_entry.pack()

        tk.Button(self.win, text="Save", command=self.save_customer).pack(pady=10)

    def save_customer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        remarks = self.remarks_entry.get()

        entry_date_str = self.date_entry.get().strip()
        entry_date = None
        if entry_date_str:
            try:
                # Expect YYYY-MM-DD
                datetime.strptime(entry_date_str, "%Y-%m-%d")
                entry_date = entry_date_str
            except ValueError:
                messagebox.showerror("Error", "Entry Date must be YYYY-MM-DD")
                return

        # address/village selection
        address_val = self.address_cb.get()
        address_id = None
        if address_val:
            # try to parse "id - address" format if present
            try:
                address_id = int(address_val.split(" - ")[0])
            except Exception:
                address_id = None

        village_val = self.village_cb.get()
        village_id = None
        if village_val:
            try:
                village_id = int(village_val.split(" - ")[0])
            except Exception:
                village_id = None

        if not name or not phone:
            messagebox.showerror("Error", "Name and Phone are required")
            return

        # prefer add_customer to include optional address_id and village_id
        address_text = None
        if address_val and not address_id:
            # user selected a free text address (unlikely because combobox is readonly)
            address_text = address_val

        add_customer(
            name=name,
            phone=phone,
            address=address_text,
            remarks=remarks,
            address_id=address_id,
            village_id=village_id,
            entry_date=entry_date
        )
        messagebox.showinfo("Success", "Customer added successfully")
        self.win.destroy()

    def load_address_village(self):
        # Populate address combobox
        addresses = get_all_addresses()
        self.address_full[:] = [f"{a['address_id']} - {a['address']}" for a in addresses]
        self.address_cb["values"] = self.address_full

        villages = get_all_villages()
        self.village_full[:] = [f"{v['village_id']} - {v['name']}" for v in villages]
        self.village_cb["values"] = self.village_full

    def add_address_dialog(self):
        def save():
            text = entry.get()
            if text:
                add_address(text)
                self.load_address_village()
                dlg.destroy()

        dlg = tk.Toplevel(self.win)
        dlg.title("Add Address")
        tk.Label(dlg, text="Address").pack()
        entry = tk.Entry(dlg, width=50)
        entry.pack()
        tk.Button(dlg, text="Save", command=save).pack()

    def add_village_dialog(self):
        def save():
            text = entry.get()
            if text:
                add_village(text)
                self.load_address_village()
                dlg.destroy()

        dlg = tk.Toplevel(self.win)
        dlg.title("Add Village")
        tk.Label(dlg, text="Village Name").pack()
        entry = tk.Entry(dlg, width=50)
        entry.pack()
        tk.Button(dlg, text="Save", command=save).pack()
