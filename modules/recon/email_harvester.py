from pyhunter import PyHunter
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class EmailHarvester(BaseModule):
    """Finds email addresses associated with a domain using the Hunter.io API."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DOMAIN': ['example.com', 'The target domain to search for emails.'],
            'HUNTER_API_KEY': ['', 'Your Hunter.io API key.']
        }

    def run(self, options):
        """
        Executes the email harvesting.
        """
        domain = options.get('DOMAIN')
        api_key = options.get('HUNTER_API_KEY')
        console = Console()

        if not api_key:
            console.print("[!] HUNTER_API_KEY is not set. Please set it using 'config HUNTER_API_KEY <your_key>'.", style="bold red")
            return

        if not domain:
            console.print("[!] DOMAIN option not set.", style="bold red")
            return

        try:
            console.print(f"[*] Searching for emails at '{domain}' using Hunter.io...")
            hunter = PyHunter(api_key)
            results = hunter.domain_search(domain=domain, limit=20, emails_type='personal')

            if not results or not results.get('emails'):
                console.print(f"[yellow]No emails found for '{domain}'.[/yellow]")
                return

            table = Table(title=f"Emails Found for {domain}")
            table.add_column("Email", style="cyan")
            table.add_column("Type")
            table.add_column("Confidence")
            table.add_column("Sources")

            for email_info in results['emails']:
                sources = ", ".join([src['domain'] for src in email_info.get('sources', [])[:2]])
                table.add_row(
                    email_info.get('value'),
                    email_info.get('type', 'N/A'),
                    str(email_info.get('confidence', 'N/A')),
                    sources
                )
            
            console.print(table)

        except Exception as e:
            console.print(f"[!] An error occurred: {e}", style="bold red")
