#!/bin/bash

# WiFi-Purple Installation Script
# By EmreKybs
# Version: 2.0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║        🌐 WiFi-Purple Installation Script 🌐                ║"
echo "║                                                              ║"
echo "║                    By EmreKybs                               ║"
echo "║                    Version 2.0                               ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Error: This script must be run as root${NC}"
    echo -e "${YELLOW}💡 Please run: sudo bash INSTALL.sh${NC}"
    exit 1
fi

echo -e "${CYAN}🔍 Checking system compatibility...${NC}"
sleep 1

# Check OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    echo -e "${GREEN}✓ Operating System: $OS${NC}"
else
    echo -e "${RED}❌ Cannot detect OS${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python Version: $PYTHON_VERSION${NC}"

# Check internet connection
echo -e "${CYAN}🌐 Checking internet connection...${NC}"
if ping -c 1 google.com &> /dev/null; then
    echo -e "${GREEN}✓ Internet connection: OK${NC}"
else
    echo -e "${RED}❌ No internet connection${NC}"
    echo -e "${YELLOW}⚠️  Installation may fail without internet${NC}"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║              Starting Installation Process                   ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Update package list
echo -e "${CYAN}📦 Step 1/7: Updating package list...${NC}"
apt update -qq
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Package list updated${NC}"
else
    echo -e "${RED}❌ Failed to update package list${NC}"
    exit 1
fi
echo ""

# Upgrade existing packages (optional)
read -p "$(echo -e ${YELLOW}Do you want to upgrade existing packages? This may take time. [y/N]: ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${CYAN}⬆️  Upgrading packages...${NC}"
    apt upgrade -y
    echo -e "${GREEN}✓ Packages upgraded${NC}"
fi
echo ""

# Install Python dependencies
echo -e "${CYAN}🐍 Step 2/7: Installing Python dependencies...${NC}"
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt -q
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Python dependencies installed${NC}"
        echo -e "  - rich"
        echo -e "  - colorama"
    else
        echo -e "${RED}❌ Failed to install Python dependencies${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, skipping...${NC}"
fi
echo ""

# Install aircrack-ng suite
echo -e "${CYAN}🛠️  Step 3/7: Installing aircrack-ng suite...${NC}"
apt install -y aircrack-ng > /dev/null 2>&1
if command -v aircrack-ng &> /dev/null; then
    AIRCRACK_VERSION=$(aircrack-ng --help 2>&1 | head -n 1 | awk '{print $3}')
    echo -e "${GREEN}✓ aircrack-ng installed (version: $AIRCRACK_VERSION)${NC}"
else
    echo -e "${RED}❌ Failed to install aircrack-ng${NC}"
    exit 1
fi
echo ""

# Install bully
echo -e "${CYAN}⚡ Step 4/7: Installing bully (WPS attack tool)...${NC}"
apt install -y bully > /dev/null 2>&1
if command -v bully &> /dev/null; then
    echo -e "${GREEN}✓ bully installed${NC}"
else
    echo -e "${YELLOW}⚠️  bully installation failed (optional tool)${NC}"
fi
echo ""

# Install mdk3
echo -e "${CYAN}📶 Step 5/7: Installing mdk3 (fake AP tool)...${NC}"
apt install -y mdk3 > /dev/null 2>&1
if command -v mdk3 &> /dev/null; then
    echo -e "${GREEN}✓ mdk3 installed${NC}"
else
    echo -e "${YELLOW}⚠️  mdk3 installation failed (optional tool)${NC}"
fi
echo ""

# Install terminal emulators
echo -e "${CYAN}🖥️  Step 6/7: Installing terminal emulators...${NC}"
apt install -y xterm > /dev/null 2>&1
if command -v xterm &> /dev/null; then
    echo -e "${GREEN}✓ xterm installed${NC}"
else
    echo -e "${YELLOW}⚠️  xterm installation failed${NC}"
fi

apt install -y gnome-terminal > /dev/null 2>&1
if command -v gnome-terminal &> /dev/null; then
    echo -e "${GREEN}✓ gnome-terminal installed${NC}"
else
    echo -e "${YELLOW}⚠️  gnome-terminal not available (optional)${NC}"
fi
echo ""

# Setup directories and permissions
echo -e "${CYAN}📁 Step 7/7: Setting up directories and permissions...${NC}"

