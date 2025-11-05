// arduino_serial_reader.ino

void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
  Serial.println("Arduino UNO R4 Initialized.");
  Serial.println("Waiting for forecasted power data from Client-3...");
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming string until the newline character
    String data = Serial.readStringUntil('\n');
    
    // Print the received data to the Serial Monitor
    Serial.print("Received Forecast Value: ");
    Serial.println(data);
  }
}