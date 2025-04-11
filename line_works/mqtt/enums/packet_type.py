from enum import IntEnum


class PacketType(IntEnum):
    CONNECT = 1  # 接続リクエスト
    CONNACK = 2  # 接続応答
    PUBLISH = 3  # メッセージ配信
    PUBACK = 4  # QoS 1 配信確認
    PUBREC = 5  # QoS 2 受信確認 (Part 1)
    PUBREL = 6  # QoS 2 配信リリース (Part 2)
    PUBCOMP = 7  # QoS 2 配信完了 (Part 3)
    SUBSCRIBE = 8  # 購読リクエスト
    SUBACK = 9  # 購読応答
    UNSUBSCRIBE = 10  # 購読解除リクエスト
    UNSUBACK = 11  # 購読解除応答
    PINGREQ = 12  # 接続維持リクエスト
    PINGRESP = 13  # 接続維持応答
    DISCONNECT = 14  # 接続終了通知
