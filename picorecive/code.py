import board
import busio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize keyboard
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# UART setup
uart = busio.UART(
    board.GP0,
    board.GP1,
    baudrate=115200,
    timeout=0.01
)

# Custom command map
customCommandMap = {
    "DEFINE": "# Custom command DEFINE placeholder",
    "ATTACK_F": "# Custom command ATTACK_F placeholder",
}

# Modifier keys
modifierKeys = {
    "CTRL": Keycode.CONTROL,
    "SHIFT": Keycode.SHIFT,
    "ALT": Keycode.ALT,
    "GUI": Keycode.GUI
}

# Normal keys
keycodeMap = {
    "ENTER": Keycode.ENTER,
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
    # Add letters/numbers if needed
    "A": Keycode.A, "B": Keycode.B, "C": Keycode.C,
    "D": Keycode.D, "E": Keycode.E, "F": Keycode.F,
    "G": Keycode.G, "H": Keycode.H, "I": Keycode.I,
    "J": Keycode.J, "K": Keycode.K, "L": Keycode.L,
    "M": Keycode.M, "N": Keycode.N, "O": Keycode.O,
    "P": Keycode.P, "Q": Keycode.Q, "R": Keycode.R,
    "S": Keycode.S, "T": Keycode.T, "U": Keycode.U,
    "V": Keycode.V, "W": Keycode.W, "X": Keycode.X,
    "Y": Keycode.Y, "Z": Keycode.Z,
    "0": Keycode.ZERO, "1": Keycode.ONE, "2": Keycode.TWO,
    "3": Keycode.THREE, "4": Keycode.FOUR, "5": Keycode.FIVE,
    "6": Keycode.SIX, "7": Keycode.SEVEN, "8": Keycode.EIGHT,
    "9": Keycode.NINE,
}

buffer = ""

# Parse keys into modifiers and main keys
def parse_keys(parts):
    modifiers = []
    keys = []
    for part in parts:
        part_upper = part.upper()
        if part_upper in modifierKeys:
            modifiers.append(modifierKeys[part_upper])
        elif part_upper in keycodeMap:
            keys.append(keycodeMap[part_upper])
        # else: ignore unknown keys
    return modifiers, keys

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
        # split into modifiers + keys
        modifiers, keys = parse_keys(parts)
        if modifiers or keys:
            keyboard.press(*modifiers)
            keyboard.send(*keys) if keys else None
            keyboard.release_all()

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
