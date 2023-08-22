// !! Have to install //
// include extern library
/***************************/
// IR Library
#include <IRremote.h>
// Humid & Temperature Library
#include <DHT11.h>
#include <DHT.h>
// LUX Library
#include <Wire.h>
#include <WAT_ALS468.h>

// Init arduino pin number
int pin = A0;
const int RECV_PIN = 7;

// Init Humid Sensor
//DHT11 dht11(pin);
DHT dht(pin, DHT11);

// Init IR Sensor
IRrecv irrecv(RECV_PIN);
IRsend irsend;
decode_results results;

// Init Lux Sensor (A4-SCA, A5-ACL)
WAT_ALS468 luxModule;


// Setup Function
void setup()
{
  Serial.begin(9600);

  // IR Receive
  irrecv.enableIRIn();
  irrecv.blink13(true);

  // dht
  dht.begin();

  // IR Send
  // Have to Implement

  // LUX
  luxModule.begin();
}


// Loop Function
void loop()
{
  GasFunction();
  LightFunction();
  HumidFunction();
  //IRFunction();

  // Seperate next sensor value
  Serial.println(""); 
  // delay 4 second
  delay(4000);
}

// Gas Function
void GasFunction()
{
  // read the input on analog pin 0:
  int sensorValue = analogRead(A1);
  //Serial.print("Gas: ");
  //Serial.print(sensorValue);
  //Serial.println("ppm");
  Serial.print(sensorValue);
  Serial.print(",");
}

// Light Function
void LightFunction()
{
  uint16_t lux = luxModule.readLightLevel();
  //Serial.print("Light: ");
  //Serial.print(lux);
  //Serial.println("lx");
  Serial.print(lux);
  Serial.print(",");
}

// Humid & Temp Function
void HumidFunction()
{
  int humi = dht.readHumidity();
  int temp = dht.readTemperature();
  
  char stringBuffer[100];
  char humiTemp[10];
  char tempTemp[10];
  
  dtostrf(humi, 4, 1, humiTemp);
  dtostrf(temp, 4, 1, tempTemp);
    
  //sprintf(stringBuffer, "humidity: %s%%, temperature: %sºC", humiTemp, tempTemp);
  //Serial.println(stringBuffer);
  Serial.print(humiTemp);
  Serial.print(",");
  Serial.print(tempTemp);
  /*
  int i;
  float humi, temp;
  if((i = dht11.read(humi, temp)) == 0) {
    char stringBuffer[100];
    char humiTemp[10];
    char tempTemp[10];
    
    dtostrf(humi, 4, 1, humiTemp);
    dtostrf(temp, 4, 1, tempTemp);
    
    //sprintf(stringBuffer, "Humidity: %s%%\nTemperature: %sºC", humiTemp, tempTemp);
    //Serial.println(stringBuffer);
    Serial.print(humiTemp);
    Serial.print(",");
    Serial.print(tempTemp);
  }*/
}

// IR Function
void IRFunction()
{
  if(irrecv.decode(&results)){
    // IR Receive
    Serial.println(results.value, HEX);
    //Serial.println(g);
    irrecv.resume();

    // IR Send
    irsend.sendNEC(0xC5000, 8);
  }
}
