
import customtkinter as ctk
from gui.utils import center_window, StyledMessage
from gui.simulation_os import SimulationOS # Will be created next

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OS Security Login")
        center_window(self, 550, 750)
        
        self.admin_user, self.admin_pw = "admin", "123"
        self.user_user, self.user_pw = "user", "123"
        
        title_f = ctk.CTkFrame(self, fg_color="transparent")
        title_f.pack(pady=(60, 40))
        ctk.CTkLabel(title_f, text="OS", font=("Trebuchet MS", 80, "bold"), text_color="#3b8ed0").pack()
        ctk.CTkLabel(title_f, text="Simulation System", font=("Trebuchet MS", 28, "bold"), text_color="#555").pack()
        
        self.u_in = ctk.CTkEntry(self, placeholder_text="User name", width=400, height=65, font=("Arial", 20), justify="center")
        self.u_in.pack(pady=12); self.u_in.focus_set()
        self.p_in = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=400, height=65, font=("Arial", 20), justify="center")
        self.p_in.pack(pady=12)
        
        self.u_in.bind("<Return>", lambda e: self.p_in.focus_set())
        self.p_in.bind("<Return>", lambda e: self.login())
        
        ctk.CTkButton(self, text="Login", width=300, height=80, font=("Arial", 22, "bold"), command=self.login).pack(pady=35)
        
        self.f_btn = ctk.CTkButton(self, text="Forget Password?", fg_color="transparent", text_color="#3b8ed0", 
                                   font=("Arial", 16, "underline"), command=self.reset_pw)
        self.f_btn.pack(side="bottom", pady=60)

    def login(self):
        u, p = self.u_in.get().strip().lower(), self.p_in.get().strip()
        role = "admin" if u == self.admin_user and p == self.admin_pw else "user" if u == self.user_user and p == self.user_pw else None
        if role:
            self.withdraw()
            SimulationOS(self, role)
        else: StyledMessage(self, "Error", "Invalid Credentials!")

    def reset_pw(self):
        self.withdraw()
        win = ctk.CTkToplevel(self)
        win.title("Reset Account")
        center_window(win, 500, 550)
        win.attributes("-topmost", True)
        
        ctk.CTkLabel(win, text="Reset User Data", font=("Arial", 24, "bold")).pack(pady=40)
        nu = ctk.CTkEntry(win, placeholder_text="New Username", width=350, height=65, justify="center", font=("Arial", 20))
        nu.pack(pady=15); nu.focus_set()
        np = ctk.CTkEntry(win, placeholder_text="New Password", show="*", width=350, height=65, justify="center", font=("Arial", 20))
        np.pack(pady=15)
        
        nu.bind("<Return>", lambda e: np.focus_set())
        np.bind("<Return>", lambda e: save())

        def save():
            if nu.get().strip() and np.get().strip():
                self.user_user, self.user_pw = nu.get().strip().lower(), np.get().strip()
                StyledMessage(win, "Success", "Updated!", is_error=False)
                self.deiconify(); win.destroy()
        
        ctk.CTkButton(win, text="Save", width=220, height=70, font=("Arial", 18, "bold"), command=save).pack(side="bottom", pady=50)
        win.protocol("WM_DELETE_WINDOW", lambda: [self.deiconify(), win.destroy()])
