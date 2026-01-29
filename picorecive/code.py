import board
import busio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize the keyboard
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# UART setup
uart = busio.UART(
    board.GP0,  # TX
    board.GP1,  # RX
    baudrate=115200,
    timeout=0.01
)

# Custom command map
customCommandMap = {
    "DEFINE": "# Custom command DEFINE placeholder",
    "ATTACK_F": "# Custom command ATTACK_F placeholder",
}

# Explicit keycode map ONLY (safe on CircuitPython)
keycodeMap = {
    "ENTER": Keycode.ENTER,
    "GUI": Keycode.GUI,
    "SHIFT": Keycode.SHIFT,
    "CTRL": Keycode.CONTROL,
    "ALT": Keycode.ALT,
    "TAB": Keycode.TAB,
    "ESC": Keycode.ESCAPE,
    "SPACE": Keycode.SPACEBAR,
    "DELETE": Keycode.DELETE,
    "BACKSPACE": Keycode.BACKSPACE,
    "UP": Keycode.UP_ARROW,
    "DOWN": Keycode.DOWN_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    "CAPSLOCK": Keycode.CAPS_LOCK,
    "F1": Keycode.F1,
    "F2": Keycode.F2,
    "F3": Keycode.F3,
    "F4": Keycode.F4,
    "F5": Keycode.F5,
    "F6": Keycode.F6,
    "F7": Keycode.F7,
    "F8": Keycode.F8,
    "F9": Keycode.F9,
    "F10": Keycode.F10,
    "F11": Keycode.F11,
    "F12": Keycode.F12,
}

buffer = ""

def parse_keycode(key):
    return keycodeMap.get(key.upper())

def parse_keys(parts):
    keys = []
    for part in parts:
        k = parse_keycode(part)
        if k:
            keys.append(k)
        # else:
        #     print("Unknown key:", repr(part))  # optional debug
    return keys

def run_command(command_line):
    parts = command_line.strip().split()
    if not parts:
        return

    command = parts[0].upper()

    if command == "DELAY" and len(parts) > 1:
        time.sleep(float(parts[1]) / 1000)

    elif command == "STRING":
        keyboard_layout.write(" ".join(parts[1:]))

    elif command == "STRINGLN":
        keyboard_layout.write(" ".join(parts[1:]))
        keyboard.send(Keycode.ENTER)

    elif command == "REM":
        print("#", " ".join(parts[1:]))

    elif command in customCommandMap:
        print(customCommandMap[command])

    else:
        keys = parse_keys(parts)
        if keys:
            keyboard.send(*keys)

print("UART HID listener ready")

while True:
    char = uart.read(1)
    if char:
        try:
            c = char.decode("utf-8")
        except UnicodeError:
            continue

        if c == "\n" or c == "\r":
            command = buffer.strip()
            buffer = ""
            if command:
                print("Running command:", command)
                run_command(command)
                time.sleep(0.05)
        else:
            buffer += c

    time.sleep(0.005)