# Create directories
mkdir -p /tmp/wifi-purple
mkdir -p ~/wifi-purple-captures
mkdir -p /wordlist

echo -e "${GREEN}✓ Directories created:${NC}"
echo -e "  - /tmp/wifi-purple"
echo -e "  - ~/wifi-purple-captures"
echo -e "  - /wordlist"

# Create sample wordlist for fake AP
if [ ! -f /wordlist/fakeAP.txt ]; then
    cat > /wordlist/fakeAP.txt << EOF
FreeWiFi
Free_Internet
PublicWiFi
GuestNetwork
Airport_WiFi
Hotel_WiFi
Starbucks_WiFi
McDonalds_WiFi
Free_Hotspot
Public_Network
EOF
    echo -e "${GREEN}✓ Sample fake AP wordlist created${NC}"
fi

# Set executable permissions
chmod +x wifi_purple_gui.py 2>/dev/null
chmod +x wifi_purple_improved.py 2>/dev/null
chmod +x INSTALL.sh 2>/dev/null

echo -e "${GREEN}✓ Permissions set${NC}"
echo ""

# Check wireless interface
echo -e "${CYAN}📡 Detecting wireless interfaces...${NC}"
WIRELESS_INTERFACES=$(iwconfig 2>/dev/null | grep -o "^[^ ]*" | grep -v "lo")
if [ -z "$WIRELESS_INTERFACES" ]; then
    echo -e "${YELLOW}⚠️  No wireless interfaces detected${NC}"
    echo -e "${YELLOW}   Make sure your WiFi adapter is connected${NC}"
else
    echo -e "${GREEN}✓ Wireless interfaces found:${NC}"
    for iface in $WIRELESS_INTERFACES; do
        echo -e "  - $iface"
    done
fi
echo ""

# Installation summary
echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║              Installation Complete! ✅                       ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}📊 Installation Summary:${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "✓ Python dependencies installed"
echo -e "✓ aircrack-ng suite installed"
echo -e "✓ Additional tools installed"
echo -e "✓ Directories created"
echo -e "✓ Permissions configured"
echo ""

echo -e "${CYAN}🚀 Quick Start Guide:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}1. Run WiFi-Purple GUI (Recommended):${NC}"
echo -e "   ${GREEN}sudo python3 wifi_purple_gui.py${NC}"
echo ""
echo -e "${YELLOW}2. Run WiFi-Purple Terminal:${NC}"
echo -e "   ${GREEN}sudo python3 wifi_purple_improved.py${NC}"
echo ""
echo -e "${YELLOW}3. Check your wireless interface:${NC}"
echo -e "   ${GREEN}iwconfig${NC}"
echo ""
echo -e "${YELLOW}4. Read the documentation:${NC}"
echo -e "   ${GREEN}cat README.md${NC}"
echo ""

echo -e "${RED}⚠️  IMPORTANT LEGAL NOTICE:${NC}"
echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}This tool is for EDUCATIONAL and AUTHORIZED testing ONLY!${NC}"
echo -e "${YELLOW}Unauthorized access to networks is ILLEGAL.${NC}"
echo -e "${YELLOW}Always obtain written permission before testing.${NC}"
echo ""

echo -e "${CYAN}📚 Additional Resources:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "• GitHub: https://github.com/emrekybs"
echo -e "• Documentation: README.md"
echo -e "• Wordlists: /usr/share/wordlists/"
echo ""

echo -e "${GREEN}Thank you for using WiFi-Purple! 💜${NC}"
echo ""

# Optional: Create desktop shortcut
read -p "$(echo -e ${YELLOW}Do you want to create a desktop shortcut? [y/N]: ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DESKTOP_FILE="/usr/share/applications/wifi-purple.desktop"
    CURRENT_DIR=$(pwd)
    
    cat > $DESKTOP_FILE << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WiFi-Purple
Comment=WiFi Security Testing Tool
Exec=sudo python3 $CURRENT_DIR/wifi_purple_gui.py
Icon=network-wireless
Terminal=true
Categories=Network;Security;
EOF
    
    chmod +x $DESKTOP_FILE
    echo -e "${GREEN}✓ Desktop shortcut created${NC}"
    echo -e "  You can find it in your applications menu"
fi

echo ""
echo -e "${PURPLE}Installation script completed successfully!${NC}"
echo ""
