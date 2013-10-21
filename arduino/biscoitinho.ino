/*
  Repeating Web client
 
 This sketch connects to a a web server and makes a request
 using a Wiznet Ethernet shield. You can use the Arduino Ethernet shield, or
 the Adafruit Ethernet shield, either one will work, as long as it's got
 a Wiznet Ethernet module on board.
 
 This example uses DNS, by assigning the Ethernet client with a MAC address,
 IP address, and DNS address.
 
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 
 created 19 Apr 2012
 by Tom Igoe
 
 http://arduino.cc/en/Tutorial/WebClientRepeating
 This code is in the public domain.
 
 */

#include <SPI.h>
#include <Ethernet.h>
#include <SoftwareSerial.h>

//Thermal
#define BUFFER_SIZE 80
SoftwareSerial Thermal(2, 3);
int header = 0;
int heatTime = 80;
int heatInterval = 255;
char printDensity = 15; 
char printBreakTime = 15;

//Button
const int buttonPin = 5;     // the number of the pushbutton pin
const int ledPin =  4;      // the number of the LED pin
int buttonState = 0;         // variable for reading the pushbutton status
int buttonPressed = 0;

//Ethernet
// assign a MAC address for the ethernet controller.
// fill in your address here:
byte mac[] = { 
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
// fill in an available IP address on your network here,
// for manual configuration:
IPAddress ip(192,168,69,177);

// initialize the library instance:
EthernetClient client;

IPAddress server(192,168,69,1);

unsigned long lastConnectionTime = 0;          // last time you connected to the server, in milliseconds
boolean lastConnected = false;                 // state of the connection last time through the main loop
const unsigned long postingInterval = 60*100;  // delay between updates, in milliseconds

void setup() {
  
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);      
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);  
  // start serial port:
  Serial.begin(9600);
  // give the ethernet module time to boot up:
  delay(1000);
  // start the Ethernet connection using a fixed IP address and DNS server:
  Ethernet.begin(mac, ip);
  // print the Ethernet board/shield's IP address:
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
  Thermal.begin(19200); // to write to our new printer
  initPrinter();
}

void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH && buttonPressed == LOW) {
    buttonPressed = HIGH;
  }
    
  // if there's incoming data from the net connection.
  // send it out the serial port.  This is for debugging
  // purposes only:
  if (client.available()) {
    uint8_t header = 0;
    uint8_t buffer[BUFFER_SIZE];
    uint8_t pos = 0;
    while(client.available() > 0 && pos < BUFFER_SIZE) {
      if (header == 1) {
      buffer[pos++] = client.read(); //Take a character from serial port and check what it is   
      }
      else if (client.read() == '\x03') {
        header = 1;
        pos = 0;
      }
      if (pos > 0) {
        Thermal.write(buffer, pos);
        Serial.write(buffer, pos);
        pos = 0;
      }
    }
  }
  // if there's no net connection, but there was one last time
  // through the loop, then stop the client:
  if (!client.connected() && lastConnected) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    buttonPressed = LOW;
  }

  // if you're not connected, and ten seconds have passed since
  // your last connection, then connect again and send data:
  if(!client.connected() && (millis() - lastConnectionTime > postingInterval) && buttonPressed == HIGH) {
    httpRequest();
    buttonPressed = LOW;
  }
  // store the state of the connection for next time through
  // the loop:
  lastConnected = client.connected();
}


void initPrinter()
{
 //Modify the print speed and heat
 Thermal.write(27);
 Thermal.write(55);
 Thermal.write(7); //Default 64 dots = 8*('7'+1)
 Thermal.write(heatTime); //Default 80 or 800us
 Thermal.write(heatInterval); //Default 2 or 20us
 //Modify the print density and timeout
 Thermal.write(18);
 Thermal.write(35);
 int printSetting = (printDensity<<4) | printBreakTime;
 Thermal.write(printSetting); //Combination of printDensity and printBreakTime
 Serial.println();
 Serial.println("Printer ready"); 
 //Thermal.println("Printer ready!");
}

// this method makes a HTTP connection to the server:
void httpRequest() {
  // if there's a successful connection:
  if (client.connect(server, 5000)) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.println("GET / HTTP/1.1");
    client.println("Host: www.arduino.cc");
    client.println("User-Agent: arduino-ethernet");
    client.println("Connection: close");
    client.println();
  
    // note the time that the connection was made:
    lastConnectionTime = millis();
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println("disconnecting.");
    client.stop();
  }
}




