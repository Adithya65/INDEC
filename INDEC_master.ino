
 
 #include <Wire.h>
#include <Adafruit_BMP085.h>
#define seaLevelPressure_hPa 1013.25

Adafruit_BMP085 bmp;
#include "DHT.h"
#define DHTPIN 5
String z;
DHT dht(DHTPIN, DHT11);
#define DUMP_REGS

#include <Wire.h>
#include <APDS9930.h>
int i;
float sensorValue;
APDS9930 apds = APDS9930();
float ambient_light = 0;


void setup()
{

  // Initialize Serial port
  Serial.begin(9600);
  dht.begin();
  if ( apds.init() )
  {
    i = 0;
  }
if (!bmp.begin()) {
 i=0;
  while (1) {}
  }

  // Start running the APDS-9930 light sensor (no interrupts)
  if ( apds.enableLightSensor(false) )
  {
    i = 0;
  }



}


void loop()
{ delay(1000);

  // Read the light levels (ambient, red, green, blue)
  if (  !apds.readAmbientLightLux(ambient_light)) {
    i = 0;
  }
  else
  {


  }

  // Wait 1 second before next reading

  sensorValue = analogRead(0); // read analog input pin 0




  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float L=analogRead(1);
  
   float p=bmp.readPressure();
    

     
    float alt=bmp.readAltitude();
     

     
    float sp=bmp.readSealevelPressure();
    
  z = String(h) + String(',') + String(t) + String(',') + String(1) + String(',') + String(sensorValue)+String(',')+String(L)+String(',')+String(p)+String(',')+String(alt)+String(',')+String(sp);
  Serial.println(z);

}
