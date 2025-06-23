import subprocess
from core.base_module import BaseModule
from rich.console import Console

class CommandExecutor(BaseModule):
    """Executes a single command on the target system."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'CMD': ['whoami', 'The command to execute.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the specified command.
        """
        cmd = options.get('CMD')
        console = Console()

        if not cmd:
            console.print("[!] CMD option cannot be empty.", style="bold red")
            return

        console.print(f"[*] Executing command: {cmd}")

        try:
            # Using subprocess.run for better control and capturing output
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            console.print("[bold green][+] Command executed successfully.[/bold green]")
            if output:
                console.print(f"--- STDOUT ---\n{output}\n--------------")
            if error:
                console.print(f"--- STDERR ---\n{error}\n--------------")
            if not output and not error:
                console.print("[*] Command produced no output.")

        except FileNotFoundError:
            console.print(f"[!] Command not found: '{cmd.split()[0]}'. Is it in the system's PATH?", style="bold red")
        except subprocess.TimeoutExpired:
            console.print("[!] Command timed out after 30 seconds.", style="bold red")
        except Exception as e:
            console.print(f"[!] An error occurred while executing the command: {e}", style="bold red")
