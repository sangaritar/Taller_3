#include <Servo.h>

#define PI 3.1415926535897932384626433832795

// Condiciones del manipulador (longitudes)
float distancia1 = 102.4;
float distancia2 = 138.6;
float distancia3 = 155;

// Verde
int servoRotaPin = 33; 
//Morado
int servoCuerpoPin = 27; 
// Amarillo
int servoBrazoPin = 49; 
// Naranja 
int servoGarraPin = 43;

int pos = 50 ;

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
   servoBrazo.write(pos);
   
   servoGarra.attach(servoGarraPin); 
   servoGarra.write(pos);
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



    
    // Servo de rotación
    int girar = constrain(rotacion, -90, 90); //Limita el movimiento 
    int nuevaPos = servoRota.read() + girar; //Posicion nueva
    nuevaPos = constrain(nuevaPos, 0, 180);
    servoRota.write(nuevaPos);
    //delay(500);

    // Servo de cuerpo
    int girarCuerpo = constrain(cuerpo, -90, 90); //Limita el movimiento 
    int nuevaPosCuerpo = servoCuerpo.read() + girarCuerpo; //Posicion nueva
    nuevaPosCuerpo = constrain(nuevaPosCuerpo, 0, 180);
    servoCuerpo.write(nuevaPosCuerpo);
    //delay(500);

    // Servo de brazo
    int girarBrazo = constrain(brazo, -90, 90); //Limita el movimiento 
    int nuevaPosBrazo = servoBrazo.read() + girarBrazo; //Posicion nueva
    nuevaPosBrazo = constrain(nuevaPosBrazo, 0, 180);
    servoBrazo.write(nuevaPosBrazo);
    //delay(500);

  }

// Cinematica directa

  theta1 = servoRota.read() ; // Ángulo de rotación del servo 1
  theta2 = servoCuerpo.read(); // Ángulo de rotación del servo 2
  theta3 = servoBrazo.read(); // Ángulo de rotación del servo 3

  x = distancia1*cos(theta2)*cos(theta1) + distancia2*cos(theta2 + theta3)*cos(theta1);
  y = distancia1*cos(theta2)*sin(theta1) + distancia2*cos(theta2 + theta3)*sin(theta1);
  z = distancia3 + distancia1*sin(theta2) + distancia2*sin(theta2 + theta3);

  String mensaje = String(x) + ',' + String(y) + ',' + String(z) ;
  
  Serial.println(mensaje);

  if (x == coordenadaX_garra && y == coordenadaY_garra && z == coordenadaZ_garra) {
    servoGarra.write(90);
    //delay(5000); // Mantener la garra abierta durante 5 segundo
    servoGarra.write(0);

}
}