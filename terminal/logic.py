
class TerminalLogic:
    def __init__(self, system_state, simulation_os):
        self.system_state = system_state
        self.os = simulation_os
        self.commands = {
            "help": self.cmd_help,
            "ps": self.cmd_ps,
            "kill": self.cmd_kill,
            "clear": self.cmd_clear,
            "ls": self.cmd_ls,
            "whoami": self.cmd_whoami,
            "sysinfo": self.cmd_sysinfo
        }

    def execute(self, command_line):
        parts = command_line.strip().split()
        if not parts:
            return ""
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in self.commands:
            return self.commands[cmd](args)
        else:
            return f"Command not found: {cmd}. Type 'help' for available commands."

    def cmd_help(self, args):
        help_text = "AVAILABLE COMMANDS:\n"
        help_text += "  ps       - List active processes\n"
        help_text += "  kill [N] - Terminate process by name or PID\n"
        help_text += "  ls       - List files in system\n"
        help_text += "  sysinfo  - Display system specifications\n"
        help_text += "  whoami   - Display current user role\n"
        help_text += "  clear    - Clear terminal output\n"
        return help_text

    def cmd_ps(self, args):
        output = f"{'PID':<10} | {'NAME':<20} | {'CPU %':<10}\n"
        output += "-" * 45 + "\n"
        for p in self.system_state.processes:
            output += f"{p['pid']:<10} | {p['name']:<20} | {p['cpu_usage']:<10}%\n"
        return output

    def cmd_kill(self, args):
        if not args:
            return "Usage: kill [Process Name or PID]"
        target = args[0]
        # Try PID first
        p = None
        if target.isdigit():
            p = self.system_state.get_process_by_pid(int(target))
        else:
            p = self.system_state.get_process_by_name(target)
            
        if p:
            if p['pid'] == 1 and self.os.role != "admin":
                return "ACCESS DENIED: Cannot terminate kernel process."
            self.system_state.remove_process(p['pid'])
            self.os.update_pm_view()
            self.os.update_mem_view()
            return f"Process {p['name']} (PID:{p['pid']}) terminated successfully."
        return f"Error: Process '{target}' not found."

    def cmd_ls(self, args):
        output = "FILESYSTEM CONTENTS:\n"
        for f in self.system_state.get_files():
            is_sys = "[SYS]" if f in self.system_state.get_sys_files() else ""
            output += f"  {f:<25} {is_sys}\n"
        return output

    def cmd_whoami(self, args):
        return f"Current Session: {self.os.role.upper()}\nSecurity Clearance: Level {'5' if self.os.role == 'admin' else '1'}"

    def cmd_sysinfo(self, args):
        return (f"OS ARCHITECTURE: X-64 FUTURISTIC\n"
                f"KERNEL VERSION: 4.2.0-SIM\n"
                f"TOTAL MEMORY: {self.system_state.TOTAL_MEMORY_BLOCKS} blocks\n"
                f"CPU CORES: 128 Simulated Threads\n"
                f"AI STATUS: ONLINE")

    def cmd_clear(self, args):
        return "__CLEAR__"
