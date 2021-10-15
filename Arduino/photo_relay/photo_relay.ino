// This code is used to read the photoresistor and write the data in the serial port
// At the same time, the relay, connected to the digital pin 7, is controlled sending a HIGH or LOW signal

char relay_status;


void setup() {
  
  Serial.begin(9600);
  pinMode(7,OUTPUT);

}


void loop() {
  
  if (Serial.available()>0){
    
    relay_status = Serial.read();
    
    if (relay_status == 'L'){

      digitalWrite(7,HIGH);
      
    }
    else{

      digitalWrite(7,LOW);
    
    }
  }
  
  else{
    
    Serial.write(analogRead(A0)/4);

  }
  
}
