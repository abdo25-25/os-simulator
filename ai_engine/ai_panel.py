
import customtkinter as ctk

class AIPanel(ctk.CTkFrame):
    def __init__(self, parent, ai_assistant):
        super().__init__(parent, fg_color="#0a0a0a", border_width=1, border_color="#00d4ff")
        self.ai = ai_assistant
        
        # Title
        ctk.CTkLabel(self, text="AI CORE ASSISTANT", font=("Orbitron", 16, "bold"), text_color="#00d4ff").pack(pady=10)
        
        # Analysis Box
        self.analysis_box = ctk.CTkTextbox(self, height=150, font=("Consolas", 12), fg_color="transparent", text_color="#00ff41")
        self.analysis_box.pack(padx=10, pady=5, fill="x")
        
        # Recommendations
        ctk.CTkLabel(self, text="RECOMMENDATIONS:", font=("Orbitron", 12, "bold"), text_color="#ff007f").pack(pady=(10, 0))
        self.rec_box = ctk.CTkTextbox(self, height=100, font=("Consolas", 12), fg_color="transparent", text_color="white")
        self.rec_box.pack(padx=10, pady=5, fill="x")
        
        # Quick Insight
        self.insight_label = ctk.CTkLabel(self, text="Insight: Initializing...", font=("Consolas", 10, "italic"), text_color="#555")
        self.insight_label.pack(side="bottom", pady=10)

    def update_ai_status(self):
        analysis, recs = self.ai.analyze_system()
        
        self.analysis_box.delete("1.0", "end")
        self.analysis_box.insert("end", analysis)
        
        self.rec_box.delete("1.0", "end")
        for r in recs:
            self.rec_box.insert("end", f"> {r}\n")
            
        self.insight_label.configure(text=f"Insight: {self.ai.get_quick_insight()}")
