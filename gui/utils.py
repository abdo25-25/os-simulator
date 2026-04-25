
import customtkinter as ctk

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class StyledMessage(ctk.CTkToplevel):
    def __init__(self, parent, title, message, is_error=True):
        super().__init__(parent)
        self.title(title)
        center_window(self, 400, 250)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        
        icon = "❌" if is_error else "✅"
        color = "#d32f2f" if is_error else "#2e7d32"
        ctk.CTkLabel(self, text=icon, font=("Arial", 50)).pack(pady=(25, 5))
        ctk.CTkLabel(self, text=message, font=("Arial", 16, "bold"), text_color=color, wraplength=350).pack(pady=10)
        ctk.CTkButton(self, text="OK", width=140, height=45, command=self.destroy).pack(pady=20)

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, prompt, is_multiline=False, show_choice=False, labels=("Yes", "No"), content="", readonly=False):
        super().__init__(parent)
        self.title(title)
        center_window(self, 650, 500)
        self.attributes("-topmost", True)
        self.result = None
        self.choice = None

        ctk.CTkLabel(self, text=prompt, font=("Trebuchet MS", 22, "bold"), text_color="#3b8ed0", wraplength=600).pack(pady=(35, 15))

        if show_choice:
            btn_f = ctk.CTkFrame(self, fg_color="transparent")
            btn_f.pack(pady=50)
            ctk.CTkButton(btn_f, text=labels[0], width=200, height=80, font=("Arial", 20, "bold"), command=lambda: self.set_choice(True)).pack(side="left", padx=20)
            ctk.CTkButton(btn_f, text=labels[1], width=200, height=80, font=("Arial", 20, "bold"), fg_color="#555", command=lambda: self.set_choice(False)).pack(side="left", padx=20)
        else:
            if is_multiline:
                self.txt = ctk.CTkTextbox(self, width=550, height=250, font=("Arial", 16), fg_color="white", text_color="black")
                self.txt.pack(pady=10); self.txt.focus_set()
                if content: self.txt.insert("1.0", content)
                if readonly: self.txt.configure(state="disabled")
                else:
                    self.txt.bind("<Shift-Return>", lambda e: None)
                    self.txt.bind("<Return>", self.handle_enter)
            else:
                self.ent = ctk.CTkEntry(self, width=500, height=70, font=("Arial", 22), justify="center")
                self.ent.pack(pady=20); self.ent.focus_set()
                self.ent.bind("<Return>", lambda e: self.on_submit())

            if not readonly:
                ctk.CTkButton(self, text="Confirm", width=300, height=80, font=("Arial", 22, "bold"), command=self.on_submit).pack(side="bottom", pady=40)
            else:
                ctk.CTkButton(self, text="Close", width=300, height=80, font=("Arial", 22, "bold"), command=self.destroy).pack(side="bottom", pady=40)

    def handle_enter(self, event):
        if not (event.state & 0x0001):
            self.on_submit()
            return "break"

    def set_choice(self, val): self.choice = val; self.destroy()
    def on_submit(self):
        if hasattr(self, 'ent'): self.result = self.ent.get().strip()
        elif hasattr(self, 'txt'): self.result = self.txt.get("1.0", "end-1c").strip()
        self.destroy()
