def log_switch_event(message: str):
    """
    Appends a log message with a timestamp to monitor_switch.log
    """
    from datetime import datetime
    with open("monitor_switch.log", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
def list_connected_keyboards() -> list:
    """
    Returns a list of all connected keyboard names (Windows only).
    """
    os_name = platform.system()
    if os_name == "Windows":
        try:
            result = subprocess.run(["wmic", "path", "Win32_Keyboard", "get", "Name"], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            # Remove header and empty lines
            keyboards = [line.strip() for line in lines[1:] if line.strip()]
            return keyboards
        except Exception as e:
            print(f"Error listing keyboards: {e}")
            return []
    else:
        return []
import time

def any_keyboard_connected() -> bool:
    """
    Returns True if any keyboard is connected (Windows only).
    """
    os_name = platform.system()
    try:
        if os_name == "Windows":
            keyboards = list_connected_keyboards()
            return len(keyboards) > 0
        else:
            print(f"Keyboard detection is only supported on Windows. Current OS: {os_name}")
            return False
    except Exception as e:
        print(f"Error detecting keyboard: {e}")
        return False

def monitor_keyboard_and_switch(poll_interval: float = 2.0):
    """
    Monitors for the presence of any keyboard and switches monitor inputs accordingly.
    When any keyboard is plugged in, sets monitors to DisplayPort. When none are attached, sets to USB-C.
    :param poll_interval: How often to check (in seconds).
    """
    print(f"Monitoring for any keyboard (polling every {poll_interval} seconds)...")
    last_connected = None
    last_monitor_inputs = {1: 'Unknown', 2: 'Unknown'}
    try:
        while True:
            connected = any_keyboard_connected()
            if last_connected is None:
                last_connected = connected
            if connected and not last_connected:
                print("Keyboard detected.")
                set_both_monitors_to_displayport()
                last_monitor_inputs[1] = 'DisplayPort'
                last_monitor_inputs[2] = 'DisplayPort'
                log_switch_event("Keyboard detected. Switched both monitors to DisplayPort.")
            elif not connected and last_connected:
                print("No keyboard detected.")
                set_both_monitors_to_usbc()
                last_monitor_inputs[1] = 'USB-C'
                last_monitor_inputs[2] = 'USB-C'
                log_switch_event("No keyboard detected. Switched both monitors to USB-C.")
            else:
                # Print status even if nothing changed
                if connected:
                    print("Keyboard detected.")
                else:
                    print("No keyboard detected.")
            print(f"Monitor 1 last input: {last_monitor_inputs[1]}, Monitor 2 last input: {last_monitor_inputs[2]}")
            last_connected = connected
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("Stopped monitoring.")

import sys
import subprocess
import platform

def switch_mouse_input():
    """
    Placeholder for switching Logitech mouse input.
    To be implemented: logic for switching mouse pairing or input.
    """
    print("Mouse input switching not yet implemented.")



def set_monitor_input(display_num: int, input_code: str):
    """
    Sets the input source of a monitor using ddcctl (macOS) or ClickMonitorDDC (Windows).
    :param display_num: The display number (1, 2, ...)
    :param input_code: The input code as a string (e.g., '15' for DisplayPort, '27' for USB-C)
    """
    os_name = platform.system()
    if os_name == "Darwin":
        cmd = [
            "ddcctl",
            "-d", str(display_num),
            "-i", str(input_code)
        ]
    elif os_name == "Windows":
        # For DisplayPort, input_code should be 'DisplayPort', for USB-C use '27'
        if input_code == '15':
            input_arg = "DisplayPort"
        elif input_code == '27':
            input_arg = "27"
        else:
            input_arg = input_code
        cmd = [
            r"C:\\Users\\ermak\\tools\\ClickMonitorDDC_7_2\\ClickMonitorDDC_7_2.exe",
            str(display_num), "t", "s", input_arg, "t", "s", "DisplayPort" if input_code == '15' else "USB-C"
        ] if input_code in ['15', '27'] else [
            r"C:\\Users\\ermak\\tools\\ClickMonitorDDC_7_2\\ClickMonitorDDC_7_2.exe",
            str(display_num), "t", "s", input_arg
        ]
    else:
        print(f"Unsupported OS: {os_name}")
        return

    print(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Set display {display_num} to input {input_code}. Output:\n{result.stdout}")
    except FileNotFoundError:
        tool_name = 'ddcctl' if os_name == 'Darwin' else 'C:\\Users\\ermak\\tools\\ClickMonitorDDC_7_2\\ClickMonitorDDC_7_2.exe'
        print(f"Required tool not found. Please ensure {tool_name} is present.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set display {display_num}: {e.stderr}")

def set_both_monitors_to_displayport():
    set_monitor_input(1, '15')
    set_monitor_input(2, '15')

def set_both_monitors_to_usbc():
    set_monitor_input(1, '27')
    set_monitor_input(2, '27')

def toggle_monitor_input(display_num: int):
    """
    Toggles the input source of a monitor (currently sets to DisplayPort as example).
    :param display_num: The display number (1, 2, ...)
    """
    set_monitor_input(display_num, '15')

if __name__ == "__main__":
    monitor_keyboard_and_switch()
