#!/usr/bin/env python3
"""
Interactive GNOME Monitor Switcher
Dynamic CLI for selecting monitors and refresh rates using gdctl
"""

import subprocess
import sys
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class MonitorMode:
    """Represents a single monitor mode (resolution + refresh rate)"""
    resolution: str
    refresh_rate: str
    
    @property
    def mode_string(self) -> str:
        """Returns the mode in gdctl format: 3440x1440@179.981"""
        return f"{self.resolution}@{self.refresh_rate}"
    
    @property
    def display_name(self) -> str:
        """Returns user-friendly display name"""
        return f"{self.resolution} @ {self.refresh_rate} Hz"


@dataclass  
class Monitor:
    """Represents a monitor with all its available modes"""
    id: str
    name: str
    vendor: str = ""
    product: str = ""
    modes: List[MonitorMode] = field(default_factory=list)
    current_mode: Optional[MonitorMode] = None
    
    @property
    def display_name(self) -> str:
        """Returns user-friendly monitor name"""
        return f"{self.name} ({self.id})"
    
    def get_modes_by_resolution(self) -> dict:
        """Groups modes by resolution for better UI"""
        grouped = {}
        for mode in self.modes:
            if mode.resolution not in grouped:
                grouped[mode.resolution] = []
            grouped[mode.resolution].append(mode)
        
        # Sort refresh rates within each resolution (highest first)
        for resolution in grouped:
            grouped[resolution].sort(key=lambda m: float(m.refresh_rate), reverse=True)
        
        return grouped


