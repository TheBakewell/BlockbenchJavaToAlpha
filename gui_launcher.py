import tkinter as tk
from tkinter import filedialog, messagebox
import convert
# To compile it into exe: pyinstaller --onefile --noconsole gui_launcher.py
COLOR_BG = "#d4d0c8"
COLOR_BTN = "#d4d0c8"
COLOR_WHITE = "#ffffff"
COLOR_SHADOW = "#808080"

class AlphaConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bakewell's Alpha Model Converter")
        self.root.geometry("400x200")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.selected_file = None

        self.classic_font = ("Tahoma", 9)
        self.classic_font_bold = ("Tahoma", 9, "bold")

        self.setup_ui()

    def setup_ui(self):
        lbl = tk.Label(self.root, text="Select a .java Model File made for MC 1.17+:", bg=COLOR_BG, font=self.classic_font)
        lbl.pack(pady=(20, 5))

        self.entry_var = tk.StringVar(value="No file selected...")
        entry = tk.Entry(self.root, textvariable=self.entry_var, width=50, state='readonly', 
                         relief="sunken", bd=2, font=self.classic_font)
        entry.pack(padx=20, pady=5)

        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(pady=20)

        self.create_retro_button(btn_frame, "Browse...", self.browse_file).pack(side="left", padx=5)

        self.create_retro_button(btn_frame, "Convert!", self.start_conversion, width=15).pack(side="left", padx=5)

    def create_retro_button(self, parent, text, command, width=10):
        return tk.Button(parent, text=text, command=command, width=width,
                         bg=COLOR_BTN, font=self.classic_font,
                         relief="raised", bd=2, activebackground=COLOR_BTN)

    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Java files", "*.java")])
        if file:
            self.selected_file = file
            self.entry_var.set(os.path.basename(file))

    def start_conversion(self):
        if not self.selected_file:
            messagebox.showwarning("Error", "Please select a file first!")
            return
        
        try:
            output_name = convert.run_conversion(self.selected_file)
            messagebox.showinfo("Success", f"Converted successfully!\nSaved as {output_name}")
        except Exception as e:
            messagebox.showerror("Conversion Failed", f"Error: {str(e)}")

if __name__ == "__main__":
    import os
    root = tk.Tk()
    app = AlphaConverterGUI(root)
    root.mainloop()