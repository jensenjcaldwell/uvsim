import classes
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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

        style = ttk.Style()
        style.configure("TButton", foreground="black")

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

            raw_code = self.code_editor.get("1.0", tk.END).strip()

            lines = [line.strip() for line in raw_code.split("\n") if line.strip()]

            if len(lines) > 100:
                messagebox.showerror(
                    "Validation Error",
                    f"Memory limit exceeded: You have {len(lines)} instructions, but the max is 100."
                )
                return
            
            self.sim.load_from_list(lines)

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
            messagebox.showerror("File Not Found", "The selected file could not be found. Please choose another file.")
        except ValueError as e:
            messagebox.showerror("Execution Error", str(e))
        except Exception as e:
            print(f"Error: {e}")

    def reset_program(self):
        self.sim = classes.simulator()
        self.refresh_ui()

    def browse_file(self):
        selected_file = filedialog.askopenfilename()
        if selected_file:
            with open(selected_file, "r", encoding="utf-8") as file_handle:
                file_contents = file_handle.read()

            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert("1.0", file_contents)

    def save_program(self):
        target_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not target_file:
            return

        program_text = self.code_editor.get("1.0", tk.END).rstrip()
        with open(target_file, "w", encoding="utf-8") as file_handle:
            file_handle.write(program_text)

    def _build_ui(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, fill=tk.X, padx=20)

        self.btn_open = ttk.Button(control_frame, text="Open File", command=self.browse_file)
        self.btn_open.pack(side="left", padx=5)

        self.btn_save = ttk.Button(control_frame, text="Save As", command=self.save_program)
        self.btn_save.pack(side="left", padx=5)

        ttk.Separator(control_frame, orient="vertical").pack(side="left", fill="y")

        self.btn_run = ttk.Button(control_frame, text="Run Code", command=self.run_program)
        self.btn_run.pack(side="left", padx=5)

        self.btn_reset = ttk.Button(control_frame, text="Reset", command=self.reset_program)
        self.btn_reset.pack(side="left", padx=5)

        # Team Member 3 will plug their color function to this button
        self.btn_theme = ttk.Button(control_frame, text="Color Theme")
        self.btn_theme.pack(side="right", padx=5)

        accumulator_frame = ttk.LabelFrame(self.root, text=" CPU Status ", padding=(10, 5))
        accumulator_frame.pack(pady=10, padx=20, fill=tk.X)

        self.accumulator_value = ttk.Label(accumulator_frame, text=f"Accumulator: {self.sim.accumulator}", font=("Arial", 12, "bold"))
        self.accumulator_value.pack(side="top", pady=5)

        editor_frame = ttk.LabelFrame(self.root, text=" BasicML Code Editor ", padding=(10, 10))
        editor_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.code_editor = tk.Text(editor_frame, width=60, height=15,font=("Consolas",12))
        self.code_editor.pack(side="left", fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(editor_frame, command=self.code_editor.yview)
        scrollbar.pack(side="left", fill="y")
        self.code_editor.config(yscrollcommand=scrollbar.set)

        output_frame = ttk.LabelFrame(self.root, text=" Program Output ", padding=(10, 10))
        output_frame.pack(pady=(0, 15), padx=20, fill=tk.X) # Pushed to the bottom

        # Team Member 4 will wire this text box to receive the WRITE commands
        self.output_console = tk.Text(output_frame, height=5, state="disabled", bg="#f0f0f0", font=("Consolas", 10))
        self.output_console.pack(side="left", fill=tk.X, expand=True)
        
        out_scroll = ttk.Scrollbar(output_frame, command=self.output_console.yview)
        out_scroll.pack(side="left", fill="y")
        self.output_console.config(yscrollcommand=out_scroll.set)
        
    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = UVsimUI()
    app.start()  

