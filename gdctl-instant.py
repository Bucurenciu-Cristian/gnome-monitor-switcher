#!/usr/bin/env python3
"""
Instant Monitor Switching using GNOME's gdctl
Perfect solution for instant monitor configuration changes
"""

import subprocess
import sys
import time
from pathlib import Path

# Monitor configurations with maximum refresh rates
MONITORS = {
    'DP-2': {
        'name': 'ASUS 34" UltraWide',
        'vendor': 'AUS',
        'product': 'VG34VQEL1A',
        'description': 'ASUS monitor with 3440x1440 resolution',
        'max_mode': '3440x1440@100.006'
    },
    'DP-3': {
        'name': 'LG 29" UltraWide', 
        'vendor': 'GSM',
        'product': 'LG ULTRAWIDE',
        'description': 'LG monitor with 2560x1080 resolution',
        'max_mode': '2560x1080@60.000'
    },
    'DP-4': {
        'name': 'Iiyama 34" UltraWide',
        'vendor': 'IVM',
        'product': 'PL3481WQ', 
        'description': 'Iiyama monitor with 3440x1440 resolution',
        'max_mode': '3440x1440@179.981'
    },
    'eDP-1': {
        'name': 'Built-in Laptop Display',
        'vendor': 'CSO',
        'product': '0x1319',
        'description': 'Built-in laptop screen with 2880x1920 resolution',
        'max_mode': '2880x1920@60.000'
    }
}

def run_command(cmd, show_output=False):
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if show_output and result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"Error running command: {e}", file=sys.stderr)
        return False, "", str(e)

def get_connected_monitors():
    """Get list of currently connected monitors from gdctl"""
    success, output, _ = run_command("gdctl show")
    if not success:
        return set()
    
    connected = set()
    lines = output.split('\n')
    
    for line in lines:
        # Look for monitor lines like "├──Monitor DP-2 (ASUSTek COMPUTER INC 34")"
        if '──Monitor ' in line and '(' in line:
            # Extract monitor ID (e.g., "DP-2", "eDP-1")
            parts = line.split('Monitor ')
            if len(parts) > 1:
                monitor_id = parts[1].split(' ')[0]
                connected.add(monitor_id)
    
    return connected


def backup_config():
    """Save current configuration to backup and cleanup old backups"""
    backup_dir = Path.home() / "bin" / "monitors" / "configs"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Get current config and save it
    success, output, _ = run_command("gdctl show")
    if success:
        backup_file = backup_dir / f"gdctl-backup-{int(time.time())}.txt"
        with open(backup_file, 'w') as f:
            f.write(output)
        print(f"✓ Configuration backed up to: {backup_file}")
        
        # Cleanup old backups - keep only 5 most recent
        backup_files = sorted(backup_dir.glob("gdctl-backup-*.txt"), 
                            key=lambda x: x.stat().st_mtime, reverse=True)
        if len(backup_files) > 5:
            for old_backup in backup_files[5:]:
                old_backup.unlink()
                print(f"  Cleaned up old backup: {old_backup.name}")
        
        return str(backup_file)
    return None

