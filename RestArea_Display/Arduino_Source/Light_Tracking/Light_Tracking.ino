#include <Wire.h>
#include <WAT_ALS468.h>
 
WAT_ALS468 luxModule;
 
// 프로그램 초기화
void setup()
{
  Serial.begin(9600);
  Serial.println(F("Arduino Examples - WAT_ALS468 Example"));
  Serial.println("    https://docs.whiteat.com/?p=5567");
  luxModule.begin();
}
 
// 계속 실행할 무한 루프
void loop() 
{
  uint16_t lux = luxModule.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  delay(1000);
}
