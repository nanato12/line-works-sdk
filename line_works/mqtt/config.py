from line_works.config import UA

HOST = "wss://jp1-web-noti.worksmobile.com/wmqtt"
HEADERS = {
    "user-agent": UA,
    "origin": "https://talk.worksmobile.com",
    "sec-websocket-protocol": "mqtt",
}
KEEP_ALIVE_INTERVAL_SEC = 50
