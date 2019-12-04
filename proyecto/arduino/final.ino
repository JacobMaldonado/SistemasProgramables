//libreria dht11
#include "DHT.h"
#define DHTPin 2
#define DHTTYPE DHT11

// DECLARACION DE VARIABLES PARA PINES
const int pinecho = 8;
const int pintrigger = 9;
//const int pinecho2 = 5;
//const int pintrigger2 = 6;
const int pinled = 13;
//variables humedad y temperatura
int h;
int t;
//pines para la fotoresistencia
//const int DHTPin = 2;
DHT dht(DHTPin, DHTTYPE);
//variables fotoresistencia
const int LEDPin = 13;
const int LDRPin = A1;
const int threshold = 100;
int valFoto;
//tiempo de calibracion sensor movimiento
int calibrationTime = 30;
//momento en el que el sensor emite un impulso bajo
long unsigned int lowIn;
//cantidad de ms que el sensor tiene que ser baja
//antes de que el movimiento se ha detenido
long unsigned int pause = 2000; 
boolean lockLow = true;
boolean takeLowTime;
int pirPin = 3;//pin al que esta conectado
boolean mov;
//sensor de flama
int Analogpin = A0;
int Digitalpin = 4;
int val;
boolean flamita;
float sensor;
// VARIABLES PARA CALCULOS
unsigned int tiempo, distancia;
unsigned int tiempo2, distancia2;

void setup() { 
  // PREPARAR LA COMUNICACION SERIAL
  Serial.begin(9600);
  dht.begin();
  //calibrar sensor de movimiento
  calibrarMovimiento();
  // CONFIGURAR PINES DE ENTRADA Y SALIDA
  pinMode(pinecho, INPUT);
  pinMode(pintrigger, OUTPUT);
  //pinMode(pinecho2, INPUT);
  //pinMode(pintrigger2, OUTPUT);
  pinMode(13, OUTPUT);  
  //fotoresistencia
  pinMode(LEDPin, OUTPUT);
  pinMode(LDRPin, INPUT);
  //sensor de movimiento
  pinMode(pirPin, INPUT);
  pinMode(pinled, OUTPUT);
  digitalWrite(pirPin, LOW);
  pinMode (Digitalpin, INPUT);
  pinMode (Analogpin, INPUT);
}

void loop() {
  ultrasonico();
  //ultrasonico2();
  foto();
  movimiento();
  flama();
  hyt();
  Serial.println("----");
}

void ultrasonico(){
  // ENVIAR PULSO DE DISPARO EN EL PIN "TRIGGER"
  digitalWrite(pintrigger, LOW);
  delayMicroseconds(2);
  digitalWrite(pintrigger, HIGH);
  // EL PULSO DURA AL MENOS 10 uS EN ESTADO ALTO
  delayMicroseconds(10);
  digitalWrite(pintrigger, LOW);
 
  // MEDIR EL TIEMPO EN ESTADO ALTO DEL PIN "ECHO" EL PULSO ES PROPORCIONAL A LA DISTANCIA MEDIDA
  tiempo = pulseIn(pinecho, HIGH);
 
  // LA VELOCIDAD DEL SONIDO ES DE 340 M/S O 29 MICROSEGUNDOS POR CENTIMETRO
  // DIVIDIMOS EL TIEMPO DEL PULSO ENTRE 58, TIEMPO QUE TARDA RECORRER IDA Y VUELTA UN CENTIMETRO LA ONDA SONORA
  distancia = tiempo / 58;
 
  // ENVIAR EL RESULTADO AL MONITOR SERIAL
  Serial.print(distancia);
  Serial.println(" cm");
  delay(200);
}

void foto(){
  valFoto = analogRead(LDRPin);
  if(valFoto>threshold){
      digitalWrite(LEDPin, HIGH);
      Serial.print("fotores: ");
      Serial.println(valFoto);
    }else{
      digitalWrite(LEDPin, LOW); 
      Serial.print("fotores: ");
      Serial.println(valFoto);
    }
}

void calibrarMovimiento(){
  //Dar al sensor algún tiempo para su calibrado
    Serial.print("calibrando sensor ");
    for(int i = 0; i < calibrationTime; i++){ 
        Serial.print("."); 
        delay(1000); 
    } 
    Serial.println(" echo"); 
    Serial.println("SENSOR ACTIVO"); 
    delay(50);   
}

void movimiento(){
   Serial.println(mov); 
  if(digitalRead(pirPin) == HIGH){ 
    if(lockLow){ // Se asegura que esperamos una transición a LOW antes de cualquier salida 
      adicional: lockLow = false; 
//      Serial.println("---"); 
//      Serial.print("movimiento detectado "); 
//      Serial.print(millis()/1000); 
//      Serial.println(" sec"); 
      delay(50); 
    } 
    takeLowTime = true; 
    mov=true;
    Serial.print("mov: ");
    Serial.println(mov);
  } 
  if(digitalRead(pirPin) == LOW){ 
    //digitalWrite(pinled, LOW); 
    // El LED visualiza el estado de los sensores de pin de salida 
    if(takeLowTime){
      lowIn = millis(); 
      // guarda el tiempo de la transición de HIGH a LOW 
      takeLowTime = false; 
      mov=false;
      Serial.print("mov: ");
      Serial.println(mov);
      // asegurar que esto se hace solamente al inicio de una fase de baja 
    } // Si el sensor es baja por más de la pausa dada, 
    // suponemos que hay más movimientos que van a suceder 
    if(!lockLow && millis() - lowIn > pause){ 
      // se cerciora este bloque de código sólo se ejecuta nuevamente después de
      // que una nueva secuencia de movimiento se ha detectado
      lockLow = true; 
//      Serial.print("motion ended at "); //output
//      Serial.print((millis() - pause)/1000);
//      Serial.println(" sec");
      delay(50);
    }
  }  
}

void flama(){
  sensor = analogRead(Analogpin);
  //Serial.println(sensor);
  
  val = digitalRead (Digitalpin) ;

  if(val == HIGH){
    flamita=true;
    Serial.print("flamita: ");   
    Serial.println(flamita);
    
  }else{
    flamita=false;
    Serial.print("flamita: ");   
    Serial.println(flamita);
  }
  delay(1000);
}


void hyt(){
  h = dht.readHumidity();// Lee la humedad
  t = dht.readTemperature();//Lee la temperatura
  //////////////////////////////////////////////////Humedad
  Serial.print("Humedad: ");                 
  Serial.print(h);//Escribe la humedad
  Serial.println(" %");                     
  delay (2500);
  ///////////////////////////////////////////////////Temperatura              
  Serial.print("Temperatura: ");                  
  Serial.print(t);//Escribe la temperatura
  Serial.println(" °C'");                   
  delay (2500); 
}
