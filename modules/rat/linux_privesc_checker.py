import subprocess
import os
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class LinuxPrivescChecker(BaseModule):
    """Scans for common Linux privilege escalation vectors."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the privilege escalation checks.
        """
        console = Console()

        if os.name == 'nt':
            console.print("[!] This module is designed for Linux targets.", style="bold red")
            return

        console.print("[*] Starting Linux privilege escalation checks...")
        self.check_suid_binaries(console)
        self.check_writable_files(console)
        # Add more checks here in the future

        console.print("[*] Privilege escalation check complete.")

    def check_suid_binaries(self, console):
        """Finds SUID/SGID binaries which are often used for privesc."""
        console.print("\n[*] Searching for SUID/SGID binaries...")
        cmd = "find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            output = result.stdout.strip()
            if output:
                table = Table(title="Potentially Interesting SUID/SGID Files", show_header=True, header_style="bold magenta")
                table.add_column("Permissions", style="dim")
                table.add_column("Owner")
                table.add_column("Group")
                table.add_column("Path")
                
                common_bins = ['nmap', 'find', 'vim', 'bash', 'cp', 'mv', 'socat', 'python', 'perl', 'ruby']
                for line in output.split('\n'):
                    parts = line.split()
                    if len(parts) >= 10:
                        perms = parts[2]
                        owner = parts[4]
                        group = parts[5]
                        path = parts[10]
                        is_highlighted = any(bin_name in path for bin_name in common_bins)
                        style = "yellow" if is_highlighted else ""
                        table.add_row(perms, owner, group, path, style=style)
                console.print(table)
            else:
                console.print("[*] No SUID/SGID binaries found.")
        except Exception as e:
            console.print(f"[!] Failed to check for SUID binaries: {e}", style="bold red")

    def check_writable_files(self, console):
        """Finds world-writable files and directories."""
        console.print("\n[*] Searching for world-writable files and directories...")
        # Implement this check similarly to the SUID check
        console.print("[*] World-writable file check not yet implemented.")
