"""
Group_Inventory_Form.py
Robust Inventory Form with Real-Time Validation and Validation Trace Log
Platform: Python Tkinter Desktop GUI
"""

import math
import tkinter as tk
from datetime import datetime
from tkinter import messagebox


GREEN = "#1b8a3a"
RED = "#c0392b"
GRAY = "#6b7280"
BG = "#f3f4f6"
PANEL_BG = "#ffffff"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_MONO = ("Consolas", 10)

PESO = "\u20b1"  # ₱


root = tk.Tk()
root.title("Robust Inventory Form")
root.geometry("900x700")
root.minsize(820, 640)
root.configure(bg=BG)

name_var = tk.StringVar()
quantity_var = tk.StringVar()
price_var = tk.StringVar()

field_valid = {"name": False, "quantity": False, "price": False}



def parse_name(text):
    text = text.strip()
    if not text:
        return None, "Product name must not be empty."
    return text, None


def parse_quantity(text):
    text = text.strip()
    if not text:
        return None, "Quantity is required."
    try:
        if "_" in text:  
            raise ValueError
        quantity = int(text) 
    except ValueError:
        return None, "Quantity must be a whole number (no letters or decimals)."
    if quantity <= 0:
        return None, "Quantity must be greater than zero."
    return quantity, None


def parse_price(text):
    text = text.strip().replace(",", "")
    if not text:
        return None, "Unit price is required."
    try:
        if "_" in text:
            raise ValueError
        price = float(text)
        if not math.isfinite(price): 
            raise ValueError
    except ValueError:
        return None, "Unit price must be a valid number."
    if price <= 0:
        return None, "Unit price must be greater than zero."
    return price, None



title_label = tk.Label(root, text="Robust Inventory Form", font=FONT_TITLE,
                       bg=BG, fg="#111827")
title_label.pack(pady=(12, 6))

# --- Product Information panel ---
info_frame = tk.LabelFrame(root, text=" Product Information ", font=FONT_BOLD,
                           bg=PANEL_BG, padx=15, pady=10)
info_frame.pack(fill="x", padx=15, pady=6)
info_frame.columnconfigure(1, weight=1)

tk.Label(info_frame, text="Product Name:", font=FONT, bg=PANEL_BG,
         anchor="w").grid(row=0, column=0, sticky="w", pady=(4, 0))
name_entry = tk.Entry(info_frame, textvariable=name_var, font=FONT)
name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=(4, 0))
name_msg = tk.Label(info_frame, text="", font=("Segoe UI", 9), bg=PANEL_BG,
                    anchor="w", fg=GRAY)
name_msg.grid(row=1, column=1, sticky="w", padx=10)

tk.Label(info_frame, text="Quantity:", font=FONT, bg=PANEL_BG,
         anchor="w").grid(row=2, column=0, sticky="w", pady=(4, 0))
quantity_entry = tk.Entry(info_frame, textvariable=quantity_var, font=FONT)
quantity_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=(4, 0))
quantity_msg = tk.Label(info_frame, text="", font=("Segoe UI", 9), bg=PANEL_BG,
                        anchor="w", fg=GRAY)
quantity_msg.grid(row=3, column=1, sticky="w", padx=10)

tk.Label(info_frame, text=f"Unit Price ({PESO}):", font=FONT, bg=PANEL_BG,
         anchor="w").grid(row=4, column=0, sticky="w", pady=(4, 0))
price_entry = tk.Entry(info_frame, textvariable=price_var, font=FONT)
price_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=(4, 0))
price_msg = tk.Label(info_frame, text="", font=("Segoe UI", 9), bg=PANEL_BG,
                     anchor="w", fg=GRAY)
price_msg.grid(row=5, column=1, sticky="w", padx=10)


status_frame = tk.Frame(root, bg=BG)
status_frame.pack(fill="x", padx=15, pady=(2, 0))
tk.Label(status_frame, text="Overall Validation Status:", font=FONT_BOLD,
         bg=BG).pack(side="left")
overall_status = tk.Label(status_frame, text="Waiting for input...",
                          font=FONT_BOLD, bg=BG, fg=GRAY)
overall_status.pack(side="left", padx=8)

button_frame = tk.Frame(root, bg=BG)
button_frame.pack(fill="x", padx=15, pady=8)


output_frame = tk.LabelFrame(root, text=" Inventory Output ", font=FONT_BOLD,
                             bg=PANEL_BG, padx=8, pady=8)
output_frame.pack(fill="both", expand=True, padx=15, pady=6)

output_scroll = tk.Scrollbar(output_frame)
output_scroll.pack(side="right", fill="y")
inventory_text = tk.Text(output_frame, height=9, font=FONT_MONO, wrap="word",
                         state="disabled", yscrollcommand=output_scroll.set)
inventory_text.pack(side="left", fill="both", expand=True)
output_scroll.config(command=inventory_text.yview)
inventory_text.tag_configure("success", foreground=GREEN)


log_frame = tk.LabelFrame(root, text=" Validation Trace Log ", font=FONT_BOLD,
                          bg=PANEL_BG, padx=8, pady=8)
log_frame.pack(fill="both", expand=True, padx=15, pady=(6, 12))

log_scroll = tk.Scrollbar(log_frame)
log_scroll.pack(side="right", fill="y")
log_text = tk.Text(log_frame, height=8, font=("Consolas", 9), wrap="word",
                   state="disabled", bg="#111827", fg="#e5e7eb",
                   yscrollcommand=log_scroll.set)
