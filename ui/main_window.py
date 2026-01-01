import tkinter as tk
from tkinter import ttk, messagebox

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
        tk.Label(
            self.root,
            text="Sandhu Enterprises – EMI Management System",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        ).pack(fill=tk.X)

    # ================= LEFT MENU =================
    def create_menu(self):
        menu_frame = tk.Frame(self.root, bg="#ecf0f1", width=200)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons = [
            ("Customers", self.open_customers),
            ("Records", self.open_items),   # renamed logically
            ("Payments", self.open_payments),
            ("Exit", self.root.quit)
        ]

        for text, command in buttons:
            tk.Button(
                menu_frame,
                text=text,
                font=("Arial", 12),
                width=18,
                pady=8,
                command=command
            ).pack(pady=5)

    # ================= MAIN CONTENT =================
    def create_content_area(self):
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            self.content_frame,
            text="Welcome to Sandhu Enterprises EMI System",
            font=("Arial", 16),
            bg="white"
        ).pack(expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

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
                ("Interest (%)", data.get("interest_rate")),
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

            rows = max(len(left_fields), len(right_fields))
            for i in range(rows):
                # Left column
                if i < len(left_fields):
                    label_l, val_l = left_fields[i]
                    tk.Label(inner, text=f"{label_l}:", anchor="e", width=18, font=("Segoe UI", 10, "bold"), bg="#ffffff").grid(row=i*2, column=0, sticky="e", padx=12, pady=(8,2))
                    val_lbl_l = tk.Label(inner, text=str(val_l) if val_l is not None else "", anchor="w", justify="left", wraplength=320, font=("Segoe UI", 10), bg="#ffffff", bd=1, relief="groove")
                    val_lbl_l.grid(row=i*2, column=1, sticky="we", padx=6, pady=(8,2))
                else:
                    # empty cells to keep alignment
                    tk.Label(inner, text="", bg="#ffffff").grid(row=i*2, column=0)
                    tk.Label(inner, text="", bg="#ffffff").grid(row=i*2, column=1)

                # Right column
                if i < len(right_fields):
                    label_r, val_r = right_fields[i]
                    tk.Label(inner, text=f"{label_r}:", anchor="e", width=18, font=("Segoe UI", 10, "bold"), bg="#ffffff").grid(row=i*2, column=2, sticky="e", padx=12, pady=(8,2))
                    val_lbl_r = tk.Label(inner, text=str(val_r) if val_r is not None else "", anchor="w", justify="left", wraplength=320, font=("Segoe UI", 10), bg="#ffffff", bd=1, relief="groove")
                    val_lbl_r.grid(row=i*2, column=3, sticky="we", padx=6, pady=(8,2))
                else:
                    tk.Label(inner, text="", bg="#ffffff").grid(row=i*2, column=2)
                    tk.Label(inner, text="", bg="#ffffff").grid(row=i*2, column=3)

                # single separator across both columns
                sep = tk.Frame(inner, height=1, bg="#e5e7eb")
                sep.grid(row=i*2+1, column=0, columnspan=4, sticky="we", padx=8, pady=(4,4))

            # Increase dialog width to accommodate two columns
            try:
                dlg.geometry("920x520")
            except Exception:
                pass

            # Bottom action bar with Close
            action_bar = tk.Frame(dlg, bg="#ffffff")
            action_bar.pack(fill=tk.X)
            tk.Button(action_bar, text="Close", command=dlg.destroy, bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=12, pady=8)

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
        village_entry = tk.Entry(filter_frame)
        village_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filter_frame, text="Item:", bg="white").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        item_entry = tk.Entry(filter_frame)
        item_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(filter_frame, text="Paid Status:", bg="white").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        status_cb = ttk.Combobox(filter_frame, values=["All", "Paid", "Unpaid"], state="readonly", width=10)
        status_cb.grid(row=0, column=7, padx=5, pady=5)
        status_cb.set("All")

        # ========== Table Frame ==========
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = [
            "Customer ID", "Name", "Phone", "Village", "Item",
            "Total Amount", "Paid Amount", "Due Amount", "Installment Mode", "Total Installments", "Paid Status"
        ]

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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
            tree.column(col, width=120, anchor="center")

        # ========== Search Logic ==========
        from models.report_model import get_all_customer_items  # You can modify this to include payment info

        def search_records():
            # Fetch all customer items
            rows = get_all_customer_items()  # Ideally add village/payment data in your query

            # Clear existing
            for i in tree.get_children():
                tree.delete(i)

            for row in rows:
                # Filtering
                if name_entry.get() and name_entry.get().lower() not in row.get("customer_name", "").lower():
                    continue
                if village_entry.get() and village_entry.get().lower() not in (row.get("village_name", "") or "").lower():
                    continue
                if item_entry.get() and item_entry.get().lower() not in row.get("brand", "").lower():
                    continue
                paid_status = row.get("paid_status", "Unpaid")  # adjust field name as per your DB
                if status_cb.get() != "All" and status_cb.get() != paid_status:
                    continue

                tree.insert(
                    "",
                    "end",
                    values=[
                        row.get("customer_id") or "",
                        row.get("customer_name") or "",
                        row["customer_phone"],
                        row.get("village_name") or row.get("customer_address") or "",
                        row.get("brand") or "",
                        row.get("item_amount") or "",
                        row.get("paid_amount") or "",
                        row.get("due_amount") or "",
                        row.get("installment_mode") or "",
                        row.get("total_installments") or "",
                        paid_status
                    ]
                )
                        

        # Search button
        tk.Button(
            filter_frame,
            text="🔍 Search",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            command=search_records
        ).grid(row=0, column=8, padx=10)

        # Initial load
        search_records()

