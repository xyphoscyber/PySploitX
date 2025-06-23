import psutil
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class ProcessLister(BaseModule):
    """Lists running processes on the target system."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the process listing.
        """
        console = Console()
        console.print("[*] Listing running processes...")

        try:
            table = Table(title="Running Processes", show_header=True, header_style="bold magenta")
            table.add_column("PID", style="dim", width=6)
            table.add_column("Name", style="cyan")
            table.add_column("Username", style="yellow")
            table.add_column("CPU %", justify="right")
            table.add_column("Memory %", justify="right")

            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    # To get initial CPU percent, a small sleep is needed
                    pinfo['cpu_percent'] = proc.cpu_percent(interval=0.01)
                    table.add_row(
                        str(pinfo['pid']),
                        pinfo['name'],
                        pinfo['username'] or 'N/A',
                        f"{pinfo['cpu_percent']:.1f}",
                        f"{pinfo['memory_percent']:.1f}"
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            console.print(table)

        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
