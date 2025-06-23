import requests
import socket
from core.base_module import BaseModule
from rich.console import Console

class SubdomainScanner(BaseModule):
    """Scans for subdomains of a given domain using a built-in wordlist."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DOMAIN': ['example.com', 'The target domain to scan for subdomains.']
        }

    def run(self, options):
        """
        Executes the subdomain scan.
        """
        domain = options.get('DOMAIN')
        console = Console()

        if not domain:
            console.print("[!] DOMAIN option not set.", style="bold red")
            return

        # A small, common wordlist for demonstration.
        # In a real scenario, this would be much larger or configurable.
        wordlist = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'admin', 'cpanel', 'webdisk', 'autodiscover', 'm', 'support', 'dev',
            'test', 'api', 'shop', 'blog', 'news', 'forum', 'vpn', 'portal'
        ]

        console.print(f"[*] Starting subdomain scan for '{domain}'...")
        found_subdomains = []

        for sub in wordlist:
            full_domain = f"{sub}.{domain}"
            try:
                # Check if the domain resolves
                ip = socket.gethostbyname(full_domain)
                console.print(f"[green][+] Found: {full_domain} ({ip})[/green]")
                found_subdomains.append(full_domain)
            except socket.gaierror:
                # Doesn't resolve, so we can ignore it
                pass
            except Exception as e:
                console.print(f"[yellow][!] Error checking {full_domain}: {e}[/yellow]")

        if found_subdomains:
            console.print(f"\n[bold green]Scan complete. Found {len(found_subdomains)} subdomains.[/bold green]")
        else:
            console.print(f"\n[yellow]Scan complete. No subdomains found from the list.[/yellow]")
