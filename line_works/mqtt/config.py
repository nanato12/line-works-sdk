from line_works.config import UA

HOST = "wss://jp1-web-noti.worksmobile.com/wmqtt"
HEADERS = {
    "user-agent": UA,
    "origin": "https://talk.worksmobile.com",
    "sec-websocket-protocol": "mqtt",
}

# keepalive の送信間隔。CONNECT パケットの Keep Alive にもこの値を使う
KEEP_ALIVE_INTERVAL_SEC = 50

# サーバは通知以外なにも送ってこない (MQTT の PINGREQ にも、テキストの
# "keepalive" にも、WebSocket の ping にも応答しない)。そのため受信ベースの
# 無通信タイムアウトは既定で無効 (None)。死んだ接続の検出は TCP keepalive と
# サーバ側のクローズに頼り、必要なら呼び出し側で定期的に繋ぎ直す
IDLE_TIMEOUT_SEC: float | None = None

# WebSocket の TCP ソケットに設定する keepalive (秒)。NAT で静かに
# 捨てられた接続をカーネルに検出させる
TCP_KEEPALIVE_IDLE_SEC = 60
TCP_KEEPALIVE_INTERVAL_SEC = 10
TCP_KEEPALIVE_COUNT = 3

# WebSocket の close ハンドシェイクを待つ最大秒数
CLOSE_TIMEOUT_SEC = 5

# 再送された PUBLISH を弾くために覚えておく unique_id の数
DEDUPE_CACHE_SIZE = 1000

# 再接続の待ち時間 (指数バックオフ) の上限と、
# バックオフをリセットするのに必要な接続継続時間
RECONNECT_BACKOFF_MAX_SEC = 300
STABLE_CONNECTION_SEC = 60
