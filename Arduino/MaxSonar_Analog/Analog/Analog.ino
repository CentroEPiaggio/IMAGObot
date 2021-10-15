const int anPin = 0; // connect to pin 3
long anVolt, mm;

void setup() {
Serial.begin(9600);
}

void read_sensor(){
anVolt = analogRead(anPin);
mm = anVolt * 5;
}

void print_range(){
Serial.println(mm);
}

void loop() {
read_sensor();
print_range();
delay(5000);
}
