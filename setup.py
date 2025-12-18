"""
Setup configuration for Security-Tools-Suite
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Security-Tools-Suite",
    version="1.0.0",
    author="Rohith D",
    author_email="rohithd300900@gmail.com",
    description="A comprehensive Python-based collection of security tools for penetration testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ROHITHD300900/Security-Tools-Suite",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Security Professionals",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "BeautifulSoup4>=4.12.0",
        "paramiko>=3.4.0",
        "Scapy>=2.5.0",
        "colorama>=0.4.6",
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "port-scanner=port_scanner:main",
            "password-analyzer=password_analyzer:main",
        ],
    },
)
