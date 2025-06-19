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

from blackout.core import Blackout
import argparse
import os


def build_parser():
    parser = argparse.ArgumentParser(
        description="Blackout: Raw packet network flooder",
        epilog="You need root privileges to run this script.",
        add_help=False,
    )

    host = parser.add_argument_group("Target Settings")
    host.add_argument("host", help="Targe host or IP address")
    host.add_argument("-p", "--port", default=80, type=int, help="Port to flood")

    flood = parser.add_argument_group("Flood Settings")
    flood.add_argument(
        "-m",
        "--mode",
        default="SYN",
        type=str.upper,
        help="Flood mode to use (SYN, ACK, FIN, RST, UDP)",
    )
    flood.add_argument(
        "-t", "--threads", default=1, type=int, help="Number of threads to use"
    )

    meta = parser.add_argument_group("Information")
    meta.add_argument("-h", "--help", action="help", help="Show this help menu")
    meta.add_argument(
        "-v",
        "--version",
        action="version",
        version="Blackout v1.0.0",
        help="Show program version",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not os.geteuid() == 0:
        parser.error("you must run this script with root privileges.")

    blackout = Blackout()
    blackout.run(target=args.host, port=args.port, flag=args.mode, threads=args.threads)
