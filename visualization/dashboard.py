
import customtkinter as ctk

class FuturisticDashboard(ctk.CTkFrame):
    def __init__(self, parent, system_state):
        super().__init__(parent, fg_color="transparent")
        self.system_state = system_state
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        # CPU Metric
        self.cpu_frame = self.create_metric_tile("CPU LOAD", "0%", "#00d4ff")
        self.cpu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Memory Metric
        self.mem_frame = self.create_metric_tile("MEMORY PRESSURE", "0%", "#ff007f")
        self.mem_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Stability Metric
        self.stab_frame = self.create_metric_tile("SYSTEM STABILITY", "100%", "#39ff14")
        self.stab_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    def create_metric_tile(self, title, value, color):
        frame = ctk.CTkFrame(self, fg_color="#1a1a1a", border_width=2, border_color=color)
        ctk.CTkLabel(frame, text=title, font=("Orbitron", 14, "bold"), text_color=color).pack(pady=(10, 0))
        label = ctk.CTkLabel(frame, text=value, font=("Orbitron", 32, "bold"), text_color="white")
        label.pack(pady=(5, 10))
        
        # Store label for updates
        if "CPU" in title: self.cpu_label = label
        elif "MEMORY" in title: self.mem_label = label
        elif "STABILITY" in title: self.stab_label = label
        
        return frame

    def update_metrics(self):
        self.cpu_label.configure(text=f"{int(self.system_state.total_cpu_load)}%")
        self.mem_label.configure(text=f"{int(self.system_state.memory_pressure)}%")
        self.stab_label.configure(text=f"{int(self.system_state.system_stability)}%")
        
        # Dynamic color changing based on pressure
        if self.system_state.total_cpu_load > 80: self.cpu_label.configure(text_color="#ff4b2b")
        else: self.cpu_label.configure(text_color="white")
        
        if self.system_state.memory_pressure > 80: self.mem_label.configure(text_color="#ff4b2b")
        else: self.mem_label.configure(text_color="white")
