import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from models.customer_model import add_customer
from models.address_model import get_all_addresses, add_address
from models.village_model import get_all_villages, add_village
from models.item_model import add_item
from models.guarantor_model import add_guarantor
from services.emi_calculate import calculate_emi


class CustomerItemUI:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Add Customer with Item & Guarantor")
        self.window.geometry("600x750")
        self.window.resizable(False, False)

        self.num_guarantors = tk.IntVar(value=1)
        self.emi_data = None
        self.guarantor_entries = []

        self.ask_num_guarantors()

    # ================= STEP 1: Ask Number of Guarantors =================
    def ask_num_guarantors(self):
        self.clear_window()

        tk.Label(self.window, text="Select Number of Guarantors", font=("Arial", 12, "bold")).pack(pady=20)

        num_cb = ttk.Combobox(self.window, textvariable=self.num_guarantors, values=[1, 2], state="readonly", width=20)
        num_cb.pack(pady=10)
        self.num_guarantors.set(1)

        tk.Button(self.window, text="Next", command=self.show_full_form).pack(pady=20)

    # ================= STEP 2: Show Full Form =================
    def show_full_form(self):
        self.clear_window()
        row = 0
        form = tk.Frame(self.window, padx=10, pady=10)
        form.pack(fill=tk.BOTH, expand=True)
        self.form_frame = form

        # --------- CUSTOMER INFO ---------
        tk.Label(form, text="Customer Information", font=("Arial", 14, "bold"), bg="#f5f7fa", fg="#2c3e50").grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        tk.Label(form, text="Name:").grid(row=row, column=0, sticky="e")
        self.name_entry = tk.Entry(form, width=40)
        self.name_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(form, text="Phone:").grid(row=row, column=0, sticky="e")
        self.phone_entry = tk.Entry(form, width=40)
        self.phone_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(form, text="Address:").grid(row=row, column=0, sticky="e")
        # editable so typing filters suggestions
        self.address_cb = ttk.Combobox(form, width=37, state="normal")
        self.address_cb.grid(row=row, column=1, pady=2)
        tk.Button(form, text="Add Address", command=self.add_address_dialog).grid(row=row, column=2, padx=5)
        row += 1

        # full lists for local filtering
        self.address_full = []

        tk.Label(form, text="Remarks:").grid(row=row, column=0, sticky="e")
        self.remarks_entry = tk.Entry(form, width=40)
        self.remarks_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(form, text="Entry Date (DD-MM-YYYY):").grid(row=row, column=0, sticky="e")
        self.date_entry = tk.Entry(form, width=40)
        self.date_entry.grid(row=row, column=1, pady=2)
        self.date_entry.insert(0, date.today().strftime('%d-%m-%Y'))
        row += 1

        tk.Label(form, text="Village:").grid(row=row, column=0, sticky="e")
        self.village_cb = ttk.Combobox(form, width=37, state="normal")
        self.village_cb.grid(row=row, column=1, pady=2)
        tk.Button(form, text="Add Village", command=self.add_village_dialog).grid(row=row, column=2, padx=5)
        row += 1

        # full lists for local filtering
        self.village_full = []

        # after creating widgets, bind key-release to filter suggestions
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

        self.address_cb.bind('<KeyRelease>', lambda e: _filter(self.address_cb, self.address_full))
        self.village_cb.bind('<KeyRelease>', lambda e: _filter(self.village_cb, self.village_full))

        # --------- ITEM / EMI INFO ---------
        tk.Label(form, text="Item / EMI Information", font=("Arial", 14, "bold"), bg="#f5f7fa", fg="#2c3e50").grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        labels = ["Brand", "Model", "Item Amount", "Advance", "Interest", "Installments", "Mode"]
        self.entries = {}

        interest_row = None
        for text in labels:
            tk.Label(form, text=text+":").grid(row=row, column=0, sticky="e")
            if text == "Mode":
                self.mode_cb = ttk.Combobox(form, values=["MONTHLY", "WEEKLY", "DAILY", "ONE-TIME"], state="readonly", width=37)
                self.mode_cb.grid(row=row, column=1, pady=2)
                self.mode_cb.set("MONTHLY")
                self.mode_cb.bind("<<ComboboxSelected>>", self.on_mode_change)
            else:
                entry = tk.Entry(form, width=40)
                entry.grid(row=row, column=1, pady=2)
                self.entries[text] = entry
                if text == "Interest":
                    # remember row where Interest is placed so we can position the interest type combobox next to it
                    interest_row = row
            row += 1

        # Interest type combobox (placed next to Interest)
        if interest_row is None:
            interest_row = 0
        self.interest_type_cb = ttk.Combobox(form, values=["Percent", "Amount"], state="readonly", width=10)
        self.interest_type_cb.grid(row=interest_row, column=2, padx=5)
        self.interest_type_cb.set("Percent")

        # --------- GUARANTOR INFO ---------
        tk.Label(form, text="Guarantor Information", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        self.guarantor_entries = []
        for i in range(self.num_guarantors.get()):
            tk.Label(form, text=f"Guarantor {i+1} Name:").grid(row=row, column=0, sticky="e")
            name_entry = tk.Entry(form, width=40)
            name_entry.grid(row=row, column=1, pady=2)
            row += 1

            tk.Label(form, text=f"Guarantor {i+1} Phone:").grid(row=row, column=0, sticky="e")
            phone_entry = tk.Entry(form, width=40)
            phone_entry.grid(row=row, column=1, pady=2)
            row += 1

            tk.Label(form, text=f"Guarantor {i+1} Address:").grid(row=row, column=0, sticky="e")
            address_entry = tk.Entry(form, width=40)
            address_entry.grid(row=row, column=1, pady=2)
            row += 1

            self.guarantor_entries.append({
                "name": name_entry,
                "phone": phone_entry,
                "address": address_entry
            })

        # --------- BUTTONS ---------
        tk.Button(form, text="Calculate EMI", command=self.calculate_emi, font=("Arial", 12, "bold"), bg="#3498db", fg="white", width=15, height=2).grid(row=row, column=0, pady=10)
        tk.Button(form, text="Save All", command=self.save_all, font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", width=15, height=2).grid(row=row, column=1, pady=10)
        row += 1

        self.result_label = tk.Label(form, text="", fg="green")
        self.result_label.grid(row=row, column=0, columnspan=2)
        # populate address/village lists
        self.load_address_village()

    # ================= CLEAR WINDOW =================
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def load_address_village(self):
        addresses = get_all_addresses()
        self.address_full[:] = [f"{a['address_id']} - {a['address']}" for a in addresses]
        self.address_cb["values"] = self.address_full

        villages = get_all_villages()
        self.village_full[:] = [f"{v['village_id']} - {v['name']}" for v in villages]
        self.village_cb["values"] = self.village_full

    def on_mode_change(self, event=None):
        if self.mode_cb.get() == "ONE-TIME":
            self.entries["Installments"].delete(0, tk.END)
            self.entries["Installments"].insert(0, "1")
            self.entries["Installments"].config(state="disabled")
        else:
            self.entries["Installments"].config(state="normal")

    # ================= EMI CALCULATION =================
    def calculate_emi(self):
        try:
            item_amount = float(self.entries["Item Amount"].get())
            advance = float(self.entries["Advance"].get())
            interest = float(self.entries["Interest"].get())
            installments = int(self.entries["Installments"].get())

            interest_type = self.interest_type_cb.get() or 'Percent'

            self.emi_data = calculate_emi(item_amount, advance, interest, installments, interest_type=interest_type)
            self.result_label.config(text=f"EMI Amount: ₹{self.emi_data['installment_amount']}")
        except Exception:
            messagebox.showerror("Error", "Invalid item/EMI values")

    def add_address_dialog(self):
        def save():
            text = entry.get()
            if text:
                add_address(text)
                self.load_address_village()
                dlg.destroy()

        dlg = tk.Toplevel(self.window)
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

        dlg = tk.Toplevel(self.window)
        dlg.title("Add Village")
        tk.Label(dlg, text="Village Name").pack()
        entry = tk.Entry(dlg, width=50)
        entry.pack()
        tk.Button(dlg, text="Save", command=save).pack()

    # ================= SAVE EVERYTHING =================
    def save_all(self):
        if not self.emi_data:
            messagebox.showerror("Error", "Calculate EMI first")
            return

        # Save Customer
        # parse selected address
        address_val = self.address_cb.get()
        address_id = None
        address_text = None
        if address_val:
            parts = address_val.split(" - ", 1)
            try:
                address_id = int(parts[0])
                address_text = parts[1] if len(parts) > 1 else None
            except Exception:
                address_text = address_val

        village_val = self.village_cb.get()
        village_id = None
        if village_val:
            try:
                village_id = int(village_val.split(" - ")[0])
            except Exception:
                village_id = None

        # Validate entry date
        entry_date_str = None
        entry_date_val = self.date_entry.get().strip() if hasattr(self, 'date_entry') else ''
        if entry_date_val:
            try:
                try:
                    # Try DD-MM-YYYY first
                    parsed_date = datetime.strptime(entry_date_val, "%d-%m-%Y")
                    entry_date_str = parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    # Try YYYY-MM-DD
                    datetime.strptime(entry_date_val, "%Y-%m-%d")
                    entry_date_str = entry_date_val
            except ValueError:
                messagebox.showerror("Error", "Entry Date must be DD-MM-YYYY or YYYY-MM-DD")
                return

        customer_id = add_customer(
            name=self.name_entry.get(),
            phone=self.phone_entry.get(),
            address=address_text,
            remarks=self.remarks_entry.get(),
            address_id=address_id,
            village_id=village_id,
            entry_date=entry_date_str
        )

        # Save Item
        start_date = date.today()
        if entry_date_str:
            # Use the provided entry_date as item start_date
            start_date = date.fromisoformat(entry_date_str)

        add_item(
            customer_id=customer_id,
            brand=self.entries["Brand"].get(),
            model=self.entries["Model"].get(),
            serial_no=None,
            invoice_no=None,
            item_amount=float(self.entries["Item Amount"].get()),
            advance_amount=float(self.entries["Advance"].get()),
            finance_amount=self.emi_data["finance_amount"],
            interest_rate=float(self.entries["Interest"].get()),
            interest_type=self.interest_type_cb.get().upper(),
            installment_mode=self.mode_cb.get(),
            total_installments=int(self.entries["Installments"].get()),
            installment_amount=self.emi_data["installment_amount"],
            start_date=start_date
        )

        # Save Guarantors
        for g in self.guarantor_entries:
            add_guarantor(
                customer_id,
                g["name"].get(),
                g["phone"].get(),
                g["address"].get()
            )

        messagebox.showinfo("Success", "Customer, Item & Guarantor(s) added successfully")
        self.window.destroy()
