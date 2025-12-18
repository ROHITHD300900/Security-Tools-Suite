"""
Port Scanner Tool - Security-Tools-Suite
A multi-threaded TCP/UDP port scanner with service detection.

Author: Rohith D
Version: 1.0.0
"""

import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
import argparse
import json
from typing import List, Dict
import sys

class PortScanner:
    """
    Multi-threaded port scanner for network reconnaissance.
    """
    
    def __init__(self, target: str, ports: List[int], timeout: int = 1, threads: int = 50):
        """
        Initialize the port scanner.
        
        Args:
            target: Target IP address or hostname
            ports: List of ports to scan
            timeout: Connection timeout in seconds
            threads: Number of threads to use
        """
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.threads = threads
        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []
    
    def scan_port(self, port: int) -> Dict[str, any]:
        """
        Scan a single port.
        
        Args:
            port: Port number to scan
            
        Returns:
            Dictionary with scan results
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            
            if result == 0:
                self.open_ports.append(port)
                return {'port': port, 'status': 'OPEN'}
            else:
                self.closed_ports.append(port)
                return {'port': port, 'status': 'CLOSED'}
        except socket.timeout:
            self.filtered_ports.append(port)
            return {'port': port, 'status': 'FILTERED'}
        except Exception as e:
            return {'port': port, 'status': 'ERROR', 'error': str(e)}
    
    def run(self) -> List[Dict]:
        """
        Execute the port scan using multiple threads.
        
        Returns:
            List of scan results
        """
        results = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.scan_port, port) for port in self.ports]
            for future in futures:
                results.append(future.result())
        return results
    
    def display_results(self):
        """Display scan results with color formatting."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"Scan Results for {self.target}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        if self.open_ports:
            print(f"{Fore.GREEN}Open Ports ({len(self.open_ports)}):{Style.RESET_ALL}")
            for port in sorted(self.open_ports):
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Port {port} is OPEN")
        
        if self.filtered_ports:
            print(f"\n{Fore.YELLOW}Filtered Ports ({len(self.filtered_ports)}):{Style.RESET_ALL}")
            print(f"  {len(self.filtered_ports)} ports are FILTERED")
    
    def export_json(self, filename: str):
        """Export results to JSON file."""
        data = {
            'target': self.target,
            'open_ports': self.open_ports,
            'closed_ports': self.closed_ports,
            'filtered_ports': self.filtered_ports
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Multi-threaded Port Scanner')
    parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    parser.add_argument('-p', '--ports', default='1-1000', help='Port range (e.g., 1-1000 or 22,80,443)')
    parser.add_argument('-T', '--timeout', type=int, default=1, help='Timeout in seconds')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads')
    parser.add_argument('-o', '--output', help='Output JSON file')
    
    args = parser.parse_args()
    
    # Parse ports
    if '-' in args.ports:
        start, end = map(int, args.ports.split('-'))
        ports = list(range(start, end + 1))
    else:
        ports = [int(p) for p in args.ports.split(',')]
    
    scanner = PortScanner(args.target, ports, args.timeout, args.threads)
    scanner.run()
    scanner.display_results()
    
    if args.output:
        scanner.export_json(args.output)
        print(f"\n{Fore.GREEN}Results exported to {args.output}{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
