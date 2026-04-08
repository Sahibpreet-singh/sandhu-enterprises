import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

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
            font=("Arial", 14, "bold"),
            bg="#f5f7fa",
            fg="#2c3e50",
            padx=15,
            pady=15,
            relief="solid",
            bd=2
        )
        form.pack(fill=tk.X, padx=15, pady=15)

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
            "Interest",
            "Installments",
            "Mode",
            "Payment Date"
        ]

        self.entries = {}

        interest_row = None
        for i, text in enumerate(labels, start=1):
            tk.Label(form, text=text, bg="white").grid(row=i, column=0, sticky="w")
            entry = tk.Entry(form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[text] = entry
            if text == "Interest":
                interest_row = i

        # Interest type combobox (Percent / Amount) placed next to Interest entry
        if interest_row is None:
            interest_row = 1
        self.interest_type_cb = ttk.Combobox(form, values=["Percent", "Amount"], state="readonly", width=8)
        self.interest_type_cb.grid(row=interest_row, column=2, padx=4)
        self.interest_type_cb.set("Percent")
        # -------- Mode dropdown --------
        self.entries["Mode"].destroy()
        self.mode_cb = ttk.Combobox(
            form,
            values=["MONTHLY", "WEEKLY", "DAILY", "ONE-TIME"],
            state="readonly",
            width=27
        )
        self.mode_cb.grid(row=7, column=1, padx=5, pady=2)
        self.mode_cb.set("MONTHLY")
        self.mode_cb.bind("<<ComboboxSelected>>", self.on_mode_change)
        self.entries["Payment Date"].config(state="disabled")

        # -------- Buttons --------
        btn_frame = tk.Frame(form, bg="#f5f7fa")
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)

        tk.Button(
            btn_frame,
            text="Calculate EMI",
            width=15,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            command=self.calculate
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Save Item",
            width=15,
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            command=self.save_item
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Clear",
            width=10,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
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

    def on_mode_change(self, event=None):
        if self.mode_cb.get() == "ONE-TIME":
            self.entries["Installments"].delete(0, tk.END)
            self.entries["Installments"].insert(0, "1")
            self.entries["Installments"].config(state="disabled")
            self.entries["Payment Date"].config(state="normal")
            self.entries["Payment Date"].delete(0, tk.END)
            self.entries["Payment Date"].insert(0, date.today().strftime('%d-%m-%Y'))
        else:
            self.entries["Installments"].config(state="normal")
            self.entries["Payment Date"].delete(0, tk.END)
            self.entries["Payment Date"].config(state="disabled")

    # ================= EMI CALCULATION =================
    def calculate(self):
        try:
            item_amount = float(self.entries["Item Amount"].get())
            advance = float(self.entries["Advance"].get())
            interest = float(self.entries["Interest"].get())
            installments = int(self.entries["Installments"].get())

            if advance >= item_amount:
                raise ValueError("Advance cannot be >= item amount")

            interest_type = self.interest_type_cb.get() or 'Percent'

            self.emi_data = calculate_emi(
                item_amount,
                advance,
                interest,
                installments,
                interest_type=interest_type
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

        # Validate item fields before saving
        brand = self.entries["Brand"].get().strip()
        model = self.entries["Model"].get().strip()
        item_amount_str = self.entries["Item Amount"].get().strip()
        advance_str = self.entries["Advance"].get().strip()
        interest_str = self.entries["Interest"].get().strip()
        installments_str = self.entries["Installments"].get().strip()
        interest_type = self.interest_type_cb.get().upper()

        # Check required fields
        if not brand:
            messagebox.showerror("Validation Error", "Brand is required")
            return
        if not model:
            messagebox.showerror("Validation Error", "Model is required")
            return
        if not item_amount_str:
            messagebox.showerror("Validation Error", "Item Amount is required")
            return
        if not advance_str:
            messagebox.showerror("Validation Error", "Advance Amount is required")
            return
        if not interest_str:
            messagebox.showerror("Validation Error", "Interest Rate is required")
            return
        if not installments_str:
            messagebox.showerror("Validation Error", "Number of Installments is required")
            return
        if self.mode_cb.get() == "ONE-TIME" and not self.entries["Payment Date"].get().strip():
            messagebox.showerror("Validation Error", "Payment Date is required for ONE-TIME mode")
            return

        # Validate numeric fields
        try:
            item_amount = float(item_amount_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Item Amount must be a valid number")
            return

        try:
            advance_amount = float(advance_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Advance Amount must be a valid number")
            return

        try:
            interest_rate = float(interest_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Interest Rate must be a valid number")
            return

        try:
            total_installments = int(installments_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Number of Installments must be a valid whole number")
            return

        # Parse payment date for ONE-TIME
        payment_date_str = self.entries["Payment Date"].get().strip()
        if self.mode_cb.get() == "ONE-TIME":
            try:
                try:
                    payment_date = datetime.strptime(payment_date_str, '%d-%m-%Y').date()
                except ValueError:
                    payment_date = date.fromisoformat(payment_date_str)
            except Exception:
                messagebox.showerror("Validation Error", "Payment Date must be DD-MM-YYYY or YYYY-MM-DD")
                return
        else:
            payment_date = date.today()

        # Validate ranges and logic
        if item_amount <= 0:
            messagebox.showerror("Validation Error", "Item Amount must be greater than 0")
            return

        if advance_amount < 0:
            messagebox.showerror("Validation Error", "Advance Amount cannot be negative")
            return

        if advance_amount > item_amount:
            messagebox.showerror("Validation Error", "Advance Amount cannot exceed Item Amount")
            return

        if total_installments <= 0:
            messagebox.showerror("Validation Error", "Number of Installments must be greater than 0")
            return

        # Validate interest rate based on type
        if interest_type.startswith('P'):  # PERCENT
            if not (0 <= interest_rate <= 100):
                messagebox.showerror("Validation Error", "Interest Rate (Percent) must be between 0 and 100")
                return
        else:  # ABSOLUTE
            if interest_rate < 0:
                messagebox.showerror("Validation Error", "Interest Amount must be non-negative")
                return

        try:
            customer_id = int(self.customer_cb.get().split(" - ")[0])

            add_item(
                customer_id=customer_id,
                brand=brand,
                model=model,
                serial_no=None,
                invoice_no=None,
                item_amount=item_amount,
                advance_amount=advance_amount,
                finance_amount=self.emi_data["finance_amount"],
                interest_rate=interest_rate,
                installment_mode=self.mode_cb.get(),
                total_installments=total_installments,
                installment_amount=self.emi_data["installment_amount"],
                start_date=payment_date,
                interest_type=interest_type
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
