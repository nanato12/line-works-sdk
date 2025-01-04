from enum import IntEnum


class NotificationType(IntEnum):
    NORMAL = 101
    AWAY = 102  # TODO: 不在メッセージの詳細仕様を確認
    LEAVE = 202
    INVITE = 203
    KICK = 204

    # コマンドメッセージタイプ
    CMD_READ = 93004

    # 通知メッセージタイプ
    NOTIFICATION_MESSAGE = 1
    NOTIFICATION_STICKER = 18
    NOTIFICATION_FILE = 16
    NOTIFICATION_SERVICE = 100
    NOTIFICATION_EMOJI = 27
    NOTIFICATION_IMAGE = 11
    NOTIFICATION_BADGE = 41  # TODO: バッジ更新通知の詳細仕様を確認
