import socket
from core.base_module import BaseModule

class DnsLookup(BaseModule):
    """Performs a DNS lookup to find the IP address for a domain."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DOMAIN': ['example.com', 'The domain to perform a DNS lookup on.']
        }

    def run(self, options):
        """
        Executes the DNS lookup.
        """
        domain = options.get('DOMAIN')
        if not domain:
            print("[!] DOMAIN option not set.")
            return

        try:
            ip_address = socket.gethostbyname(domain)
            print(f"[*] DNS lookup for '{domain}':")
            print(f"[+] IP Address: {ip_address}")
        except socket.gaierror:
            print(f"[!] Could not resolve host: {domain}")
        except Exception as e:
            print(f"[!] An error occurred: {e}")
