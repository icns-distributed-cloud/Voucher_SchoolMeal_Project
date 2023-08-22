#include <DHT11.h>
#include <DHT.h>

int pin = A0;

//DHT11 dht11(pin);
DHT dht(pin, DHT11);

void setup() {
  Serial.begin(9600);
  delay(2000);

  dht.begin();
}

void loop() {
  int humi = dht.readHumidity();
  int temp = dht.readTemperature();
  
  char stringBuffer[100];
  char humiTemp[10];
  char tempTemp[10];
  
  dtostrf(humi, 4, 1, humiTemp);
  dtostrf(temp, 4, 1, tempTemp);
    
  sprintf(stringBuffer, "humidity: %s%%, temperature: %sºC", humiTemp, tempTemp);
  Serial.println(stringBuffer);
  
  /*
  int i;
  float humi, temp;
  if((i = dht11.read(humi, temp)) == 0) {
    char stringBuffer[100];
    char humiTemp[10];
    char tempTemp[10];
    
    dtostrf(humi, 4, 1, humiTemp);
    dtostrf(temp, 4, 1, tempTemp);
    
    sprintf(stringBuffer, "humidity: %s%%, temperature: %sºC", humiTemp, tempTemp);
    Serial.println(stringBuffer);
  }
  else{
    Serial.print("Error:");
    Serial.print(i);
  }*/
  delay(2000);
}
