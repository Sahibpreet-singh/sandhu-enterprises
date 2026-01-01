import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from models.customer_model import get_all_customers
from models.item_model import add_item
from services.emi_calculate import calculate_emi


class ItemUI:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.emi_data = None
        self.customers = []
        self.create_form()

    # ================= FORM =================
    def create_form(self):
        form = tk.LabelFrame(
            self.frame,
            text="Add Item (EMI)",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        form.pack(fill=tk.X, padx=10, pady=10)

        # -------- Customer --------
        tk.Label(form, text="Customer", bg="white").grid(row=0, column=0, sticky="w")
        self.customer_cb = ttk.Combobox(form, width=30, state="readonly")
        self.customer_cb.grid(row=0, column=1, padx=5, pady=2)

        self.load_customers()

        # -------- Item fields --------
        labels = [
            "Brand",
            "Model",
            "Item Amount",
            "Advance",
            "Interest (%)",
            "Installments",
            "Mode"
        ]

        self.entries = {}

        for i, text in enumerate(labels, start=1):
            tk.Label(form, text=text, bg="white").grid(row=i, column=0, sticky="w")
            entry = tk.Entry(form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[text] = entry

        # -------- Mode dropdown --------
        self.entries["Mode"].destroy()
        self.mode_cb = ttk.Combobox(
            form,
            values=["MONTHLY", "WEEKLY", "DAILY"],
            state="readonly",
            width=27
        )
        self.mode_cb.grid(row=7, column=1, padx=5, pady=2)
        self.mode_cb.set("MONTHLY")

        # -------- Buttons --------
        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)

        tk.Button(
            btn_frame,
            text="Calculate EMI",
            width=15,
            command=self.calculate
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Save Item",
            width=15,
            bg="#27ae60",
            fg="white",
            command=self.save_item
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Clear",
            width=10,
            command=self.clear_form
        ).pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(
            form,
            bg="white",
            fg="green",
            font=("Arial", 11, "bold")
        )
        self.result_label.grid(row=9, column=0, columnspan=2, pady=5)

    # ================= LOAD CUSTOMERS =================
    def load_customers(self):
        self.customers = get_all_customers()
        self.customer_cb["values"] = [
            f'{c["customer_id"]} - {c["name"]}' for c in self.customers
        ]

    # ================= EMI CALCULATION =================
    def calculate(self):
        try:
            item_amount = float(self.entries["Item Amount"].get())
            advance = float(self.entries["Advance"].get())
            interest = float(self.entries["Interest (%)"].get())
            installments = int(self.entries["Installments"].get())

            if advance >= item_amount:
                raise ValueError("Advance cannot be >= item amount")

            self.emi_data = calculate_emi(
                item_amount,
                advance,
                interest,
                installments
            )

            self.result_label.config(
                text=(
                    f'Finance Amount: ₹{self.emi_data["finance_amount"]} | '
                    f'EMI: ₹{self.emi_data["installment_amount"]}'
                )
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= SAVE ITEM =================
    def save_item(self):
        if not self.emi_data:
            messagebox.showerror("Error", "Calculate EMI first")
            return

        if not self.customer_cb.get():
            messagebox.showerror("Error", "Select customer")
            return

        try:
            customer_id = int(self.customer_cb.get().split(" - ")[0])

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

            messagebox.showinfo("Success", "Item added successfully")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= CLEAR =================
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.mode_cb.set("MONTHLY")
        self.customer_cb.set("")
        self.result_label.config(text="")
        self.emi_data = None
