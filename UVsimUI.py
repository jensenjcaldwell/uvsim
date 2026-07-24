from turtle import color
import classes
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import re
from io import StringIO

_COLOR_SCHEME_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "color_scheme.txt")


class OutputCapture(StringIO):
    def __init__(self, ui, original_stdout):
        super().__init__()
        self.ui = ui
        self.original_stdout = original_stdout

    def write(self, s):
        if s and hasattr(self.ui, "output_console"):
            self.ui.output_console.config(state="normal")
            self.ui.output_console.insert(tk.END, s)
            self.ui.output_console.see(tk.END)
            self.ui.output_console.config(state="disabled")
            self.ui.root.update_idletasks()

        return len(s)

    def flush(self):
        pass


class UVsimUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UVsim")
        self.root.geometry("800x700")

        self.primary_color = ""
        self.off_color = ""

        file = open(_COLOR_SCHEME_PATH)
        content = file.readlines()
        self.primary_color = content[0].strip()
        self.off_color = content[1].strip()
        file.close()
        self.root.configure(bg=self.primary_color)

        self.style = ttk.Style()
        self.style.configure("TButton", foreground=self.primary_color)

        self.sim = classes.simulator()
        self.register_value_labels = {}
        self.last_output = ""

        self.tabs = []
        self.active_tab_id = None
        self._next_tab_id = 0

        self._build_ui()

        self._original_stdout = sys.stdout
        sys.stdout = OutputCapture(self, self._original_stdout)

        self.refresh_ui()

    def update_changes(self):
        for tab in self.tabs:
            tab["editor"].configure(
                bg=self.off_color,
                fg=self.primary_color
            )

        self.output_console.config(bg=self.off_color, fg=self.primary_color)
        self.output_console.config(state="disabled")
        self.style.configure("TButton", foreground=self.primary_color)
        self._restyle_tabs()
        self.root.update_idletasks()


    def _format_register_value(self, value):
        if isinstance(value, classes.Instruction):
            return f"{value.sign}{value.code:02d}{value.operand:02d}"
        return str(value)

    def refresh_ui(self):
        self.accumulator_value.config(
            text=f"Accumulator: {self.sim.accumulator}"
        )

    def create_editor_tab(self, title="Untitled", file_contents=""):
        tab_id = self._next_tab_id
        self._next_tab_id += 1

        editor_frame = ttk.Frame(self.editor_container)

        editor = tk.Text(
            editor_frame,
            width=60,
            height=15,
            font=("Consolas", 12),
            bg=self.off_color,
            fg=self.primary_color
        )
        editor.pack(side="left", fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            editor_frame,
            command=editor.yview
        )
        scrollbar.pack(side="right", fill="y")

        editor.config(yscrollcommand=scrollbar.set)
        editor.insert("1.0", file_contents)

        # Stack every tab's editor in the same spot; tkraise() picks the visible one.
        editor_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        button_frame = tk.Frame(self.tab_bar, bd=1, relief="raised")
        button_frame.pack(side="left", padx=(0, 2), pady=2)

        title_label = tk.Label(button_frame, text=title, padx=8, pady=4, cursor="hand2")
        title_label.pack(side="left")

        close_label = tk.Label(button_frame, text="×", padx=6, pady=4, cursor="hand2", fg="#8a1f1f")
        close_label.pack(side="left")

        tab = {
            "id": tab_id,
            "title": title,
            "editor_frame": editor_frame,
            "editor": editor,
            "button_frame": button_frame,
            "title_label": title_label,
            "close_label": close_label,
        }
        self.tabs.append(tab)

        title_label.bind("<Button-1>", lambda _event, tid=tab_id: self.select_tab(tid))
        button_frame.bind("<Button-1>", lambda _event, tid=tab_id: self.select_tab(tid))
        close_label.bind("<Button-1>", lambda _event, tid=tab_id: self.close_tab(tid))

        self.select_tab(tab_id)

        return editor

    def _find_tab(self, tab_id):
        return next((tab for tab in self.tabs if tab["id"] == tab_id), None)

    def select_tab(self, tab_id):
        if self._find_tab(tab_id) is None:
            return

        self.active_tab_id = tab_id
        self._restyle_tabs()
        self._find_tab(tab_id)["editor_frame"].tkraise()

    def _restyle_tabs(self):
        active_bg = self.off_color
        inactive_bg = "#d9d9d9"

        for tab in self.tabs:
            is_active = tab["id"] == self.active_tab_id
            bg = active_bg if is_active else inactive_bg

            tab["button_frame"].config(relief="sunken" if is_active else "raised", bg=bg)
            tab["title_label"].config(bg=bg, fg=self.primary_color)
            tab["close_label"].config(bg=bg)

    def get_active_editor(self):
        tab = self._find_tab(self.active_tab_id)
        return tab["editor"] if tab else None

    def rename_active_tab(self, new_title):
        tab = self._find_tab(self.active_tab_id)
        if tab is None:
            return
        tab["title"] = new_title
        tab["title_label"].config(text=new_title)

    def _show_run_header(self):
        tab = self._find_tab(self.active_tab_id)
        file_name = tab["title"] if tab else "program"

        self.output_console.config(state="normal")
        self.output_console.tag_configure(
            "run_header",
            foreground="#999999",
            font=("Consolas", 10, "italic")
        )
        self.output_console.insert(tk.END, f"Running {file_name}\n", "run_header")
        self.output_console.config(state="disabled")

    def close_tab(self, tab_id):
        index = next((i for i, tab in enumerate(self.tabs) if tab["id"] == tab_id), None)
        if index is None:
            return

        tab = self.tabs.pop(index)
        tab["button_frame"].destroy()
        tab["editor_frame"].destroy()

        if not self.tabs:
            self.create_editor_tab("Untitled")
            return

        if self.active_tab_id == tab_id:
            new_index = min(index, len(self.tabs) - 1)
            self.select_tab(self.tabs[new_index]["id"])

    def _prompt_for_signed_word(self):
        popup = tk.Toplevel(self.root)
        popup.title("READ Input")
        popup.transient(self.root)
        popup.grab_set()

        ttk.Label(popup, text="Enter a 4-digit number, with optional sign:").pack(padx=12, pady=(12, 6))
        value_entry = ttk.Entry(popup, width=16)
        value_entry.pack(padx=12, pady=6)
        value_entry.focus_set()

        error_label = ttk.Label(popup, text="", foreground="red")
        error_label.pack(padx=12, pady=(0, 6))

        result = {"value": None}

        def submit_value():
            raw = value_entry.get().strip()
            if not re.fullmatch(r"[+-]?\d{4}", raw):
                error_label.config(text="Use format 1234, +1234, or -0042")
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
            self.output_console.config(state="normal")
            self.output_console.delete("1.0", tk.END)
            self.output_console.config(state="disabled")

            self.sim = classes.simulator()

            active_editor = self.get_active_editor()

            if active_editor is None:
                messagebox.showerror(
                    "No Active File",
                    "There is no active program tab to run."
                )
                return

            self._show_run_header()

            raw_code = active_editor.get("1.0", tk.END).strip()

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

    def browse_file(self):
        selected_file = filedialog.askopenfilename(
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if not selected_file:
            return

        try:
            with open(selected_file, "r", encoding="utf-8") as file_handle:
                file_contents = file_handle.read()

            try:
                normalized_lines = classes.normalize_program_lines(file_contents.splitlines())
                file_contents = "\n".join(normalized_lines)
            except ValueError:
                # Keep original file text when it is not a valid UVSim program.
                pass

            file_name = os.path.basename(selected_file)

            self.create_editor_tab(
                title=file_name,
                file_contents=file_contents
            )

        except OSError as error:
            messagebox.showerror(
                "File Error",
                f"Could not open the selected file:\n{error}"
            )

    def save_program(self):
        active_editor = self.get_active_editor()

        if active_editor is None:
            messagebox.showerror(
                "No Active File",
                "There is no active program tab to save."
            )
            return

        target_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not target_file:
            return

        program_text = active_editor.get("1.0", tk.END).rstrip()

        try:
            with open(target_file, "w", encoding="utf-8") as file_handle:
                file_handle.write(program_text)

            file_name = os.path.basename(target_file)
            self.rename_active_tab(file_name)

        except OSError as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the file:\n{error}"
            )

    def color_theme_window(self):
        default_primary = "#4C721D"
        default_off_color = "#FFFFFF"

        popup = tk.Toplevel(self.root)
        popup.title("Color theme selection")
        top_label = ttk.Label(popup, text="select color scheme")
        primary_label = ttk.Label(popup, text="Primary:")
        primary_box = ttk.Entry(popup)
        primary_box.insert(0,self.primary_color)
        off_color_label = ttk.Label(popup, text="Off-color:")
        off_color_box = ttk.Entry(popup)
        off_color_box.insert(0,self.off_color)
        
        def reset_colors():
            classes.saved_colors(default_primary,default_off_color)
            primary_box.delete(0,tk.END)
            off_color_box.delete(0,tk.END)
            primary_box.insert(0,default_primary)
            off_color_box.insert(0,default_off_color)
            self.primary_color = default_primary
            self.off_color = default_off_color
            self.root.configure(bg=self.primary_color)
            self.update_changes()


        def get_color_info():
            primary_input = primary_box.get().strip()
            off_color_input = off_color_box.get().strip()

            if (classes.is_Valid_Hex(primary_input) and classes.is_Valid_Hex(off_color_input)):
                classes.saved_colors(primary_input,off_color_input)
                self.primary_color = primary_input
                self.off_color = off_color_input
                self.root.configure(bg=self.primary_color)
                self.update_changes()

            else:
                bad_popup = tk.Toplevel(self.root)
                bad_popup.title("invalid hex")
                bad_label = ttk.Label(bad_popup, text="one or two of the hex colors is incorrect, setting colors to default")
                bad_label.grid(row=0,column=0,columnspan=2,pady=20)
                reset_colors()

        save = ttk.Button(popup, text="save",command=get_color_info)
        reset = ttk.Button(popup, text="reset",command=reset_colors)
        top_label.grid(row=0,column=0,columnspan=2,pady=20)
        primary_label.grid(row=1,column=0,pady=5)
        primary_box.grid(row=1,column=1,pady=5)
        off_color_label.grid(row=2,column=0,pady=20)
        off_color_box.grid(row=2,column=1,pady=20)
        save.grid(row=3,column=0,columnspan=1,pady=20)
        reset.grid(row=3,column=1,columnspan=1,pady=20)

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

        self.btn_theme = ttk.Button(control_frame, text="Color Theme",command=self.color_theme_window)
        self.btn_theme.pack(side="right", padx=5)

        self.accumulator_value = ttk.Label(
            control_frame,
            text=f"Accumulator: {self.sim.accumulator}"
        )
        self.accumulator_value.pack(side="right", padx=10)

        editor_frame = ttk.LabelFrame(self.root, text=" BasicML Code Editor ", padding=(10, 10))
        editor_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.tab_bar = tk.Frame(editor_frame, bg=self.off_color)
        self.tab_bar.pack(side="top", fill=tk.X)

        self.editor_container = ttk.Frame(editor_frame)
        self.editor_container.pack(side="top", fill=tk.BOTH, expand=True)

        # Start the program with one empty editor tab.
        self.create_editor_tab("Untitled")

        output_frame = ttk.LabelFrame(self.root, text=" Program Output ", padding=(10, 10))
        output_frame.pack(pady=(0, 15), padx=20, fill=tk.X) # Pushed to the bottom

        self.output_console = tk.Text(output_frame, height=5, state="disabled", bg=self.off_color, font=("Consolas", 10))
        self.output_console.pack(side="left", fill=tk.X, expand=True)
        
        out_scroll = ttk.Scrollbar(output_frame, command=self.output_console.yview)
        out_scroll.pack(side="left", fill="y")
        self.output_console.config(yscrollcommand=out_scroll.set)
        
    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = UVsimUI()
    app.start()  