def switch_to_single_monitor(monitor_id, with_backup=True, verbose=True):
    """Switch to single monitor using gdctl"""
    if monitor_id not in MONITORS:
        print(f"❌ Unknown monitor: {monitor_id}")
        return False
    
    # Safety check: Verify monitor is actually connected
    connected_monitors = get_connected_monitors()
    if monitor_id not in connected_monitors:
        monitor = MONITORS[monitor_id]
        print(f"❌ Monitor {monitor_id} ({monitor['name']}) is not connected!")
        
        if len(connected_monitors) == 1 and 'eDP-1' in connected_monitors:
            print("ℹ️  You appear to be on laptop-only mode (away from home setup)")
        else:
            print(f"ℹ️  Currently connected monitors: {', '.join(sorted(connected_monitors))}")
        
        print("💡 Use 'available' command to see only connected monitors")
        return False
    
    monitor = MONITORS[monitor_id]
    
    if verbose:
        print(f"🔄 Switching to: {monitor['name']} ({monitor_id})")
        print(f"   {monitor['description']} at {monitor['max_mode']}")
    
    # Backup current configuration
    if with_backup:
        backup_config()
    
    # Apply single monitor configuration using gdctl with maximum refresh rate
    max_mode = monitor['max_mode']
    if verbose:
        print(f"🔄 Applying configuration at maximum refresh rate ({max_mode})...")
        cmd = f"gdctl set --verbose --logical-monitor --primary --monitor {monitor_id} --mode {max_mode}"
    else:
        cmd = f"gdctl set --logical-monitor --primary --monitor {monitor_id} --mode {max_mode}"
    
    success, output, error = run_command(cmd, show_output=verbose)
    
    if success:
        if verbose:
            print(f"✅ Successfully switched to {monitor['name']}!")
            print("🚀 Change applied instantly - no logout required!")
        return True
    else:
        print(f"❌ Failed to switch to {monitor_id}: {error}")
        return False

def show_current_config():
    """Display current monitor configuration"""
    print("Current monitor configuration:")
    print("=" * 50)
    success, output, _ = run_command("gdctl show")
    if success:
        print(output)
    else:
        print("❌ Failed to get monitor configuration")

def list_available_monitors():
    """List all available monitors"""
    print("Available monitors:")
    print("=" * 50)
    
    for monitor_id, monitor in MONITORS.items():
        print(f"📺 {monitor_id}: {monitor['name']}")
        print(f"   {monitor['description']}")
        print(f"   Vendor: {monitor['vendor']}, Product: {monitor['product']}")
        print()

def show_available_monitors():
    """Show only currently connected monitors"""
    connected_monitors = get_connected_monitors()
    
    if not connected_monitors:
        print("❌ No monitors detected!")
        return
    
    print("Currently connected monitors:")
    print("=" * 50)
    
    for monitor_id in sorted(connected_monitors):
        if monitor_id in MONITORS:
            monitor = MONITORS[monitor_id]
            print(f"✅ {monitor_id}: {monitor['name']}")
            print(f"   {monitor['description']}")
            print(f"   Vendor: {monitor['vendor']}, Product: {monitor['product']}")
        else:
            print(f"⚠️  {monitor_id}: Unknown monitor (not in configuration)")
        print()
    
    # Show environment context
    if len(connected_monitors) == 1 and 'eDP-1' in connected_monitors:
        print("🏠 Environment: Laptop-only mode (away from home setup)")
    elif {'DP-2', 'DP-3', 'DP-4'}.issubset(connected_monitors):
        print("🏠 Environment: Full home setup (all external monitors connected)")
    else:
        external_count = len(connected_monitors - {'eDP-1'})
        print(f"🏠 Environment: Partial setup ({external_count} external monitor(s) connected)")
    
    print()
    print("Available commands:")
    for monitor_id in sorted(connected_monitors):
        if monitor_id in MONITORS:
            monitor = MONITORS[monitor_id]
            print(f"  {monitor_id.lower().replace('-', '')} - Switch to {monitor['name']}")
    
    if {'DP-2', 'DP-3', 'DP-4'}.issubset(connected_monitors):
        print(f"  triple - Custom triple monitor layout")

