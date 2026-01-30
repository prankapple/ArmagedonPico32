import board
import digitalio
import storage
import usb_hid

switch = digitalio.DigitalInOut(board.GP10)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP  # ON = grounded

if switch.value:
    # SAFE MODE
    print("SAFE MODE: USB storage enabled")
else:
    # ARMED MODE
    print("ARMED MODE: HID only")
    storage.disable_usb_drive()
    usb_hid.enable()
