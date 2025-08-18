# Troubleshooting Guide - GNOME Monitor Switcher

Complete troubleshooting guide for resolving common issues with the GNOME monitor switching system.

## 🚨 Quick Diagnosis

### Emergency Commands
```bash
# Check system status
mavailable              # Show connected monitors
mshow                   # Show current configuration  
gdctl show              # Raw GNOME display status
gdctl show --modes      # Available resolutions/refresh rates

# Recovery commands
gdctl show > ~/recovery-config.txt    # Save current working config
# Restore from backup: gdctl set < ~/bin/monitors/configs/gdctl-backup-TIMESTAMP.txt
```

## 🔍 Common Issues

### 1. "Command not found: m0/m1/m3"

**Symptoms:**
```bash
$ m0
zsh: command not found: m0
```

**Diagnosis:**
```bash
# Check if aliases are loaded
alias | grep "m0"
# Should show: m0='~/bin/monitors/gdctl-instant.py DP-2'

# Check if script exists
ls -la ~/bin/monitors/gdctl-instant.py
# Should show: -rwxr-xr-x ... gdctl-instant.py
```

**Solutions:**

#### A. Aliases not loaded
```bash
# Reload shell configuration
source ~/.zshrc    # For zsh users
source ~/.bashrc   # For bash users

# Or add aliases manually
cat ~/bin/monitors/aliases.sh >> ~/.zshrc
source ~/.zshrc
```

#### B. Script not executable
```bash
chmod +x ~/bin/monitors/gdctl-instant.py

# Test direct execution
~/bin/monitors/gdctl-instant.py available
```

#### C. Wrong shell configuration file
```bash
# Check your current shell
echo $SHELL

# For zsh users (default on modern Fedora)
echo "source ~/bin/monitors/aliases.sh" >> ~/.zshrc

# For bash users  
echo "source ~/bin/monitors/aliases.sh" >> ~/.bashrc
```

---

### 2. "Monitor not connected" Errors

**Symptoms:**
```bash
$ m0
❌ Monitor DP-2 (ASUS 34" UltraWide) is not connected!
ℹ️  Currently connected monitors: DP-1, eDP-1
```

**Diagnosis:**
```bash
# Check physical connections
gdctl show
# Look for your monitors in the output

# Check cable connections
# Try different DisplayPort/HDMI ports
# Power cycle monitors
```

**Solutions:**

#### A. Different monitor IDs
```bash
# Find actual monitor IDs
gdctl show | grep "Monitor"
# Output example: ├──Monitor DP-1 (Your Monitor Brand)

# Update script with correct IDs
# Edit ~/bin/monitors/gdctl-instant.py line 13-42
# Change DP-2 to your actual monitor ID (e.g., DP-1)
```

#### B. Monitor detection issues
```bash
# Restart GNOME Shell (Wayland)
pkill -f gnome-shell
# System will restart shell automatically

# Or restart display manager (X11)
sudo systemctl restart gdm
```

#### C. Hardware connection problems
- Check cable quality (use high-quality DisplayPort cables)
- Try different ports on GPU and monitor
- Power cycle monitors (off/on)
- Check GPU driver status: `nvidia-smi` or `lspci | grep VGA`

---

### 3. Wrong Refresh Rates or Resolutions

**Symptoms:**
```bash
# Monitor switched but wrong refresh rate
$ mshow
Current mode: 3440x1440@59.973  # Expected: @180.000
```

**Diagnosis:**
```bash
# Check available modes for your monitor
gdctl show --modes | grep "3440x1440"
# Look for highest available refresh rate
```

**Solutions:**

#### A. Update maximum refresh rates in script
```bash
# Edit ~/bin/monitors/gdctl-instant.py
# Find MONITORS dictionary (around line 13)
# Update max_mode with actual supported rate:

'DP-4': {
    'max_mode': '3440x1440@180.000'  # Use exact value from gdctl show --modes
}
```

#### B. Graphics driver limitations
```bash
# Check GPU driver
nvidia-smi                    # For NVIDIA
glxinfo | grep "OpenGL"      # For general GPU info

# Update drivers if needed
sudo dnf update               # Update all packages
# Or install proprietary drivers for NVIDIA/AMD
```

---

### 4. Triple Monitor Layout Issues (m3)

**Symptoms:**
```bash
$ m3
❌ Triple monitor setup requires all 3 external monitors!
Missing monitors: DP-3
```

**Diagnosis:**
```bash
# Check which monitors are actually connected
mavailable
# Count external monitors (non-eDP-1)
```

**Solutions:**

#### A. Not all monitors connected
- Connect all required monitors (DP-2, DP-3, DP-4)
- Check power and cable connections
- Restart monitors if needed

#### B. Customize triple layout for your setup
```bash
# Edit ~/bin/monitors/gdctl-instant.py
# Find restore_triple_monitor() function (around line 203)
# Update required_monitors set:

required_monitors = {'DP-1', 'DP-2'}  # Your actual monitor IDs
```

#### C. Positioning problems
```bash
# Test individual positions
gdctl set --logical-monitor --monitor DP-1 --mode 3440x1440@144.000 --x 0 --y 0

# Calculate positions based on monitor widths
# Monitor 1 (left): x=0
# Monitor 2 (right): x=3440 (width of monitor 1)
# Monitor 3 (bottom): y=1440 (height of top monitor)
```

---

### 5. Performance Issues

**Symptoms:**
- Slow monitor switching (>5 seconds)
- System freezes during switching
- High CPU usage

**Solutions:**

#### A. Reduce refresh rates temporarily
```bash
# Test with lower refresh rates
gdctl set --logical-monitor --primary --monitor DP-4 --mode 3440x1440@100.000
# If faster, update script to use 100Hz instead of 180Hz
```

