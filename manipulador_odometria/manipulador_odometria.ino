#include <Servo.h>

#define PI 3.1415926535897932384626433832795

// Condiciones del manipulador (longitudes)
float distancia1 = 102.4;
float distancia2 = 138.6;
float distancia3 = 155;

Servo servoRota; 
Servo servoCuerpo; 
Servo servoBrazo; 

int servoRotaPin = 31; 
int servoCuerpoPin = 33; 
int servoBrazoPin = 35; 
int pos = 90;

float theta1 = 0;
float theta2 = 0;
float theta3 = 0;

float x = 0;
float y = 0;
float z = 0;

void setup() {
   Serial.begin(9600);
   
   servoRota.attach(servoRotaPin);
   servoRota.write(pos);
   
   servoCuerpo.attach(servoCuerpoPin);
   servoCuerpo.write(pos);

   servoBrazo.attach(servoBrazoPin);
   servoBrazo.write(pos);
}

void loop() {
  if (Serial.available()) {

    int rotacion = Serial.parseInt();
    int cuerpo = Serial.parseInt();
    int brazo = Serial.parseInt();

    // Servo de rotación
    int girar = constrain(rotacion, -90, 90); //Limita el movimiento 
    int nuevaPos = servoRota.read() + girar; //Posicion nueva
    nuevaPos = constrain(nuevaPos, 0, 180);
    servoRota.write(nuevaPos);

    // Servo de cuerpo
    int girarCuerpo = constrain(cuerpo, -90, 90); //Limita el movimiento 
    int nuevaPosCuerpo = servoCuerpo.read() + girarCuerpo; //Posicion nueva
    nuevaPosCuerpo = constrain(nuevaPosCuerpo, 0, 180);
    servoCuerpo.write(nuevaPosCuerpo);

    // Servo de brazo
    int girarBrazo = constrain(brazo, -90, 90); //Limita el movimiento 
    int nuevaPosBrazo = servoBrazo.read() + girarBrazo; //Posicion nueva
    nuevaPosBrazo = constrain(nuevaPosBrazo, 0, 180);
    servoBrazo.write(nuevaPosBrazo);
    
  }

// Cinematica directa

  theta1 = servoRota.read() ; // Ángulo de rotación del servo 1
  theta2 = servoCuerpo.read(); // Ángulo de rotación del servo 2
  theta3 = servoBrazo.read(); // Ángulo de rotación del servo 3

  x = distancia1*cos(theta2)*cos(theta1) + distancia2*cos(theta2 + theta3)*cos(theta1);
  y = distancia1*cos(theta2)*sin(theta1) + distancia2*cos(theta2 + theta3)*sin(theta1);
  z = distancia3 + distancia1*sin(theta2) + distancia2*sin(theta2 + theta3);

  Serial.print("Coordenadas: (");
  Serial.print(x);
  Serial.print(", ");
  Serial.print(y);
  Serial.print(", ");
  Serial.print(z);
  Serial.println(")");
  delay(50);
}
