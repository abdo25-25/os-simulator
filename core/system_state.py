
import random
from core.config import TOTAL_MEMORY_BLOCKS, KERNEL_MEMORY_BLOCKS, PROCESS_COLORS

class SystemState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemState, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        import threading
        self.lock = threading.Lock()
        self.TOTAL_MEMORY_BLOCKS = TOTAL_MEMORY_BLOCKS
        self.files = {"kernel.sys": "Locked", "boot.log": "OK", "readme.txt": "Welcome"}
        self.sys_files = ["kernel.sys", "boot.log"]
        self.processes = [] 
        self.memory = [None] * TOTAL_MEMORY_BLOCKS
        self.next_pid = 2 
        
        # Simulation Metrics
        self.total_cpu_load = 0
        self.memory_pressure = 0
        self.system_stability = 100

        # Initialize Kernel_Core process
        kernel_process = {"pid": 1, "name": "Kernel_Core", "color": "#7f1d1d", "cpu_usage": 2, "memory_blocks": KERNEL_MEMORY_BLOCKS}
        self.processes.append(kernel_process)

        for i in range(KERNEL_MEMORY_BLOCKS):
            self.memory[i] = 1

    def get_next_pid(self):
        pid = self.next_pid
        self.next_pid += 1
        return pid

    def add_process(self, name, memory_blocks=0):
        pid = self.get_next_pid()
        color = random.choice(PROCESS_COLORS)
        new_process = {"pid": pid, "name": name, "color": color, "cpu_usage": 0, "memory_blocks": memory_blocks}
        self.processes.append(new_process)
        return new_process

    def remove_process(self, pid):
        self.processes = [p for p in self.processes if p["pid"] != pid]
        for i in range(TOTAL_MEMORY_BLOCKS):
            if self.memory[i] == pid:
                self.memory[i] = None

    def allocate_memory(self, pid, size):
        # Simple first-fit allocation for now
        for i in range(KERNEL_MEMORY_BLOCKS, TOTAL_MEMORY_BLOCKS - size + 1):
            if all(self.memory[x] is None for x in range(i, i + size)):
                for j in range(i, i + size):
                    self.memory[j] = pid
                return True
        return False

    def deallocate_memory(self, pid):
        for i in range(TOTAL_MEMORY_BLOCKS):
            if self.memory[i] == pid:
                self.memory[i] = None

    def get_process_by_pid(self, pid):
        return next((p for p in self.processes if p["pid"] == pid), None)

    def get_process_by_name(self, name):
        return next((p for p in self.processes if p["name"] == name), None)

    def get_memory_usage(self):
        return len([block for block in self.memory if block is not None])

    def get_free_memory(self):
        return TOTAL_MEMORY_BLOCKS - self.get_memory_usage()

    def get_memory_map(self):
        return self.memory

    def get_files(self):
        return self.files

    def get_sys_files(self):
        return self.sys_files

    def add_file(self, name, content):
        self.files[name] = content

    def delete_file(self, name):
        if name in self.files:
            del self.files[name]

