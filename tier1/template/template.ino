#include <DHT.h>
#include <DHT_U.h>
#include <Adafruit_BLE_UART.h>
#include <AESLib.h>
#include <math.h>

#define DHT_TYPE DHT11
#define DHT_PIN 21
#define NUM_VALUES 3
#define BUFFER_SIZE 32

DHT dht(DHT_PIN, DHT_TYPE);
double values[NUM_VALUES];
const char *names[NUM_VALUES] = {"Humidity", "Temperature", "Heat Index"};

unsigned long lastTimeSent;
const long timeInterval = 5000;
int seq = 0; //sequence number
uint8_t key[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p'};
char data[] = "0123456789012345";

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

void setup() {
  Serial1.begin(9600);
  dht.begin();
  lastTimeSent = millis();
}

void loop() {
  unsigned long currentTime = millis();
  if (lastTimeSent + timeInterval < currentTime) {

    //collect data here
    values[0] = dht.readHumidity();
    values[1] = dht.readTemperature();
    values[2] = dht.computeHeatIndex(values[0], values[1], false);

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
    Serial1.println();
    lastTimeSent = currentTime;
  }
}
