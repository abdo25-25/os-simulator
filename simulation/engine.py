
import threading
import time
import random
from core.system_state import SystemState

class SimulationEngine:
    def __init__(self):
        self.system_state = SystemState()
        self.running = False
        self.thread = None
        self.update_interval = 0.5 # Update every 0.5 seconds

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            self._update_processes()
            self._simulate_system_load()
            time.sleep(self.update_interval)

    def _update_processes(self):
        for process in self.system_state.processes:
            if process["pid"] == 1: # Kernel process
                process["cpu_usage"] = random.randint(1, 5)
                continue
            
            # Simulate dynamic CPU usage
            # Base usage + random fluctuation
            base_cpu = process.get("base_cpu", random.randint(5, 15))
            process["base_cpu"] = base_cpu
            fluctuation = random.randint(-5, 10)
            process["cpu_usage"] = max(0, min(100, base_cpu + fluctuation))

            # Simulate dynamic memory usage (growing/shrinking slightly)
            if random.random() < 0.1: # 10% chance to change memory
                change = random.choice([-1, 1])
                new_size = process["memory_blocks"] + change
                if 1 <= new_size <= 50: # Limit process size
                    # This is a simplified memory simulation for now
                    # Real allocation/deallocation logic would be more complex
                    process["memory_blocks"] = new_size

    def _simulate_system_load(self):
        # Calculate total system load
        total_cpu = sum(p["cpu_usage"] for p in self.system_state.processes)
        self.system_state.total_cpu_load = min(100, total_cpu)
        
        # Calculate memory pressure
        total_mem_used = self.system_state.get_memory_usage()
        self.system_state.memory_pressure = (total_mem_used / self.system_state.TOTAL_MEMORY_BLOCKS) * 100

        # Simulate random spikes or "lag" if load is high
        if self.system_state.total_cpu_load > 80:
            if random.random() < 0.2:
                # Potential "system lag" event
                pass 