log_text.pack(side="left", fill="both", expand=True)
log_scroll.config(command=log_text.yview)
log_text.tag_configure("ok", foreground="#4ade80")
log_text.tag_configure("error", foreground="#f87171")
log_text.tag_configure("info", foreground="#93c5fd")



def log_event(message, tag="info"):
    """Append a time-stamped line to the Validation Trace Log."""
    stamp = datetime.now().strftime("%H:%M:%S")
    log_text.config(state="normal")
    log_text.insert("end", f"[{stamp}] {message}\n", tag)
    log_text.see("end")
    log_text.config(state="disabled")


def clear_log():
    log_text.config(state="normal")
    log_text.delete("1.0", "end")
    log_text.config(state="disabled")


def append_inventory(text):
    inventory_text.config(state="normal")
    inventory_text.insert("end", text, "success")
    inventory_text.see("end")
    inventory_text.config(state="disabled")


def clear_inventory():
    if messagebox.askyesno("Clear Inventory",
                           "Delete ALL submitted inventory records?"):
        inventory_text.config(state="normal")
        inventory_text.delete("1.0", "end")
        inventory_text.config(state="disabled")
        log_event("Inventory output cleared by user.", "info")


def show_message(label, error, empty_ok_text=""):
    """Show a green 'valid' or red error message on a validation label."""
    if error is None:
        label.config(text="\u2714 Valid", fg=GREEN)
    else:
        label.config(text="\u2718 " + error, fg=RED)


def update_overall_status():
    if all(field_valid.values()):
        overall_status.config(text="\u2714 All inputs are valid - ready to submit",
                              fg=GREEN)
    elif not (name_var.get() or quantity_var.get() or price_var.get()):
        overall_status.config(text="Waiting for input...", fg=GRAY)
    else:
        overall_status.config(text="\u2718 Some inputs are invalid", fg=RED)



def validate_name(*args):
    value, error = parse_name(name_var.get())
    field_valid["name"] = error is None
    show_message(name_msg, error)
    if error is None:
        log_event(f"Product Name '{value}' -> Accepted", "ok")
    else:
        log_event(f"Product Name '{name_var.get()}' -> Error: {error}", "error")
    update_overall_status()


def validate_quantity(*args):
    value, error = parse_quantity(quantity_var.get())
    field_valid["quantity"] = error is None
    show_message(quantity_msg, error)
    if error is None:
        log_event(f"Quantity '{quantity_var.get()}' -> Accepted ({value})", "ok")
    else:
        log_event(f"Quantity '{quantity_var.get()}' -> Rejected: {error}", "error")
    update_overall_status()


def validate_price(*args):
    value, error = parse_price(price_var.get())
    field_valid["price"] = error is None
    show_message(price_msg, error)
    if error is None:
        log_event(f"Unit Price '{price_var.get()}' -> Accepted ({value:.2f})", "ok")
    else:
        log_event(f"Unit Price '{price_var.get()}' -> Rejected: {error}", "error")
    update_overall_status()


name_var.trace_add("write", validate_name)
quantity_var.trace_add("write", validate_quantity)
price_var.trace_add("write", validate_price)



def submit_product():
    raw_name = name_var.get()
    raw_qty = quantity_var.get()
    raw_price = price_var.get()
    log_event("Submit Product clicked.", "info")

    try:
        name, error = parse_name(raw_name)
        if error:
            raise ValueError(error)
        quantity, error = parse_quantity(raw_qty)
        if error:
            raise ValueError(error)
        price, error = parse_price(raw_price)
        if error:
            raise ValueError(error)

        total_value = quantity * price

    except ValueError as err:
        messagebox.showerror("Invalid Input", str(err))
        log_event(f"Submit rejected: {err}", "error")
        return
    except Exception as err:  
        messagebox.showerror("Unexpected Error", f"Something went wrong:\n{err}")
        log_event(f"Submit failed (unexpected): {err}", "error")
        return

    record = (
        f"Product Name: {name}\n"
        f"Quantity: {quantity}\n"
        f"Unit Price: {PESO}{price:,.2f}\n"
        f"Total Value: {PESO}{total_value:,.2f}\n"
        f"Status: Successfully Added\n"
        f"{'-' * 40}\n"
    )
    append_inventory(record)
    log_event(f"Submit accepted: '{name}' x{quantity} @ {PESO}{price:,.2f} "
              f"= {PESO}{total_value:,.2f}", "ok")
    messagebox.showinfo("Success", f"'{name}' was added to the inventory.")
    clear_form(log=False)



def clear_form(log=True):
    name_var.set("")
    quantity_var.set("")
    price_var.set("")

    for label in (name_msg, quantity_msg, price_msg):
        label.config(text="", fg=GRAY)
    for key in field_valid:
        field_valid[key] = False
    update_overall_status()

    name_entry.focus_set()
    if log:
        log_event("Clear Form clicked: all fields reset.", "info")



tk.Button(button_frame, text="Submit Product", font=FONT_BOLD, bg="#2563eb",
          fg="white", activebackground="#1d4ed8", activeforeground="white",
          padx=14, pady=4, command=submit_product).pack(side="left")
tk.Button(button_frame, text="Clear Form", font=FONT_BOLD, padx=14, pady=4,
          command=clear_form).pack(side="left", padx=8)
tk.Button(button_frame, text="Clear Inventory", font=FONT, padx=10, pady=4,
          command=clear_inventory).pack(side="right")
tk.Button(button_frame, text="Clear Log", font=FONT, padx=10, pady=4,
          command=clear_log).pack(side="right", padx=8)


root.bind("<Return>", lambda event: submit_product())


log_event("Application started. Validation trace is active.", "info")
name_entry.focus_set()
root.mainloop()