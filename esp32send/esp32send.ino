#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

#define RXD2 16
#define TXD2 17

void setup() {
  Serial.begin(115200);          // USB debug
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);

  SerialBT.begin("ArmagedonPico32"); // Bluetooth device name

  Serial.println("Bluetooth ready. Pair and send text.");
}

void loop() {
  // From Bluetooth → Pico
  if (SerialBT.available()) {
    String msg = SerialBT.readStringUntil('\n');
    Serial2.println(msg);        // send to Pico
    Serial.println("BT -> Pico: " + msg);
  }

  // (optional) From Pico → Bluetooth
  if (Serial2.available()) {
    String msg = Serial2.readStringUntil('\n');
    SerialBT.println(msg);
    Serial.println("Pico -> BT: " + msg);
  }
}
