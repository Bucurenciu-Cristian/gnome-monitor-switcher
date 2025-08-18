# GNOME Monitor Switcher ⚡

A powerful instant monitor switching solution for GNOME/Wayland systems. Switch between monitor configurations in under 1 second with maximum refresh rates and intelligent safety validation.

## ✨ Features

- **⚡ Instant Switching**: Sub-second monitor configuration changes using GNOME's `gdctl`
- **🛡️ Safety Validation**: Prevents switching to disconnected monitors with smart error messages
- **🏠 Environment Detection**: Automatically detects home/laptop/partial setups
- **🎯 Custom Layouts**: Optimized triple monitor configuration with portrait orientation
- **📦 Automatic Backups**: Safe configuration management with timestamped rollback capability
- **🚀 Smart Aliases**: Simple single-letter commands for daily workflow

## 🚀 Quick Start

### Essential Commands
```bash
m0          # Switch to ASUS monitor (3440x1440@100Hz)
m1          # Switch to Iiyama monitor (3440x1440@180Hz) 
m3          # Custom triple monitor layout (all monitors)
mavailable  # Show only connected monitors
mshow       # Show current configuration
```

### Triple Monitor Layout (m3)
```
┌─────────────┐  ┌────────────────────────────────┐
│             │  │         Iiyama DP-4           │
│    LG       │  │    3440x1440@180Hz (Primary)   │
│   DP-3      │  └────────────────────────────────┘
│ Portrait    │  ┌────────────────────────────────┐
│ 2560x1080   │  │         ASUS DP-2             │
│   @60Hz     │  │      3440x1440@100Hz          │
└─────────────┘  └────────────────────────────────┘
```

## 📂 Installation for New Systems

### Prerequisites
- **Operating System**: Fedora Linux (tested on Fedora 42+)
- **Desktop Environment**: GNOME with Wayland
- **Python**: Python 3 (usually pre-installed)
- **gdctl**: Included with modern GNOME installations

### Quick Install
```bash
# 1. Clone this repository
git clone https://github.com/YOUR_USERNAME/gnome-monitor-switcher.git
cd gnome-monitor-switcher

# 2. Copy script to ~/bin/monitors/
mkdir -p ~/bin/monitors
cp gdctl-instant.py ~/bin/monitors/
chmod +x ~/bin/monitors/gdctl-instant.py

# 3. Add aliases to your shell
cat aliases.sh >> ~/.zshrc  # For zsh users
# or
cat aliases.sh >> ~/.bashrc # For bash users

# 4. Reload your shell
source ~/.zshrc  # or source ~/.bashrc
```

### Verification
```bash
# Test the installation
mavailable  # Should show your connected monitors
gdctl show  # Verify gdctl is working
```

## 📖 Usage Guide

### Direct Script Usage
```bash
# Switch to specific monitors
~/bin/monitors/gdctl-instant.py DP-2      # ASUS monitor
~/bin/monitors/gdctl-instant.py DP-4      # Iiyama monitor  
~/bin/monitors/gdctl-instant.py eDP-1     # Laptop display
~/bin/monitors/gdctl-instant.py triple    # Custom triple layout

# Information commands
~/bin/monitors/gdctl-instant.py show       # Current configuration
~/bin/monitors/gdctl-instant.py available  # Connected monitors only
~/bin/monitors/gdctl-instant.py list       # All available monitors (help)
```

### Alias Commands (Recommended)
```bash
m0          # Switch to primary external monitor
m1          # Switch to secondary external monitor  
m3          # Enable triple monitor layout
mavailable  # Show connected monitors with usage tips
mshow       # Display current monitor configuration
```

### Environment Context
The system automatically detects your setup:

**🏠 Full Home Setup** (All 3+ monitors connected)
- All aliases work (m0, m1, m3)
- Triple monitor layout available
- Maximum refresh rates enabled

**💻 Laptop Mode** (Built-in display only)
- Limited to laptop display commands
- Clear feedback about missing monitors
- Suggests available alternatives

