"""
Password Strength Analyzer - Security-Tools-Suite
Analyze password strength with entropy calculation and crack time estimation.

Author: Rohith D
Version: 1.0.0
"""

import math
import re
from typing import Dict
from colorama import Fore, Style
import argparse

class PasswordAnalyzer:
    """
    Analyzes password strength based on multiple criteria.
    """
    
    CRACK_SPEEDS = {
        'online': 100,  # guesses per second
        'offline': 1e9,  # guesses per second
        'gpu': 1e11,  # guesses per second
    }
    
    def __init__(self, password: str):
        """
        Initialize the password analyzer.
        
        Args:
            password: Password to analyze
        """
        self.password = password
        self.length = len(password)
        self.metrics = {}
    
    def calculate_entropy(self) -> float:
        """
        Calculate password entropy.
        
        Returns:
            Entropy value in bits
        """
        charset_size = 0
        
        if re.search(r'[a-z]', self.password):
            charset_size += 26
        if re.search(r'[A-Z]', self.password):
            charset_size += 26
        if re.search(r'[0-9]', self.password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'\"\\|,.<>?/]', self.password):
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        entropy = self.length * math.log2(charset_size)
        return entropy
    
    def estimate_crack_time(self, entropy: float, speed: str = 'online') -> str:
        """
        Estimate time to crack the password.
        
        Args:
            entropy: Entropy in bits
            speed: Crack speed ('online', 'offline', 'gpu')
            
        Returns:
            Human-readable time estimate
        """
        possibilities = 2 ** entropy
        guesses_per_second = self.CRACK_SPEEDS.get(speed, 100)
        seconds = possibilities / guesses_per_second / 2  # on average
        
        if seconds < 1:
            return 'Less than 1 second'
        elif seconds < 60:
            return f'{int(seconds)} seconds'
        elif seconds < 3600:
            return f'{int(seconds/60)} minutes'
        elif seconds < 86400:
            return f'{int(seconds/3600)} hours'
        elif seconds < 2592000:
            return f'{int(seconds/86400)} days'
        elif seconds < 31536000:
            return f'{int(seconds/2592000)} months'
        else:
            return f'{int(seconds/31536000)} years'
    
    def check_common_patterns(self) -> Dict[str, bool]:
        """
        Check for common password patterns.
        
        Returns:
            Dictionary of pattern checks
        """
        return {
            'has_lowercase': bool(re.search(r'[a-z]', self.password)),
            'has_uppercase': bool(re.search(r'[A-Z]', self.password)),
            'has_numbers': bool(re.search(r'[0-9]', self.password)),
            'has_special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'\"\\|,.<>?/]', self.password)),
            'no_spaces': ' ' not in self.password,
            'sufficient_length': self.length >= 12,
        }
    
    def get_strength_rating(self, entropy: float) -> str:
        """
        Get password strength rating based on entropy.
        
        Args:
            entropy: Entropy in bits
            
        Returns:
            Strength rating
        """
        if entropy < 30:
            return 'Very Weak'
        elif entropy < 50:
            return 'Weak'
        elif entropy < 70:
            return 'Fair'
        elif entropy < 90:
            return 'Good'
        elif entropy < 120:
            return 'Strong'
        else:
            return 'Very Strong'
    
    def analyze(self) -> Dict:
        """
        Perform complete password analysis.
        
        Returns:
            Dictionary with all analysis results
        """
        entropy = self.calculate_entropy()
        patterns = self.check_common_patterns()
        strength = self.get_strength_rating(entropy)
        
        return {
            'password_length': self.length,
            'entropy_bits': round(entropy, 2),
            'strength': strength,
            'patterns': patterns,
            'crack_time_online': self.estimate_crack_time(entropy, 'online'),
            'crack_time_offline': self.estimate_crack_time(entropy, 'offline'),
            'crack_time_gpu': self.estimate_crack_time(entropy, 'gpu'),
        }
    
    def display_results(self):
        """Display analysis results with color formatting."""
        results = self.analyze()
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"Password Strength Analysis")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        strength = results['strength']
        if strength in ['Very Weak', 'Weak']:
            color = Fore.RED
        elif strength in ['Fair']:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
        
        print(f"Strength: {color}{strength}{Style.RESET_ALL}")
        print(f"Entropy: {results['entropy_bits']} bits")
        print(f"Length: {results['password_length']} characters\n")
        
        print(f"{Fore.CYAN}Crack Time Estimates:{Style.RESET_ALL}")
        print(f"  Online (100 guesses/sec): {results['crack_time_online']}")
        print(f"  Offline (1B guesses/sec): {results['crack_time_offline']}")
        print(f"  GPU Attack (100B guesses/sec): {results['crack_time_gpu']}\n")
        
        print(f"{Fore.CYAN}Pattern Analysis:{Style.RESET_ALL}")
        for pattern, present in results['patterns'].items():
            status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if present else f"{Fore.RED}✗{Style.RESET_ALL}"
            print(f"  {status} {pattern.replace('_', ' ').title()}")


def main():
    parser = argparse.ArgumentParser(description='Password Strength Analyzer')
    parser.add_argument('-p', '--password', required=True, help='Password to analyze')
    
    args = parser.parse_args()
    
    analyzer = PasswordAnalyzer(args.password)
    analyzer.display_results()


if __name__ == '__main__':
    main()
