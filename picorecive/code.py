import board
import busio
import time

uart = busio.UART(
    board.GP0,  # TX (not used here, but required)
    board.GP1,  # RX
    baudrate=115200,
    timeout=0.1
)

while True:
    data = uart.readline()
    if data:
        print("Received:", data.decode("utf-8").strip())
    time.sleep(0.05)
