import shodan
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class ShodanScanner(BaseModule):
    """Queries the Shodan API for information on a target IP or domain."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'TARGET': ['example.com', 'The target IP address or domain.'],
            'SHODAN_API_KEY': ['', 'Your Shodan API key.']
        }

    def run(self, options):
        """
        Executes the Shodan scan.
        """
        target = options.get('TARGET')
        api_key = options.get('SHODAN_API_KEY')
        console = Console()

        if not api_key:
            console.print("[!] SHODAN_API_KEY is not set. Please set it using 'config SHODAN_API_KEY <your_key>'.", style="bold red")
            return

        if not target:
            console.print("[!] TARGET option not set.", style="bold red")
            return

        try:
            api = shodan.Shodan(api_key)
            console.print(f"[*] Querying Shodan for '{target}'...")
            
            # For domains, we resolve to IP first as Shodan primarily works with IPs
            try:
                import socket
                ip_address = socket.gethostbyname(target)
                console.print(f"[*] Resolved '{target}' to {ip_address}")
                host_info = api.host(ip_address)
            except socket.gaierror:
                # If it's not a domain, assume it's an IP
                host_info = api.host(target)

            table = Table(title=f"Shodan Information for {host_info.get('ip_str')}")
            table.add_column("Property", style="cyan")
            table.add_column("Value")

            table.add_row("Organization", str(host_info.get('org', 'N/A')))
            table.add_row("Operating System", str(host_info.get('os', 'N/A')))
            table.add_row("Country", str(host_info.get('country_name', 'N/A')))
            table.add_row("City", str(host_info.get('city', 'N/A')))
            table.add_row("Last Update", str(host_info.get('last_update', 'N/A')))
            table.add_row("Hostnames", ", ".join(host_info.get('hostnames', [])))
            
            console.print(table)

            if host_info.get('data'):
                ports_table = Table(title="Open Ports and Services")
                ports_table.add_column("Port", style="magenta")
                ports_table.add_column("Banner")
                for item in host_info['data']:
                    port = str(item['port'])
                    banner_data = item.get('data', 'No banner data').strip()
                    ports_table.add_row(port, banner_data)
                console.print(ports_table)

        except shodan.APIError as e:
            console.print(f"[!] Shodan API error: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
