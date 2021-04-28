int TriggerPIN1 = 9;
int EchoPIN1 = 10;
int TriggerPIN2 = 5;
int EchoPIN2 = 4;
int buzzerPin = 8;
void setup(){
  pinMode(TriggerPIN1,OUTPUT);
  pinMode(EchoPIN2,INPUT);
  pinMode(TriggerPIN2,OUTPUT);
  pinMode(EchoPIN2,INPUT);
  pinMode (buzzerPin, OUTPUT);
  Serial.begin(9600); 
  }

void loop(){  
  digitalWrite(TriggerPIN1,LOW);
  delayMicroseconds(2);
  digitalWrite(TriggerPIN1,HIGH);
  delayMicroseconds(2);
  digitalWrite(TriggerPIN1,LOW);

  long timedelay = pulseIn(EchoPIN1,HIGH);
  int distance1 = 0.0343 * (timedelay/2);

  Serial.print("Sensor 1 : ");
  Serial.println(distance1);
  if (distance1 <20) {
    digitalWrite (buzzerPin, HIGH);
   delay (200);
   digitalWrite (buzzerPin, LOW);
   delay (200);
  }

  delayMicroseconds(2);

  digitalWrite(TriggerPIN2,LOW);
  delayMicroseconds(2);
  digitalWrite(TriggerPIN2,HIGH);
  delayMicroseconds(2);
  digitalWrite(TriggerPIN2,LOW);

  long td = pulseIn(EchoPIN2,HIGH);
  int distance2 = 0.0343 * (td/2);

  Serial.print("Sensor 2 : ");
  Serial.println(distance2);
    if (distance2 <20) {
      digitalWrite (buzzerPin, HIGH);
     delay (200);
     digitalWrite (buzzerPin, LOW);
     delay (200);
    }
