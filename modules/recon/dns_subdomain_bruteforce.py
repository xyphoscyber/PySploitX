import socket
import threading
from queue import Queue
from core.base_module import BaseModule
from rich.console import Console
from rich.progress import Progress

class DnsSubdomainBruteforce(BaseModule):
    """Bruteforces subdomains for a given domain using a wordlist."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DOMAIN': ['', 'The target domain (e.g., example.com).'],
            'WORDLIST': ['/usr/share/wordlists/dns/subdomains-top1000-5000.txt', 'Path to the subdomain wordlist.'],
            'THREADS': [20, 'Number of threads to use.']
        }

    def _worker(self, q, domain, progress, task, found_subdomains):
        """Worker thread function."""
        while not q.empty():
            subdomain = q.get()
            full_domain = f"{subdomain}.{domain}"
            try:
                # Resolve the domain name
                ip_address = socket.gethostbyname(full_domain)
                progress.console.print(f"[bold green][+] Found: {full_domain} -> {ip_address}[/bold green]")
                found_subdomains.append(full_domain)
            except socket.gaierror:
                # This means the subdomain does not exist
                pass
            except Exception as e:
                progress.console.print(f"[!] Error resolving {full_domain}: {e}", style="bold red")
            finally:
                progress.update(task, advance=1)
                q.task_done()

    def run(self, options):
        """
        Executes the subdomain bruteforce.
        """
        domain = options.get('DOMAIN')
        wordlist_path = options.get('WORDLIST')
        num_threads = int(options.get('THREADS'))
        console = Console()

        if not domain or not wordlist_path:
            console.print("[!] DOMAIN and WORDLIST must be set.", style="bold red")
            return

        try:
            with open(wordlist_path, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            console.print(f"[!] Wordlist not found at: {wordlist_path}", style="bold red")
            return

        q = Queue()
        for word in wordlist:
            q.put(word)

        found_subdomains = []
        threads = []

        with Progress(console=console) as progress:
            task = progress.add_task("[cyan]Bruteforcing subdomains...", total=len(wordlist))
            for _ in range(num_threads):
                thread = threading.Thread(target=self._worker, args=(q, domain, progress, task, found_subdomains))
                thread.daemon = True
                thread.start()
                threads.append(thread)

            q.join() # Wait for all tasks to be completed

        if found_subdomains:
            console.print(f"\n[bold green]Scan complete. Found {len(found_subdomains)} subdomains.[/bold green]")
        else:
            console.print("\n[*] Scan complete. No subdomains found with this wordlist.")
