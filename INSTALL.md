# Installation Guide - GNOME Monitor Switcher

Complete installation guide for setting up instant monitor switching on fresh Fedora/GNOME systems.

## 📋 Prerequisites Check

### System Requirements
```bash
# 1. Verify Fedora Linux
cat /etc/fedora-release
# Expected: Fedora Linux XX (...)

# 2. Verify GNOME Desktop Environment
echo $XDG_CURRENT_DESKTOP
# Expected: GNOME

# 3. Verify Wayland (recommended)
echo $XDG_SESSION_TYPE
# Expected: wayland

# 4. Verify Python 3
python3 --version
# Expected: Python 3.9+ 

# 5. Verify gdctl availability
gdctl --help
# Should show gdctl usage information
```

### Hardware Requirements
- **Multi-monitor setup**: 2+ external monitors
- **DisplayPort connections**: Most reliable for high refresh rates
- **Graphics support**: GPU capable of driving multiple high-resolution displays

## 🚀 Quick Installation

### Method 1: Clone from GitHub (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/gnome-monitor-switcher.git
cd gnome-monitor-switcher

# 2. Run the install script
./install.sh

# 3. Reload your shell
source ~/.zshrc  # or ~/.bashrc
```

### Method 2: Manual Installation
```bash
# 1. Create directory structure
mkdir -p ~/bin/monitors

# 2. Download the script
curl -o ~/bin/monitors/gdctl-instant.py https://raw.githubusercontent.com/YOUR_USERNAME/gnome-monitor-switcher/main/gdctl-instant.py
chmod +x ~/bin/monitors/gdctl-instant.py

# 3. Add aliases to shell configuration
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/gnome-monitor-switcher/main/aliases.sh >> ~/.zshrc

# 4. Reload shell
source ~/.zshrc
```

## 🔧 Detailed Setup Process

### Step 1: Directory Preparation
```bash
# Create the monitors directory
mkdir -p ~/bin/monitors

# Create config backup directory
mkdir -p ~/bin/monitors/configs

# Verify directories
ls -la ~/bin/monitors/
# Should show: configs/ directory
```

### Step 2: Script Installation
```bash
# Make the script executable
chmod +x ~/bin/monitors/gdctl-instant.py

# Test script execution
~/bin/monitors/gdctl-instant.py --help
# Should show usage information
```

### Step 3: Monitor Detection
```bash
# Discover your monitors
gdctl show --modes

# Note down your monitor IDs (e.g., DP-1, DP-2, HDMI-A-1)
# Note down available resolutions and refresh rates
```

### Step 4: Configuration Customization

Edit the monitor configuration in `gdctl-instant.py` to match your hardware:

```python
# Located around line 13-42 in gdctl-instant.py
MONITORS = {
    'DP-1': {  # Change to your monitor ID
        'name': 'Your Monitor Brand/Model',
        'vendor': 'VENDOR_CODE',  # From gdctl show
        'product': 'PRODUCT_CODE',  # From gdctl show
        'description': 'Monitor description with resolution',
        'max_mode': '3440x1440@144.000'  # From gdctl show --modes
    },
    # Add more monitors as needed
}
```

### Step 5: Alias Configuration

#### For Zsh Users (Default on modern Fedora)
```bash
# Add to ~/.zshrc
echo "
# Monitor switching aliases
alias m0='~/bin/monitors/gdctl-instant.py DP-1'      # Primary monitor
alias m1='~/bin/monitors/gdctl-instant.py DP-2'      # Secondary monitor  
alias m3='~/bin/monitors/gdctl-instant.py triple'    # Multi-monitor setup
alias mavailable='~/bin/monitors/gdctl-instant.py available'
alias mshow='~/bin/monitors/gdctl-instant.py show'
" >> ~/.zshrc
```

#### For Bash Users
```bash
# Add to ~/.bashrc
echo "
# Monitor switching aliases
alias m0='~/bin/monitors/gdctl-instant.py DP-1'      # Primary monitor
alias m1='~/bin/monitors/gdctl-instant.py DP-2'      # Secondary monitor  
alias m3='~/bin/monitors/gdctl-instant.py triple'    # Multi-monitor setup
alias mavailable='~/bin/monitors/gdctl-instant.py available'
alias mshow='~/bin/monitors/gdctl-instant.py show'
" >> ~/.bashrc
```

### Step 6: Shell Reload and Testing
```bash
# Reload shell configuration
source ~/.zshrc  # or source ~/.bashrc

# Test alias availability
which m0
# Should show: alias m0='~/bin/monitors/gdctl-instant.py DP-1'

