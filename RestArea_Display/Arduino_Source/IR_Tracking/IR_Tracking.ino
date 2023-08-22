#include <IRremote.h>

const int RECV_PIN = 7;

IRrecv irrecv(RECV_PIN);
IRsend irsend;
decode_results results;

void setup(){
  Serial.begin(9600);

  // IR Receive
  irrecv.enableIRIn();
  irrecv.blink13(true);

  // IR Send
}

void loop(){
  if(irrecv.decode(&results)){
    // IR Receive
    Serial.println(results.value, HEX);
    //Serial.println(g);
    irrecv.resume();

    // IR Send
    irsend.sendNEC(0xC5000, 8);
  }
}
