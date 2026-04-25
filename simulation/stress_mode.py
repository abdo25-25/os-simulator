
import random
import time
import threading

class StressMode:
    def __init__(self, system_state, simulation_os):
        self.system_state = system_state
        self.os = simulation_os
        self.active = False
        self.score = 0
        self.thread = None

    def toggle(self):
        if not self.active:
            self.active = True
            self.score = 0
            self.system_state.system_stability = 100
            self.thread = threading.Thread(target=self._run_stress, daemon=True)
            self.thread.start()
            return "STRESS MODE: ACTIVATED"
        else:
            self.active = False
            return "STRESS MODE: DEACTIVATED"

    def _run_stress(self):
        while self.active:
            # Randomly spawn heavy processes
            if random.random() < 0.3:
                name = f"STRESS_PROC_{random.randint(100, 999)}"
                mem = random.randint(10, 40)
                p = self.system_state.add_process(name, mem)
                p["base_cpu"] = random.randint(30, 60)
                self.system_state.allocate_memory(p["pid"], mem)
                self.os.log_io(f"STRESS: Spawned {name}")
            
            # Decrease stability if load is high
            if self.system_state.total_cpu_load > 85 or self.system_state.memory_pressure > 85:
                self.system_state.system_stability -= random.randint(1, 5)
            else:
                self.system_state.system_stability = min(100, self.system_state.system_stability + 1)
            
            # Check for crash
            if self.system_state.system_stability <= 0:
                self.os.log_io("CRITICAL FAILURE: SYSTEM CRASHED")
                self.active = False
                # Visual crash effect would go here
                break
                
            self.score += 10
            time.sleep(2)
