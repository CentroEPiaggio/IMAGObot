
#include <SoftwareSerial.h>

// 10 connesso al pin 5, 11 al pin 4 del sensore
SoftwareSerial mySerial(10, 11,true); // RX, TX 

char *buffer;
byte x;
char array[4];

void setup() {

  Serial.begin(9600);
  mySerial.begin(9600);
}

void reading(){

mySerial.println();

while (mySerial.available())
{
   x= mySerial.readBytes(buffer,1);
   if(*buffer==0x52){ // R
   x= mySerial.readBytes(buffer,1);
   array[0]=*buffer; 
   x= mySerial.readBytes(buffer,1);
   array[1]=*buffer; 
   x= mySerial.readBytes(buffer,1);
   array[2]=*buffer; 
   x= mySerial.readBytes(buffer,1);
   array[3]=*buffer; 
   
   }
   
}

}
void loop() {

  reading(); 
 
  if (array[0]!= 48){  // 48 in ASCII è 0
    Serial.print(array[0]);
}
  Serial.print(array[1]);
  Serial.print(array[2]);
  Serial.println(array[3]);

  delay(500);

}
