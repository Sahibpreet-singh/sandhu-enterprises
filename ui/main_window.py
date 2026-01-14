import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date
from ui.login_ui import SUPERADMIN_PASSWORD

from ui.customer_item_ui import CustomerItemUI
from models.report_model import get_all_customer_items   # ← READ DATA ONLY


class MainWindow:
    
    def __init__(self, root, user):
        self.root = root
        self.user = user  # admin or superadmin

        self.root.title("Sandhu Enterprises – EMI Management System")
        
        # Maximize window
        self.root.state("zoomed")   # ← maximized on Windows
        self.root.resizable(True, True)  # allow resizing if needed

        self.create_header()
        self.create_menu()
        self.create_content_area()


    # ================= HEADER =================
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#34495e")
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="🏢 Sandhu Enterprises",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="white",
            pady=10
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="EMI Management System",
            font=("Arial", 14),
            bg="#34495e",
            fg="#bdc3c7",
            pady=10
        ).pack(side=tk.LEFT, padx=10)

        # User info
        user_text = f"👤 {self.user.get('username', 'User')}" if self.user else "👤 Guest"
        tk.Label(
            header_frame,
            text=user_text,
            font=("Arial", 10),
            bg="#34495e",
            fg="#ecf0f1",
            pady=10
        ).pack(side=tk.RIGHT, padx=20)

    # ================= LEFT MENU =================
    def create_menu(self):
        menu_frame = tk.Frame(self.root, bg="#34495e", width=220)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Menu title
        tk.Label(
            menu_frame,
            text="📋 Menu",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white",
            pady=10
        ).pack(fill=tk.X)

        buttons = [
            ("👥 Customers", self.open_customers),
            ("📊 Records", self.open_items),   # renamed logically
            ("💰 Payments", self.open_payments),
            ("➕ Record Payment", self.open_record_payment),
            ("🚪 Exit", self.root.quit)
        ]

        for text, command in buttons:
            btn = tk.Button(
                menu_frame,
                text=text,
                font=("Arial", 11, "bold"),
                width=20,
                pady=12,
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                relief="flat",
                borderwidth=0,
                command=command
            )
            btn.pack(pady=8, padx=10)
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2980b9"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#3498db"))

    # ================= MAIN CONTENT =================
    def create_content_area(self):
        self.content_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Welcome container
        welcome_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        welcome_frame.pack(expand=True)

        # Main welcome title
        tk.Label(
            welcome_frame,
            text="🏢 Welcome to Sandhu Enterprises",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f8f9fa"
        ).pack(pady=(20, 5))

        tk.Label(
            welcome_frame,
            text="EMI Management System",
            font=("Arial", 18),
            fg="#34495e",
            bg="#f8f9fa"
        ).pack(pady=(0, 20))

        # Description
        tk.Label(
            welcome_frame,
            text="Manage customers, items, payments, and installments efficiently.\nSelect an option from the menu to get started.",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#f8f9fa",
            justify="center"
        ).pack(pady=(0, 10))

        # Current Date
        from datetime import date
        current_date = date.today().strftime("%B %d, %Y")
        tk.Label(
            welcome_frame,
            text=f"Today: {current_date}",
            font=("Arial", 10, "italic"),
            fg="#34495e",
            bg="#f8f9fa"
        ).pack(pady=(0, 20))

        # Quick Actions
        actions_frame = tk.Frame(welcome_frame, bg="#f8f9fa")
        actions_frame.pack(pady=(10, 20))

        tk.Label(
            actions_frame,
            text="Quick Actions",
            font=("Arial", 14, "bold"),
            fg="#2c3e50",
            bg="#f8f9fa"
        ).pack(pady=(0, 10))

        actions = [
            ("➕ Add Customer", self.add_customer),
            ("💰 Record Payment", self.open_record_payment),
            ("📊 View Records", self.open_items),
            ("🔍 Search Payments", self.open_payments)
        ]

        for text, command in actions:
            btn = tk.Button(
                actions_frame,
                text=text,
                font=("Arial", 11, "bold"),
                width=18,
                pady=8,
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                relief="raised",
                borderwidth=2,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=10)
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2980b9"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#3498db"))

        # Quick Stats Dashboard
        stats_frame = tk.Frame(welcome_frame, bg="#f8f9fa")
        stats_frame.pack(pady=(10, 20))

        # Store stat labels for refresh
        self.stat_labels = []

        # Get stats
        try:
            from models.customer_model import get_total_customers
            from models.item_model import get_total_items
            from models.payment_model import get_total_payments, get_total_due
            total_customers = get_total_customers()
            total_items = get_total_items()
            total_payments = get_total_payments()
            total_due = get_total_due()
        except Exception:
            total_customers = total_items = total_payments = total_due = 0

        stats = [
            ("👥 Total Customers", total_customers, "#3498db"),
            ("📦 Total Items", total_items, "#e74c3c"),
            ("💰 Total Payments", f"₹{total_payments:,.0f}", "#27ae60"),
            ("📊 Total Due", f"₹{total_due:,.0f}", "#f39c12")
        ]

        for i, (label, value, color) in enumerate(stats):
            stat_card = tk.Frame(stats_frame, bg=color, bd=2, relief="raised")
            stat_card.grid(row=0, column=i, padx=10, pady=5, ipadx=20, ipady=10)

            tk.Label(
                stat_card,
                text=label,
                font=("Arial", 10, "bold"),
                fg="white",
                bg=color
            ).pack()

            value_label = tk.Label(
                stat_card,
                text=str(value),
                font=("Arial", 16, "bold"),
                fg="white",
                bg=color
            )
            value_label.pack()
            self.stat_labels.append(value_label)

        # Refresh button
        tk.Button(
            welcome_frame,
            text="🔄 Refresh Stats",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            command=self.refresh_welcome_stats
        ).pack(pady=(10, 0))

    def refresh_welcome_stats(self):
        """Refresh the stats displayed on the welcome screen."""
        try:
            from models.customer_model import get_total_customers
            from models.item_model import get_total_items
            from models.payment_model import get_total_payments, get_total_due
            total_customers = get_total_customers()
            total_items = get_total_items()
            total_payments = get_total_payments()
            total_due = get_total_due()
        except Exception:
            total_customers = total_items = total_payments = total_due = 0

        stats = [
            total_customers,
            total_items,
            f"₹{total_payments:,.0f}",
            f"₹{total_due:,.0f}"
        ]

        for i, value in enumerate(stats):
            if i < len(self.stat_labels):
                self.stat_labels[i].config(text=str(value))

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def open_record_payment(self):
        """Open a dedicated Record Payment dialog (reusable from menu or Payments view)."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Record Payment")
        dlg.geometry("700x320")

        tk.Label(dlg, text="Select Item (type to search by customer/name/address/item):").pack(pady=6)
        item_cb = ttk.Combobox(dlg, width=120, state="normal")
        item_cb.pack(pady=4)

        # load items (only those with due > 0 by default)
        from models.report_model import search_customer_items as _search_items
        rows = _search_items({"status": "Unpaid"})
        item_full = []
        item_map = {}
        for r in rows:
            # show village and address together so address is always visible
            loc_parts = [p for p in (r.get('village_name'), r.get('customer_address')) if p]
            location = " / ".join(loc_parts)
            display = f"{r.get('item_id')} - {r.get('customer_name','')} - {location} - {r.get('brand') or ''} {r.get('model') or ''} - Due: {r.get('due_amount') or 0}"
            item_full.append(display)
            item_map[display] = r
        item_cb['values'] = item_full

        def _filter_items(event=None):
            val = item_cb.get().strip().lower()
            if not val:
                item_cb['values'] = item_full
                return
            matches = [s for s in item_full if val in s.lower()]
            item_cb['values'] = matches
            if matches:
                try:
                    item_cb.event_generate('<Down>')
                except Exception:
                    pass

        item_cb.bind('<KeyRelease>', _filter_items)

        from decimal import Decimal
        due_var = tk.StringVar(value="Due: -")
        tk.Label(dlg, textvariable=due_var).pack(pady=6)

        def update_due(event=None):
            sel = item_cb.get()
            r = item_map.get(sel)
            if r:
                due_var.set(f"Due: {r.get('due_amount') or 0}")
        item_cb.bind('<<ComboboxSelected>>', update_due)

        tk.Label(dlg, text="Amount Paid (₹):").pack()
        amount_entry = tk.Entry(dlg)
        amount_entry.pack()

        tk.Label(dlg, text="Payment Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(dlg)
        date_entry.insert(0, date.today().isoformat())
        date_entry.pack()

        def save_payment():
            sel = item_cb.get()
            r = item_map.get(sel)
            if not r:
                messagebox.showerror("Error", "Please select a valid item.")
                return
            try:
                amt = Decimal(str(amount_entry.get()))
            except Exception:
                messagebox.showerror("Error", "Invalid amount.")
                return
            due = r.get('due_amount') or 0
            due_d = Decimal(str(due))
            if amt <= 0 or amt > due_d:
                messagebox.showerror("Error", f"Amount must be >0 and <= due ({due_d})")
                return
            payment_date = date_entry.get().strip()
            try:
                # basic date format check
                if payment_date:
                    from datetime import datetime as _dt
                    _dt.strptime(payment_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Payment date must be YYYY-MM-DD")
                return
            from models.payment_model import add_payment
            remaining = add_payment(r.get('item_id'), payment_date, amt, r.get('item_amount'))
            messagebox.showinfo("Success", f"Payment recorded. Remaining: {remaining}")
            dlg.destroy()
            # Refresh payments view if visible
            try:
                self.open_payments()
            except Exception:
                pass

        tk.Button(dlg, text="Save Payment", bg="#27ae60", fg="white", command=save_payment).pack(pady=10)

    # ================= CUSTOMERS =================
    def open_customers(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="Customer Management",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)

        tk.Button(
            self.content_frame,
            text="➕ Add Customer (with Item)",
            font=("Arial", 12),
            width=24,
            bg="#27ae60",
            fg="white",
            command=self.add_customer
        ).pack(pady=10)

    def add_customer(self):
        CustomerItemUI(self.root)   # correct usage

    def export_records(self, detail_map):
        # Simple export of currently loaded records to CSV
        import csv
        rows = [detail_map[iid] for iid in detail_map]
        if not rows:
            messagebox.showinfo('Export', 'No records to export')
            return
        path = 'records_export.csv'
        keys = ['customer_id','customer_name','customer_address','village_name','brand']
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['customer_id','name','address','village','brand'])
            for r in rows:
                w.writerow([r.get('customer_id'), r.get('customer_name'), r.get('customer_address'), r.get('village_name'), r.get('brand')])
        messagebox.showinfo('Export', f'Exported {len(rows)} records to {path}')

    # ================= RECORDS (OLD ITEMS) =================
    def open_items(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="Customer & Item Report",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)

        # Sorting function (works for string and numeric columns)
        def sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            try:
                l.sort(key=lambda t: float(t[0]) if t[0] else 0, reverse=reverse)
            except Exception:
                l.sort(key=lambda t: (t[0] or "").lower(), reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda: sort_column(tv, col, not reverse))

        # Toolbar and table container
        toolbar = tk.Frame(self.content_frame, bg="#ffffff")
        toolbar.pack(fill=tk.X, padx=10, pady=(5, 0))
        tk.Button(toolbar, text="🔄 Refresh", command=lambda: populate(get_all_customer_items()), bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=6)
        tk.Button(toolbar, text="📤 Export CSV", command=lambda: self.export_records(detail_map), bg="#3498db", fg="white").pack(side=tk.LEFT)

        # Frame for table and scrollbars
        table_frame = tk.Frame(self.content_frame, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Simplified columns for Records view (Excel-like appearance)
        columns = ["Customer ID", "Name", "Address", "Village", "Brand"]

        # Use clam theme for better styling on Windows
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure("Custom.Treeview", font=("Segoe UI", 10), rowheight=26, background="#ffffff", fieldbackground="#ffffff")
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#eef3fb")
        style.map('Custom.Treeview', background=[('selected', '#cce5ff')])

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Custom.Treeview", selectmode="browse")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=vsb.set)

        # Horizontal scrollbar
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=hsb.set)

        # Set column headings, widths and add sorting
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            if col in ("Address", "Name"):
                tree.column(col, width=300, anchor="w")
            else:
                tree.column(col, width=140, anchor="center")

        # Make mouse-wheel scroll the tree when hovered
        def _on_mousewheel(event):
            # Windows and Mac
            if hasattr(event, 'delta') and event.delta:
                tree.yview_scroll(int(-1 * (event.delta / 120)), 'units')
            else:
                # Linux (Button-4/5)
                if event.num == 4:
                    tree.yview_scroll(-1, 'units')
                elif event.num == 5:
                    tree.yview_scroll(1, 'units')

        def _bind_scroll(e):
            tree.bind_all('<MouseWheel>', _on_mousewheel)
            tree.bind_all('<Button-4>', _on_mousewheel)
            tree.bind_all('<Button-5>', _on_mousewheel)

        def _unbind_scroll(e):
            tree.unbind_all('<MouseWheel>')
            tree.unbind_all('<Button-4>')
            tree.unbind_all('<Button-5>')

        tree.bind('<Enter>', _bind_scroll)
        tree.bind('<Leave>', _unbind_scroll)

        # helper to populate tree and keep a map for details
        detail_map = {}

        # Configure simple zebra striping tags
        tree.tag_configure('odd', background='#ffffff')
        tree.tag_configure('even', background='#f6f6f6')

        def populate(rows):
            # clear
            for i in tree.get_children():
                tree.delete(i)
            detail_map.clear()

            for idx, row in enumerate(rows):
                vals = [
                    row.get("customer_id") or "",
                    row.get("customer_name") or "",
                    row.get("customer_address") or "",
                    row.get("village_name") or "",
                    row.get("brand") or ""
                ]
                tag = 'even' if idx % 2 == 0 else 'odd'
                iid = tree.insert("", "end", values=vals, tags=(tag,))
                detail_map[iid] = row

        # Double-click opens a scrollable, styled details popup
        def on_double_click(event):
            item = tree.focus()
            if not item:
                return
            data = detail_map.get(item)
            if not data:
                return

            dlg = tk.Toplevel(self.content_frame)
            dlg.title(f"Customer {data.get('customer_id')} Details")
            dlg.geometry("720x520")
            dlg.transient(self.root)
            dlg.grab_set()
            dlg.resizable(True, True)

            # Header
            header = tk.Frame(dlg, bg="#f5f7fa")
            header.pack(fill=tk.X)
            tk.Label(header, text=str(data.get("customer_name") or ""), font=("Segoe UI", 14, "bold"), bg="#f5f7fa").pack(anchor="w", padx=12, pady=(8, 0))
            tk.Label(header, text=f"ID: {data.get('customer_id') or ''}    •    Entry Date: {data.get('entry_date') or ''}", font=("Segoe UI", 9), bg="#f5f7fa").pack(anchor="w", padx=12, pady=(0, 8))

            # Scrollable area
            container = tk.Frame(dlg)
            container.pack(fill=tk.BOTH, expand=True)

            canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0, bg="#ffffff")
            vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            canvas.configure(yscrollcommand=vsb.set)

            inner = tk.Frame(canvas, bg="#ffffff")
            canvas.create_window((0, 0), window=inner, anchor="nw")

            def _on_frame_config(e):
                canvas.configure(scrollregion=canvas.bbox("all"))
            inner.bind('<Configure>', _on_frame_config)

            # Mouse-wheel scrolling for the canvas
            def _on_mousewheel(e):
                if hasattr(e, 'delta') and e.delta:
                    canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units')
                else:
                    if getattr(e, 'num', None) == 4:
                        canvas.yview_scroll(-1, 'units')
                    elif getattr(e, 'num', None) == 5:
                        canvas.yview_scroll(1, 'units')

            def _bind_canvas_scroll(ev):
                canvas.bind_all('<MouseWheel>', _on_mousewheel)
                canvas.bind_all('<Button-4>', _on_mousewheel)
                canvas.bind_all('<Button-5>', _on_mousewheel)

            def _unbind_canvas_scroll(ev):
                canvas.unbind_all('<MouseWheel>')
                canvas.unbind_all('<Button-4>')
                canvas.unbind_all('<Button-5>')

            inner.bind('<Enter>', _bind_canvas_scroll)
            inner.bind('<Leave>', _unbind_canvas_scroll)

            fields = [
                ("Customer ID", data.get("customer_id")),
                ("Name", data.get("customer_name")),
                ("Phone", data.get("customer_phone")),
                ("Address", data.get("customer_address")),
                ("Village", data.get("village_name")),
                ("Remarks", data.get("customer_remarks")),
                ("Entry Date", data.get("entry_date")),
                ("Brand", data.get("brand")),
                ("Model", data.get("model")),
                ("Item Amount", data.get("item_amount")),
                ("Advance", data.get("advance_amount")),
                ("Finance", data.get("finance_amount")),
                ("Interest (%)", (f"{data.get('interest_rate')}%" if ((data.get('interest_type','PERCENT') or '').upper().startswith('P')) else f"{data.get('interest_rate')} (amt)")),
                ("Interest Type", (data.get('interest_type') or '').upper()),

                ("Installment Amount", data.get("installment_amount")),
                ("Installment Mode", data.get("installment_mode")),
                ("Total Installments", data.get("total_installments")),
                ("Guarantor Name", data.get("guarantor_name")),
                ("Guarantor Phone", data.get("guarantor_phone")),
                ("Guarantor Address", data.get("guarantor_address"))
            ]

            # Render fields in a side-by-side two-column layout with separators to mimic cells
            # Split fields roughly in half so they display left/right to reduce vertical scrolling
            half = (len(fields) + 1) // 2
            left_fields = fields[:half]
            right_fields = fields[half:]

            # Make columns 1 and 3 expandable
            inner.grid_columnconfigure(1, weight=1)
            inner.grid_columnconfigure(3, weight=1)

            # Prepare interest values: show either percent or amount in separate fields
            interest_val = data.get('interest_rate')
            interest_type = (data.get('interest_type') or '').upper()
            interest_percent = f"{interest_val}%" if interest_val is not None and interest_type.startswith('P') else ""
            interest_amount = f"{interest_val}" if interest_val is not None and not interest_type.startswith('P') else ""

            # Sections: Customer, Item/Financial, Guarantor
            sections = [
                ("Customer Details", [
                    ("Customer ID", data.get("customer_id")),
                    ("Name", data.get("customer_name")),
                    ("Phone", data.get("customer_phone")),
                    ("Address", data.get("customer_address")),
                    ("Village", data.get("village_name")),
                    ("Remarks", data.get("customer_remarks")),
                    ("Entry Date", data.get("entry_date")),
                ]),
                ("Item / Financial", [
                    ("Brand", data.get("brand")),
                    ("Model", data.get("model")),
                    ("Item Amount", data.get("item_amount")),
                    ("Advance", data.get("advance_amount")),
                    ("Finance", data.get("finance_amount")),
                    ("Interest (Percent)", interest_percent),
                    ("Interest (Amount)", interest_amount),
                    ("Interest Type", (data.get('interest_type') or '').upper()),
                    ("Installment Amount", data.get("installment_amount")),
                    ("Installment Mode", data.get("installment_mode")),
                    ("Total Installments", data.get("total_installments")),
                ]),
                ("Guarantor", [
                    ("Guarantor Name", data.get("guarantor_name")),
                    ("Guarantor Phone", data.get("guarantor_phone")),
                    ("Guarantor Address", data.get("guarantor_address")),
                ])
            ]

            labels_map = {}
            current_row = 0

            for sec_title, sec_fields in sections:
                # Section header
                tk.Label(inner, text=sec_title, font=("Segoe UI", 11, "bold"), bg="#ffffff").grid(row=current_row, column=0, columnspan=4, sticky="w", padx=12, pady=(12,6))
                current_row += 1

                # split fields for two-column layout inside this section
                half = (len(sec_fields) + 1) // 2
                left_fields = sec_fields[:half]
                right_fields = sec_fields[half:]

                rows_sec = max(len(left_fields), len(right_fields))
                for i in range(rows_sec):
                    # Left column
                    if i < len(left_fields):
                        label_l, val_l = left_fields[i]
                        tk.Label(inner, text=f"{label_l}:", anchor="e", width=18, font=("Segoe UI", 10, "bold"), bg="#ffffff").grid(row=current_row, column=0, sticky="e", padx=12, pady=(8,2))
                        val_lbl_l = tk.Label(inner, text=str(val_l) if val_l is not None else "", anchor="w", justify="left", wraplength=320, font=("Segoe UI", 10), bg="#ffffff", bd=1, relief="groove")
                        val_lbl_l.grid(row=current_row, column=1, sticky="we", padx=6, pady=(8,2))
                        labels_map[label_l] = val_lbl_l
                    else:
                        tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=0)
                        tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=1)

                    # Right column
                    if i < len(right_fields):
                        label_r, val_r = right_fields[i]
                        tk.Label(inner, text=f"{label_r}:", anchor="e", width=18, font=("Segoe UI", 10, "bold"), bg="#ffffff").grid(row=current_row, column=2, sticky="e", padx=12, pady=(8,2))
                        val_lbl_r = tk.Label(inner, text=str(val_r) if val_r is not None else "", anchor="w", justify="left", wraplength=320, font=("Segoe UI", 10), bg="#ffffff", bd=1, relief="groove")
                        val_lbl_r.grid(row=current_row, column=3, sticky="we", padx=6, pady=(8,2))
                        labels_map[label_r] = val_lbl_r
                    else:
                        tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=2)
                        tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=3)

                    current_row += 1

                # solid separator line for the section
                sep = tk.Frame(inner, height=2, bg="#2c3e50")
                sep.grid(row=current_row, column=0, columnspan=4, sticky="we", padx=8, pady=(8,0))
                current_row += 1

            # Payment history section
            tk.Label(inner, text="Payment History", font=("Segoe UI", 12, "bold"), bg="#ffffff").grid(row=current_row, column=0, columnspan=4, sticky="w", padx=12, pady=(12,4))
            current_row += 1

            payments = []
            item_id = data.get('item_id')
            if item_id:
                try:
                    from models.payment_model import get_payments_by_item
                    payments = get_payments_by_item(item_id)
                except Exception:
                    payments = []

            if payments:
                ph_cols = ["Date", "Amount Paid", "Remaining"]
                ph_tree = ttk.Treeview(inner, columns=ph_cols, show="headings", height=6)
                for pc in ph_cols:
                    ph_tree.heading(pc, text=pc)
                    ph_tree.column(pc, width=140, anchor="center")
                ph_tree.grid(row=current_row, column=0, columnspan=4, sticky="we", padx=12, pady=(4,12))
                for p in payments:
                    ph_tree.insert("", "end", values=[p.get('payment_date'), p.get('amount_paid'), p.get('remaining_amount')])
                current_row += 1
            else:
                tk.Label(inner, text="No payment history.", fg="#666", bg="#ffffff").grid(row=current_row, column=0, columnspan=4, sticky="w", padx=12, pady=(4,12))
                current_row += 1

            # -- Edit flow: open modal to edit basic customer fields
            def open_edit_dialog():
                from models.customer_model import get_customer_by_id, update_customer
                from models.address_model import get_all_addresses, add_address
                from models.village_model import get_all_villages, add_village

                customer_id = data.get('customer_id')
                if not customer_id:
                    messagebox.showerror("Error", "Cannot edit: missing customer id")
                    return

                edit = tk.Toplevel(dlg)
                edit.title(f"Edit Customer {customer_id}")
                edit.transient(dlg)
                edit.grab_set()
                edit.resizable(False, False)

                # Form
                tk.Label(edit, text="Name:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
                name_e = tk.Entry(edit, width=40)
                name_e.grid(row=0, column=1, padx=8, pady=6)
                name_e.insert(0, data.get('customer_name') or "")

                tk.Label(edit, text="Phone:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
                phone_e = tk.Entry(edit, width=40)
                phone_e.grid(row=1, column=1, padx=8, pady=6)
                phone_e.insert(0, data.get('customer_phone') or "")

                tk.Label(edit, text="Address:").grid(row=2, column=0, padx=8, pady=6, sticky="e")
                addresses = get_all_addresses()
                address_list = [f"{a['address_id']} - {a['address']}" for a in addresses]
                address_cb = ttk.Combobox(edit, values=address_list, width=38, state="normal")
                address_cb.grid(row=2, column=1, padx=8, pady=6)
                # set current value (prefer address_id if available)
                if data.get('address_id'):
                    current_addr = next((f"{a['address_id']} - {a['address']}" for a in addresses if a['address_id'] == data.get('address_id')), None)
                    if current_addr:
                        address_cb.set(current_addr)
                else:
                    address_cb.set(data.get('customer_address') or "")

                tk.Label(edit, text="Village:").grid(row=3, column=0, padx=8, pady=6, sticky="e")
                villages = get_all_villages()
                village_list = [f"{v['village_id']} - {v['name']}" for v in villages]
                village_cb = ttk.Combobox(edit, values=village_list, width=38, state="normal")
                village_cb.grid(row=3, column=1, padx=8, pady=6)
                if data.get('village_id'):
                    current_vill = next((f"{v['village_id']} - {v['name']}" for v in villages if v['village_id'] == data.get('village_id')), None)
                    if current_vill:
                        village_cb.set(current_vill)
                else:
                    village_cb.set(data.get('village_name') or "")

                tk.Label(edit, text="Remarks:").grid(row=4, column=0, padx=8, pady=6, sticky="e")
                remarks_e = tk.Entry(edit, width=40)
                remarks_e.grid(row=4, column=1, padx=8, pady=6)
                remarks_e.insert(0, data.get('customer_remarks') or "")

                tk.Label(edit, text="Entry Date (YYYY-MM-DD):").grid(row=5, column=0, padx=8, pady=6, sticky="e")
                entry_date_e = tk.Entry(edit, width=40)
                entry_date_e.grid(row=5, column=1, padx=8, pady=6)
                entry_date_e.insert(0, data.get('entry_date') or "")

                # Buttons
                btn_frame = tk.Frame(edit)
                btn_frame.grid(row=6, column=0, columnspan=2, pady=(6,8))

                def on_save():
                    name = name_e.get().strip()
                    if not name:
                        messagebox.showerror("Error", "Name is required")
                        return
                    phone = phone_e.get().strip()

                    # Address handling: if the user selected or typed an id - text pair, parse id
                    address_val = address_cb.get().strip()
                    address_id = None
                    address_text = None
                    if address_val:
                        if " - " in address_val:
                            try:
                                address_id = int(address_val.split(" - ", 1)[0])
                                address_text = address_val.split(" - ", 1)[1]
                            except Exception:
                                address_id = None
                                address_text = address_val
                        else:
                            # create new address
                            try:
                                address_id = add_address(address_val)
                                address_text = address_val
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to add address: {e}")
                                return

                    # Village handling similarly
                    village_val = village_cb.get().strip()
                    village_id = None
                    if village_val:
                        if " - " in village_val:
                            try:
                                village_id = int(village_val.split(" - ", 1)[0])
                            except Exception:
                                village_id = None
                        else:
                            try:
                                village_id = add_village(village_val)
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to add village: {e}")
                                return

                    remarks = remarks_e.get().strip() or None
                    entry_date = entry_date_e.get().strip() or None

                    try:
                        update_customer(customer_id, name, phone, address_text, remarks, address_id, village_id, entry_date)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                        return

                    # Refresh local data and UI
                    new_data = get_customer_by_id(customer_id)
                    if new_data:
                        data.update(new_data)

                    # Update displayed labels for changed fields
                    labels_map.get('Name').config(text=str(data.get('customer_name') or ""))
                    labels_map.get('Phone').config(text=str(data.get('customer_phone') or ""))
                    labels_map.get('Address').config(text=str(data.get('customer_address') or ""))
                    labels_map.get('Village').config(text=str(data.get('village_name') or ""))
                    labels_map.get('Remarks').config(text=str(data.get('customer_remarks') or ""))
                    labels_map.get('Entry Date').config(text=str(data.get('entry_date') or ""))

                    # Refresh the main table
                    rows = get_all_customer_items()
                    populate(rows)

                    edit.destroy()
                    messagebox.showinfo("Success", "Customer updated successfully")

                tk.Button(btn_frame, text="Save", command=on_save, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=6)
                tk.Button(btn_frame, text="Cancel", command=edit.destroy).pack(side=tk.LEFT, padx=6)

            # Bottom action bar with Close
            action_bar = tk.Frame(dlg, bg="#ffffff")
            action_bar.pack(fill=tk.X)
            tk.Button(action_bar, text="Close", command=dlg.destroy, bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)
            tk.Button(action_bar, text="Edit", command=open_edit_dialog, bg="#3498db", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)
            tk.Button(action_bar, text="Installment Details", command=lambda: self.show_installment_details(data.get('item_id'), dlg), bg="#8e44ad", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)

            # Permanent delete (superadmin only)
            customer_id = data.get('customer_id')
            def on_permanent_delete():
                # Prompt for superadmin password (hidden)
                pwd = simpledialog.askstring("Superadmin Password", "Enter superadmin password to permanently delete customer:", show="*")
                if pwd is None:
                    return
                if pwd != SUPERADMIN_PASSWORD:
                    messagebox.showerror("Error", "Incorrect superadmin password")
                    return

                if not messagebox.askyesno("Confirm Deletion", "Permanently delete this customer and all related records? This action cannot be undone."):
                    return

                try:
                    from models.customer_model import delete_customer
                    delete_customer(customer_id)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete customer: {e}")
                    return

                # Refresh main table and close dialog
                rows = get_all_customer_items()
                populate(rows)
                dlg.destroy()
                messagebox.showinfo("Success", "Customer permanently deleted")

            if self.user and (self.user.get('role') or '').lower() == 'superadmin':
                tk.Button(action_bar, text="Delete (Permanent)", command=on_permanent_delete, bg="#c0392b", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)

            # Close on Escape
            dlg.bind('<Escape>', lambda e: dlg.destroy())

        tree.bind("<Double-1>", on_double_click)

        # Fetch data and populate
        rows = get_all_customer_items()
        populate(rows)

        # Initial load
        # Note: records intentionally show a simplified list; double-click a row to open full details
        # Populate with all rows initially
        rows = get_all_customer_items()
        populate(rows)

        # Initial load
        # Note: records intentionally show a simplified list; double-click a row to open full details
        # Populate with all rows initially
        rows = get_all_customer_items()
        populate(rows)





    def show_customer_details(self, data, parent=None):
        """Show the customer/item detail dialog (used by Records and Payments)."""
        dlg = tk.Toplevel(parent or self.root)
        dlg.title(f"Customer {data.get('customer_id')} Details")
        dlg.geometry("720x520")
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.resizable(True, True)

        # Header
        header = tk.Frame(dlg, bg="#f5f7fa")
        header.pack(fill=tk.X)
        tk.Label(header, text=str(data.get("customer_name") or ""), font=("Segoe UI", 14, "bold"), bg="#f5f7fa").pack(anchor="w", padx=12, pady=(8, 0))
        tk.Label(header, text=f"ID: {data.get('customer_id') or ''}    •    Entry Date: {data.get('entry_date') or ''}", font=("Segoe UI", 9), bg="#f5f7fa").pack(anchor="w", padx=12, pady=(0, 8))

        # Scrollable area
        container = tk.Frame(dlg)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0, bg="#ffffff")
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=vsb.set)

        inner = tk.Frame(canvas, bg="#ffffff")
        canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_frame_config(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind('<Configure>', _on_frame_config)

        # Mouse-wheel scrolling for the canvas
        def _on_mousewheel(e):
            if hasattr(e, 'delta') and e.delta:
                canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units')
            else:
                if getattr(e, 'num', None) == 4:
                    canvas.yview_scroll(-1, 'units')
                elif getattr(e, 'num', None) == 5:
                    canvas.yview_scroll(1, 'units')

        def _bind_canvas_scroll(ev):
            canvas.bind_all('<MouseWheel>', _on_mousewheel)
            canvas.bind_all('<Button-4>', _on_mousewheel)
            canvas.bind_all('<Button-5>', _on_mousewheel)

        def _unbind_canvas_scroll(ev):
            canvas.unbind_all('<MouseWheel>')
            canvas.unbind_all('<Button-4>')
            canvas.unbind_all('<Button-5>')

        inner.bind('<Enter>', _bind_canvas_scroll)
        inner.bind('<Leave>', _unbind_canvas_scroll)

        fields = [
            ("Customer ID", data.get("customer_id")),
            ("Name", data.get("customer_name")),
            ("Phone", data.get("customer_phone")),
            ("Address", data.get("customer_address")),
            ("Village", data.get("village_name")),
            ("Remarks", data.get("customer_remarks")),
            ("Entry Date", data.get("entry_date")),
            ("Brand", data.get("brand")),
            ("Model", data.get("model")),
            ("Item Amount", data.get("item_amount")),
            ("Advance", data.get("advance_amount")),
            ("Finance", data.get("finance_amount")),
            ("Interest (%)", (f"{data.get('interest_rate')}%" if ((data.get('interest_type','PERCENT') or '').upper().startswith('P')) else f"{data.get('interest_rate')} (amt)")),
            ("Interest Type", (data.get('interest_type') or '').upper()),

            ("Installment Amount", data.get("installment_amount")),
            ("Installment Mode", data.get("installment_mode")),
            ("Total Installments", data.get("total_installments")),
            ("Guarantor Name", data.get("guarantor_name")),
            ("Guarantor Phone", data.get("guarantor_phone")),
            ("Guarantor Address", data.get("guarantor_address"))
        ]

        # Render fields in a side-by-side two-column layout with separators to mimic cells
        # Split fields roughly in half so they display left/right to reduce vertical scrolling
        half = (len(fields) + 1) // 2
        left_fields = fields[:half]
        right_fields = fields[half:]

        # Make columns 1 and 3 expandable
        inner.grid_columnconfigure(1, weight=1)
        inner.grid_columnconfigure(3, weight=1)

        # Prepare interest values: show either percent or amount in separate fields
        interest_val = data.get('interest_rate')
        interest_type = (data.get('interest_type') or '').upper()
        interest_percent = f"{interest_val}%" if interest_val is not None and interest_type.startswith('P') else ""
        interest_amount = f"{interest_val}" if interest_val is not None and not interest_type.startswith('P') else ""

        # Sections: Customer, Item/Financial, Guarantor
        sections = [
            ("Customer Details", [
                ("Customer ID", data.get("customer_id")),
                ("Name", data.get("customer_name")),
                ("Phone", data.get("customer_phone")),
                ("Address", data.get("customer_address")),
                ("Village", data.get("village_name")),
                ("Remarks", data.get("customer_remarks")),
                ("Entry Date", data.get("entry_date")),
            ]),
            ("Item / Financial", [
                ("Brand", data.get("brand")),
                ("Model", data.get("model")),
                ("Item Amount", data.get("item_amount")),
                ("Advance", data.get("advance_amount")),
                ("Finance", data.get("finance_amount")),
                ("Interest (Percent)", interest_percent),
                ("Interest (Amount)", interest_amount),
                ("Interest Type", (data.get('interest_type') or '').upper()),
                ("Installment Amount", data.get("installment_amount")),
                ("Installment Mode", data.get("installment_mode")),
                ("Total Installments", data.get("total_installments")),
            ]),
            ("Guarantor", [
                ("Guarantor Name", data.get("guarantor_name")),
                ("Guarantor Phone", data.get("guarantor_phone")),
                ("Guarantor Address", data.get("guarantor_address")),
            ]),
        ]

        labels_map = {}
        current_row = 0

        for sec_title, sec_fields in sections:
            # Section header
            tk.Label(inner, text=sec_title, font=("Segoe UI", 11, "bold"), bg="#ffffff").grid(row=current_row, column=0, columnspan=4, sticky="w", padx=12, pady=(12,6))
            current_row += 1

            # split fields for two-column layout inside this section
            half = (len(sec_fields) + 1) // 2
            left_fields = sec_fields[:half]
            right_fields = sec_fields[half:]

            rows_sec = max(len(left_fields), len(right_fields))
            for i in range(rows_sec):
                # Left column
                if i < len(left_fields):
                    label_l, val_l = left_fields[i]
                    tk.Label(inner, text=f"{label_l}:", anchor="e", width=18, font=("Segoe UI", 10, "bold"), bg="#ffffff").grid(row=current_row, column=0, sticky="e", padx=12, pady=(8,2))
                    val_lbl_l = tk.Label(inner, text=str(val_l) if val_l is not None else "", anchor="w", justify="left", wraplength=320, font=("Segoe UI", 10), bg="#ffffff", bd=1, relief="groove")
                    val_lbl_l.grid(row=current_row, column=1, sticky="we", padx=6, pady=(8,2))
                    labels_map[label_l] = val_lbl_l
                else:
                    tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=0)
                    tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=1)

                # Right column
                if i < len(right_fields):
                    label_r, val_r = right_fields[i]
                    tk.Label(inner, text=f"{label_r}:", anchor="e", width=18, font=("Segoe UI", 10, "bold"), bg="#ffffff").grid(row=current_row, column=2, sticky="e", padx=12, pady=(8,2))
                    val_lbl_r = tk.Label(inner, text=str(val_r) if val_r is not None else "", anchor="w", justify="left", wraplength=320, font=("Segoe UI", 10), bg="#ffffff", bd=1, relief="groove")
                    val_lbl_r.grid(row=current_row, column=3, sticky="we", padx=6, pady=(8,2))
                    labels_map[label_r] = val_lbl_r
                else:
                    tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=2)
                    tk.Label(inner, text="", bg="#ffffff").grid(row=current_row, column=3)

                current_row += 1

            # solid separator line for the section
            sep = tk.Frame(inner, height=2, bg="#2c3e50")
            sep.grid(row=current_row, column=0, columnspan=4, sticky="we", padx=8, pady=(8,0))
            current_row += 1

        # Payment history section
        tk.Label(inner, text="Payment History", font=("Segoe UI", 12, "bold"), bg="#ffffff").grid(row=current_row, column=0, columnspan=4, sticky="w", padx=12, pady=(12,4))
        current_row += 1

        payments = []
        item_id = data.get('item_id')
        if item_id:
            try:
                from models.payment_model import get_payments_by_item
                payments = get_payments_by_item(item_id)
            except Exception:
                payments = []

        if payments:
            ph_cols = ["Date", "Amount Paid", "Remaining"]
            ph_tree = ttk.Treeview(inner, columns=ph_cols, show="headings", height=6)
            for pc in ph_cols:
                ph_tree.heading(pc, text=pc)
                ph_tree.column(pc, width=140, anchor="center")
            ph_tree.grid(row=current_row, column=0, columnspan=4, sticky="we", padx=12, pady=(4,12))
            for p in payments:
                ph_tree.insert("", "end", values=[p.get('payment_date'), p.get('amount_paid'), p.get('remaining_amount')])
            current_row += 1
        else:
            tk.Label(inner, text="No payment history.", fg="#666", bg="#ffffff").grid(row=current_row, column=0, columnspan=4, sticky="w", padx=12, pady=(4,12))
            current_row += 1

        # -- Edit flow: open modal to edit basic customer fields
        def open_edit_dialog():
            from models.customer_model import get_customer_by_id, update_customer
            from models.address_model import get_all_addresses, add_address
            from models.village_model import get_all_villages, add_village

            customer_id = data.get('customer_id')
            if not customer_id:
                messagebox.showerror("Error", "Cannot edit: missing customer id")
                return

            edit = tk.Toplevel(dlg)
            edit.title(f"Edit Customer {customer_id}")
            edit.transient(dlg)
            edit.grab_set()
            edit.resizable(False, False)

            # Form
            tk.Label(edit, text="Name:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
            name_e = tk.Entry(edit, width=40)
            name_e.grid(row=0, column=1, padx=8, pady=6)
            name_e.insert(0, data.get('customer_name') or "")

            tk.Label(edit, text="Phone:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
            phone_e = tk.Entry(edit, width=40)
            phone_e.grid(row=1, column=1, padx=8, pady=6)
            phone_e.insert(0, data.get('customer_phone') or "")

            tk.Label(edit, text="Address:").grid(row=2, column=0, padx=8, pady=6, sticky="e")
            addresses = get_all_addresses()
            address_list = [f"{a['address_id']} - {a['address']}" for a in addresses]
            address_cb = ttk.Combobox(edit, values=address_list, width=38, state="normal")
            address_cb.grid(row=2, column=1, padx=8, pady=6)
            # set current value (prefer address_id if available)
            if data.get('address_id'):
                current_addr = next((f"{a['address_id']} - {a['address']}" for a in addresses if a['address_id'] == data.get('address_id')), None)
                if current_addr:
                    address_cb.set(current_addr)
            else:
                address_cb.set(data.get('customer_address') or "")

            tk.Label(edit, text="Village:").grid(row=3, column=0, padx=8, pady=6, sticky="e")
            villages = get_all_villages()
            village_list = [f"{v['village_id']} - {v['name']}" for v in villages]
            village_cb = ttk.Combobox(edit, values=village_list, width=38, state="normal")
            village_cb.grid(row=3, column=1, padx=8, pady=6)
            if data.get('village_id'):
                current_vill = next((f"{v['village_id']} - {v['name']}" for v in villages if v['village_id'] == data.get('village_id')), None)
                if current_vill:
                    village_cb.set(current_vill)
            else:
                village_cb.set(data.get('village_name') or "")

            tk.Label(edit, text="Remarks:").grid(row=4, column=0, padx=8, pady=6, sticky="e")
            remarks_e = tk.Entry(edit, width=40)
            remarks_e.grid(row=4, column=1, padx=8, pady=6)
            remarks_e.insert(0, data.get('customer_remarks') or "")

            tk.Label(edit, text="Entry Date (YYYY-MM-DD):").grid(row=5, column=0, padx=8, pady=6, sticky="e")
            entry_date_e = tk.Entry(edit, width=40)
            entry_date_e.grid(row=5, column=1, padx=8, pady=6)
            entry_date_e.insert(0, data.get('entry_date') or "")

            # Buttons
            btn_frame = tk.Frame(edit)
            btn_frame.grid(row=6, column=0, columnspan=2, pady=(6,8))

            def on_save():
                name = name_e.get().strip()
                if not name:
                    messagebox.showerror("Error", "Name is required")
                    return
                phone = phone_e.get().strip()

                # Address handling: if the user selected or typed an id - text pair, parse id
                address_val = address_cb.get().strip()
                address_id = None
                address_text = None
                if address_val:
                    if " - " in address_val:
                        try:
                            address_id = int(address_val.split(" - ", 1)[0])
                            address_text = address_val.split(" - ", 1)[1]
                        except Exception:
                            address_id = None
                            address_text = address_val
                    else:
                        # create new address
                        try:
                            address_id = add_address(address_val)
                            address_text = address_val
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to add address: {e}")
                            return

                # Village handling similarly
                village_val = village_cb.get().strip()
                village_id = None
                if village_val:
                    if " - " in village_val:
                        try:
                            village_id = int(village_val.split(" - ", 1)[0])
                        except Exception:
                            village_id = None
                    else:
                        try:
                            village_id = add_village(village_val)
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to add village: {e}")
                            return

                remarks = remarks_e.get().strip() or None
                entry_date = entry_date_e.get().strip() or None

                try:
                    update_customer(customer_id, name, phone, address_text, remarks, address_id, village_id, entry_date)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return

                # Refresh local data and UI
                new_data = get_customer_by_id(customer_id)
                if new_data:
                    data.update(new_data)

                # Update displayed labels for changed fields
                labels_map.get('Name').config(text=str(data.get('customer_name') or ""))
                labels_map.get('Phone').config(text=str(data.get('customer_phone') or ""))
                labels_map.get('Address').config(text=str(data.get('customer_address') or ""))
                labels_map.get('Village').config(text=str(data.get('village_name') or ""))
                labels_map.get('Remarks').config(text=str(data.get('customer_remarks') or ""))
                labels_map.get('Entry Date').config(text=str(data.get('entry_date') or ""))

                # Refresh the main table
                rows = get_all_customer_items()
                populate(rows)

                edit.destroy()
                messagebox.showinfo("Success", "Customer updated successfully")

            tk.Button(btn_frame, text="Save", command=on_save, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=6)
            tk.Button(btn_frame, text="Cancel", command=edit.destroy).pack(side=tk.LEFT, padx=6)

        # Bottom action bar with Close
        action_bar = tk.Frame(dlg, bg="#ffffff")
        action_bar.pack(fill=tk.X)
        tk.Button(action_bar, text="Close", command=dlg.destroy, bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)
        tk.Button(action_bar, text="Edit", command=open_edit_dialog, bg="#3498db", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)
        tk.Button(action_bar, text="Installment Details", command=lambda: self.show_installment_details(data.get('item_id'), dlg), bg="#8e44ad", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)

        # Permanent delete (superadmin only)
        customer_id = data.get('customer_id')
        def on_permanent_delete():
            # Prompt for superadmin password (hidden)
            pwd = simpledialog.askstring("Superadmin Password", "Enter superadmin password to permanently delete customer:", show="*")
            if pwd is None:
                return
            if pwd != SUPERADMIN_PASSWORD:
                messagebox.showerror("Error", "Incorrect superadmin password")
                return

            if not messagebox.askyesno("Confirm Deletion", "Permanently delete this customer and all related records? This action cannot be undone."):
                return

            try:
                from models.customer_model import delete_customer
                delete_customer(customer_id)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete customer: {e}")
                return

            # Refresh main table and close dialog
            rows = get_all_customer_items()
            populate(rows)
            dlg.destroy()
            messagebox.showinfo("Success", "Customer permanently deleted")

        if self.user and (self.user.get('role') or '').lower() == 'superadmin':
            tk.Button(action_bar, text="Delete (Permanent)", command=on_permanent_delete, bg="#c0392b", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)

        # Close on Escape
        dlg.bind('<Escape>', lambda e: dlg.destroy())

    def show_installment_details(self, item_id, parent=None):
        """Show installment schedule and allocation dialog for an item_id."""
        from models.item_model import get_item_by_id
        from models.payment_model import get_payments_by_item
        from services.emi_calculate import generate_due_dates
        from datetime import datetime, date as _date
        from tkinter import messagebox

        if not item_id:
            messagebox.showinfo("Info", "No item associated with this selection")
            return

        item = get_item_by_id(item_id)
        if not item:
            messagebox.showerror("Error", "Item not found")
            return

        # Parse start_date (DB may return date or string)
        start = item.get('start_date')
        if isinstance(start, str):
            try:
                start = datetime.strptime(start, '%Y-%m-%d').date()
            except Exception:
                start = _date.today()
        if not start:
            start = _date.today()

        total = int(item.get('total_installments') or 0)
        inst_amt = float(item.get('installment_amount') or 0)
        mode = item.get('installment_mode') or 'MONTHLY'

        due_dates = generate_due_dates(start, total, mode)

        payments = get_payments_by_item(item_id) or []

        # Prepare installments data
        installments = []
        for idx, dd in enumerate(due_dates, start=1):
            installments.append({
                'no': idx,
                'due_date': dd,
                'expected': inst_amt,
                'received': 0.0,
                'balance': inst_amt,
                'receipts': [],
                'remarks': ''
            })

        # Allocate payments to installments in chronological order
        for p in payments:
            amt = float(p.get('amount_paid') or 0)
            p_date = p.get('payment_date')
            p_id = p.get('payment_id') or p.get('id') or None

            # normalize payment date
            if isinstance(p_date, str):
                try:
                    p_date = datetime.strptime(p_date, '%Y-%m-%d').date()
                except Exception:
                    p_date = _date.today()

            i = 0
            while amt > 0 and i < len(installments):
                inst = installments[i]
                if inst['balance'] > 0:
                    apply_amt = min(amt, inst['balance'])
                    inst['received'] += apply_amt
                    inst['balance'] -= apply_amt
                    inst['receipts'].append({'payment_id': p_id, 'amount': apply_amt, 'payment_date': p_date})
                    amt = round(amt - apply_amt, 2)
                else:
                    i += 1

        # Compute derived fields for display
        today = _date.today()
        for inst in installments:
            # receipt ids
            r_ids = [str(r['payment_id']) for r in inst['receipts'] if r['payment_id']]
            inst['receipt_no'] = ','.join(r_ids)

            # overdues received (payments that occurred after due date)
            overdue_received = sum(r['amount'] for r in inst['receipts'] if r['payment_date'] and r['payment_date'] > inst['due_date'])
            inst['overdue_received'] = round(overdue_received, 2)

            # determine overdays
            if inst['received'] >= inst['expected'] and inst['receipts']:
                # find date when installment was fully paid
                cum = 0
                full_date = None
                for r in inst['receipts']:
                    cum += r['amount']
                    if cum >= inst['expected']:
                        full_date = r['payment_date']
                        break
                if full_date:
                    inst['overdays'] = max(0, (full_date - inst['due_date']).days)
                else:
                    inst['overdays'] = 0
            else:
                # not fully paid
                inst['overdays'] = max(0, (today - inst['due_date']).days) if today > inst['due_date'] else 0

            # remarks
            if inst['received'] >= inst['expected']:
                inst['remarks'] = 'Paid'
                if inst['overdays'] > 0:
                    inst['remarks'] += f" (Late by {inst['overdays']}d)"
            elif inst['received'] > 0:
                inst['remarks'] = f"Partial ({inst['received']}/{inst['expected']})"
                if inst['overdays'] > 0:
                    inst['remarks'] += f" - Overdue {inst['overdays']}d"
            else:
                inst['remarks'] = 'Unpaid' + (f" - Overdue {inst['overdays']}d" if inst['overdays'] > 0 else '')

        # Build dialog
        dlg2 = tk.Toplevel(parent or self.root)
        dlg2.title(f"Installment Details for Item {item_id}")
        dlg2.geometry('900x520')

        cols = ["#","Due Date","Expected","Received","Receipt No","Overdays","Rcd Overdues","Balance","Remarks"]
        tree2 = ttk.Treeview(dlg2, columns=cols, show='headings')
        for c in cols:
            tree2.heading(c, text=c)
            tree2.column(c, width=100, anchor='center')
        tree2.pack(fill=tk.BOTH, expand=True)

        # Insert rows
        for inst in installments:
            tree2.insert('', 'end', values=[
                inst['no'],
                inst['due_date'].isoformat() if hasattr(inst['due_date'], 'isoformat') else str(inst['due_date']),
                f"{inst['expected']:.2f}",
                f"{inst['received']:.2f}",
                inst.get('receipt_no', ''),
                inst.get('overdays', 0),
                f"{inst.get('overdue_received', 0):.2f}",
                f"{inst.get('balance', 0):.2f}",
                inst.get('remarks', '')
            ])

        # Close on escape
        dlg2.bind('<Escape>', lambda e: dlg2.destroy())

    # ================= PAYMENTS =================
    def open_payments(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="Payment Search & Filter",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)

        # ========== Filter Panel ==========
        filter_frame = tk.Frame(self.content_frame, bg="white")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Name:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(filter_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Village:", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        # make combobox editable so typing filters suggestions
        village_cb = ttk.Combobox(filter_frame, width=30, state="normal")
        village_cb.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filter_frame, text="Address:", bg="white").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        address_cb = ttk.Combobox(filter_frame, width=40, state="normal")
        address_cb.grid(row=0, column=5, padx=5, pady=5)

        # store full lists so we can filter locally
        village_full = []
        address_full = []

        def load_address_village():
            from models.village_model import get_all_villages
            from models.address_model import get_all_addresses
            villages = get_all_villages()
            village_full[:] = [f"{v['village_id']} - {v['name']}" for v in villages]
            village_cb["values"] = village_full
            addresses = get_all_addresses()
            address_full[:] = [f"{a['address_id']} - {a['address']}" for a in addresses]
            address_cb["values"] = address_full

        def _filter_combobox(cb, full_list, event=None):
            val = cb.get()
            if not val:
                cb['values'] = full_list
                return
            val_l = val.strip().lower()
            matches = [s for s in full_list if val_l in s.lower()]
            cb['values'] = matches
            if matches:
                try:
                    # open dropdown to show suggestions
                    cb.event_generate('<Down>')
                except Exception:
                    pass

        # bind typing events to filter suggestions
        village_cb.bind('<KeyRelease>', lambda e: _filter_combobox(village_cb, village_full, e))
        address_cb.bind('<KeyRelease>', lambda e: _filter_combobox(address_cb, address_full, e))

        load_address_village()

        tk.Label(filter_frame, text="Item:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        item_entry = tk.Entry(filter_frame)
        item_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Paid Status:", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        status_cb = ttk.Combobox(filter_frame, values=["All", "Paid", "Unpaid"], state="readonly", width=10)
        status_cb.grid(row=1, column=3, padx=5, pady=5)
        status_cb.set("All")

        tk.Label(filter_frame, text="Due Min:", bg="white").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        due_min_entry = tk.Entry(filter_frame, width=10)
        due_min_entry.grid(row=1, column=5, padx=5, pady=5)

        tk.Label(filter_frame, text="Due Max:", bg="white").grid(row=1, column=6, padx=5, pady=5, sticky="e")
        due_max_entry = tk.Entry(filter_frame, width=10)
        due_max_entry.grid(row=1, column=7, padx=5, pady=5)

        tk.Label(filter_frame, text="From Date (YYYY-MM-DD):", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        from_date_entry = tk.Entry(filter_frame)
        from_date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="To Date (YYYY-MM-DD):", bg="white").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        to_date_entry = tk.Entry(filter_frame)
        to_date_entry.grid(row=2, column=3, padx=5, pady=5)

        # ========== Table Frame ==========
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = [
            "Customer ID", "Name", "Phone", "Village", "Address", "Item",
            "Total Amount", "Paid Amount", "Due Amount", "Installment Mode", "Total Installments", "Paid Status"
        ]

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # mapping of tree iid -> underlying row data for detail lookups
        detail_map = {}

        # Double-click handler for Payments table to show installment details
        def on_pay_double_click(event):
            itm = tree.focus()
            if not itm:
                return
            r = detail_map.get(itm)
            if not r:
                return
            # Open the full customer/item detail dialog (includes payment history and Installment Details)
            self.show_customer_details(r, parent=self.content_frame)

        tree.bind("<Double-1>", on_pay_double_click)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.content_frame, orient="horizontal", command=tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=hsb.set)

        # Headings
        for col in columns:
            tree.heading(col, text=col)
            # make Address column wider for readability
            if col == "Address":
                tree.column(col, width=240, anchor="center")
            else:
                tree.column(col, width=120, anchor="center")

        # ========== Search Logic ==========
        from models.report_model import get_all_customer_items  # You can modify this to include payment info

        def search_records():
            # Build filter dict from UI inputs
            # extract village name/address from combobox value 'id - name'
            village_val = village_cb.get().strip()
            if village_val:
                parts = village_val.split(" - ", 1)
                village_filter = parts[1] if len(parts) > 1 else parts[0]
            else:
                village_filter = None

            address_val = address_cb.get().strip()
            if address_val:
                parts = address_val.split(" - ", 1)
                address_filter = parts[1] if len(parts) > 1 else parts[0]
            else:
                address_filter = None

            filters = {
                "name": name_entry.get().strip() or None,
                "village": village_filter,
                "address": address_filter,
                "item": item_entry.get().strip() or None,
                "status": status_cb.get() if status_cb.get() != "All" else None,
            }

            # parse due min/max as floats if provided
            try:
                due_min = due_min_entry.get().strip()
                filters["due_min"] = float(due_min) if due_min else None
            except ValueError:
                filters["due_min"] = None

            try:
                due_max = due_max_entry.get().strip()
                filters["due_max"] = float(due_max) if due_max else None
            except ValueError:
                filters["due_max"] = None

            # date filters (no validation here; DB expects YYYY-MM-DD)
            payment_from = from_date_entry.get().strip()
            payment_to = to_date_entry.get().strip()
            if payment_from:
                filters["payment_from"] = payment_from
            if payment_to:
                filters["payment_to"] = payment_to

            # Call model search that performs SQL-level filtering (efficient)
            from models.report_model import search_customer_items
            rows = search_customer_items(filters)

            # Clear existing
            for i in tree.get_children():
                tree.delete(i)

            for row in rows:
                paid_status = row.get("paid_status", "Unpaid")
                iid = tree.insert(
                    "",
                    "end",
                    values=[
                        row.get("customer_id") or "",
                        row.get("customer_name") or "",
                        row.get("customer_phone") or "",
                        row.get("village_name") or "",
                        row.get("customer_address") or "",
                        f"{row.get('brand') or ''} {row.get('model') or ''}".strip(),
                        row.get("item_amount") or "",
                        row.get("total_paid") or 0,
                        row.get("due_amount") or 0,
                        row.get("installment_mode") or "",
                        row.get("total_installments") or "",
                        paid_status
                    ]
                )
                detail_map[iid] = row
                        

        # Search button
        tk.Button(
            filter_frame,
            text="🔍 Search",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            command=search_records
        ).grid(row=0, column=8, padx=10)

        tk.Button(
            filter_frame,
            text="� Payment Records",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self.open_payment_records()
        ).grid(row=0, column=9, padx=10)

        tk.Button(
            filter_frame,
            text="💸 Record Payment",
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: self.open_record_payment()
        ).grid(row=0, column=10, padx=10)

        # Initial load
        search_records()

    def open_payment_records(self):
        """Open a dialog listing all individual payment records with customer details."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Payment Records")
        dlg.geometry("900x520")

        top = tk.Frame(dlg)
        top.pack(fill=tk.X, padx=8, pady=6)
        tk.Label(top, text="From (YYYY-MM-DD):").pack(side=tk.LEFT)
        from_e = tk.Entry(top, width=12)
        from_e.pack(side=tk.LEFT, padx=6)
        tk.Label(top, text="To (YYYY-MM-DD):").pack(side=tk.LEFT, padx=(10,0))
        to_e = tk.Entry(top, width=12)
        to_e.pack(side=tk.LEFT, padx=6)
        tk.Label(top, text="Name:").pack(side=tk.LEFT, padx=(10,0))
        name_e = tk.Entry(top, width=20)
        name_e.pack(side=tk.LEFT, padx=6)

        # Treeview
        cols = ["Payment ID","Date","Customer ID","Name","Phone","Item ID","Brand","Amount Paid","Remaining"]
        tree = ttk.Treeview(dlg, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor='center')
        tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        vsb = ttk.Scrollbar(dlg, orient="vertical", command=tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=vsb.set)

        def load_records():
            from models.payment_model import get_all_payments
            filters = {}
            if from_e.get().strip():
                filters["payment_from"] = from_e.get().strip()
            if to_e.get().strip():
                filters["payment_to"] = to_e.get().strip()
            if name_e.get().strip():
                filters["customer_name"] = name_e.get().strip()
            rows = get_all_payments(filters)
            for i in tree.get_children():
                tree.delete(i)
            for r in rows:
                tree.insert("", "end", values=[
                    r.get('payment_id') or r.get('id') or '',
                    r.get('payment_date'),
                    r.get('customer_id') or '',
                    r.get('customer_name') or '',
                    r.get('customer_phone') or '',
                    r.get('item_id') or '',
                    f"{r.get('brand') or ''} {r.get('model') or ''}".strip(),
                    r.get('amount_paid') or '',
                    r.get('remaining_amount') or ''
                ])

        tk.Button(top, text="🔄 Reload", command=load_records, bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=8)
        tk.Button(top, text="Close", command=dlg.destroy, bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=8)

        load_records()
