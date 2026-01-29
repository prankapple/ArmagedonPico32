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
    "STRINGLN": "# Custom command STRINGLN placeholder"
}

# Optional keycode map if you want real key presses
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
    "SPACEBAR": Keycode.SPACEBAR,
    "SPACE": Keycode.SPACEBAR
}


buffer = ""  # incoming characters

def parse_keycode(key):
    """Return Keycode for a key string, fallback to Keycode.KEY"""
    return keycodeMap.get(key.upper(), getattr(Keycode, key.upper(), None))

def parse_keys(parts):
    """Convert parts into a comma-separated keycode string"""
    keys = []
    for part in parts:
        k = parse_keycode(part)
        if k:
            keys.append(k)
    return keys

def run_command(command_line):
    """Convert a single line into HID actions or comments"""
    parts = command_line.strip().split()
    if not parts:
        return

    command = parts[0].upper()

    if command == "DELAY":
        delay_time = float(parts[1]) / 1000.0
        time.sleep(delay_time)
    elif command == "STRING":
        string_content = " ".join(parts[1:])
        keyboard_layout.write(string_content)
    elif command == "REM":
        # comment, just print for debugging
        print("# " + " ".join(parts[1:]))
    elif command in customCommandMap:
        print(customCommandMap[command])
    else:
        # treat as key press
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

        if c == "\n":
            command = buffer.strip()
            buffer = ""
            if command:
                print("Running command:", command)
                run_command(command)
                time.sleep(0.05)  # small delay between commands
        else:
            buffer += c

    time.sleep(0.005)

