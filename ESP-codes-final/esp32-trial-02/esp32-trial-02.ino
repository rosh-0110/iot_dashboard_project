
#include <SPIFFS.h>
#include <WiFiSettings.h>

const uint32_t LED_PIN = 2;
#define LED_ON  LOW
#define LED_OFF HIGH

void setup() {
    Serial.begin(115200);
    SPIFFS.begin(true);  

    pinMode(LED_PIN, OUTPUT);

    WiFiSettings.onSuccess  = []() {
        digitalWrite(LED_PIN, LED_ON); 
    };
    WiFiSettings.onFailure  = []() {
        digitalWrite(LED_PIN, LED_OFF); 
    };
    WiFiSettings.onWaitLoop = []() {
        digitalWrite(LED_PIN, !digitalRead(LED_PIN)); 
        return 500; 
    };

    // Define custom settings saved by WifiSettings
   
    String host = WiFiSettings.string( "server_host", "roshini.project.org");
    int    port = WiFiSettings.integer("server_port", 443);

    WiFiSettings.connect(true, 30);
}

void loop() {
   
}
