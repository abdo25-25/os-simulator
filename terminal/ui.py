
import customtkinter as ctk
from terminal.logic import TerminalLogic

class HackerTerminal(ctk.CTkFrame):
    def __init__(self, parent, system_state, simulation_os):
        super().__init__(parent, fg_color="#050505", border_width=1, border_color="#00ff41")
        self.logic = TerminalLogic(system_state, simulation_os)
        
        # Output Area
        self.output = ctk.CTkTextbox(self, font=("Consolas", 14), fg_color="transparent", text_color="#00ff41")
        self.output.pack(padx=10, pady=(10, 5), fill="both", expand=True)
        self.output.insert("end", "SYSTEM TERMINAL v2.0.4\nTYPE 'HELP' FOR COMMANDS\n\n")
        self.output.configure(state="disabled")
        
        # Input Area
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(padx=10, pady=(0, 10), fill="x")
        
        ctk.CTkLabel(input_frame, text="> ", font=("Consolas", 16, "bold"), text_color="#00ff41").pack(side="left")
        
        self.entry = ctk.CTkEntry(input_frame, font=("Consolas", 14), fg_color="transparent", border_width=0, text_color="white")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

    def on_enter(self, event):
        cmd = self.entry.get().strip()
        if not cmd:
            return
        
        self.entry.delete(0, "end")
        self.write_output(f"> {cmd}\n")
        
        result = self.logic.execute(cmd)
        if result == "__CLEAR__":
            self.output.configure(state="normal")
            self.output.delete("1.0", "end")
            self.output.configure(state="disabled")
        elif result:
            self.write_output(f"{result}\n\n")

    def write_output(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")