#### B. Check system resources
```bash
# Monitor system performance
htop
# Look for high CPU/memory usage

# Check graphics memory
nvidia-smi              # NVIDIA users
cat /sys/kernel/debug/dri/0/amdgpu_gtt_mm    # AMD users (if available)
```

#### C. Disable composition temporarily
```bash
# For testing only - disables visual effects
gsettings set org.gnome.mutter experimental-features "[]"
# Restart GNOME Shell: pkill -f gnome-shell
```

---

### 6. GNOME/Wayland Compatibility Issues

**Symptoms:**
```bash
$ gdctl --help
bash: gdctl: command not found
```

**Solutions:**

#### A. Update GNOME
```bash
# Check GNOME version
gnome-shell --version
# Requires GNOME 40+ for gdctl

# Update if needed
sudo dnf update gnome-shell mutter
```

#### B. Wayland vs X11 issues
```bash
# Check session type
echo $XDG_SESSION_TYPE
# Should be: wayland

# Switch to Wayland if on X11
# Logout → Select "GNOME" (not "GNOME on Xorg") → Login
```

#### C. Alternative for older systems
```bash
# For GNOME <40, use xrandr-based approach
# (Note: Requires X11 session)
xrandr --output DP-2 --mode 3440x1440 --rate 100
```

---

## 🔧 Advanced Troubleshooting

### Script Debugging

#### Enable verbose output
```bash
# Add debugging to script calls
~/bin/monitors/gdctl-instant.py DP-2 --verbose
# (Note: --verbose might not be implemented, modify script if needed)
```

#### Manual gdctl testing
```bash
# Test gdctl commands manually
gdctl set --logical-monitor --primary --monitor DP-2 --mode 3440x1440@100.006

# Check for error messages
gdctl set --logical-monitor --monitor WRONG-ID --mode 1920x1080@60.000
# Should show clear error about missing monitor
```

### Configuration Backup and Restore

#### Create working configuration backup
```bash
# Save current working config
gdctl show > ~/bin/monitors/working-config-$(date +%s).txt

# Restore from backup if needed
# (Note: gdctl doesn't have direct restore - need manual recreation)
```

#### Monitor log files
```bash
# Check system logs for display issues
journalctl -f | grep -i display
journalctl -f | grep -i gdctl
journalctl -f | grep -i mutter
```

### Hardware-Specific Issues

#### NVIDIA Graphics
```bash
# Check NVIDIA driver status
nvidia-smi

# Update NVIDIA drivers
sudo dnf update nvidia*

# Check for multiple GPU systems
lspci | grep VGA
# Ensure monitors connected to correct GPU
```

#### AMD Graphics  
```bash
# Check AMD driver
lspci | grep VGA
dmesg | grep amdgpu

# Update drivers
sudo dnf update mesa* xorg-x11-drv-amdgpu
```

#### Intel Graphics
```bash
# Check Intel graphics
lspci | grep VGA
dmesg | grep i915

# Usually works out-of-box, update if needed
sudo dnf update mesa* xorg-x11-drv-intel
```

---

## 📊 Performance Optimization

### Reduce Switching Time
```bash
# Skip backup creation for faster switching
# Edit gdctl-instant.py, find switch_to_single_monitor()
# Change: success = switch_to_single_monitor(command, with_backup=False)
```

### Memory Usage Optimization
```bash
# Monitor memory usage
ps aux | grep gdctl
ps aux | grep python

# Clean old backups (see cleanup section in README)
find ~/bin/monitors/configs/ -name "gdctl-backup-*" -mtime +7 -delete
```

---

## 🆘 When All Else Fails

### Reset to Single Monitor
```bash
# Emergency reset to laptop display only
gdctl set --logical-monitor --primary --monitor eDP-1 --mode 2880x1920@60.000
```

### Complete System Reset
```bash
# Reset all GNOME display settings
gsettings reset-recursively org.gnome.mutter
gsettings reset-recursively org.gnome.shell

# Restart GNOME Shell
pkill -f gnome-shell
```

### Get Help
```bash
# Gather system information for support
echo "=== System Info ===" > ~/monitor-debug.txt
uname -a >> ~/monitor-debug.txt
gnome-shell --version >> ~/monitor-debug.txt
echo "=== Monitors ===" >> ~/monitor-debug.txt
gdctl show >> ~/monitor-debug.txt
echo "=== Graphics ===" >> ~/monitor-debug.txt  
lspci | grep VGA >> ~/monitor-debug.txt

# Share monitor-debug.txt when asking for help
```

---

## 📞 Support Resources

### Community Support
- **Fedora Forums**: https://ask.fedoraproject.org/
- **GNOME Discourse**: https://discourse.gnome.org/
- **r/Fedora**: Reddit community for Fedora-specific issues

### Bug Reports
- **GNOME Mutter**: https://gitlab.gnome.org/GNOME/mutter/-/issues
- **Fedora Bugzilla**: https://bugzilla.redhat.com/

### Documentation
- **GNOME Display Configuration**: https://wiki.gnome.org/Projects/Mutter
- **Wayland**: https://wayland.freedesktop.org/

---

## 🔄 Version-Specific Issues

### Fedora 42+
- Full gdctl support
- Maximum compatibility

### Fedora 38-41
- gdctl available but may have limitations
- Test thoroughly before deployment

### Fedora <38
- gdctl may not be available
- Consider xrandr-based alternatives
- Recommend system upgrade

---

**💡 Pro Tip**: Always test monitor configurations in a safe environment first. Keep a backup of working configurations, and know how to quickly revert to single-monitor mode if issues occur.

This troubleshooting guide covers the most common issues. For hardware-specific problems, consult your monitor and graphics card documentation.