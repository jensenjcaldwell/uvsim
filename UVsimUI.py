import main
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import re
from io import StringIO

root = tk.Tk()
root.title("UVsim")
root.geometry("800x700")

last_output = ""
original_stdout = sys.stdout

sim = main.simulator()
register_value_labels = {}


def _format_register_value(value):
    if isinstance(value, main.Instruction):
        return f"{value.sign}{value.code:02d}{value.operand:02d}"
    return str(value)


def refresh_ui():
    accumulator_value.config(text=str(sim.accumulator))
    for reg_num, label in register_value_labels.items():
        label.config(text=_format_register_value(sim.registers[reg_num]))


def _prompt_for_signed_word():
    popup = tk.Toplevel(root)
    popup.title("READ Input")
    popup.transient(root)
    popup.grab_set()

    ttk.Label(popup, text="Enter a signed 4-digit number:").pack(padx=12, pady=(12, 6))
    value_entry = ttk.Entry(popup, width=16)
    value_entry.pack(padx=12, pady=6)
    value_entry.focus_set()

    error_label = ttk.Label(popup, text="", foreground="red")
    error_label.pack(padx=12, pady=(0, 6))

    result = {"value": None}

    def submit_value():
        raw = value_entry.get().strip()
        if not re.fullmatch(r"[+-]\d{4}", raw):
            error_label.config(text="Use format +1234 or -0042")
            return
        result["value"] = raw
        # Clear input wait flag once valid input has been provided.
        sim.input_flag = False
        popup.destroy()

    ttk.Button(popup, text="Submit", command=submit_value).pack(padx=12, pady=(0, 12))
    popup.bind("<Return>", lambda _event: submit_value())
    root.wait_window(popup)
    return result["value"]

def run_program():
    try:
        # Reset simulator state on each run so stale values do not leak between runs.
        global sim
        sim = main.simulator()

        sim.read_program(file_entry.get())

        steps = 0
        max_steps = 100000
        while True:
            status = sim.advance()

            if status == "INPUT_NEEDED" and sim.input_flag:
                value = _prompt_for_signed_word()
                if value is None:
                    raise ValueError("Input cancelled.")
                sim.inputval = value
                # Keep flag true after submit so simulator can consume this value.
                sim.input_flag = True
                continue

            if status == "RUNTIME_ERROR":
                messagebox.showerror("Runtime Error", sim.last_error or "A runtime error occurred.")
                break

            if status == "HALTED":
                break

            if isinstance(status, str) and status.startswith("Error"):
                raise ValueError(status)

            steps += 1
            if steps > max_steps:
                raise RuntimeError("Execution exceeded max step limit.")

        refresh_ui()
    except Exception as e:
        print(f"Error: {e}")
    


class OutputCapture(StringIO):
    def write(self, s):
        global last_output
        last_output = s.rstrip('\n')
        return original_stdout.write(s)

sys.stdout = OutputCapture()

### Filepath and run button

file_frame = ttk.Frame(root)
file_frame.pack(pady=10, fill=tk.X, padx=10)

file_entry = ttk.Entry(file_frame, width=50)
file_entry.insert(0, "filepath.txt")
file_entry.pack(side='left', padx=10)

run_button = ttk.Button(file_frame, text="Run", command=run_program)

run_button.pack(side='left', padx=10)


### Accumulator display
accumulator_frame = ttk.Frame(root, relief='solid', borderwidth=1)
accumulator_frame.pack(pady=50, padx=50)

accumulator_label = ttk.Label(accumulator_frame, text="Accumulator:")
accumulator_label.pack(side='top', padx=5, pady=5)
accumulator_value = ttk.Label(accumulator_frame, text=str(sim.accumulator))
accumulator_value.pack(side='top', padx=5, pady=5)

#### Register grid
register_frame = ttk.Frame(root)
register_frame.pack(pady=10, fill=tk.X, padx=10)

columns = 10
rows = len(sim.registers) // columns
if len(sim.registers) % columns:
    rows += 1

for col in range(columns):
    for row in range(rows):
        reg_num = col * rows + row
        
        if reg_num >= len(sim.registers):
            break
        
        # Create a frame with a border for each register
        reg_container = ttk.Frame(register_frame, relief='solid', borderwidth=1)
        reg_container.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        reg_label = ttk.Label(reg_container, text=f"R{reg_num}:")
        reg_label.pack(side='left', padx=5, pady=5)
        
        # Separator line between label and value
        separator = ttk.Separator(reg_container, orient='vertical')
        separator.pack(side='left', fill='y', padx=2)
        
        reg_value = ttk.Label(reg_container, text=str(sim.registers[reg_num]))
        reg_value.pack(side='left', padx=5, pady=5)
        register_value_labels[reg_num] = reg_value

    refresh_ui()

root.mainloop()

