CONNECTION_PACKET = bytearray(
    [
        0x10,  # CONNECT パケットタイプ
        0x0C,  # 残りのパケット長
        0x00,
        0x04,  # プロトコル名長 (4バイト)
        0x4D,
        0x51,
        0x54,
        0x54,  # "MQTT" のASCIIコード
        0x04,  # プロトコルレベル (MQTT v3.1.1)
        0x02,  # 接続フラグ (クリーンセッション)
        0x00,
        0x3C,  # キープアライブ (60秒)
        0x00,
        0x00,  # クライアントID長 web-beejs_から始まるID
    ]
)

PINGREQ_PACKET = bytearray([0xC0, 0x00])  # PINGREQパケット
