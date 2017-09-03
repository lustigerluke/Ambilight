
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "FastLED.h"


//WIFI CONFIG
const char *ssid = "Floppy_Disk_W2"; //  your network SSID (name)
const char *pass = "Luc1lle#";       // your network password

int debug = 0;


//UDP CONFIG
WiFiUDP udp;
unsigned int localPort = 2390;  // local port to listen for UDP packets

//LED CONFIG
#define NUM_LEDS 96             // How many leds in your strip?
#define DATA_PIN 1              // Status LED
#define DATA_PIN1 4             // Leiste 1

CRGB statusled[1];
CRGB leds[NUM_LEDS];


int defRED   = 255;
int defGREEN = 070;
int defBLUE  = 000;

//time CONFIG
unsigned long currentMillis = millis();
unsigned long previousMillis = currentMillis;

int loop_counter = 0;
int nothing_counter = 0;
int received_package_counter = 0;
int processed_package_counter = 0;
int processed_LED60_counter = 0;



void setup()
{
  delay(1000);
  Serial.begin(115200);
  Serial.println();
  Serial.println();

  // We start by connecting to a WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  
  Serial.println("WiFi connected");
  Serial.println(WiFi.SSID());
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.macAddress());

  Serial.println("Starting UDP");
  udp.begin(localPort);
  Serial.print("Local port: ");
  Serial.println(udp.localPort());


  Serial.print("LED setup: ");
  FastLED.addLeds<WS2812B, DATA_PIN>(statusled, 1);
  FastLED.addLeds<NEOPIXEL, DATA_PIN1>(leds, NUM_LEDS);
 
  for(int x = 0; x < NUM_LEDS ; x++){  leds[x] = CRGB(defRED,defGREEN,defBLUE);}
  FastLED.show();   //update led stripe
  
  Serial.println("done!");
}

void loop()
{

  
  loop_counter = loop_counter + 1;
  
  int cb = udp.parsePacket();
  //Serial.print("cb: ");
  //Serial.println(cb);
  byte packetBuffer[cb];  //buffer to hold incoming and outgoing packets
  char charMatrix[480];    //Matrix to hold char values
  String package;         //long String representing char Mtrix

  
  if (!cb) {
    nothing_counter = nothing_counter + 1;
    //Serial.println("Nix");
  }
  else {
    received_package_counter = received_package_counter + 1;

    //Serial.println("OK");
    
    // We've received a packet, read the data from it
    udp.read(packetBuffer, cb); // read the packet into the buffer


    //convert every byte to a character
    int i=0;  
    while(i<cb){

      charMatrix[i]= char (packetBuffer[i]);
      i++;
    }
    
    //convert the character array to String
    package=charMatrix;
    //Serial.println(package);


    //Serial.println("Package: ");
    //Serial.println(package);
    //Serial.println();



    // set default LED value for all LEDs
    if (package[0]=='a') 
    {
      package=package.substring(2);
      defRED = package.toInt();
      package=package.substring(4);
      defGREEN = package.toInt();
      package=package.substring(4);
      defBLUE = package.toInt();
      package=package.substring(4);
      Serial.print("defRed: ");
      Serial.println(defRED);
      Serial.print("defGreen: ");
      Serial.println(defGREEN);
      Serial.print("defBLUE: ");
      Serial.println(defBLUE);

      //write value in every cell of LEDs-matrix
      for(int x = 0; x < NUM_LEDS ; x++){  leds[x] = CRGB(defRED,defGREEN,defBLUE);}
    }//endif package[0] == 'a'


    // set single LEDs --------------------------------
    if (package[0] == 'A')
    {
      int adr;      
      int red;
      int gre;
      int blu;


      while ( package.length() >= 16 ){

        package = package.substring(1); //delete "A" before every led command
  
        adr = package.toInt();
        package=package.substring(4); //delete the first int value and the seperator char
  
        red = package.toInt();
        package=package.substring(4);
  
        gre = package.toInt();
        package=package.substring(4);
        
        blu = package.toInt();
        package=package.substring(3);

        if(adr == 60)
        {
          processed_LED60_counter = processed_LED60_counter + 1;
          Serial.println(blu);
        }

        //Serial.println(adr);
        leds[adr] = CRGB(red,gre,blu);
    
      }
      
      processed_package_counter = processed_package_counter + 1;
       
      
      //fps_counter
      currentMillis = millis();
      if (currentMillis - previousMillis >=  1000 ) {
        previousMillis = currentMillis;
        
        Serial.println();
        Serial.print("Loop counter: ");
        Serial.println(loop_counter);
        loop_counter = 0;
        
        Serial.print("Nothing happened counter; ");
        Serial.println(nothing_counter);
        nothing_counter = 0;

        Serial.print("received package counter: ");
        Serial.println(received_package_counter);
        received_package_counter = 0;

        Serial.print("processed LED 60 counter: ");
        Serial.println(processed_LED60_counter);
        processed_LED60_counter = 0;

     
      } //endif for rps
    }//endif message for led commands

    
    FastLED.show();   //update led stripe
    
  } //else (end what t0 do if input was available)

  


}//loop

