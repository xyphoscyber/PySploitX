import whois
from core.base_module import BaseModule
from rich.console import Console
from rich.panel import Panel

class WhoisLookup(BaseModule):
    """Retrieves WHOIS information for a given domain."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DOMAIN': ['', 'The target domain to look up (e.g., example.com).']
        }

    def run(self, options):
        """
        Executes the WHOIS lookup.
        """
        domain_name = options.get('DOMAIN')
        console = Console()

        if not domain_name:
            console.print("[!] DOMAIN must be set.", style="bold red")
            return

        console.print(f"[*] Performing WHOIS lookup for {domain_name}...")

        try:
            w = whois.whois(domain_name)
            
            if w.domain_name:
                info_text = ""
                for key, value in w.items():
                    if value:
                        # Format lists nicely
                        if isinstance(value, list):
                            value_str = '\n'.join([f"  - {v}" for v in value])
                            info_text += f"[bold cyan]{key.replace('_', ' ').title()}:[/bold cyan]\n{value_str}\n"
                        else:
                            info_text += f"[bold cyan]{key.replace('_', ' ').title()}:[/bold cyan] {value}\n"
                
                console.print(Panel(
                    info_text.strip(),
                    title=f"[bold]WHOIS Information for {w.domain_name}[/bold]",
                    expand=False
                ))
            else:
                console.print(f"[!] Could not retrieve WHOIS information for {domain_name}. The domain may not exist or the TLD is not supported.", style="bold red")

        except whois.parser.PywhoisError as e:
            console.print(f"[!] WHOIS lookup failed: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")