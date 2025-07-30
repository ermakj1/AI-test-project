
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
    # Example usage:
    # Toggle both monitors to DisplayPort
    toggle_monitor_input(1)
    toggle_monitor_input(2)
    # Or set both to DisplayPort:
    # set_both_monitors_to_displayport()
    # Or set both to USB-C:
    # set_both_monitors_to_usbc()