**⚡ Partial Setup** (Some external monitors)
- Shows which commands will work
- Adapts to available hardware
- Environment-specific guidance

## 🔧 Hardware Configuration

### Supported Monitor Setup
```yaml
ASUS_DP-2:
  model: "VG34VQEL1A"
  resolution: "3440x1440"
  refresh_rate: "100Hz"
  position: "bottom-right"

Iiyama_DP-4:
  model: "PL3481WQ"
  resolution: "3440x1440"
  refresh_rate: "180Hz"
  position: "top-right (primary)"

LG_DP-3:
  model: "LG ULTRAWIDE"
  resolution: "2560x1080"
  refresh_rate: "60Hz"
  orientation: "portrait"
  position: "left"

Laptop_eDP-1:
  resolution: "2880x1920"
  refresh_rate: "60Hz"
  type: "built-in"
```

### Customization for Different Hardware
To adapt for your monitors, edit the `MONITORS` dictionary in `gdctl-instant.py`:

```python
MONITORS = {
    'DP-2': {
        'name': 'Your Monitor Name',
        'vendor': 'VENDOR',
        'product': 'MODEL',
        'description': 'Description with resolution',
        'max_mode': '3440x1440@100.006'  # Use gdctl show --modes to find
    },
    # ... add your monitors
}
```

## 🛡️ Safety & Backup Features

### Automatic Configuration Backup
- Every monitor switch creates a timestamped backup
- Stored in `~/bin/monitors/configs/gdctl-backup-TIMESTAMP.txt`
- Easy restoration if something goes wrong

### Smart Validation
- **Connection Check**: Prevents switching to disconnected monitors
- **Mode Validation**: Ensures refresh rates are supported
- **Environment Awareness**: Provides context-specific error messages
- **Graceful Failures**: Clear feedback with suggested alternatives

### Error Recovery
```bash
# If something goes wrong, restore from backup:
gdctl set $(cat ~/bin/monitors/configs/gdctl-backup-LATEST.txt)
```

## 🚀 Performance

### Benchmarks
- **Switch Time**: < 1 second for any configuration
- **Startup Time**: < 0.5 seconds for script execution
- **Memory Usage**: Minimal (Python script + gdctl)
- **CPU Impact**: Negligible during normal operation

### Refresh Rate Optimization
- **ASUS Monitor**: 100Hz (maximum supported)
- **Iiyama Monitor**: 180Hz (maximum supported)
- **LG Monitor**: 60Hz (portrait orientation)
- **All simultaneously**: No performance degradation

## 📚 Additional Documentation

- **[INSTALL.md](INSTALL.md)**: Detailed installation guide for fresh systems
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**: Common issues and solutions
- **[SESSION-SUMMARY.md](SESSION-SUMMARY.md)**: Development history and technical details

## 🎯 Use Cases

### Daily Workflow
- **Development**: `m1` for high-refresh coding, `m3` for multi-window workflow
- **Gaming**: `m1` for 180Hz gaming performance
- **Productivity**: `m3` for maximum screen real estate
- **Travel**: Automatic laptop-mode detection when away

### Remote Work
- **Home Office**: `m3` for full desktop experience
- **Coffee Shop**: Automatic laptop-only mode
- **Hotel**: `m0` or `m1` for external monitor when available
- **Client Site**: Safe operation with unknown monitor setups

## 🔄 Version History

- **v1.0**: Initial release with basic monitor switching
- **v1.1**: Added triple monitor layout and portrait orientation
- **v1.2**: Enhanced safety validation and environment detection
- **v1.3**: Added comprehensive documentation and GitHub repository

## 📄 License

MIT License - feel free to adapt for your own monitor setup.

## 🤝 Contributing

This is a personal setup repository, but feel free to:
- Fork for your own hardware configuration
- Submit issues for general bugs
- Share adaptations for different monitor combinations

---

**⚡ Instant switching** | **🛡️ Production ready** | **🚀 Maximum performance** | **Powered by GNOME gdctl**