# Test monitor detection
mavailable
# Should show your connected monitors
```

## 🎛️ Custom Configuration

### Multi-Monitor Layout Setup

For triple monitor setups, customize the layout in the `restore_triple_monitor()` function:

```python
# Around line 231 in gdctl-instant.py
cmd = """gdctl set --verbose \\
    --logical-monitor --monitor DP-1 --mode 2560x1080@60.000 --transform 270 --x 0 --y 0 \\
    --logical-monitor --primary --monitor DP-2 --mode 3440x1440@144.000 --x 1080 --y 0 \\
    --logical-monitor --monitor DP-3 --mode 3440x1440@100.000 --x 1080 --y 1440"""
```

### Positioning Guide
- `--x 0 --y 0`: Top-left position
- `--transform 270`: Portrait orientation (90° rotation)
- `--primary`: Makes this monitor the primary display
- Use monitor pixel widths/heights for positioning calculations

### Refresh Rate Optimization
```bash
# Find maximum supported refresh rates
gdctl show --modes | grep "YOUR_RESOLUTION"

# Common high refresh rates to try:
# 144.000, 165.000, 180.000, 240.000
```

## ✅ Verification Checklist

### Basic Functionality
- [ ] `gdctl --help` shows usage information
- [ ] `mavailable` lists connected monitors
- [ ] `mshow` displays current configuration
- [ ] Single monitor switching works (`m0`, `m1`)

### Advanced Features
- [ ] Triple monitor layout works (`m3`)
- [ ] Automatic backups created in `~/bin/monitors/configs/`
- [ ] Error handling works when monitors disconnected
- [ ] Maximum refresh rates achieved for all monitors

### Performance Tests
- [ ] Monitor switching completes in < 2 seconds
- [ ] No graphical glitches during switching
- [ ] All monitors maintain proper resolution and refresh rate
- [ ] System remains stable under frequent switching

## 🔧 Troubleshooting Installation

### Common Issues

#### 1. gdctl Command Not Found
```bash
# Verify GNOME version
gnome-shell --version
# gdctl requires GNOME 40+ (usually available on Fedora 34+)

# On older systems, try:
sudo dnf update gnome-shell
```

#### 2. Permission Issues
```bash
# Fix script permissions
chmod +x ~/bin/monitors/gdctl-instant.py

# Fix directory permissions
chmod 755 ~/bin/monitors/
```

#### 3. Monitor Not Detected
```bash
# Check physical connections
gdctl show
# Monitor should appear in output

# Try different DisplayPort/HDMI ports
# Restart GNOME session if needed
```

#### 4. Alias Not Working
```bash
# Check if alias was added correctly
grep "alias m0" ~/.zshrc  # or ~/.bashrc

# Reload shell
source ~/.zshrc

# Test direct script execution
~/bin/monitors/gdctl-instant.py available
```

## 🚀 Post-Installation Setup

### Daily Usage Optimization
```bash
# Create desktop shortcuts (optional)
cat > ~/.local/share/applications/monitor-switcher.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Monitor Switcher
Comment=Quick monitor configuration switching
Exec=/home/$USER/bin/monitors/gdctl-instant.py available
Icon=preferences-desktop-display
Terminal=true
Categories=System;Settings;
EOF
```

### Backup Configuration
```bash
# Create initial backup of working configuration
~/bin/monitors/gdctl-instant.py show > ~/bin/monitors/working-config-backup.txt
```

### Integration with System
```bash
# Optional: Add to PATH for system-wide access
echo 'export PATH="$HOME/bin/monitors:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Now you can use: gdctl-instant.py from anywhere
```

## 📚 Next Steps

After successful installation:

1. **Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for common issues
2. **Customize monitor layout** for your specific setup
3. **Test all scenarios**: home/laptop/partial monitor setups
4. **Create custom aliases** for your workflow needs

## 🎯 Installation Support

### Automated Install Script

Create an automated installer for your specific setup:

```bash
#!/bin/bash
# install.sh - Automated installer for GNOME Monitor Switcher

echo "🚀 Installing GNOME Monitor Switcher..."

# Create directories
mkdir -p ~/bin/monitors/configs

# Copy files
cp gdctl-instant.py ~/bin/monitors/
chmod +x ~/bin/monitors/gdctl-instant.py

# Add aliases
cat aliases.sh >> ~/.zshrc

echo "✅ Installation complete!"
echo "💡 Run 'source ~/.zshrc' to activate aliases"
echo "🔍 Test with 'mavailable' command"
```

This comprehensive installation guide ensures you can set up the monitor switching system on any fresh Fedora/GNOME system without missing any steps.

---

**📝 Note**: Customize monitor IDs, resolutions, and refresh rates based on your specific hardware configuration.