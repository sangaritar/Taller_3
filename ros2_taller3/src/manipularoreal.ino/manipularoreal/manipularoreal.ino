#include <Servo.h>

#define PI 3.1415926535897932384626433832795

// Condiciones del manipulador (longitudes)
float distancia1 = 102.4;
float distancia2 = 138.6;
float distancia3 = 155;

// Verde
int servoRotaPin = 44; 
//Morado
int servoCuerpoPin = 46; 
// Amarillo
int servoBrazoPin = 12; 
// Naranja 
int servoGarraPin = 13;

int pos = 45 ;

int aperturaGarra= 0;

Servo servoRota; 
Servo servoCuerpo; 
Servo servoBrazo; 
Servo servoGarra; 

float theta1 = 0;
float theta2 = 0;
float theta3 = 0;

float x = 0;
float y = 0;
float z = 0;


float coordenadaX_garra = 0.0; // Coordenada X para activar la garra
float coordenadaY_garra = 0.0; // Coordenada Y para activar la garra
float coordenadaZ_garra = 0.0; // Coordenada Z para activar la garra

void setup() {
   Serial.begin(9600);
   
   servoRota.attach(servoRotaPin);
   servoRota.write(pos);
   
   servoCuerpo.attach(servoCuerpoPin);
   servoCuerpo.write(pos);

   servoBrazo.attach(servoBrazoPin);
   servoBrazo.write(0);
   
   servoGarra.attach(servoGarraPin); 
   servoGarra.write(aperturaGarra);
}

void loop() {
  if (Serial.available()) {

  String input_str = Serial.readStringUntil('p');
  char charArray[input_str.length() + 1];
  //Serial.println("recibido"+ input_str);
  
  input_str.toCharArray(charArray, sizeof(charArray));

  char* token = strtok(charArray, ",");

  float rotacion = atof(token);
  token = strtok(NULL, ",");

  
  float cuerpo = atof(token);
  token = strtok(NULL, ",");
     
  float brazo = atof(token);
  token = strtok(NULL, ",");

  //token = strtok(NULL, ",");

if (rotacion == 0.0 && cuerpo == 105.0  && brazo == 0.0){


    // Servo de cuerpo
    int girarCuerpo = constrain(cuerpo, -120, 120); // Limita el movimiento 
    int nuevaPosCuerpo = servoCuerpo.read() + girarCuerpo; // Posicion nueva
    nuevaPosCuerpo = constrain(nuevaPosCuerpo, 0, 180);
    servoCuerpo.write(nuevaPosCuerpo);

    delay(3000);
    
    servoGarra.write(180);

    delay(3000);

     servoRota.write(pos);
     servoCuerpo.write(pos);
     servoBrazo.write(0);
   
    delay(6000);

    servoCuerpo.write(nuevaPosCuerpo);
    

    delay(1000);

    servoGarra.write(0);

    delay(3000);

     servoRota.write(pos);
     servoCuerpo.write(pos);
     servoBrazo.write(0);

  
} else if (rotacion > -151.0 && rotacion < 151.0 || cuerpo > -151.0 && cuerpo < 151.0 || brazo > -151.0 && brazo < 151.0) {
    // Servo de rotación
    int girar = constrain(rotacion, -90, 90); // Limita el movimiento 
    int nuevaPos = servoRota.read() + girar; // Posicion nueva
    nuevaPos = constrain(nuevaPos, 0, 180);
    servoRota.write(nuevaPos);

    // Servo de cuerpo
    int girarCuerpo = constrain(cuerpo, -120, 120); // Limita el movimiento 
    int nuevaPosCuerpo = servoCuerpo.read() + girarCuerpo; // Posicion nueva
    nuevaPosCuerpo = constrain(nuevaPosCuerpo, 0, 180);
    servoCuerpo.write(nuevaPosCuerpo);

    // Servo de brazo
    int girarBrazo = constrain(brazo, -90, 90); // Limita el movimiento 
    int nuevaPosBrazo = servoBrazo.read() + girarBrazo; // Posicion nueva
    nuevaPosBrazo = constrain(nuevaPosBrazo, 0, 180);
    servoBrazo.write(nuevaPosBrazo);
  }
  
    //Servo de garra
    
    if (rotacion == 500.0 && cuerpo == 500.0 && brazo == 500.0) { 
    servoGarra.write(0);
  } else if (rotacion == -500 && cuerpo == -500.0 && brazo == -500.0) {
    servoGarra.write(180);
    
  }

  
   
  }

}