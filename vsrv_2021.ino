#define DOOR_SENSOR_PIN A1
#define RX 2
#define TX 3
#define LED 8
#define open_value 10

#include "SoftwareSerial.h"
#include <TimerOne.h>

SoftwareSerial bluetooth(RX, TX);

int current_value = 522;
bool door_already_open = 0;
bool led_status = 0;
bool current_led_status = 0;

void blink_led() {
  if (led_status) {
    digitalWrite(LED, current_led_status);
    current_led_status = !current_led_status;
  } else {
    digitalWrite(LED, LOW);
  }
}

void read_value() {
  current_value = analogRead(A1);
  current_value = abs(current_value - 522);
}

bool check_values() {
  float values_sum = 0;
  bool door_status; 
  
  for (int i = 0; i < 10; i++) {
    read_value();
    values_sum += current_value;
    delay(50);
  }
 
  if (values_sum / 10 < open_value) {
    door_status = 1;
  } else {
    door_status = 0;
  }

  return door_status;
}


void setup() {
  bluetooth.begin(9600);
  
  pinMode(DOOR_SENSOR_PIN, INPUT);
  pinMode(LED, OUTPUT);

  Timer1.initialize(200000);
  Timer1.attachInterrupt(blink_led);
}

void loop() {
  read_value();
  
  if (current_value < open_value) {
    if (check_values()) {
      if (!door_already_open) {
        bluetooth.println(1);
        door_already_open = 1;
        led_status = 1;
      }
    } else {
      led_status = 0;
      door_already_open = 0;
      delay(5000);
    }
  } else {
    delay(50);
  }
}
