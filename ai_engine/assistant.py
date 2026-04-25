
import random

class AIAssistant:
    def __init__(self, system_state):
        self.system_state = system_state
        self.last_analysis = ""
        self.recommendations = []

    def analyze_system(self):
        self.recommendations = []
        cpu = self.system_state.total_cpu_load
        mem = self.system_state.memory_pressure
        
        analysis = f"AI ANALYSIS AT {random.randint(1000, 9999)}ms:\n"
        
        if cpu > 80:
            analysis += "CRITICAL: CPU load exceeding safety thresholds.\n"
            heavy_proc = sorted(self.system_state.processes, key=lambda x: x['cpu_usage'], reverse=True)[0]
            self.recommendations.append(f"Terminate high-load process: {heavy_proc['name']} (PID:{heavy_proc['pid']})")
        elif cpu > 50:
            analysis += "WARNING: Moderate CPU activity detected.\n"
        else:
            analysis += "STATUS: CPU operations nominal.\n"
            
        if mem > 80:
            analysis += "CRITICAL: Memory pressure high. Fragmentation imminent.\n"
            self.recommendations.append("Initiate memory defragmentation.")
        elif mem > 60:
            analysis += "WARNING: Memory usage rising.\n"
            
        if not self.recommendations:
            self.recommendations.append("System optimized. No action required.")
            
        self.last_analysis = analysis
        return analysis, self.recommendations

    def get_quick_insight(self):
        insights = [
            "Kernel integrity: 100%",
            "I/O latency: 0.02ms",
            "Network handshake: Secure",
            "Encryption layers: Active",
            "Neural link: Stable"
        ]
        return random.choice(insights)
