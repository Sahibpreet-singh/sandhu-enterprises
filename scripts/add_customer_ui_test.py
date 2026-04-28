from tkinter import Tk, messagebox
from ui.customer_ui import AddCustomerWindow


# -------------------------------
# Suppress Popups (for automation)
# -------------------------------

def suppress_messageboxes():
    messagebox.showinfo = lambda *a, **k: None
    messagebox.showerror = lambda *a, **k: None


# -------------------------------
# Fill Customer Form
# -------------------------------

def fill_customer_form(window):
    window.name_entry.insert(0, "UI Test User")
    window.phone_entry.insert(0, "1234567890")
    window.remarks_entry.insert(0, "Added via UI automation")

    # Set date
    window.date_entry.delete(0, "end")
    window.date_entry.insert(0, "2025-12-31")


# -------------------------------
# Main Automation Logic
# -------------------------------

def run_ui_automation():
    print("\n🚀 Starting UI Automation...\n")

    suppress_messageboxes()

    root = Tk()
    root.withdraw()  # Hide main window

    try:
        win = AddCustomerWindow(root)

        # Fill form fields
        fill_customer_form(win)

        # Trigger save action
        win.save_customer()

        print("✅ Customer saved successfully!")

    except Exception as e:
        print("❌ Automation failed:", e)

    finally:
        root.destroy()
        print("\n🏁 Automation Finished\n")


# -------------------------------
# Entry Point
# -------------------------------

if __name__ == "__main__":
    run_ui_automation()