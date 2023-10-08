#include <ArduinoJson.h>
#include <SoftwareSerial.h>
SoftwareSerial espSerial(0, 1);    // Rx:0, Tx:1
const int lightSensorPin = A1;
StaticJsonDocument<200> doc;

void setup() {
  espSerial.begin(9600);          // Initialize serial communication at 9600 baud
}

void loop() {
  int lightValue = analogRead(lightSensorPin);  // Read the analog value from the sensor
  String outputString = "";
  doc["ParamName"] = "Light_Intensity";
  doc["ParamValue"] = lightValue;
  serializeJson(doc, outputString);
  espSerial.println(outputString);           // Write the value to NodeMCU
  doc.clear();
  delay(1000);
}
