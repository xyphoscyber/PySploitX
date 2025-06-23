from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

try:
    import dns.resolver
    import dns.zone
    import dns.query
except ImportError:
    pass

class DnsZoneTransfer(BaseModule):
    """Attempts a DNS Zone Transfer (AXFR)."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DOMAIN': ['', 'The target domain to query.']
        }

    def run(self, options):
        """
        Executes the DNS zone transfer attempt.
        """
        domain = options.get('DOMAIN')
        console = Console()

        if not domain:
            console.print("[!] DOMAIN must be set.", style="bold red")
            return

        console.print(f"[*] Attempting DNS Zone Transfer for {domain}...")

        try:
            # Find the nameservers for the domain
            ns_records = dns.resolver.resolve(domain, 'NS')
            nameservers = [str(ns.target) for ns in ns_records]
            console.print(f"[*] Found nameservers: {', '.join(nameservers)}")

            found_records = False
            for ns in nameservers:
                console.print(f"[*] Querying nameserver: {ns}")
                try:
                    # Attempt the zone transfer
                    zone = dns.zone.from_xfr(dns.query.xfr(ns, domain, timeout=10))
                    
                    if zone:
                        console.print(f"[bold green][+] Zone transfer successful from {ns}![/bold green]")
                        found_records = True
                        table = Table(title=f"DNS Records from {ns}", show_header=True, header_style="bold magenta")
                        table.add_column("Name", style="cyan")
                        table.add_column("TTL", style="yellow")
                        table.add_column("Type", style="green")
                        table.add_column("Value", style="white")

                        for name, node in zone.nodes.items():
                            for rdataset in node.rdatasets:
                                for rdata in rdataset:
                                    table.add_row(str(name), str(rdataset.ttl), str(dns.rdatatype.to_text(rdataset.rdtype)), str(rdata))
                        console.print(table)
                        break # Stop after the first successful transfer

                except dns.exception.FormError:
                    console.print(f"[-] Zone transfer failed for {ns}: FormError - Server might not support AXFR.", style="yellow")
                except dns.exception.Timeout:
                    console.print(f"[-] Zone transfer failed for {ns}: Timeout.", style="yellow")
                except Exception as e:
                    console.print(f"[-] Zone transfer failed for {ns}: {e}", style="yellow")
            
            if not found_records:
                console.print("[*] No servers allowed a zone transfer.")

        except dns.resolver.NoNameservers:
            console.print(f"[!] Could not find any nameservers for {domain}.", style="bold red")
        except dns.resolver.NXDOMAIN:
            console.print(f"[!] The domain {domain} does not exist.", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
