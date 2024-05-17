// Example for library:
// https://github.com/Bodmer/TJpg_Decoder

// This example is for an ESP8266 or ESP32, it fetches a Jpeg file
// from the web and saves it in a LittleFS file. You must have LittleFS
// space allocated in the IDE.

// Chenge next 2 lines to suit your WiFi network
#define WIFI_SSID "WIFI SSID HERE"
#define PASSWORD "PASSWORD HERE"


// Include the jpeg decoder library
#include <TJpg_Decoder.h>
#include <Servo.h>

// Include LittleFS
#include <FS.h>
#include "LittleFS.h"

// Include WiFi and http client
#ifdef ARDUINO_ARCH_ESP8266
  #include <ESP8266WiFi.h>
  #include <ESP8266HTTPClient.h>
  #include <ESP8266WiFiMulti.h>
  #include <WiFiClientSecureBearSSL.h>
#else
  #include <WiFi.h>
  #include <HTTPClient.h>
#endif

// Load tabs attached to this sketch
#include "List_LittleFS.h"
#include "Web_Fetch.h"

// Include the TFT library https://github.com/Bodmer/TFT_eSPI
#include "SPI.h"
#include <TFT_eSPI.h>              // Hardware-specific library
TFT_eSPI tft = TFT_eSPI();         // Invoke custom library

Servo servo; 
// This next function will be called during decoding of the jpeg file to
// render each block to the TFT.  If you use a different TFT library
// you will need to adapt this function to suit.
bool tft_output(int16_t x, int16_t y, uint16_t w, uint16_t h, uint16_t* bitmap)
{
  // Stop further decoding as image is running off bottom of screen
  if ( y >= tft.height() ) return 0;

  // This function will clip the image block rendering automatically at the TFT boundaries
  tft.pushImage(x, y, w, h, bitmap);

  // Return 1 to decode next block
  return 1;
}
void setup()
{
  Serial.begin(115200);
  Serial.println("\n\n Testing TJpg_Decoder library");
    tft.begin();
    tft.fillScreen(TFT_BLACK);
    tft.setRotation(1);
    TJpgDec.setJpgScale(1);
    TJpgDec.setSwapBytes(true);
    TJpgDec.setCallback(tft_output);
    servo.attach(D1); 
    // Initialise LittleFS
    if (!LittleFS.begin()) {
      Serial.println("LittleFS initialisation failed!");
      while (1) yield(); // Stay here twiddling thumbs waiting
    }
    Serial.println("\r\nInitialisation done.");
    WiFi.begin(WIFI_SSID, PASSWORD);
    tft.setCursor(0, 50);
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println("Checking Wi-Fi Connection  ");
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.print(".");
    
    }
    tft.setCursor(0, 60);
    tft.println("Wi-Fi Connected");
    delay(2000);
    tft.setRotation(0);
    if (!LittleFS.exists("/logo.jpg")) {
       uint32_t t = millis();
       bool loaded_ok = getFile("https://raw.githubusercontent.com/kdani3/diy-lovebox/main/assets/diy-lovebox-logo-black-160x128.jpg", "/logo.jpg");
       t = millis() - t;
       if (loaded_ok) { Serial.print(t); Serial.println(" ms to download"); }
    }
    TJpgDec.drawFsJpg(0, 0, "/logo.jpg", LittleFS);
    delay(5000);
    tft.setRotation(1);

    //tft.setTextFont(1);
    //tft.fillScreen(TFT_BLACK);
    tft.setCursor(50, 0);
    tft.setTextFont(2);
    tft.setTextSize(1);
    tft.setTextColor(TFT_RED);
    tft.print("Lovebox\n");
    delay(1000);
    tft.setCursor(50, 100);
    tft.setTextColor(TFT_WHITE);
    tft.println("Initialising");
    tft.println();
    delay(3000);

  
    tft.fillScreen(TFT_BLACK);
    tft.setRotation(0);

    Serial.println();
    
}
void loop()
{
  // List files stored in LittleFS
  listLittleFS();
  // Time recorded for test purposes
  uint32_t t = millis();
  
 if (LittleFS.exists("/latest.jpg") == true) {
    LittleFS.remove("/latest.jpg");
  }
  // Fetch the jpg file from the specified URL, examples only, from imgur
  bool loaded_ok = getFile("https://URL OF THE DOCKER/image_handling/media/USERNAME FOR RECEIVER/latest", "/latest.jpg");

  t = millis() - t;
  if (loaded_ok) { Serial.print(t); Serial.println(" ms to download"); }
  // List files stored in LittleFS, should have the file now
  listLittleFS();

  t = millis();

  // Now draw the LittleFS file
  cache_latest_jpg();

  if(LittleFS.exists("/latest.jpg")==true){
    TJpgDec.drawFsJpg(0, 0, "/latest.jpg", LittleFS);
    move_servo();
  }
  else{
    if (LittleFS.exists("/latest-cached.jpg") == true) {
      TJpgDec.drawFsJpg(0, 0, "/latest-cached.jpg", LittleFS);
    }
  }
  t = millis() - t;
  Serial.print(t); Serial.println(" ms to draw to TFT");

  // Wait forever
  while(!loaded_ok) yield();
}


void cache_latest_jpg(){
  File sourceFile = LittleFS.open("/latest.jpg", "r");
  
  if (LittleFS.exists("/latest.jpg") == true){
  
    if (LittleFS.exists("/latest-cached.jpg") == true) {
      LittleFS.remove("/latest-cached.jpg");
    }
    File destFile = LittleFS.open("/latest-cached.jpg", "w");
  
    // Reset the file cursor position to the beginning of the source file
    sourceFile.seek(0);
    
    while (sourceFile.available()) {
      destFile.write(sourceFile.read());
    }
  
    // Close the files
    sourceFile.close();
    destFile.close();
  
    Serial.println("File duplicated successfully");
  }
}

void move_servo() {
  for(int i=0;i<=3;i++){
    for (int angle = 90; angle <= 160; angle++) {
      servo.write(angle);
      delay(20); // Smaller delay for smooth movement
    }
  
    delay(100); // Pause for a moment
  
    // Move the servo back to the left
    for (int angle = 160; angle >= 40; angle--) { // Larger back and forth movement
      servo.write(angle);
      delay(20); // Smaller delay for smooth movement
    }
  }
      delay(100); // Pause for a moment

      servo.write(90);
      delay(10); // Smaller delay for smooth movement
 
}
