import tkinter as tk
from tkinter import messagebox
from models.customer_model import insert_customer


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
        self.address_entry = tk.Entry(self.win)
        self.address_entry.pack()

        tk.Label(self.win, text="Remarks").pack()
        self.remarks_entry = tk.Entry(self.win)
        self.remarks_entry.pack()

        tk.Button(self.win, text="Save", command=self.save_customer).pack(pady=10)

    def save_customer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        remarks = self.remarks_entry.get()

        if not name or not phone:
            messagebox.showerror("Error", "Name and Phone are required")
            return

        insert_customer(name, phone, address, remarks)
        messagebox.showinfo("Success", "Customer added successfully")
        self.win.destroy()
