#!/bin/bash
# aliases.sh - Monitor switching aliases for GNOME Monitor Switcher
# 
# Usage: Add these aliases to your shell configuration
#   For zsh: cat aliases.sh >> ~/.zshrc
#   For bash: cat aliases.sh >> ~/.bashrc
#
# Then reload your shell: source ~/.zshrc (or source ~/.bashrc)

# =============================================================================
# GNOME Monitor Switcher Aliases
# =============================================================================
# Instant monitor configuration switching using gdctl
# Requires: ~/bin/monitors/gdctl-instant.py to be installed and executable

# Monitor switching aliases (INSTANT with gdctl)
alias m0='~/bin/monitors/gdctl-instant.py DP-2'       # ASUS 34" UltraWide (3440x1440@100Hz)
alias m1='~/bin/monitors/gdctl-instant.py DP-4'       # Iiyama 34" UltraWide (3440x1440@180Hz)
alias m3='~/bin/monitors/gdctl-instant.py triple'     # Custom triple monitor layout

# Information and utility aliases
alias mavailable='~/bin/monitors/gdctl-instant.py available'  # Show connected monitors
alias mshow='~/bin/monitors/gdctl-instant.py show'            # Show current configuration

# =============================================================================
# Usage Examples:
# =============================================================================
# 
# m0          # Switch to ASUS monitor (100Hz) - perfect for productivity
# m1          # Switch to Iiyama monitor (180Hz) - perfect for gaming  
# m3          # Switch to triple monitor layout - maximum screen real estate
# mavailable  # Check which monitors are connected
# mshow       # Display current monitor configuration
#
# =============================================================================
# Monitor Layout (m3 command):
# =============================================================================
#
#  ┌─────────────┐  ┌────────────────────────────────┐
#  │             │  │         Iiyama DP-4           │
#  │    LG       │  │    3440x1440@180Hz (Primary)  │
#  │   DP-3      │  └────────────────────────────────┘
#  │ Portrait    │  ┌────────────────────────────────┐
#  │ 2560x1080   │  │         ASUS DP-2             │
#  │   @60Hz     │  │      3440x1440@100Hz          │
#  └─────────────┘  └────────────────────────────────┘
#
# =============================================================================
# Monitor Specifications:
# =============================================================================
# 
# ASUS DP-2: VG34VQEL1A
#   - Resolution: 3440x1440
#   - Refresh Rate: 100Hz
#   - Position: Bottom-right in triple layout
#   - Use Case: Productivity work, coding
#
# Iiyama DP-4: PL3481WQ  
#   - Resolution: 3440x1440
#   - Refresh Rate: 180Hz (maximum)
#   - Position: Top-right in triple layout (primary)
#   - Use Case: Gaming, high-refresh content
#
# LG DP-3: LG ULTRAWIDE
#   - Resolution: 2560x1080 
#   - Refresh Rate: 60Hz
#   - Orientation: Portrait (270° rotation)
#   - Position: Left side in triple layout
#   - Use Case: Vertical content, code, chat
#
# Built-in eDP-1: Laptop Display
#   - Resolution: 2880x1920
#   - Refresh Rate: 60Hz
#   - Use Case: Mobile/travel mode
#
# =============================================================================
# Environment Detection:
# =============================================================================
# 
# The system automatically detects your setup:
#
# 🏠 Full Home Setup (All monitors connected):
#   - All aliases work (m0, m1, m3)
#   - Triple monitor layout available  
#   - Maximum refresh rates enabled
#
# 💻 Laptop Mode (Built-in display only):
#   - Limited to laptop display commands
#   - Clear feedback about missing monitors
#   - Automatic environment detection
#
# ⚡ Partial Setup (Some monitors connected):
#   - Shows which commands will work
#   - Adapts to available hardware
#   - Environment-specific guidance
#
# =============================================================================
# Installation Notes:
# =============================================================================
#
# 1. These aliases assume the gdctl-instant.py script is located at:
#    ~/bin/monitors/gdctl-instant.py
#
# 2. The script must be executable:
#    chmod +x ~/bin/monitors/gdctl-instant.py
#
# 3. Monitor IDs (DP-2, DP-4, etc.) are specific to this hardware setup
#    Customize them based on your system's monitor detection
#
# 4. To find your monitor IDs:
#    gdctl show
#
# 5. To find available refresh rates:
#    gdctl show --modes
#
# =============================================================================
# Customization for Different Hardware:
# =============================================================================
#
# To adapt these aliases for your monitors:
# 
# 1. Run: gdctl show
#    Note your monitor IDs (e.g., HDMI-A-1, DP-1, etc.)
#
# 2. Run: gdctl show --modes  
#    Note maximum refresh rates for each monitor
#
# 3. Edit gdctl-instant.py MONITORS dictionary with your hardware
#
# 4. Update these aliases with your monitor IDs:
#    alias m0='~/bin/monitors/gdctl-instant.py YOUR-MONITOR-ID'
#
# =============================================================================
# Safety Features:
# =============================================================================
#
# ✅ Connection Validation: Won't switch to disconnected monitors
# ✅ Automatic Backups: Configuration saved before each change  
# ✅ Error Recovery: Clear error messages with suggestions
# ✅ Environment Detection: Smart handling of different setups
# ✅ Instant Switching: Sub-second response time
#
# =============================================================================