def setup_dual_monitor():
    """Setup dual monitor for portable/travel use - laptop + any external monitor"""
    print("🔄 Setting up dual monitor configuration (portable mode)...")
    print("   Layout: Laptop (left) | External Monitor (right)")
    
    # Check if laptop display is connected
    connected_monitors = get_connected_monitors()
    
    if 'eDP-1' not in connected_monitors:
        print("❌ Laptop display (eDP-1) not detected!")
        return False
    
    # Find any available external monitor (prioritize DP-3 for ARZOPA, but accept any)
    external_monitor = None
    actual_name = "External Monitor"
    
    # Check what's actually connected and get its real info
    success, output, _ = run_command("gdctl show")
    
    for monitor_id in ['DP-3', 'DP-4', 'DP-2']:  # Prioritize DP-3 for portable ARZOPA
        if monitor_id in connected_monitors:
            external_monitor = monitor_id
            # Extract actual monitor name from gdctl output
            if monitor_id in output:
                lines = output.split('\n')
                for line in lines:
                    if f"Monitor {monitor_id}" in line:
                        # Extract manufacturer and model from the line
                        import re
                        match = re.search(r'Monitor ' + monitor_id + r' \((.*?)\)', line)
                        if match:
                            actual_name = match.group(1)
                            print(f"   Detected: {actual_name} on {monitor_id}")
                            break
            break
    
    if not external_monitor:
        print("❌ No external monitor detected!")
        print(f"   This mode is for portable/travel setup with external monitor")
        print(f"   Connected monitors: {', '.join(sorted(connected_monitors))}")
        return False
    
    print(f"   Using: Laptop (eDP-1) + External ({external_monitor})")
    
    # Backup current config
    backup_config()
    
    # Determine the best mode for the external monitor at 60Hz
    # For DP-3 when it's ARZOPA portable: use 1920x1080@60.000
    # For other monitors: use their preferred mode at 60Hz if available
    if external_monitor == 'DP-3':
        # Could be ARZOPA portable or LG - try 1920x1080 first (common for portable monitors)
        external_mode = "1920x1080@60.000"
    elif external_monitor == 'DP-4':
        external_mode = "3440x1440@59.973"  # Iiyama at 60Hz
    elif external_monitor == 'DP-2':
        external_mode = "3440x1440@59.973"  # ASUS at 60Hz
    else:
        external_mode = "1920x1080@60.000"  # Safe default
    
    # Calculate position for external monitor based on scaled laptop width
    # Based on current working config: eDP-1 at scale 1.75 uses logical width of 1644
    external_x = 1644
    
    # Build the gdctl command
    cmd = f"""gdctl set --verbose \\
        --logical-monitor --monitor eDP-1 --mode 2880x1920@60.000 --scale 1.75 --x 0 --y 0 \\
        --logical-monitor --primary --monitor {external_monitor} --mode {external_mode} --x {external_x} --y 0"""
    
    success, output, error = run_command(cmd, show_output=True)
    
    if success:
        print("✅ Dual monitor configuration applied!")
        print("📺 Monitor Details:")
        print("   • Laptop (eDP-1): Left side, 2880x1920@60Hz, 175% scale")
        print(f"   • External ({external_monitor}): Right side, {external_mode}")
        print("🚀 Perfect for portable productivity!")
    else:
        print(f"❌ Failed to setup dual monitor: {error}")
        # Try fallback with different resolution if it failed
        if "mode" in str(error).lower() and external_monitor == 'DP-3':
            print("🔄 Retrying with alternative resolution...")
            external_mode = "2560x1080@60.000"  # Try LG resolution
            cmd = f"""gdctl set --verbose \\
                --logical-monitor --monitor eDP-1 --mode 2880x1920@60.000 --scale 1.75 --x 0 --y 0 \\
                --logical-monitor --primary --monitor {external_monitor} --mode {external_mode} --x 1644 --y 0"""
            success, output, error = run_command(cmd, show_output=True)
            if success:
                print("✅ Dual monitor configuration applied with alternative resolution!")
                return True
    
    return success

