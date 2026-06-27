#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#include "video.h"

Adafruit_SH1106G display(128, 64, &Wire, -1);

uint8_t frame[1024];

void setup() {

  Wire.begin(21,22);

  display.begin(0x3C, true);

  display.clearDisplay();
}

void loop() {

  for(int i = 0; i < FRAME_COUNT; i++) {

    memcpy_P(frame, video[i], 1024);

    display.clearDisplay();

    display.drawBitmap(
      0,
      0,
      frame,
      128,
      64,
      SH110X_WHITE
    );

    display.display();

    delay(100);     // 10 FPS
  }

}