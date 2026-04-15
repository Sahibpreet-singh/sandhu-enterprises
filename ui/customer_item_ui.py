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
        self.window.title("NEW CASE DETAILS")
        self.window.geometry("1180x720")
        self.window.configure(bg="#eef4f7")
        self.window.resizable(False, False)

        self.num_guarantors = tk.IntVar(value=2)
        self.emi_data = None
        self.guarantor_entries = []

        self.show_full_form()

    # ================= STEP 1: Show Full Form =================
    def show_full_form(self):
        self.clear_window()

        self.window.configure(bg="#eef4f7")

        outer = tk.Frame(self.window, bg="#eef4f7", padx=18, pady=14)
        outer.pack(fill=tk.BOTH, expand=True)

        title_bar = tk.Frame(outer, bg="#dbe8ef", relief="groove", bd=1, height=26)
        title_bar.pack(fill="x", pady=(0, 12))
        title_bar.pack_propagate(False)
        tk.Label(
            title_bar,
            text="NEW CASE DETAILS",
            font=("Arial", 10, "bold"),
            bg="#dbe8ef",
            fg="#4d5b63",
            anchor="w",
            padx=10,
        ).pack(fill="both")

        content = tk.Frame(outer, bg="#eef4f7")
        content.pack(fill="both", expand=True)

        left_panel = tk.Frame(content, bg="#eef4f7")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_panel = tk.Frame(content, bg="#eef4f7", width=420)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        self.build_customer_section(left_panel)
        self.build_guarantor_section(left_panel)

        tk.Button(
            left_panel,
            text="CANCEL Esc",
            command=self.window.destroy,
            font=("Arial", 12, "bold"),
            width=14,
            bg="#dfe7dd",
            activebackground="#ced9cb",
            relief="ridge",
            bd=1,
        ).pack(side="left", padx=(140, 10), pady=(18, 0))

        tk.Button(
            left_panel,
            text="SAVE & EXIT F10",
            command=self.save_all,
            font=("Arial", 12, "bold"),
            width=14,
            bg="#dfe7dd",
            activebackground="#ced9cb",
            relief="ridge",
            bd=1,
        ).pack(side="left", pady=(18, 0))

        self.result_label = tk.Label(left_panel, text="", fg="#b03a2e", bg="#eef4f7", font=("Arial", 10, "bold"))
        self.result_label.pack(anchor="w", padx=145, pady=(8, 0))

        self.build_item_section(right_panel)

        self.load_address_village()
        self.calculate_emi()

    def build_customer_section(self, parent):
        section = tk.Frame(parent, bg="#eef4f7")
        section.pack(fill="x")

        self.case_id_var = tk.StringVar(value="36")

        row1 = tk.Frame(section, bg="#eef4f7")
        row1.pack(fill="x", pady=(8, 8))
        tk.Label(row1, text="FILE NO", font=("Arial", 10), bg="#eef4f7", width=10, anchor="w").pack(side="left")
        self.file_no_entry = tk.Entry(row1, width=16, relief="solid", bd=1)
        self.file_no_entry.pack(side="left", padx=(0, 24))
        tk.Label(row1, text="DATE", font=("Arial", 10), bg="#eef4f7", width=6, anchor="w").pack(side="left")
        self.date_entry = tk.Entry(row1, width=12, relief="solid", bd=1)
        self.date_entry.pack(side="left")
        self.date_entry.insert(0, date.today().strftime("%d-%m-%Y"))

        self.name_entry = self._build_labeled_entry(section, "ACCOUNT", width=41)
        self.phone_entry = self._build_labeled_entry(section, "W/O D/O S/O", width=41)
        self.address_cb = self._build_labeled_combobox(section, "ADDRESS", width=38)
        self.village_cb = self._build_labeled_combobox(section, "VILLAGE", width=38)
        self.mobile_no_entry = self._build_labeled_entry(section, "MOBILE NO", width=41)
        self.remarks_entry = self._build_labeled_entry(section, "REMARKS", width=41)

        self.address_full = []
        self.village_full = []

        def _filter(cb, full_list):
            val = cb.get()
            if not val:
                cb["values"] = full_list
                return
            val_l = val.strip().lower()
            matches = [s for s in full_list if val_l in s.lower()]
            cb["values"] = matches
            if matches:
                try:
                    cb.event_generate("<Down>")
                except Exception:
                    pass

        self.address_cb.bind("<KeyRelease>", lambda e: _filter(self.address_cb, self.address_full))
        self.village_cb.bind("<KeyRelease>", lambda e: _filter(self.village_cb, self.village_full))

    def build_item_section(self, parent):
        section = tk.Frame(parent, bg="#eef4f7")
        section.pack(fill="both", expand=True)

        header = tk.Frame(section, bg="#eef4f7")
        header.pack(fill="x", pady=(28, 10))
        tk.Label(header, text="ITEM PARTICULARS", font=("Arial", 14, "bold"), bg="#eef4f7", fg="#3d4950").pack(side="left", padx=(0, 16))

        photo_and_case = tk.Frame(header, bg="#eef4f7")
        photo_and_case.pack(side="right", anchor="n")

        case_row = tk.Frame(photo_and_case, bg="#eef4f7")
        case_row.pack(anchor="e", pady=(0, 4))
        tk.Label(case_row, text="CASE ID", font=("Arial", 9), bg="#eef4f7", fg="#4d5b63").pack(side="left", padx=(0, 6))
        tk.Label(case_row, textvariable=self.case_id_var, font=("Arial", 9), bg="#eef4f7", fg="#5166c2").pack(side="left")

        self.photo_canvas = tk.Canvas(photo_and_case, width=190, height=170, bg="#f8fbef", highlightthickness=1, highlightbackground="#8d9a84")
        self.photo_canvas.pack()
        self.photo_canvas.create_line(0, 0, 190, 170, fill="#b2bba9")
        self.photo_canvas.create_line(190, 0, 0, 170, fill="#b2bba9")

        form = tk.Frame(section, bg="#eef4f7")
        form.pack(fill="x", pady=(0, 10))

        self.entries = {}

        row = tk.Frame(form, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text="ITEM", font=("Arial", 10), bg="#eef4f7", width=9, anchor="w").pack(side="left")
        self.item_entry = tk.Entry(row, width=28, relief="solid", bd=1)
        self.item_entry.pack(side="left", padx=(0, 16))
        self.entries["Brand"] = self.item_entry

        row = tk.Frame(form, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text="BRAND", font=("Arial", 10), bg="#eef4f7", width=9, anchor="w").pack(side="left")
        brand_entry = tk.Entry(row, width=16, relief="solid", bd=1)
        brand_entry.pack(side="left", padx=(0, 10))
        tk.Label(row, text="MODEL", font=("Arial", 10), bg="#eef4f7", width=8, anchor="w").pack(side="left")
        model_entry = tk.Entry(row, width=14, relief="solid", bd=1)
        model_entry.pack(side="left")
        self.entries["Brand"] = brand_entry
        self.entries["Model"] = model_entry

        row = tk.Frame(form, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text="SRNO", font=("Arial", 10), bg="#eef4f7", width=9, anchor="w").pack(side="left")
        self.serial_no_entry = tk.Entry(row, width=28, relief="solid", bd=1)
        self.serial_no_entry.pack(side="left")
        self.entries["Serial No"] = self.serial_no_entry

        row = tk.Frame(form, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text="INVOICE NO.", font=("Arial", 10), bg="#eef4f7", width=9, anchor="w").pack(side="left")
        self.invoice_no_entry = tk.Entry(row, width=28, relief="solid", bd=1)
        self.invoice_no_entry.pack(side="left")
        self.entries["Invoice No"] = self.invoice_no_entry

        row = tk.Frame(form, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text="AMOUNT", font=("Arial", 10), bg="#eef4f7", width=9, anchor="w").pack(side="left")
        item_amount_entry = tk.Entry(row, width=18, relief="solid", bd=1)
        item_amount_entry.pack(side="left", padx=(0, 12))
        tk.Label(row, text="ADVANCE", font=("Arial", 10), bg="#eef4f7", width=10, anchor="w").pack(side="left")
        advance_entry = tk.Entry(row, width=12, relief="solid", bd=1)
        advance_entry.pack(side="left")
        self.entries["Item Amount"] = item_amount_entry
        self.entries["Advance"] = advance_entry

        row = tk.Frame(form, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text="AMOUNT FINANCED", font=("Arial", 10), bg="#eef4f7", width=16, anchor="w").pack(side="left")
        self.finance_amount_value = tk.Label(row, text="0.00", font=("Arial", 9), bg="#eef4f7", fg="#c0392b", width=10, anchor="w")
        self.finance_amount_value.pack(side="left", padx=(0, 10))
        tk.Label(row, text="NO. OF INSTALMENTS", font=("Arial", 10), bg="#eef4f7", width=18, anchor="w").pack(side="left")
        installments_entry = tk.Entry(row, width=8, relief="solid", bd=1)
        installments_entry.pack(side="left")
        self.entries["Installments"] = installments_entry

        row = tk.Frame(form, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text="INSTALMENT AMOUNT", font=("Arial", 10), bg="#eef4f7", width=16, anchor="w").pack(side="left")
        self.installment_amount_value = tk.Label(row, text="0.00", font=("Arial", 9), bg="#eef4f7", fg="#c0392b", width=10, anchor="w")
        self.installment_amount_value.pack(side="left", padx=(0, 10))
        tk.Label(row, text="FINAL AMOUNT", font=("Arial", 10), bg="#eef4f7", width=12, anchor="w").pack(side="left")
        self.final_amount_value = tk.Label(row, text="0.00", font=("Arial", 9), bg="#eef4f7", fg="#c0392b", width=10, anchor="w")
        self.final_amount_value.pack(side="left")

        hidden = tk.Frame(section, bg="#eef4f7")
        hidden.pack(fill="x", pady=(10, 0))

        interest_row = tk.Frame(hidden, bg="#eef4f7")
        interest_row.pack(anchor="w")
        tk.Label(interest_row, text="Interest", font=("Arial", 10), bg="#eef4f7", width=16, anchor="w").pack(side="left")
        interest_entry = tk.Entry(interest_row, width=18, relief="solid", bd=1)
        interest_entry.pack(side="left", padx=(0, 8))
        self.entries["Interest"] = interest_entry
        self.interest_type_cb = ttk.Combobox(interest_row, values=["Percent", "Amount"], state="readonly", width=10)
        self.interest_type_cb.pack(side="left")
        self.interest_type_cb.set("Amount")

        mode_row = tk.Frame(hidden, bg="#eef4f7")
        mode_row.pack(anchor="w", pady=(6, 0))
        tk.Label(mode_row, text="Mode", font=("Arial", 10), bg="#eef4f7", width=16, anchor="w").pack(side="left")
        self.mode_cb = ttk.Combobox(mode_row, values=["MONTHLY", "WEEKLY", "DAILY", "ONE-TIME"], state="readonly", width=18)
        self.mode_cb.pack(side="left", padx=(0, 8))
        self.mode_cb.set("MONTHLY")
        self.mode_cb.bind("<<ComboboxSelected>>", self.on_mode_change)

        tk.Label(mode_row, text="Payment Date", font=("Arial", 10), bg="#eef4f7", width=12, anchor="w").pack(side="left")
        payment_date_entry = tk.Entry(mode_row, width=16, relief="solid", bd=1)
        payment_date_entry.pack(side="left")
        self.entries["Payment Date"] = payment_date_entry
        self.entries["Payment Date"].config(state="disabled")

        for key in ["Item Amount", "Advance", "Interest", "Installments"]:
            self.entries[key].bind("<KeyRelease>", lambda e: self.calculate_emi())

    def build_guarantor_section(self, parent):
        wrapper = tk.Frame(parent, bg="#eef4f7")
        wrapper.pack(fill="x", pady=(18, 0))

        first = tk.Frame(wrapper, bg="#eef4f7")
        first.pack(side="left", fill="x", expand=True, padx=(0, 22))

        second = tk.Frame(wrapper, bg="#eef4f7")
        second.pack(side="left", fill="x", expand=True)

        tk.Label(first, text="FIRST GUARANTOR PARTICULARS", font=("Arial", 14, "bold"), bg="#eef4f7", fg="#3d4950").pack(anchor="w", pady=(0, 10))
        tk.Label(second, text="SECOND GUARANTOR PARTICULARS", font=("Arial", 14, "bold"), bg="#eef4f7", fg="#3d4950").pack(anchor="w", pady=(0, 10))

        self.guarantor_entries = [
            self._build_guarantor_fields(first),
            self._build_guarantor_fields(second),
        ]

    def _build_guarantor_fields(self, parent):
        name_entry = self._build_labeled_entry(parent, "NAME", width=33)
        phone_entry = self._build_labeled_entry(parent, "W/O D/O S/O", width=33)
        address_entry = self._build_labeled_entry(parent, "ADDRESS", width=33)
        village_entry = self._build_labeled_entry(parent, "VILLAGE", width=33)
        mobile_entry = self._build_labeled_entry(parent, "MOBILE NO", width=33)
        remarks_entry = self._build_labeled_entry(parent, "REMARKS", width=33)

        return {
            "name": name_entry,
            "phone": mobile_entry,
            "address": address_entry,
            "village": village_entry,
            "relation": phone_entry,
            "remarks": remarks_entry,
        }

    def _build_labeled_entry(self, parent, label, width=40):
        row = tk.Frame(parent, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label, font=("Arial", 10), bg="#eef4f7", width=12, anchor="w").pack(side="left")
        entry = tk.Entry(row, width=width, relief="solid", bd=1)
        entry.pack(side="left")
        return entry

    def _build_labeled_combobox(self, parent, label, width=38):
        row = tk.Frame(parent, bg="#eef4f7")
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label, font=("Arial", 10), bg="#eef4f7", width=12, anchor="w").pack(side="left")
        cb = ttk.Combobox(row, width=width, state="normal")
        cb.pack(side="left")
        return cb

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
            self.entries["Payment Date"].config(state="normal")
            self.entries["Payment Date"].delete(0, tk.END)
            self.entries["Payment Date"].insert(0, date.today().strftime("%d-%m-%Y"))
        else:
            self.entries["Installments"].config(state="normal")
            self.entries["Payment Date"].delete(0, tk.END)
            self.entries["Payment Date"].config(state="disabled")
        self.calculate_emi()

    # ================= EMI CALCULATION =================
    def calculate_emi(self):
        try:
            item_amount = float(self.entries["Item Amount"].get() or 0)
            advance = float(self.entries["Advance"].get() or 0)
            interest = float(self.entries["Interest"].get() or 0)
            installments = int(self.entries["Installments"].get() or 1)

            interest_type = self.interest_type_cb.get() or "Percent"

            self.emi_data = calculate_emi(item_amount, advance, interest, installments, interest_type=interest_type)
            self.result_label.config(text="")
            self.finance_amount_value.config(text=f"{self.emi_data['finance_amount']:.2f}")
            self.installment_amount_value.config(text=f"{self.emi_data['installment_amount']:.2f}")
            self.final_amount_value.config(text=f"{self.emi_data['final_amount']:.2f}")
        except Exception:
            self.emi_data = None
            if hasattr(self, "finance_amount_value"):
                self.finance_amount_value.config(text="0.00")
                self.installment_amount_value.config(text="0.00")
                self.final_amount_value.config(text="0.00")

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
            self.calculate_emi()
            if not self.emi_data:
                messagebox.showerror("Error", "Invalid item/EMI values")
                return

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

        entry_date_str = None
        entry_date_val = self.date_entry.get().strip() if hasattr(self, "date_entry") else ""
        if entry_date_val:
            try:
                try:
                    parsed_date = datetime.strptime(entry_date_val, "%d-%m-%Y")
                    entry_date_str = parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    datetime.strptime(entry_date_val, "%Y-%m-%d")
                    entry_date_str = entry_date_val
            except ValueError:
                messagebox.showerror("Error", "Entry Date must be DD-MM-YYYY or YYYY-MM-DD")
                return

        customer_name = self.name_entry.get().strip()
        customer_phone = self.mobile_no_entry.get().strip() or self.phone_entry.get().strip()

        customer_id = add_customer(
            name=customer_name,
            phone=customer_phone,
            address=address_text,
            remarks=self.remarks_entry.get(),
            address_id=address_id,
            village_id=village_id,
            entry_date=entry_date_str,
        )

        start_date = date.today()
        if entry_date_str:
            start_date = date.fromisoformat(entry_date_str)

        brand = self.entries["Brand"].get().strip()
        model = self.entries["Model"].get().strip()
        item_amount_str = self.entries["Item Amount"].get().strip()
        advance_str = self.entries["Advance"].get().strip()
        interest_str = self.entries["Interest"].get().strip()
        installments_str = self.entries["Installments"].get().strip()
        payment_date_str = self.entries["Payment Date"].get().strip()
        interest_type = self.interest_type_cb.get().upper()

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

        if self.mode_cb.get() == "ONE-TIME" and not payment_date_str:
            messagebox.showerror("Validation Error", "Payment Date is required for ONE-TIME mode")
            return

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

        start_date = date.today()
        if self.mode_cb.get() == "ONE-TIME":
            try:
                try:
                    start_date = datetime.strptime(payment_date_str, "%d-%m-%Y").date()
                except ValueError:
                    start_date = date.fromisoformat(payment_date_str)
            except Exception:
                messagebox.showerror("Validation Error", "Payment Date must be DD-MM-YYYY or YYYY-MM-DD")
                return
        elif entry_date_str:
            start_date = date.fromisoformat(entry_date_str)

        if interest_type.startswith("P"):
            if not (0 <= interest_rate <= 100):
                messagebox.showerror("Validation Error", "Interest Rate (Percent) must be between 0 and 100")
                return
        else:
            if interest_rate < 0:
                messagebox.showerror("Validation Error", "Interest Amount must be non-negative")
                return

        add_item(
            customer_id=customer_id,
            brand=brand,
            model=model,
            serial_no=self.serial_no_entry.get().strip() or None,
            invoice_no=self.invoice_no_entry.get().strip() or None,
            item_amount=item_amount,
            advance_amount=advance_amount,
            finance_amount=self.emi_data["finance_amount"],
            interest_rate=interest_rate,
            interest_type=interest_type,
            installment_mode=self.mode_cb.get(),
            total_installments=total_installments,
            installment_amount=self.emi_data["installment_amount"],
            start_date=start_date,
        )

        for g in self.guarantor_entries:
            add_guarantor(
                customer_id,
                g["name"].get(),
                g["phone"].get(),
                g["address"].get(),
            )

        messagebox.showinfo("Success", "Customer, Item & Guarantor(s) added successfully")
        self.window.destroy()
