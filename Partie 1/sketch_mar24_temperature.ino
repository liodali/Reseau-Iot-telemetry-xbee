#include <SoftwareSerial.h>
#include <Math.h>
#include <String.h>
SoftwareSerial xbeePort(2, 3); // RX, TX

int pirPin = 4;    //the digital pin connected to the PIR sensor's output
int pirState = LOW; // we start, assuming no motion detected
int val = 0; // variable for reading the pin status

unsigned long currentTime=0,previousTime=0;// variable for time 
unsigned long currentTime_inv_mode=0,previousTime_inv_mode=0;// variable for time 
int valeur_brute=0;// get temperature in analog format
float old_temp=100;// old temperature
float invocation_temp=35;
int active_temp_invocation_mode=30;
int invocation_mode=0;
String textTemp="t : "; 
void setup() {
  // put your setup code here, to run once:
 Serial.begin(19200);
 Serial.println( "Arduino started sending bytes via XBee" );
   /* xbee = XBee();
   // set the data rate for the SoftwareSerial port
   xbee.setSerial(xbeePort);*/
   xbeePort.begin(9600);
   pinMode(pirPin, INPUT); // declare sensor as input
}

void loop() {




/*  
 currentTime=millis();// get current time
  if(currentTime-previousTime > 60000){ // test between previous and current time to do some jobs 
     previousTime=currentTime;
      //get abalog data from pin A0 and convert to temperature
      
      BehavioursTemperateur(0);
  }else {
    BehavioursTemperateur(1);
  }
*/
 detectMotion();

 if(invocation_mode==1){
  currentTime_inv_mode=millis();
  if(currentTime_inv_mode-previousTime_inv_mode > 120000){
    previousTime_inv_mode=currentTime_inv_mode;
    invocation_mode=0;
    xbeePort.println( "desactivation of invocation mode" );
  }
 }


  

  delay(250);
  
}

float ConvertTemp(int v){
  
    int rawvoltage= v;
float millivolts= (rawvoltage*1200.0) / 1024;
float kelvin= (millivolts/10);
  
  return kelvin;
}
// get temperature
void BehavioursTemperateur(int action){
  valeur_brute = analogRead(A0);
  float temperature_celcius =ConvertTemp(valeur_brute);
  textTemp="t : ";
  switch(action){ // have 2 action 0 print temperature
    case 0:
    if(invocation_mode==0)
      xbeePort.println( temperature_celcius );
   else{
     if(temperature_celcius >=  invocation_temp ){
       xbeePort.println( temperature_celcius );
     }
   }
    break;
    case 1: // check old temperature in not equal to current temperature we send the current temperature
     if(invocation_mode==0)
        SendTemperautre(temperature_celcius);
   else{
     if(temperature_celcius >=  invocation_temp ){
       SendTemperautre(temperature_celcius);
     }
   }
      
    break;
  }
  
}
void detectMotion(){
   val = digitalRead(pirPin); // read input value
    if (val == HIGH) { // check if the input is HIGH
        if (pirState == LOW) {
          // we have just turned on
          xbeePort.println("1");//motion detected
          // We only want to print on the output change, not state
          pirState = HIGH;
       }
    } else {
        if (pirState == HIGH){
          // we have just turned of
          xbeePort.println("0");//motion End
          // We only want to print on the output change, not state
          pirState = LOW;
       }
    }
}
void SendTemperautre(float temp){
  
  if(old_temp==100){
    old_temp=temp;
    xbeePort.println( temp );
    Serial.println(temp);
  }else if (abs(old_temp - temp)>= 1){
    if(temp>=active_temp_invocation_mode && invocation_mode==0 ){
      invocation_mode=1;
       xbeePort.println( "activation of invocation mode" );
    }
    old_temp=temp;
    textTemp.concat(temp );
     Serial.println(temp);
    xbeePort.println(textTemp);
  }
}





