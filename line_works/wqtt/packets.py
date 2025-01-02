CONNECTION_PACKET = bytearray(
    [
        0x10,  # CONNECT パケットタイプ
        0x0C,  # 残りのパケット長
        0x00,
        0x04,  # プロトコル名長
        0x4D,
        0x51,
        0x54,
        0x54,  # "MQTT"
        0x04,  # プロトコルレベル (MQTTv3.1.1)
        0x02,  # 接続フラグ
        0x00,
        0x3C,  # キープアライブ (60秒)
        0x00,
        0x00,  # クライアントID長 (空のクライアントID)
    ]
)

PINGREQ_PACKET = bytearray([0xC0, 0x00])
