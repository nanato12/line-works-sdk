# CLAUDE.md

このファイルはClaude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## プロジェクト概要

LINE WORKS SDK for Python - LINE WORKSメッセージングプラットフォームと連携するためのPython SDK。Talk APIはOpenAPI 3.1.0仕様で定義されています。

**必須要件**: Python 3.11+

## よく使うコマンド

### 開発環境セットアップ

```bash
make init  # 依存関係をインストールし、.envをテンプレートから作成
```

### コード品質チェック

```bash
make lint  # ruffリンター、フォーマッターチェック、mypy型チェックを実行
make fmt   # ruffでコードを自動フォーマットし、リント問題を修正
```

### ビルド & 公開

```bash
make build      # ソースとホイールディストリビューションをビルド
make test-pypi  # テストPyPIにアップロード
make pypi       # 本番PyPIにアップロード
```

### 実行

```bash
make run  # main.pyを実行
```

### OpenAPIコード生成

```bash
make generate  # openapi/*.ymlからAPIクライアントを再生成
```

このコマンドは、Storage APIとTalk APIのOpenAPI仕様から`line_works/openapi/`ディレクトリを再生成します。

## アーキテクチャ

### コア設計原則

- **1クラス1ファイル**: 各クラスは独自のファイルに配置
- **OpenAPI駆動**: `openapi/`ディレクトリに各サービスのAPI定義ファイルがある
- **コード生成**: `make generate`でOpenAPIファイルからPython定義を自動生成

### 主要コンポーネント

**LineWorksクライアント** (`line_works/client.py`): 認証、セッション管理、メッセージ送信を担当するメインクライアントクラス。`BaseModel` (Pydantic) と `TalkApi` (OpenAPI自動生成) の両方を継承。機能:

- `.session/{works_id}/`でのCookieベースのセッション永続化
- フォールバック認証を含む自動ログイン
- メッセージ送信: テキスト、画像、ファイル、スタンプ、Flexメッセージ
- Storage API経由のリソースアップロード処理

**MQTT統合** (`line_works/mqtt/`): WebSocket MQTT接続によるリアルタイムメッセージ受信:

- `MQTTClient`: キープアライブ機能付きWebSocket接続マネージャー
- `LineWorksTracer`: 非同期イベントループを実行するシンプルなラッパー
- `MQTTPacket`: パケット解析とペイロードデシリアライゼーション
- `add_trace_func()`による異なるパケットタイプのコールバックシステム

**OpenAPI自動生成コード** (`line_works/openapi/`): 自動生成されたAPIクライアント:

- `talk/`: メッセージ送信、チャンネル情報取得などのTalk API
- `storage/`: リソース（画像、ファイル）アップロード用のStorage API
- **リント対象外** (pyproject.toml参照)

### メッセージフロー

1. **送信**: `LineWorks`クライアント → Talk API → メッセージ送信リクエスト
2. **受信**: WebSocket → MQTTパケット → 解析されたペイロード → ユーザーコールバック
3. **リソース**: リソースパス発行 → Storage APIへアップロード → メッセージに含める

### 認証

`login_with_id()`での2段階ログインプロセス:

1. デフォルトCookieなしで最初の試行
2. 失敗した場合、`config.COOKIE`をフォールバックとして再試行
3. セッションCookieは`@save_cookie`デコレーターにより`.session/{works_id}/cookie.json`に保存

## コードスタイル

- **行の長さ**: 79文字 (ruff)
- **型チェック**: 明示的な型アノテーションが必須の厳格なmypy
- **除外対象**: `line_works/openapi/`はruffとmypyから除外（自動生成のため）
- **インポート**: ISC003、TID252、および標準的なソート/フォーマットを強制

## 重要なパターン

- **Pydanticモデル**: データバリデーションに全体的に使用
- **セッション永続化**: JSONによるCookieストレージ
- **二重API継承**: メインクライアントはPydanticとOpenAPI生成APIを組み合わせる
- **非同期MQTT**: コールバック登録によるイベント駆動型リアルタイムメッセージング
- **型安全性**: ユーザーが書いたコードはすべて完全に型付けする必要がある
