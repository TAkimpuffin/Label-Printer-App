# to build this as a program run the following command:
# pyinstaller --windowed --onefile label_printer.py
# you gotta have pyinstaller and tkinter working though obviously

import tkinter as tk
from tkinter import messagebox
import subprocess

def get_center_x(text, font_scale, label_width=800):
    char_width = 30 * font_scale
    text_width = len(text) * char_width
    return max(0, (label_width - text_width) // 2)


def generate_label():
    name = entry_name.get()
    company = entry_company.get()
    role = entry_role.get()

    font_scale = 18
    name_x = get_center_x(f"Name: {name}", font_scale)
    company_x = get_center_x(f"Company: {company}", font_scale)
    role_x = get_center_x(f"Role: {role}", font_scale)

    tspl = f"""
SIZE 75 mm,50 mm
GAP 15 mm,12 mm
DIRECTION 1
REFERENCE 0,0
CLS

TEXT {name_x},30,"0",0,{font_scale},{font_scale},"Name: {name}"
TEXT {company_x},80,"0",0,{font_scale},{font_scale},"Company: {company}"
TEXT {role_x},130,"0",0,{font_scale},{font_scale},"Role: {role}"

PRINT 1
"""
    with open("label.txt", "w") as f:
        f.write(tspl.strip() + "\n\n")
    try:
        subprocess.run(["lp", "-o", "raw", "-d", "TSC_DA210", "label.txt"], check=True)
        # messagebox.showinfo("Success", "Label sent to printer!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to print label:\n{e}")


root = tk.Tk()
root.title("Label Printer")

tk.Label(root, text="Name:").grid(row=0, column=0)
entry_name = tk.Entry(root, width=40)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Company:").grid(row=1, column=0)
entry_company = tk.Entry(root, width=40)
entry_company.grid(row=1, column=1)

tk.Label(root, text="Role:").grid(row=2, column=0)
entry_role = tk.Entry(root, width=40)
entry_role.grid(row=2, column=1)

print_button = tk.Button(root, text="Print Label", command=generate_label)
print_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
