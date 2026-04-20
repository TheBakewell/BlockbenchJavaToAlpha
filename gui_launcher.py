import tkinter as tk
import os
from tkinter import filedialog, messagebox
import convert
# NOTE To compile it into exe: pyinstaller --onefile --noconsole gui_launcher.py
COLOR_BG = "#d4d0c8"
COLOR_BTN = "#d4d0c8"
COLOR_WHITE = "#ffffff"
COLOR_SHADOW = "#808080"

class AlphaConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bakewell's Alpha Model Converter")
        self.root.geometry("400x300")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.selected_file = None

        self.classic_font = ("Tahoma", 9)
        self.classic_font_bold = ("Tahoma", 9, "bold")

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=COLOR_BG)
        header.pack(fill="x", pady=(10, 5))

        title = tk.Label(
            header,
            text="Bakewell's Model Converter",
            bg=COLOR_BG,
            font=("Tahoma", 11, "bold")
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Convert modern (1.17+) Minecraft models → Alpha 1.1.2_01 format",
            bg=COLOR_BG,
            font=("Tahoma", 8)
        )
        subtitle.pack()

        # File section
        file_frame = tk.LabelFrame(
            self.root,
            text="Input File",
            bg=COLOR_BG,
            font=self.classic_font,
            relief="groove",
            bd=2
        )
        file_frame.pack(padx=15, pady=10, fill="x")

        name_frame = tk.LabelFrame(
            self.root,
            text="Output Model Name",
            bg=COLOR_BG,
            font=self.classic_font,
            relief="groove",
            bd=2
        )
        name_frame.pack(padx=15, pady=5, fill="x")

        self.model_name_var = tk.StringVar(value="ModelUnknown")

        self.name_entry = tk.Entry(
            name_frame,
            textvariable=self.model_name_var,
            font=self.classic_font
        )
        self.name_entry.pack(padx=10, pady=5, fill="x")


        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=COLOR_BG,
            font=("Tahoma", 8),
            fg="#333333"
        )
        self.status_label.pack(pady=(0, 5))

        self.entry_var = tk.StringVar(value="No file selected...")
        entry = tk.Entry(
            file_frame,
            textvariable=self.entry_var,
            state="readonly",
            font=self.classic_font
        )
        entry.pack(padx=10, pady=5, fill="x")

        

        # Buttons
        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(pady=10)

        self.create_button(btn_frame, "Browse", self.browse_file).pack(side="left", padx=5)
        self.create_button(btn_frame, "Convert", self.start_conversion, width=15).pack(side="left", padx=5)

    def create_button(self, parent, text, command, width=10):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg="#dcdad5",
            activebackground="#e8e6e1",
            relief="raised",
            bd=2,
            font=("Tahoma", 9, "bold"),
            cursor="hand2"
        )

    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Java files", "*.java")])
        if file:
            self.selected_file = file
            base_name = os.path.splitext(os.path.basename(file))[0]

            if base_name.lower().startswith("model"):
                base_name = base_name[5:]

            self.entry_var.set(os.path.basename(file))

            self.model_name_var.set("Model" + base_name)

            self.status_var.set(f"Loaded: {os.path.basename(file)}")

    def get_final_model_name(self):
        name = self.model_name_var.get().strip()

        if not name.startswith("Model"):
            name = "Model" + name

        return name

    def start_conversion(self):

        if not self.selected_file:
            messagebox.showwarning("Error", "Please select a file first!")
            self.status_var.set("Conversion failed.")
            return
        
        self.status_var.set("Converting...")
        self.root.update_idletasks()

        try:
            output_name = convert.run_conversion(self.selected_file, model_name=self.get_final_model_name())
            messagebox.showinfo("Success", f"Converted successfully!\nSaved as {output_name}")
            self.status_var.set(f"Done: {os.path.basename(output_name)}")
        except Exception as e:
            messagebox.showerror("Conversion Failed", f"Error: {str(e)}")
            self.status_var.set("Conversion failed.")

if __name__ == "__main__":
    
    root = tk.Tk()
    app = AlphaConverterGUI(root)
    root.mainloop()
