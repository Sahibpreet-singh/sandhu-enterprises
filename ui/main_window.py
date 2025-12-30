import tkinter as tk
from tkinter import ttk

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

    # ================= RECORDS (OLD ITEMS) =================
    def open_items(self):
        self.clear_content()

        tk.Label(
            self.content_frame,
            text="Customer & Item Report",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=10)

        # Sorting function
        def sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            try:
                l.sort(key=lambda t: float(t[0]) if t[0] else 0, reverse=reverse)
            except ValueError:
                l.sort(key=lambda t: t[0], reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda: sort_column(tv, col, not reverse))

        # Frame for table and scrollbars
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = [
            "Customer ID", "Name", "Phone", "Address", "Remarks",
            "Brand", "Model", "Item Amount", "Advance", "Finance", "Interest",
            "Installment Amount", "Installment Mode", "Total Installments",
            "Guarantor Name", "Guarantor Phone", "Guarantor Address"
        ]

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=vsb.set)

        # Horizontal scrollbar
        hsb = ttk.Scrollbar(self.content_frame, orient="horizontal", command=tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=hsb.set)

        # Set column headings and add sorting
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=150, anchor="center")

        # Fetch data
        from models.report_model import get_all_customer_items
        rows = get_all_customer_items()

        # Insert data
        for row in rows:
            tree.insert(
                "",
                "end",
                values=[
                    row["customer_id"],
                    row["customer_name"],
                    row["customer_phone"],
                    row["customer_address"],
                    row["customer_remarks"],
                    row.get("brand") or "",
                    row.get("model") or "",
                    row.get("item_amount") or "",
                    row.get("advance_amount") or "",
                    row.get("finance_amount") or "",
                    row.get("interest_rate") or "",
                    row.get("installment_amount") or "",
                    row.get("installment_mode") or "",
                    row.get("total_installments") or "",
                    row.get("guarantor_name") or "",
                    row.get("guarantor_phone") or "",
                    row.get("guarantor_address") or "",
                ]
            )




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
                if name_entry.get() and name_entry.get().lower() not in row.get("name", "").lower():
                    continue
                if village_entry.get() and village_entry.get().lower() not in row.get("village", "").lower():
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
                        row["customer_address"],
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

