#include <Adafruit_BLE_UART.h>
#include <AESLib.h>
#include <math.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <Wire.h>

#define SERIAL_BAUD 9600
#define Dev_address 0x30
#define Internal_ctr01 0x08
#define Internal_ctr02 0x09
#define Internal_ctr03 0x0A
#define stat 0x07
#define magCali 0
#define NUM_VALUES 1
#define BUFFER_SIZE 32

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
double values[NUM_VALUES];
const char *names[NUM_VALUES] = {"Heading"};

unsigned long lastTimeSent;
const long timeInterval = 5000;
int seq = 0; //sequence number
uint8_t key[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p'};
char data[] = "0123456789012345";
int xl=0, xh=0, yl=0, yh=0, zl=0, zh=0;
int x=0, y=0, z=0;
String cardire = "";

// add single char to block
void append_single(int *count, char block[], uint8_t key[], char insert){
  block[*count] = insert;
  *count = *count + 1;
  if (*count == 16) {
    aes128_enc_single(key, block);
    Serial1.print(block);
    *count = 0;
  }
}

// add string to block
void append_str(int *count, char block[], uint8_t key[], const char *insertStr, int size) {
  for (int i = 0; i < size; i++) {
    append_single(count, data, key, insertStr[i]);
  }
}
void displaySensorDetails(void)
{
  sensor_t sensor;
  mag.getSensor(&sensor);
  delay(500);
}
void setup() {
  Serial1.begin(9600);
  
  //control register 0
  Wire.beginTransmission(Dev_address);
  Wire.write(0x08);//control register 0
  Wire.write(0x8);// SET the sensor
  Wire.endTransmission();  
  // control register 1
  Wire.beginTransmission(Dev_address);//address of device
  Wire.write(0x09);//address of what you want to wrie
  Wire.write(0x80);//data you want to write
  Wire.endTransmission();
  // control register 2
  Wire.beginTransmission(Dev_address);//address of device
  Wire.write(0x0A);//address of what you want to wrie
  Wire.write(0x01);//data you want to write
  Wire.endTransmission();
  
  mag.begin();
  lastTimeSent = millis();
}

void loop() {
  unsigned long currentTime = millis();

  if (lastTimeSent + timeInterval < currentTime) {

    //collect data here
    float heading;
    //check status
    Wire.beginTransmission(Dev_address);
    Wire.write(0x07);
    Wire.endTransmission();
  
    Wire.requestFrom(Dev_address, 1);
    int devstat = Wire.read();
  
    // control register 0, should it be here or loop? do I need to rerun it each time
    Wire.beginTransmission(Dev_address);
    Wire.write(0x08);//control register 0
    Wire.write(0x01);// RESET sensor and initiate magnetic field measurement
    Wire.endTransmission();
    
    Wire.beginTransmission(Dev_address);
    Wire.write(0x00); //start measuring at xlsb, 
    Wire.endTransmission();
    
    Wire.requestFrom(Dev_address, 6);
   if ((devstat & 0x01)==(0x01)){ //check the status register to make sure measurment is done
  //read 6 bytes of data, starts at xlsb, internal memory address pointer automatically moves to the next byte
     while (Wire.available() < 6);
      xl = Wire.read();//xlsb
      xh = Wire.read();//xmsb
      yl = Wire.read();//ylsb
      yh = Wire.read();//ymsb
      zl = Wire.read();//zlsb
      zh = Wire.read();//zmsb
      
      //Serial.println("data acquired");
     
    
   }
  ///////////COMBINE LSB AND MSB//////////////////////
  x = ((xh<<8) | xl);//*(1/4096);
  y = ((yh<<8) | yl);//*(1/4096);
  z = ((zh<<8) | zl);//*(1/4096);
  
  //////////CHECK FOR DIVIDE BY ZERO CONDITION/////////
   if ((x == 0) && (y < 0)){
    heading = 90; 
   } else if ((x==0) && (y>0)){
    heading = 0;
   }
  //////////CALCULATE HEADING///////////////////
   heading = (atan2(-y, x)) * (180/PI); 
  
   if (heading < 0){
    heading = heading + 360;
   } else if (heading > 360){
    heading = heading - 360;
   }
  
  
  
  ////////////PRINT OUTPUTS///////////////////
    if(heading >= 0 && heading < 90){            //Around 45
      cardire = "North";
    }else if(heading >= 90 && heading < 180){   //Around 135
      cardire = "West";
    }else if(heading >= 180 && heading < 270){  //Around 225
      cardire = "South";
    }else if(heading >= 270 && heading < 360){  //Around 315
      cardire = "East";
    }   
    if(cardire == "North"){
      if(heading <= 45){
        heading = (heading-45)*22.5 + 360;
      }else{heading = (heading-45)*22.5 + 0;}
    }else if(cardire == "East"){
      heading = (heading-315)*22.5 + 90;
    }else if(cardire == "South"){
      heading = (heading-225)*22.5 + 180;
    }else if(cardire == "West"){
      heading = (heading-135)*22.5 + 270;
    }
    heading = heading + magCali;
    if (heading < 0){
      heading += 360;
    }
    values[0] = heading;

    // start putting data in JSON format
    data[0] = '{';
    int count = 1;

    for (int i = 0; i < NUM_VALUES; i++) {
      append_single(&count, data, key, '"');
      append_str(&count, data, key, names[i], strlen(names[i]));
      append_str(&count, data, key, "\":", 2);

      // can't sprintf with floats in arduino so need a workaround
      double intPart, fractPart;
      fractPart = modf(values[i], &intPart);
      char big[BUFFER_SIZE], small[BUFFER_SIZE];
      int size = snprintf(big, BUFFER_SIZE, "%d", (int) intPart);
      append_str(&count, data, key, big, size);

      append_single(&count, data, key, '.');

      fractPart *= 100;
      size = snprintf(small, BUFFER_SIZE, "%d", (int) fractPart);
      append_str(&count, data, key, small, size);
      append_single(&count, data, key, ',');
    }
    
    append_str(&count, data, key, "\"seq\":", 6);
    char seqstr[BUFFER_SIZE];
    int size = snprintf(seqstr, BUFFER_SIZE, "%d", seq);
    append_str(&count, data, key, seqstr, size);
    append_single(&count, data, key, '}');

    while (count != 0) { // padding to fill last block
      append_single(&count, data, key, ' ');
    }
    seq++;
    Serial1.print('\n');
    lastTimeSent = currentTime;
  }
}
