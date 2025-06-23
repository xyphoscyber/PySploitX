import platform
import psutil
import datetime
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class SystemSurvey(BaseModule):
    """Gathers extensive information about the target system."""

    def get_options(self):
        """Returns the options for this module."""
        return {
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """Executes the system survey."""
        console = Console()
        console.print("[*] Starting comprehensive system survey...")

        try:
            # OS Information
            os_info = platform.uname()
            console.print(Panel(
                f"[bold cyan]System:[/bold cyan] {os_info.system}\n"
                f"[bold cyan]Node Name:[/bold cyan] {os_info.node}\n"
                f"[bold cyan]Release:[/bold cyan] {os_info.release}\n"
                f"[bold cyan]Version:[/bold cyan] {os_info.version}\n"
                f"[bold cyan]Machine:[/bold cyan] {os_info.machine}\n"
                f"[bold cyan]Processor:[/bold cyan] {os_info.processor}",
                title="[bold]Operating System[/bold]", expand=False
            ))

            # CPU Information
            cpu_freq = psutil.cpu_freq()
            console.print(Panel(
                f"[bold cyan]Physical Cores:[/bold cyan] {psutil.cpu_count(logical=False)}\n"
                f"[bold cyan]Total Cores:[/bold cyan] {psutil.cpu_count(logical=True)}\n"
                f"[bold cyan]Max Frequency:[/bold cyan] {cpu_freq.max if cpu_freq else 'N/A'} Mhz\n"
                f"[bold cyan]Current Frequency:[/bold cyan] {cpu_freq.current if cpu_freq else 'N/A'} Mhz\n"
                f"[bold cyan]CPU Usage Per Core:[/bold cyan]\n" + 
                "\n".join([f"  Core {i}: {percent}%" for i, percent in enumerate(psutil.cpu_percent(percpu=True, interval=1))]),
                title="[bold]CPU Information[/bold]", expand=False
            ))

            # Memory Information
            svmem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            console.print(Panel(
                f"[bold cyan]Total Memory:[/bold cyan] {svmem.total / (1024**3):.2f} GB\n"
                f"[bold cyan]Available Memory:[/bold cyan] {svmem.available / (1024**3):.2f} GB\n"
                f"[bold cyan]Used Memory:[/bold cyan] {svmem.used / (1024**3):.2f} GB ({svmem.percent}%)\n"
                f"[bold cyan]Total Swap:[/bold cyan] {swap.total / (1024**3):.2f} GB\n"
                f"[bold cyan]Used Swap:[/bold cyan] {swap.used / (1024**3):.2f} GB ({swap.percent}%)",
                title="[bold]Memory Information[/bold]", expand=False
            ))

            # Disk Information
            disk_table = Table(title="Disk Partitions", show_header=True, header_style="bold magenta")
            disk_table.add_column("Device")
            disk_table.add_column("Mountpoint")
            disk_table.add_column("File System")
            disk_table.add_column("Total Size")
            disk_table.add_column("Used")
            disk_table.add_column("Free")
            disk_table.add_column("Usage %")
            partitions = psutil.disk_partitions()
            for p in partitions:
                try:
                    usage = psutil.disk_usage(p.mountpoint)
                    disk_table.add_row(
                        p.device, p.mountpoint, p.fstype,
                        f"{usage.total / (1024**3):.2f} GB",
                        f"{usage.used / (1024**3):.2f} GB",
                        f"{usage.free / (1024**3):.2f} GB",
                        f"{usage.percent}%"
                    )
                except (PermissionError, FileNotFoundError):
                    continue
            console.print(disk_table)

            # Network Information
            net_table = Table(title="Network Interfaces", show_header=True, header_style="bold magenta")
            net_table.add_column("Interface")
            net_table.add_column("Address Family")
            net_table.add_column("Address")
            net_table.add_column("Netmask")
            net_table.add_column("Broadcast")
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                for address in interface_addresses:
                    net_table.add_row(
                        interface_name,
                        str(address.family).split('.')[-1],
                        address.address,
                        address.netmask or "N/A",
                        address.broadcast or "N/A"
                    )
            console.print(net_table)

            # Logged in Users
            try:
                users = psutil.users()
                if users:
                    users_table = Table(title="Logged In Users", show_header=True, header_style="bold magenta")
                    users_table.add_column("Username")
                    users_table.add_column("Terminal")
                    users_table.add_column("Host")
                    users_table.add_column("Started")
                    for user in users:
                        users_table.add_row(
                            user.name,
                            user.terminal or "N/A",
                            user.host or "N/A",
                            datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
                        )
                    console.print(users_table)
            except (AttributeError, NotImplementedError):
                console.print("[*] Could not retrieve logged in users (not supported on this platform).")

            console.print("[bold green][+] System survey complete.[/bold green]")

        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