def run_command(cmd: str, capture_output=True) -> Tuple[bool, str, str]:
    """Run shell command and return success status, stdout, stderr"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_gdctl_output() -> str:
    """Get gdctl show --modes output"""
    success, output, error = run_command("gdctl show --modes")
    if not success:
        raise RuntimeError(f"Failed to get monitor information: {error}")
    return output


def get_current_config() -> str:
    """Get current gdctl configuration"""
    success, output, error = run_command("gdctl show")
    if not success:
        raise RuntimeError(f"Failed to get current configuration: {error}")
    return output


def parse_current_modes(config_output: str) -> dict:
    """Parse current mode for each monitor from gdctl show output"""
    current_modes = {}
    current_monitor = None
    
    for line in config_output.split('\n'):
        # Monitor header: "├──Monitor DP-2 (ASUSTek COMPUTER INC 34")"
        monitor_match = re.search(r'├──Monitor\s+(\S+)\s+\((.+?)\)', line)
        if monitor_match:
            current_monitor = monitor_match.group(1)
        
        # Current mode: "│  │   └──3440x1440@59.973"  
        elif '└──' in line and '@' in line and current_monitor:
            mode_text = line.split('└──')[1].strip()
            if '@' in mode_text:
                resolution, refresh = mode_text.split('@')
                current_modes[current_monitor] = MonitorMode(resolution, refresh)
    
    return current_modes


def parse_monitors(gdctl_output: str) -> List[Monitor]:
    """Parse gdctl show --modes output into Monitor objects"""
    monitors = []
    current_monitor = None
    
    for line in gdctl_output.split('\n'):
        # Monitor header: "├──Monitor DP-2 (ASUSTek COMPUTER INC 34")"
        monitor_match = re.search(r'├──Monitor\s+(\S+)\s+\((.+?)\)', line)
        if monitor_match:
            monitor_id = monitor_match.group(1)
            monitor_name = monitor_match.group(2)
            current_monitor = Monitor(id=monitor_id, name=monitor_name)
            monitors.append(current_monitor)
        
        # Vendor: "│  ├──Vendor: AUS"
        elif '├──Vendor:' in line and current_monitor:
            current_monitor.vendor = line.split('Vendor:')[1].strip()
            
        # Product: "│  ├──Product: VG34VQEL1A" 
        elif '├──Product:' in line and current_monitor:
            current_monitor.product = line.split('Product:')[1].strip()
            
        # Mode: "│      ├──3440x1440@100.006"
        elif re.match(r'│\s+├──\d+x\d+@\d+\.\d+', line) and current_monitor:
            mode_text = line.split('├──')[1].strip()
            if '@' in mode_text:
                resolution, refresh = mode_text.split('@')
                current_monitor.modes.append(MonitorMode(resolution, refresh))
    
    # Get current modes and match them
    try:
        current_config = get_current_config()
        current_modes = parse_current_modes(current_config)
        
        for monitor in monitors:
            if monitor.id in current_modes:
                current_mode = current_modes[monitor.id]
                # Find matching mode in monitor's available modes
                for mode in monitor.modes:
                    if mode.resolution == current_mode.resolution and mode.refresh_rate == current_mode.refresh_rate:
                        monitor.current_mode = mode
                        break
    except Exception as e:
        print(f"Warning: Could not determine current modes: {e}")
    
    return monitors


def display_header():
    """Display program header"""
    print("=" * 50)
    print("🖥️  GNOME Monitor Switcher")
    print("=" * 50)
    print()


def display_monitor_menu(monitors: List[Monitor]) -> Monitor:
    """Display monitor selection menu and return selected monitor"""
    while True:
        print("Connected Monitors:")
        print("-" * 30)
        
        for i, monitor in enumerate(monitors, 1):
            current_info = ""
            if monitor.current_mode:
                current_info = f" - Currently: {monitor.current_mode.display_name}"
            print(f"[{i}] {monitor.display_name}{current_info}")
        
        print(f"\n[Q] Quit")
        print()
        
        choice = input(f"Select monitor [1-{len(monitors)}] or Q to quit: ").strip().upper()
        
        if choice == 'Q':
            print("Exiting...")
            sys.exit(0)
        
        try:
            monitor_idx = int(choice) - 1
            if 0 <= monitor_idx < len(monitors):
                return monitors[monitor_idx]
            else:
                print(f"❌ Invalid selection. Please enter 1-{len(monitors)} or Q.\n")
        except ValueError:
            print(f"❌ Invalid input. Please enter a number 1-{len(monitors)} or Q.\n")


def display_refresh_rate_menu(monitor: Monitor) -> MonitorMode:
    """Display refresh rate selection menu for a monitor"""
    while True:
        print(f"\nAvailable modes for {monitor.display_name}:")
        print("-" * 50)
        
        modes_by_resolution = monitor.get_modes_by_resolution()
        all_modes = []
        
        # Display modes grouped by resolution
        for resolution, modes in modes_by_resolution.items():
            # Check if this is the native/preferred resolution (highest pixel count)
            pixel_count = int(resolution.split('x')[0]) * int(resolution.split('x')[1])
            is_native = pixel_count == max(
                int(res.split('x')[0]) * int(res.split('x')[1]) 
                for res in modes_by_resolution.keys()
            )
            
            resolution_label = f"{resolution}"
            if is_native:
                resolution_label += " (Native)"
            
            print(f"\n{resolution_label}:")
            
            for mode in modes:
                all_modes.append(mode)
                index = len(all_modes)
                
                # Mark current mode and highest refresh rate
                markers = []
                if monitor.current_mode and mode.mode_string == monitor.current_mode.mode_string:
                    markers.append("✓ Current")
                if mode == modes[0]:  # First in sorted list = highest refresh rate
                    markers.append("⭐ Maximum")
                
                marker_text = f" ({', '.join(markers)})" if markers else ""
                print(f"  [{index}] {mode.refresh_rate} Hz{marker_text}")
        
        print(f"\n[B] Back to monitor selection")
        print(f"[Q] Quit")
        print()
        
        choice = input(f"Select mode [1-{len(all_modes)}], B to go back, or Q to quit: ").strip().upper()
        
        if choice == 'Q':
            print("Exiting...")
            sys.exit(0)
        elif choice == 'B':
            return None
        
        try:
            mode_idx = int(choice) - 1
            if 0 <= mode_idx < len(all_modes):
                return all_modes[mode_idx]
            else:
                print(f"❌ Invalid selection. Please enter 1-{len(all_modes)}, B, or Q.\n")
        except ValueError:
            print(f"❌ Invalid input. Please enter a number 1-{len(all_modes)}, B, or Q.\n")


def confirm_switch(monitor: Monitor, mode: MonitorMode) -> bool:
    """Ask user to confirm the monitor switch"""
    print(f"\n📋 Configuration Summary:")
    print(f"   Monitor: {monitor.display_name}")
    print(f"   Mode: {mode.display_name}")
    
    if monitor.current_mode:
        print(f"   Current: {monitor.current_mode.display_name}")
    
    print()
    
    while True:
        choice = input("Apply this configuration? [y/N]: ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no', '']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def backup_current_config():
    """Create backup of current configuration"""
    try:
        success, output, error = run_command("gdctl show")
        if success:
            import time
            from pathlib import Path
            
            backup_dir = Path.home() / "bin" / "monitors" / "configs"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            backup_file = backup_dir / f"gdctl-backup-{int(time.time())}.txt"
            with open(backup_file, 'w') as f:
                f.write(output)
            
            print(f"✓ Configuration backed up to: {backup_file.name}")
            return str(backup_file)
    except Exception as e:
        print(f"⚠️  Warning: Could not create backup: {e}")
        return None


def apply_configuration(monitor_id: str, mode: MonitorMode) -> bool:
    """Apply the selected monitor configuration"""
    print(f"\n🔄 Switching to {mode.display_name}...")
    
    # Create backup first
    backup_current_config()
    
    # Apply configuration
    cmd = f"gdctl set --verbose --logical-monitor --primary --monitor {monitor_id} --mode {mode.mode_string}"
    
    success, output, error = run_command(cmd)
    
    if success:
        print("✅ Successfully applied configuration!")
        print("🚀 Monitor switch completed!")
        return True
    else:
        print(f"❌ Failed to apply configuration: {error}")
        print("💡 Your previous configuration has been backed up for recovery.")
        return False


def main():
    """Main program entry point"""
    display_header()
    
    try:
        # Get and parse monitor information
        print("🔍 Detecting monitors...")
        gdctl_output = get_gdctl_output()
        monitors = parse_monitors(gdctl_output)
        
        if not monitors:
            print("❌ No monitors detected!")
            print("💡 Make sure monitors are connected and gdctl is working.")
            sys.exit(1)
        
        print(f"✓ Found {len(monitors)} monitor(s)")
        print()
        
        while True:
            # Monitor selection
            selected_monitor = display_monitor_menu(monitors)
            
            # Refresh rate selection  
            selected_mode = display_refresh_rate_menu(selected_monitor)
            
            # Handle back navigation
            if selected_mode is None:
                continue
            
            # Confirmation and application
            if confirm_switch(selected_monitor, selected_mode):
                success = apply_configuration(selected_monitor.id, selected_mode)
                if success:
                    # Update current mode for display
                    selected_monitor.current_mode = selected_mode
                
                print("\nPress Enter to continue or Ctrl+C to exit...")
                input()
                print()
            else:
                print("❌ Configuration not applied.\n")
                
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Try running 'gdctl show' to verify your system setup.")
        sys.exit(1)


if __name__ == "__main__":
    main()