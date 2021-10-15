const int pwPin1 = 3; // connect to pin 2
long sensor, mm;

void setup() {
Serial.begin(9600);
pinMode(pwPin1, INPUT); }

void read_sensor (){
sensor = pulseIn(pwPin1, HIGH);
mm = sensor;
}


void print_range(){
Serial.println(mm)
}

void loop() { read_sensor();
print_range();
delay(400);
}
