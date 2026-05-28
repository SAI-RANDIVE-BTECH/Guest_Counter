#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include "pins.h"

#ifndef GV_WIFI_SSID
#define GV_WIFI_SSID ""
#endif

#ifndef GV_WIFI_PASS
#define GV_WIFI_PASS ""
#endif

#ifndef GV_SERVER_HOST
#define GV_SERVER_HOST "192.168.1.10"
#endif

#ifndef GV_SERVER_PORT
#define GV_SERVER_PORT 8000
#endif

#ifndef GV_DEVICE_SECRET
#define GV_DEVICE_SECRET "replace_with_shared_iot_device_token"
#endif

#ifndef GV_DEVICE_ID
#define GV_DEVICE_ID "00000000-0000-0000-0000-000000000001"
#endif

#ifndef GV_EVENT_ID
#define GV_EVENT_ID "00000000-0000-0000-0000-000000000001"
#endif

#ifndef GV_GATE_LABEL
#define GV_GATE_LABEL "Gate 1"
#endif

static WiFiServer portalServer(80);
static WiFiClient apiClient;
static unsigned long lastPostMs = 0;
static bool provisionMode = false;

static const char *portalHtml =
  "<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>"
  "<style>body{font-family:Arial,sans-serif;background:#111827;color:white;padding:24px}"
  "input{width:100%;box-sizing:border-box;margin:8px 0 14px;padding:10px;border-radius:8px;border:1px solid #374151;background:#030712;color:white}"
  "button{width:100%;padding:12px;border:0;border-radius:999px;background:#f26522;color:white;font-weight:700}</style></head>"
  "<body><h2>GuestVision AI Setup</h2><p>Fill these values in firmware/platformio.ini build_flags, then upload again.</p>"
  "<form><label>WiFi SSID</label><input value='" GV_WIFI_SSID "'><label>Backend host</label><input value='" GV_SERVER_HOST "'>"
  "<label>Device ID</label><input value='" GV_DEVICE_ID "'><label>Event ID</label><input value='" GV_EVENT_ID "'>"
  "<button type='button'>Ready to Upload</button></form></body></html>";

void setLed(uint8_t pin) {
  digitalWrite(PIN_LED_GREEN, pin == PIN_LED_GREEN);
  digitalWrite(PIN_LED_YELLOW, pin == PIN_LED_YELLOW);
  digitalWrite(PIN_LED_RED, pin == PIN_LED_RED);
  digitalWrite(PIN_LED_BLUE, pin == PIN_LED_BLUE);
}

long readDistanceCm(uint8_t trigPin, uint8_t echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  const unsigned long duration = pulseIn(echoPin, HIGH, 25000);
  if (duration == 0) {
    return 999;
  }
  return (long)(duration / 58);
}

String detectDirection() {
  const long first = readDistanceCm(PIN_US1_TRIG, PIN_US1_ECHO);
  const long second = readDistanceCm(PIN_US2_TRIG, PIN_US2_ECHO);

  if (first < ULTRASONIC_NEAR_CM && second >= ULTRASONIC_NEAR_CM) {
    return "entry";
  }
  if (second < ULTRASONIC_NEAR_CM && first >= ULTRASONIC_NEAR_CM) {
    return "exit";
  }
  return "idle";
}

void handlePortal() {
  WiFiClient client = portalServer.available();
  if (!client) {
    return;
  }

  unsigned long started = millis();
  while (client.connected() && millis() - started < 1200) {
    if (client.available()) {
      client.readStringUntil('\r');
      break;
    }
  }

  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println("Connection: close");
  client.println();
  client.print(portalHtml);
  delay(10);
  client.stop();
}

bool connectWiFi() {
  if (strlen(GV_WIFI_SSID) == 0) {
    return false;
  }

  Serial.print("[WiFi] Connecting to ");
  Serial.println(GV_WIFI_SSID);
  WiFi.begin(GV_WIFI_SSID, GV_WIFI_PASS);

  for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("[WiFi] Connected: ");
    Serial.println(WiFi.localIP());
    return true;
  }

  Serial.println("[WiFi] Failed to connect.");
  return false;
}

void startProvisioningAP() {
  provisionMode = true;
  setLed(PIN_LED_BLUE);
  Serial.println("[Setup] Starting AP: GuestVision-Setup");
  WiFi.apbegin((char *)"GuestVision-Setup", (char *)"setup1234", (char *)"1");
  delay(1000);
  portalServer.begin();
  Serial.println("[Setup] Connect to GuestVision-Setup / setup1234 and open http://192.168.1.1");
}

void postRecognitionPing(const String &direction) {
  if (WiFi.status() != WL_CONNECTED) {
    setLed(PIN_LED_RED);
    return;
  }

  if (!apiClient.connect(GV_SERVER_HOST, GV_SERVER_PORT)) {
    Serial.println("[API] Connection failed");
    setLed(PIN_LED_RED);
    return;
  }

  StaticJsonDocument<256> body;
  body["event_id"] = GV_EVENT_ID;
  body["device_id"] = GV_DEVICE_ID;
  body["gate_label"] = GV_GATE_LABEL;
  body["direction"] = direction;

  String payload;
  serializeJson(body, payload);

  apiClient.print(String("POST /api/devices/ping HTTP/1.1\r\n") +
                  "Host: " + GV_SERVER_HOST + "\r\n" +
                  "Content-Type: application/json\r\n" +
                  "X-Device-Secret: " + GV_DEVICE_SECRET + "\r\n" +
                  "Connection: close\r\n" +
                  "Content-Length: " + payload.length() + "\r\n\r\n" +
                  payload);

  while (apiClient.connected() || apiClient.available()) {
    if (apiClient.available()) {
      Serial.write(apiClient.read());
    }
  }
  apiClient.stop();
  setLed(PIN_LED_GREEN);
}

void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(PIN_US1_TRIG, OUTPUT);
  pinMode(PIN_US1_ECHO, INPUT);
  pinMode(PIN_US2_TRIG, OUTPUT);
  pinMode(PIN_US2_ECHO, INPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_YELLOW, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_BLUE, OUTPUT);
  setLed(PIN_LED_YELLOW);

  Serial.println();
  Serial.println("GuestVision AI AMB82 Mini firmware");

  if (!connectWiFi()) {
    startProvisioningAP();
  } else {
    setLed(PIN_LED_GREEN);
  }
}

void loop() {
  if (provisionMode) {
    handlePortal();
    return;
  }

  const String direction = detectDirection();
  if (direction != "idle") {
    Serial.print("[Gate] ");
    Serial.println(direction);
  }

  if (millis() - lastPostMs >= FACE_POST_INTERVAL_MS) {
    lastPostMs = millis();
    postRecognitionPing(direction);
  }
}
