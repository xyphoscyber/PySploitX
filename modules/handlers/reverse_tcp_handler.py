import socket
import threading
from core.base_module import BaseModule
from core.session_manager import SESSIONS
from rich.console import Console

class ReverseTcpHandler(BaseModule):
    """Listens for incoming TCP connections (reverse shell)."""

    def get_options(self):
        """Returns the options for this module."""
        return {
            'LHOST': ['0.0.0.0', 'The local host to listen on.'],
            'LPORT': [4444, 'The local port to listen on.']
        }

    def _listener_thread(self, lhost, lport, console):
        """The main thread that listens for connections."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((lhost, lport))
                s.listen()
                console.print(f"[*] Handler started. Listening on {lhost}:{lport}...")
                
                while getattr(threading.current_thread(), "keep_running", True):
                    s.settimeout(1.0) # Timeout to check keep_running flag
                    try:
                        conn, addr = s.accept()
                        SESSIONS.create_session(conn, addr)
                    except socket.timeout:
                        continue
        except Exception as e:
            console.print(f"[!] Listener failed: {e}", style="bold red")

    def run(self, options):
        """Starts the handler."""
        lhost = options.get('LHOST')
        lport = int(options.get('LPORT'))
        console = Console()

        # The handler needs to run in the background to not block the main CLI
        # We will fully implement this backgrounding logic in the main pysploitx.py file.
        # For now, this module just defines the logic.
        console.print("[*] Starting Reverse TCP Handler in a background thread...")
        console.print("[*] When a session connects, use the 'sessions' command to see and interact with it.")
        
        listener = threading.Thread(target=self._listener_thread, args=(lhost, lport, console), daemon=True)
        listener.start()

        # In the final implementation, the main CLI will manage this thread.
        # For now, we just let it run.