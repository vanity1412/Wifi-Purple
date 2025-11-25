# 🌐 WiFi-Purple - Advanced WiFi Security Testing Tool

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-purple)
![Python](https://img.shields.io/badge/python-3.6+-blue)
![License](https://img.shields.io/badge/license-Educational-green)
![Platform](https://img.shields.io/badge/platform-Linux-orange)

A modern, user-friendly WiFi security testing tool with beautiful GUI and terminal UI.

**⚠️ For Educational and Authorized Testing Only ⚠️**

</div>

---

## ✨ Features

### 🎨 Modern GUI Interface
- **Beautiful Dark Theme** - Eye-friendly purple/dark color scheme
- **Tabbed Interface** - Organized tools, advanced features, and saved data
- **Real-time Console** - Live command output with color-coded messages
- **Smart Dialogs** - Input forms with hints and examples
- **Quick Settings** - Save your interface names for quick access
- **Status Bar** - Always know what's happening
- **Help System** - Built-in help and tooltips

### 🛠️ Powerful Tools
- **Monitor Mode Management** - Easy enable/disable monitor mode
- **Network Scanning** - Scan for WiFi networks with detailed info
- **Handshake Capture** - Capture WPA/WPA2 handshakes
- **Password Cracking** - Crack handshakes with wordlists
- **WPS Attacks** - Exploit WPS vulnerabilities
- **MAC Spoofing** - Change your MAC address
- **Fake AP** - Create fake access points

### 🚀 User-Friendly
- **Beginner Friendly** - Clear instructions and tooltips
- **Smart Defaults** - Remembers your settings
- **File Browser** - Easy file selection
- **Confirmation Dialogs** - Prevents accidental actions
- **Saved Data Manager** - Track your captured files

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/emrekybs/Wifi-Purple.git
cd Wifi-Purple
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Required Tools
```bash
sudo apt update
sudo apt install aircrack-ng bully mdk3 xterm
```

### 4. Verify Installation
```bash
airmon-ng --help
airodump-ng --help
```

---

## 🚀 Usage

### GUI Version (Recommended for Beginners)
```bash
sudo python3 wifi_purple_gui.py
```

**Features:**
- 🎨 Beautiful graphical interface
- 📊 Organized in tabs (Main Tools, Advanced, Saved Data)
- 💡 Built-in help and tooltips
- 🔄 Real-time output console
- ⚙️ Quick settings panel

### Terminal Version (For Advanced Users)
```bash
sudo python3 wifi_purple_improved.py
```

**Features:**
- 🎯 Rich terminal UI with tables
- ⚡ Fast and lightweight
- 📝 Progress indicators
- 🎨 Color-coded output

---

## 📖 Quick Start Guide

### Step 1: Start Monitor Mode
1. Open WiFi-Purple GUI
2. Set your interface name in Quick Settings (e.g., `wlan0`)
3. Click **"🔧 Start Monitor"**
4. Your interface will become `wlan0mon`

### Step 2: Scan Networks
1. Click **"🔍 Scan Networks"**
2. A terminal window will open showing nearby WiFi networks
3. Note down the **BSSID** and **Channel** of your target

### Step 3: Capture Handshake
1. Click **"🎯 Capture Handshake"**
2. Choose to scan first (if needed)
3. Enter target BSSID and Channel
4. Wait for handshake capture (look for "WPA handshake")

### Step 4: Crack Password
1. Click **"🔓 Crack Password"**
2. Select your captured `.cap` file
3. Choose a wordlist (e.g., `/usr/share/wordlists/rockyou.txt`)
4. Wait for the password to be cracked

---

## 🎯 Tool Categories

### 🔧 Setup Tools
| Tool | Description | Usage |
|------|-------------|-------|
| Start Monitor | Enable monitor mode | Required before scanning |
| Stop Monitor | Disable monitor mode | Return to normal mode |
| View Interfaces | Show network interfaces | Check your adapters |
| Restart Network | Restart NetworkManager | Fix connection issues |

### 🔍 Scanning Tools
| Tool | Description | Usage |
|------|-------------|-------|
| Scan Networks | Find WiFi networks | Discover targets |
| Capture Handshake | Capture WPA handshake | Get authentication data |

### ⚡ Attack Tools
| Tool | Description | Usage |
|------|-------------|-------|
| Crack Password | Crack handshake | Recover password |
| WPS Attack | Exploit WPS PIN | Attack WPS routers |
| Fake AP | Create fake AP | Deception attacks |

### 🛠️ Utilities
| Tool | Description | Usage |
|------|-------------|-------|
| Change MAC | Spoof MAC address | Anonymity |

---

## 💡 Tips & Tricks

### For Beginners
- ✅ Always start with Monitor Mode
- ✅ Use the built-in Help button (❓)
- ✅ Right-click buttons for more info
- ✅ Check the Saved Data tab for your captures
- ✅ Use large wordlists for better success

### For Advanced Users
- 🔥 Use custom wordlists for faster cracking
- 🔥 Combine multiple attacks for better results
- 🔥 Monitor the output console for detailed info
- 🔥 Save your captures in organized folders

### Common Issues
**Problem:** Monitor mode won't start
- **Solution:** Kill interfering processes: `sudo airmon-ng check kill`

**Problem:** No handshake captured
- **Solution:** Increase deauth packets or wait for client connection

**Problem:** Cracking takes too long
- **Solution:** Use a better wordlist or GPU-accelerated tools

---

## 🎨 Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────┐
│              🌐 WiFi-Purple 🌐                          │
│     WiFi Security Testing Tool - By EmreKybs           │
├─────────────────────────────────────────────────────────┤
│  ⚙️ Quick Settings                                      │
│  Normal Interface: [wlan0]  Monitor: [wlan0mon] [Help] │
├──────────────┬──────────────────────────────────────────┤
│  🔧 Setup    │  📟 Output Console                       │
│  🔍 Scanning │  [Real-time command output here...]      │
│  ⚡ Attacks  │                                           │
│  🛠️ Utilities│                                           │
└──────────────┴──────────────────────────────────────────┘
```

---

## 🆚 Improvements Over Original

### GUI Version (NEW!)
- ✨ **Modern Interface** - Beautiful dark-themed GUI with purple accents
- 📑 **Tabbed Layout** - Organized tools, advanced features, saved data
- 🎯 **Smart Dialogs** - Input forms with hints and examples
- 💾 **Saved Data Manager** - Track and manage captured files
- ⚙️ **Quick Settings** - Save interface names for reuse
- 🔄 **Real-time Console** - Live output with color coding
- 📂 **File Browsers** - Easy file selection
- 🧵 **Threaded Operations** - Non-blocking execution
- 📊 **Status Bar** - Always know what's happening
- ❓ **Help System** - Built-in help and tooltips
- ⌨️ **Keyboard Shortcuts** - Enter/Escape in dialogs
- 🎨 **Categorized Tools** - Setup, Scanning, Attacks, Utilities
- 💡 **Welcome Guide** - Instructions on startup
- 🗑️ **Clear Console** - Easy output management

### Terminal Version
- 🎯 **Rich UI** - Beautiful tables and panels
- 📊 **Progress Indicators** - Visual feedback
- 🎨 **Color-coded Output** - Easy to read
- 🔄 **Error Handling** - Graceful error management
- 📝 **Input Validation** - Better user input handling
- 🏗️ **Object-Oriented** - Clean code structure

---

## 📋 Requirements

### System Requirements
- **OS:** Linux (Kali Linux, Ubuntu, Debian, etc.)
- **Python:** 3.6 or higher
- **Privileges:** Root/sudo access
- **Display:** X11 (for GUI version)

### Software Dependencies
```bash
# Python packages
rich>=13.0.0
colorama>=0.4.6

# System tools
aircrack-ng    # WiFi security testing suite
bully          # WPS attack tool
mdk3           # Wireless attack tool
xterm          # Terminal emulator (for GUI)
```

### Optional Tools
```bash
gnome-terminal  # Alternative terminal (if xterm not available)
```

---

## ⚠️ Legal Disclaimer

**IMPORTANT - READ CAREFULLY:**

This tool is provided for **EDUCATIONAL PURPOSES ONLY**. 

### Legal Use Cases:
✅ Testing your own WiFi network security
✅ Authorized penetration testing with written permission
✅ Educational research in controlled environments
✅ Security auditing with proper authorization

### Illegal Use Cases:
❌ Accessing networks without permission
❌ Unauthorized penetration testing
❌ Stealing WiFi passwords
❌ Any malicious activities

### Your Responsibility:
- You are solely responsible for your actions
- Unauthorized access to networks is illegal in most countries
- Violators may face criminal prosecution
- Always obtain written permission before testing

**By using this tool, you agree to use it responsibly and legally.**

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/emrekybs/Wifi-Purple/issues)
- **GitHub:** [@emrekybs](https://github.com/emrekybs)

---

## 📜 License

This project is provided for educational purposes only. Use responsibly and legally.

---

## 🙏 Credits

**Original Author:** EmreKybs
**Improved Version:** Enhanced with modern GUI and features

### Tools Used:
- **aircrack-ng** - WiFi security testing
- **bully** - WPS attack tool
- **mdk3** - Wireless attack tool
- **Python tkinter** - GUI framework
- **Rich** - Terminal UI library

---

## 📚 Additional Resources

### Learning Resources:
- [Aircrack-ng Documentation](https://www.aircrack-ng.org/)
- [WiFi Security Basics](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access)
- [Ethical Hacking Guide](https://www.offensive-security.com/)

### Recommended Wordlists:
- `/usr/share/wordlists/rockyou.txt` (Default on Kali Linux)
- [SecLists](https://github.com/danielmiessler/SecLists)
- [CrackStation](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm)

---

<div align="center">

**Made with 💜 by EmreKybs**

⭐ Star this repo if you find it useful!

</div>
