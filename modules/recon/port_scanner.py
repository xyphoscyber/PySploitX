import socket
import threading
from queue import Queue
from core.base_module import BaseModule
from rich.console import Console

class PortScanner(BaseModule):
    """A simple TCP connect port scanner."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'RHOST': ['', 'The target host IP address.'],
            'PORTS': ['21,22,23,25,80,135,139,443,445,3306,3389,8080', 'Comma-separated list of ports to scan.'],
            'THREADS': [50, 'Number of threads to use.']
        }

    def _scan_port(self, host, port, console):
        """Scans a single port."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((host, port)) == 0:
                    console.print(f"[bold green][+] Port {port}/tcp is open[/bold green]")
        except (socket.timeout, socket.error):
            pass

    def _worker(self, q, host, console):
        """Worker thread function."""
        while not q.empty():
            port = q.get()
            self._scan_port(host, port, console)
            q.task_done()

    def run(self, options):
        """
        Executes the port scan.
        """
        rhost = options.get('RHOST')
        ports_str = options.get('PORTS')
        num_threads = int(options.get('THREADS'))
        console = Console()

        if not rhost:
            console.print("[!] RHOST must be set.", style="bold red")
            return

        try:
            ports = [int(p.strip()) for p in ports_str.split(',')]
        except ValueError:
            console.print("[!] Invalid port list. Please provide comma-separated numbers.", style="bold red")
            return

        console.print(f"[*] Starting TCP scan on {rhost} for {len(ports)} ports...")
        
        q = Queue()
        for port in ports:
            q.put(port)

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker, args=(q, rhost, console))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        q.join() # Wait for all ports to be scanned
        console.print("[*] Port scan complete.")