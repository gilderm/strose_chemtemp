
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is conntec to the Arduino digital pin 4
#define ONE_WIRE_BUS 4
#define BUTTON1_PIN 2
#define BUTTON2_PIN 8

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);
DeviceAddress tempDeviceAddress;
int numberOfDevices;

int button1State = 0;
int button2State = 0;

// function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

void setup(void)
{
  Serial.begin(9600);
  //initialize the LED pin as an output
  pinMode(BUTTON1_PIN, INPUT_PULLUP);
  pinMode(BUTTON2_PIN, INPUT_PULLUP);
  pinMode(12, OUTPUT);

  // Start up the library
  sensors.begin();
  numberOfDevices = sensors.getDeviceCount();
  for (int i = 0; i < numberOfDevices; i++) {
    sensors.getAddress(tempDeviceAddress, 0);
    Serial.print("Found device ");
    Serial.print(i, DEC);
    Serial.print(" with address: ");
    printAddress(tempDeviceAddress);
    Serial.println();
  }
}

void loop(void){ 
  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 
  //Serial.print("Celsius temperature: ");
  // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  //Serial.print(sensors.getTempCByIndex(0)); 
  //Serial.print(" - Fahrenheit temperature: ");
  //Serial.println(sensors.getTempFByIndex(0));
  Serial.print("Celsius: ");
  Serial.print(sensors.getTempC(tempDeviceAddress));
  Serial.print(" Fahrenheit: ");
  Serial.println(sensors.getTempF(tempDeviceAddress));

  button1State = digitalRead(BUTTON1_PIN);
  button2State = digitalRead(BUTTON2_PIN);
  if (button1State == 0) {
    Serial.println(" Button 1 - Pressed!");
    digitalWrite(12,HIGH);
  }
  if (button2State == 0) {
    Serial.println(" Button 2 - Pressed!");
    digitalWrite(12,HIGH);
  }
  delay(100);

  if (button1State == 0) {
    digitalWrite(12,LOW);
  }
  if (button2State == 0) {
    digitalWrite(12,LOW);
  }
}