def restore_triple_monitor():
    """Restore custom triple monitor configuration with optimal layout and refresh rates"""
    print("🔄 Restoring custom triple monitor setup...")
    print("   Layout: LG Portrait (left) | Iiyama 180Hz (top-right) | ASUS 100Hz (bottom-right)")
    
    # Safety check: Verify all 3 external monitors are connected
    connected_monitors = get_connected_monitors()
    required_monitors = {'DP-2', 'DP-3', 'DP-4'}
    missing_monitors = required_monitors - connected_monitors
    
    if missing_monitors:
        print(f"❌ Triple monitor setup requires all 3 external monitors!")
        print(f"   Missing monitors: {', '.join(sorted(missing_monitors))}")
        
        if len(connected_monitors) == 1 and 'eDP-1' in connected_monitors:
            print("ℹ️  You appear to be on laptop-only mode (away from home setup)")
        else:
            print(f"ℹ️  Currently connected: {', '.join(sorted(connected_monitors))}")
            available_external = connected_monitors - {'eDP-1'}
            if available_external:
                print(f"💡 Try single monitor mode with: {', '.join(sorted(available_external))}")
        
        return False
    
    # Backup current config
    backup_config()
    
    # Create custom triple monitor configuration with maximum refresh rates
    cmd = """gdctl set --verbose \\
        --logical-monitor --monitor DP-3 --mode 2560x1080@60.000 --transform 270 --x 0 --y 0 \\
        --logical-monitor --monitor DP-4 --mode 3440x1440@179.981 --x 1080 --y 0 \\
        --logical-monitor --primary --monitor DP-2 --mode 3440x1440@100.006 --x 1080 --y 1440"""
    
    success, output, error = run_command(cmd, show_output=True)
    
    if success:
        print("✅ Custom triple monitor configuration applied!")
        print("📺 Monitor Details:")
        print("   • LG (DP-3): Portrait Left, 2560x1080@60Hz")
        print("   • Iiyama (DP-4): Secondary, 3440x1440@180Hz")
        print("   • ASUS (DP-2): Primary, 3440x1440@100Hz")
        print("🚀 All monitors at maximum refresh rates!")
        
    else:
        print(f"❌ Failed to restore triple monitor setup: {error}")
    
    return success

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        connected_monitors = get_connected_monitors()
        
        print("GNOME Instant Monitor Switcher (gdctl)")
        print("=" * 40)
        print("Usage: gdctl-instant.py <command>")
        print("\nCommands:")
        print("  DP-2       - Switch to ASUS monitor only")
        print("  DP-3       - Switch to LG monitor only") 
        print("  DP-4       - Switch to Iiyama monitor only")
        print("  eDP-1      - Switch to laptop display only")
        print("  show       - Show current configuration")
        print("  list       - List all available monitors")
        print("  available  - Show only connected monitors")
        print("  triple     - Restore triple monitor setup")
        print("  dual       - Dual monitor (laptop + portable)")
        
        # Show current environment context
        if connected_monitors:
            print("\n" + "=" * 40)
            if len(connected_monitors) == 1 and 'eDP-1' in connected_monitors:
                print("🏠 Current: Laptop-only mode (away from home)")
                print("💡 Only 'eDP-1' command will work in this setup")
            elif {'DP-2', 'DP-3', 'DP-4'}.issubset(connected_monitors):
                print("🏠 Current: Full home setup (all monitors connected)")
                print("💡 All commands available")
            else:
                available_external = connected_monitors - {'eDP-1'}
                print(f"🏠 Current: Partial setup ({len(available_external)} external monitor(s))")
                print(f"💡 Working commands: {', '.join(sorted(connected_monitors))}")
        
        print("\nExamples:")
        print("  gdctl-instant.py DP-2      # Switch to ASUS (instant)")
        print("  gdctl-instant.py available # Show only connected monitors")
        print("  gdctl-instant.py triple    # Restore all monitors (home only)")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "show":
        show_current_config()
    elif command == "list":
        list_available_monitors()
    elif command == "available":
        show_available_monitors()
    elif command == "triple":
        success = restore_triple_monitor()
        if not success:
            sys.exit(1)
    elif command == "dual":
        success = setup_dual_monitor()
        if not success:
            sys.exit(1)
    elif command in MONITORS:
        success = switch_to_single_monitor(command)
        if not success:
            sys.exit(1)
    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Run without arguments to see available commands")
        print("💡 Use 'available' to see only connected monitors")
        sys.exit(1)

if __name__ == "__main__":
    main()