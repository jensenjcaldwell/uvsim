import classes
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import re
from io import StringIO


class OutputCapture(StringIO):
    def __init__(self, ui, original_stdout):
        super().__init__()
        self.ui = ui
        self.original_stdout = original_stdout

    def write(self, s):
        self.ui.last_output = s.rstrip("\n")
        return self.original_stdout.write(s)


class UVsimUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UVsim")
        self.root.geometry("800x700")

        self.sim = classes.simulator()
        self.register_value_labels = {}
        self.last_output = ""

        self._original_stdout = sys.stdout
        sys.stdout = OutputCapture(self, self._original_stdout)

        self._build_ui()
        self.refresh_ui()

    def _format_register_value(self, value):
        if isinstance(value, classes.Instruction):
            return f"{value.sign}{value.code:02d}{value.operand:02d}"
        return str(value)

    def refresh_ui(self):
        self.accumulator_value.config(text=str(self.sim.accumulator))
        for reg_num, label in self.register_value_labels.items():
            label.config(text=self._format_register_value(self.sim.registers[reg_num]))

    def _prompt_for_signed_word(self):
        popup = tk.Toplevel(self.root)
        popup.title("READ Input")
        popup.transient(self.root)
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
            self.sim.input_flag = False
            popup.destroy()

        ttk.Button(popup, text="Submit", command=submit_value).pack(padx=12, pady=(0, 12))
        popup.bind("<Return>", lambda _event: submit_value())
        self.root.wait_window(popup)
        return result["value"]

    def run_program(self):
        try:
            self.sim = classes.simulator()

            try:
                self.sim.read_program(self.file_entry.get())
            except ValueError as e:
                messagebox.showerror(
                    "Load Error",
                    f"The program file is malformed or improperly formatted.\n\nDetails: {e}",
                )
                return

            steps = 0
            max_steps = 100000
            while True:
                status = self.sim.advance()

                if status == "INPUT_NEEDED" and self.sim.input_flag:
                    value = self._prompt_for_signed_word()
                    if value is None:
                        raise ValueError("Input cancelled.")
                    self.sim.inputval = value
                    self.sim.input_flag = True
                    continue

                if status == "RUNTIME_ERROR":
                    messagebox.showerror("Runtime Error", self.sim.last_error or "A runtime error occurred.")
                    break

                if status == "HALTED":
                    break

                if isinstance(status, str) and status.startswith("Error"):
                    raise ValueError(status)

                steps += 1
                if steps > max_steps:
                    raise RuntimeError("Execution exceeded max step limit.")

            self.refresh_ui()
        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found",
                f"The file '{self.file_entry.get()}' could not be found. Please check the path and try again.",
            )
        except ValueError as e:
            messagebox.showerror("Execution Error", str(e))
        except Exception as e:
            print(f"Error: {e}")

    def reset_program(self):
        self.sim = classes.simulator()
        self.refresh_ui()

    def _build_ui(self):
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10, fill=tk.X, padx=10)

        self.file_entry = ttk.Entry(file_frame, width=50)
        self.file_entry.insert(0, "filepath.txt")
        self.file_entry.pack(side="left", padx=10)

        run_button = ttk.Button(file_frame, text="Run", command=self.run_program)
        run_button.pack(side="left", padx=10)

        reset_button = ttk.Button(file_frame, text="Reset", command=self.reset_program)
        reset_button.pack(side="left", padx=10)

        accumulator_frame = ttk.Frame(self.root, relief="solid", borderwidth=1)
        accumulator_frame.pack(pady=50, padx=50)

        accumulator_label = ttk.Label(accumulator_frame, text="Accumulator:")
        accumulator_label.pack(side="top", padx=5, pady=5)
        self.accumulator_value = ttk.Label(accumulator_frame, text=str(self.sim.accumulator))
        self.accumulator_value.pack(side="top", padx=5, pady=5)

        register_frame = ttk.Frame(self.root)
        register_frame.pack(pady=10, fill=tk.X, padx=10)

        columns = 10
        rows = len(self.sim.registers) // columns
        if len(self.sim.registers) % columns:
            rows += 1

        for col in range(columns):
            for row in range(rows):
                reg_num = col * rows + row

                if reg_num >= len(self.sim.registers):
                    break

                reg_container = ttk.Frame(register_frame, relief="solid", borderwidth=1)
                reg_container.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

                reg_label = ttk.Label(reg_container, text=f"R{reg_num}:")
                reg_label.pack(side="left", padx=5, pady=5)

                separator = ttk.Separator(reg_container, orient="vertical")
                separator.pack(side="left", fill="y", padx=2)

                reg_value = ttk.Label(reg_container, text=str(self.sim.registers[reg_num]))
                reg_value.pack(side="left", padx=5, pady=5)
                self.register_value_labels[reg_num] = reg_value

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = UVsimUI()
    app.start()

