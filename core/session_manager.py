import threading
from rich.console import Console
from rich.table import Table

class Session:
    """Represents a single active connection from a target."""
    def __init__(self, id, conn, addr):
        self.id = id
        self.conn = conn
        self.addr = addr
        self.is_active = True

    def send(self, data):
        """Send data to the target."""
        try:
            self.conn.sendall(data.encode('utf-8'))
            return True
        except (BrokenPipeError, ConnectionResetError):
            self.is_active = False
            return False

    def recv(self, buffer_size=4096):
        """Receive data from the target."""
        try:
            return self.conn.recv(buffer_size).decode('utf-8', 'ignore')
        except (ConnectionResetError, OSError):
            self.is_active = False
            return None

    def close(self):
        """Close the session connection."""
        self.is_active = False
        self.conn.close()

    def shell(self, console):
        """Enter an interactive shell with the target."""
        console.print(f"[bold green]Entering interactive shell for Session {self.id}...[/bold green]")
        console.print("[yellow]Type 'exit' or 'background' to leave the shell.[/yellow]")
        
        while self.is_active:
            try:
                cmd = console.input(f"[bold cyan]shell@{self.addr[0]}> [/bold cyan]")
                if cmd.lower() in ['exit', 'quit']:
                    break
                if cmd.lower() == 'background':
                    console.print("[*] Backgrounding session.")
                    break
                if not cmd:
                    continue

                if self.send(cmd + '\\n'):
                    response = self.recv()
                    if response:
                        console.print(response.strip())
                    else:
                        console.print("[red]Connection lost.[/red]")
                        break
                else:
                    console.print("[red]Connection lost.[/red]")
                    break
            except KeyboardInterrupt:
                console.print("\\n[*] Backgrounding session.")
                break
        
        console.print(f"[*] Exited shell for Session {self.id}.")


class SessionManager:
    """Manages all active sessions."""
    def __init__(self):
        self.sessions = {}
        self.next_id = 1
        self.lock = threading.Lock()
        self.console = Console()

    def create_session(self, conn, addr):
        """Creates and stores a new session."""
        with self.lock:
            session_id = self.next_id
            session = Session(session_id, conn, addr)
            self.sessions[session_id] = session
            self.next_id += 1
            self.console.print(f"\\n[bold green][+] Session {session_id} opened ({addr[0]}:{addr[1]})[/bold green]")
            return session_id

    def list_sessions(self):
        """Prints a table of all active sessions."""
        table = Table(title="Active Sessions")
        table.add_column("ID", style="cyan")
        table.add_column("Target Address", style="magenta")
        table.add_column("Status", style="green")

        with self.lock:
            if not self.sessions:
                self.console.print("[*] No active sessions.")
                return
            
            # Check for dead sessions before listing
            dead_sessions = [sid for sid, s in self.sessions.items() if not s.is_active]
            for sid in dead_sessions:
                self.sessions.pop(sid, None)

            for session_id, session in self.sessions.items():
                status = "Active" if session.is_active else "Closed"
                table.add_row(str(session_id), f"{session.addr[0]}:{session.addr[1]}", status)
        
        self.console.print(table)

    def get_session(self, session_id):
        """Retrieves a session by its ID."""
        with self.lock:
            return self.sessions.get(session_id)

    def close_session(self, session_id):
        """Closes a specific session."""
        session = self.get_session(session_id)
        if session:
            session.close()
            with self.lock:
                self.sessions.pop(session_id, None)
            self.console.print(f"[*] Session {session_id} closed.")
        else:
            self.console.print("[!] Invalid session ID.", style="bold red")

# Global instance
SESSIONS = SessionManager()