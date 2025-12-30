import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from models.customer_model import add_customer
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
        tk.Label(form, text="Customer Information", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
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
        self.address_entry = tk.Entry(form, width=40)
        self.address_entry.grid(row=row, column=1, pady=2)
        row += 1

        tk.Label(form, text="Remarks:").grid(row=row, column=0, sticky="e")
        self.remarks_entry = tk.Entry(form, width=40)
        self.remarks_entry.grid(row=row, column=1, pady=2)
        row += 1

        # --------- ITEM / EMI INFO ---------
        tk.Label(form, text="Item / EMI Information", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        labels = ["Brand", "Model", "Item Amount", "Advance", "Interest (%)", "Installments", "Mode"]
        self.entries = {}

        for text in labels:
            tk.Label(form, text=text + ":").grid(row=row, column=0, sticky="e")
            if text == "Mode":
                self.mode_cb = ttk.Combobox(form, values=["MONTHLY", "WEEKLY"], state="readonly", width=37)
                self.mode_cb.grid(row=row, column=1, pady=2)
                self.mode_cb.set("MONTHLY")
            else:
                entry = tk.Entry(form, width=40)
                entry.grid(row=row, column=1, pady=2)
                self.entries[text] = entry
            row += 1

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
        tk.Button(form, text="Calculate EMI", command=self.calculate_emi).grid(row=row, column=0, pady=10)
        tk.Button(form, text="Save All", command=self.save_all).grid(row=row, column=1, pady=10)
        row += 1

        self.result_label = tk.Label(form, text="", fg="green")
        self.result_label.grid(row=row, column=0, columnspan=2)

    # ================= CLEAR WINDOW =================
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # ================= EMI CALCULATION =================
    def calculate_emi(self):
        try:
            item_amount = float(self.entries["Item Amount"].get())
            advance = float(self.entries["Advance"].get())
            interest = float(self.entries["Interest (%)"].get())
            installments = int(self.entries["Installments"].get())

            self.emi_data = calculate_emi(item_amount, advance, interest, installments)
            self.result_label.config(text=f"EMI Amount: ₹{self.emi_data['installment_amount']}")
        except Exception:
            messagebox.showerror("Error", "Invalid item/EMI values")

    # ================= SAVE EVERYTHING =================
    def save_all(self):
        if not self.emi_data:
            messagebox.showerror("Error", "Calculate EMI first")
            return

        # Save Customer
        customer_id = add_customer(
            name=self.name_entry.get(),
            phone=self.phone_entry.get(),
            address=self.address_entry.get(),
            remarks=self.remarks_entry.get()
        )

        # Save Item
        add_item(
            customer_id=customer_id,
            brand=self.entries["Brand"].get(),
            model=self.entries["Model"].get(),
            serial_no=None,
            invoice_no=None,
            item_amount=float(self.entries["Item Amount"].get()),
            advance_amount=float(self.entries["Advance"].get()),
            finance_amount=self.emi_data["finance_amount"],
            interest_rate=float(self.entries["Interest (%)"].get()),
            installment_mode=self.mode_cb.get(),
            total_installments=int(self.entries["Installments"].get()),
            installment_amount=self.emi_data["installment_amount"],
            start_date=date.today()
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
