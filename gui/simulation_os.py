
import customtkinter as ctk
from datetime import datetime
from gui.utils import center_window, StyledMessage, CustomDialog
from core.system_state import SystemState
from core.config import OS_SIM_WINDOW_DIMENSIONS, KERNEL_MEMORY_BLOCKS
from simulation.engine import SimulationEngine
from visualization.dashboard import FuturisticDashboard
from ai_engine.assistant import AIAssistant
from ai_engine.ai_panel import AIPanel
from terminal.ui import HackerTerminal
from simulation.stress_mode import StressMode

class SimulationOS(ctk.CTkToplevel):
    def __init__(self, login_screen, role):
        super().__init__()
        self.login_screen = login_screen
        self.role = role
        center_window(self, 1450, 950) 
        self.title(f"OS Simulation - {role.upper()}")
        self.protocol("WM_DELETE_WINDOW", self.logout) 

        self.system_state = SystemState() 
        self.sim_engine = SimulationEngine()
        self.sim_engine.start()
        self.ai_assistant = AIAssistant(self.system_state)
        self.stress_mode = StressMode(self.system_state, self)

        # UI Elements
        self.create_widgets()
        self.log_io("System initialized and ready.")
        self.update_ui_periodically()

    def update_ui_periodically(self):
        # Update Dashboard
        self.dashboard.update_metrics()
        
        # Update AI Status
        self.ai_panel.update_ai_status()

        # Update dynamic parts of the UI
        current_tab = self.tabs.get()
        if current_tab == "Process Manager":
            self.update_pm_view()
        elif current_tab == "Memory Map":
            self.update_mem_view()
        
        # Schedule next update
        self.after(1000, self.update_ui_periodically)

    def create_widgets(self):
        # Header with Dashboard
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=150)
        self.header_frame.pack(padx=20, pady=(10, 0), fill="x")
        
        # Logout Button in header
        ctk.CTkButton(self.header_frame, text="⬅ LOGOUT", width=120, height=40, fg_color="#d32f2f", font=("Orbitron", 12, "bold"), command=self.logout).pack(side="left", padx=10)
        
        # Dashboard Integration
        self.dashboard = FuturisticDashboard(self.header_frame, self.system_state)
        self.dashboard.pack(side="right", fill="x", expand=True)

        # Main Content Area (AI Panel + Tabs)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(padx=20, pady=(10, 20), fill="both", expand=True)
        
        # AI Panel (Left side)
        self.ai_panel = AIPanel(self.main_container, self.ai_assistant)
        self.ai_panel.pack(side="left", fill="y", padx=(0, 10))

        # Tabview (Right side)
        self.tabs = ctk.CTkTabview(self.main_container, width=1050, height=750)
        self.tabs.pack(side="right", fill="both", expand=True)
        
        # Stress Mode Button (Bottom Right)
        self.stress_btn = ctk.CTkButton(self, text="INITIATE STRESS MODE", fg_color="#555", font=("Orbitron", 12, "bold"), command=self.toggle_stress)
        self.stress_btn.place(relx=0.98, rely=0.05, anchor="ne")

        # Setup individual tabs
        self.setup_fs_tab()
        self.setup_pm_tab()
        self.setup_mem_tab()
        self.setup_terminal_tab()
        self.setup_io_tab()

    def logout(self):
        self.sim_engine.stop()
        self.withdraw()
        self.login_screen.deiconify()

    def log_io(self, msg):
        time_str = datetime.now().strftime("%H:%M:%S")
        self.io_box.insert("end", f"[{time_str}] {msg}\n")
        self.io_box.see("end")

    def ask(self, t, p, multi=False, choice=False, labels=("Yes", "No"), content="", ro=False):
        d = CustomDialog(self, t, p, is_multiline=multi, show_choice=choice, labels=labels, content=content, readonly=ro)
        self.wait_window(d)
        return d.choice if choice else d.result

    # --- File System Tab ---
    def setup_fs_tab(self):
        tab = self.tabs.add("File System")
        self.fs_view = ctk.CTkTextbox(tab, font=("Consolas", 18), fg_color="#0a0a0a", text_color="#00ff41", border_width=1, border_color="#333")
        self.fs_view.pack(pady=15, fill="both", expand=True)
        btn_f = ctk.CTkFrame(tab, fg_color="transparent"); btn_f.pack(pady=25)
        ctk.CTkButton(btn_f, text="CREATE FILE", width=280, height=75, font=("Orbitron", 16, "bold"), border_width=1, border_color="#00d4ff", command=self.create_f).grid(row=0, column=0, padx=20)
        ctk.CTkButton(btn_f, text="OPEN FILE", width=280, height=75, font=("Orbitron", 16, "bold"), border_width=1, border_color="#00d4ff", command=self.read_f).grid(row=0, column=1, padx=20)
        ctk.CTkButton(btn_f, text="DELETE FILE", width=280, height=75, font=("Orbitron", 16, "bold"), fg_color="#d32f2f", border_width=1, border_color="#ff4b2b", command=self.del_f).grid(row=0, column=2, padx=20)
        self.update_fs_view()

    def create_f(self):
        n = self.ask("New File", "Enter Filename:")
        if n:
            content = self.ask("Editor", f"Writing content for: {n}", multi=True)
            self.system_state.add_file(n, content)
            self.log_io(f"File \'{n}\' created."); self.update_fs_view()

    def read_f(self):
        n = self.ask("Open", "Filename to open:")
        files = self.system_state.get_files()
        sys_files = self.system_state.get_sys_files()
        if n in files:
            ro = (self.role == "user" and n in sys_files)
            res = self.ask("Editor", f"Viewing: {n}", multi=True, content=files[n], readonly=ro)
            if not ro and res is not None:
                self.system_state.add_file(n, res) # Update file content
                self.log_io(f"File \'{n}\' updated.")
        else: StyledMessage(self, "Error", "File not found.")

    def del_f(self):
        n = self.ask("Delete", "Filename to delete:")
        files = self.system_state.get_files()
        sys_files = self.system_state.get_sys_files()
        if n in files:
            if n in sys_files and self.role != "admin": StyledMessage(self, "Denied", "Admin only!"); return
            self.system_state.delete_file(n)
            self.log_io(f"File \'{n}\' deleted."); self.update_fs_view()
        else: StyledMessage(self, "Error", "File not found.")

    def update_fs_view(self):
        self.fs_view.delete("1.0", "end")
        self.fs_view.insert("end", f"{'Filename':<30} | {'Type'}\n" + "-"*45 + "\n")
        files = self.system_state.get_files()
        sys_files = self.system_state.get_sys_files()
        for n in files: self.fs_view.insert("end", f"{n:<30} | {'[SYS]' if n in sys_files else 'FILE'}\n")

    # --- Process Manager Tab ---
    def setup_pm_tab(self):
        tab = self.tabs.add("Process Manager")
        self.pm_view = ctk.CTkTextbox(tab, font=("Consolas", 18), fg_color="#0a0a0a", text_color="#00d4ff", border_width=1, border_color="#333")
        self.pm_view.pack(pady=15, fill="both", expand=True)
        btn_f = ctk.CTkFrame(tab, fg_color="transparent"); btn_f.pack(pady=25)
        ctk.CTkButton(btn_f, text="INITIATE PROCESS", width=350, height=80, font=("Orbitron", 18, "bold"), border_width=1, border_color="#00d4ff", command=self.new_p).grid(row=0, column=0, padx=25)
        ctk.CTkButton(btn_f, text="TERMINATE PROCESS", width=350, height=80, font=("Orbitron", 18, "bold"), fg_color="#d32f2f", border_width=1, border_color="#ff4b2b", command=self.kill_p).grid(row=0, column=1, padx=25)
        self.update_pm_view()

    def new_p(self):
        n = self.ask("Process", "Process Name:")
        if n:
            # For now, memory blocks are asked here. This will be part of advanced simulation later.
            sz = self.ask("Memory Size", "Number of blocks to allocate (optional):")
            memory_blocks = int(sz) if sz and sz.isdigit() else 0

            new_process = self.system_state.add_process(n, memory_blocks)
            if memory_blocks > 0:
                if not self.system_state.allocate_memory(new_process["pid"], memory_blocks):
                    StyledMessage(self, "Memory", "Could not allocate contiguous memory for process!")
                    self.system_state.remove_process(new_process["pid"]) # Remove process if memory allocation fails
                    self.log_io(f"Failed to create process \'{n}\' due to memory.")
                    return

            self.log_io(f"New process \'{n}\' (PID {new_process['pid']}) started."); self.update_pm_view(); self.update_mem_view()

    def kill_p(self):
        n = self.ask("Kill", "Process Name:")
        process_to_kill = self.system_state.get_process_by_name(n)
        if process_to_kill:
            if process_to_kill['pid'] == 1 and self.role != "admin": StyledMessage(self, "Denied", "System Protection!"); return
            self.system_state.remove_process(process_to_kill['pid'])
            self.log_io(f"Process \'{n}\' terminated."); self.update_pm_view(); self.update_mem_view()
        else: StyledMessage(self, "Error", "Process not found.")

    def update_pm_view(self):
        # Save current scroll position
        scroll_pos = self.pm_view.yview()
        self.pm_view.delete("1.0", "end")
        header = f"{'PID':<10} | {'Process Name':<20} | {'CPU %':<10} | {'MEM (Blocks)':<15}\n"
        self.pm_view.insert("end", header + "-"*60 + "\n")
        for p in self.system_state.processes:
            line = f"{p['pid']:<10} | {p['name']:<20} | {p['cpu_usage']:<10}% | {p['memory_blocks']:<15}\n"
            self.pm_view.insert("end", line)
        # Restore scroll position
        self.pm_view.yview_moveto(scroll_pos[0])

    # --- Memory Map Tab ---
    def setup_mem_tab(self):
        tab = self.tabs.add("Memory Map")
        self.current_page = 0
        nav = ctk.CTkFrame(tab, fg_color="transparent"); nav.pack(pady=10)
        for i in range(10):
            ctk.CTkButton(nav, text=f"Page {i+1}", width=125, height=50, font=("Arial", 12, "bold"), 
                          command=lambda idx=i: self.switch_mem_page(idx)).grid(row=0, column=i, padx=4)
        
        self.m_scroll = ctk.CTkScrollableFrame(tab, fg_color="#121212", height=550)
        self.m_scroll.pack(fill="both", expand=True, padx=25, pady=15)
        for c in range(10): self.m_scroll.grid_columnconfigure(c, weight=1)
        
        btn_f = ctk.CTkFrame(tab, fg_color="transparent"); btn_f.pack(pady=10)
        ctk.CTkButton(btn_f, text="Manual Allocation", width=300, height=50, font=("Arial", 18, "bold"), command=self.man_alloc_ui).pack()
        self.update_mem_view()

    def switch_mem_page(self, idx): self.current_page = idx; self.update_mem_view()

    def update_mem_view(self):
        for w in self.m_scroll.winfo_children(): w.destroy()
        start = self.current_page * 100
        memory_map = self.system_state.get_memory_map()
        processes = self.system_state.processes

        for i in range(start, start + 100):
            pid = memory_map[i]
            if not pid:
                bg, tx, lbl, border = ("#121212", "#555", f"{i}", "#333")
            else:
                p = next((x for x in processes if x['pid'] == pid), None)
                bg = p['color'] if p else "#d32f2f"
                tx, lbl, border = ("white", f"PID:{pid}", "white")
            
            cell = ctk.CTkFrame(self.m_scroll, fg_color=bg, height=65, corner_radius=4, border_width=1, border_color=border)
            cell.grid(row=(i-start)//10, column=(i-start)%10, padx=2, pady=2, sticky="nsew")
            ctk.CTkLabel(cell, text=lbl, text_color=tx, font=("Orbitron", 10, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    def man_alloc_ui(self):
        pid_str = self.ask("Manual Allocation", "Enter PID to allocate:")
        idx_str = self.ask("Manual Allocation", "Enter Block Index (0-999):")
        if pid_str and idx_str and idx_str.isdigit():
            pid = int(pid_str)
            idx = int(idx_str)
            if 0 <= idx < KERNEL_MEMORY_BLOCKS: # Prevent manual allocation in kernel space
                StyledMessage(self, "Denied", "Cannot manually allocate in kernel memory space!"); return
            if 0 <= idx < self.system_state.TOTAL_MEMORY_BLOCKS:
                if self.system_state.get_process_by_pid(pid):
                    self.system_state.memory[idx] = pid
                    self.log_io(f"Manual allocation: block {idx} -> PID {pid}"); self.update_mem_view()
                else:
                    StyledMessage(self, "Error", "PID not found.")
            else:
                StyledMessage(self, "Error", "Invalid block index.")

    # --- I/O System Tab ---
    def setup_terminal_tab(self):
        tab = self.tabs.add("Terminal")
        self.terminal = HackerTerminal(tab, self.system_state, self)
        self.terminal.pack(padx=10, pady=10, fill="both", expand=True)

    def toggle_stress(self):
        msg = self.stress_mode.toggle()
        self.log_io(msg)
        if self.stress_mode.active:
            self.stress_btn.configure(text="ABORT STRESS MODE", fg_color="#d32f2f")
        else:
            self.stress_btn.configure(text="INITIATE STRESS MODE", fg_color="#555")

    def setup_io_tab(self):
        tab = self.tabs.add("I/O System")
        self.io_box = ctk.CTkTextbox(tab, font=("Consolas", 18), fg_color="#0a0a0a", text_color="#ff007f", border_width=1, border_color="#333")
        self.io_box.pack(pady=10, fill="both", expand=True)
        f = ctk.CTkFrame(tab, fg_color="transparent"); f.pack(pady=20)
        ctk.CTkButton(f, text="INPUT SIGNAL", width=250, height=60, font=("Orbitron", 12, "bold"), border_width=1, border_color="#ff007f", command=lambda: self.log_io("Keyboard Input Detected")).grid(row=0, column=0, padx=15)
        ctk.CTkButton(f, text="OUTPUT SIGNAL", width=250, height=60, font=("Orbitron", 12, "bold"), border_width=1, border_color="#ff007f", command=lambda: self.log_io("Sending to Buffer")).grid(row=0, column=1, padx=15)
