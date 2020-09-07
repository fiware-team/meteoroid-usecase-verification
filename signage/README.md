# サイネージアプリケーション

サイネージアプリケーションは、画面に表示する画像を制御するための、RaspberryPiやPCで動作するPythonスクリプトである。

## 機能

APIによって渡されたURLから画像データを取得し、画面に表示する機能を持っている。


## インストール

サイネージアプリケーションは、画像を画面に表示するためにOpenCVを使用し、APIサーバーのためにFlaskを使用している。
以下のように依存パッケージをインストールする。

```bash
pip install -r requirements.txt
```

## 使い方

### アプリケーションの起動

サイネージアプリケーションを起動するには以下のように実行します。

```bash
python main.py
```

### APIの呼び出し方法

サイネージアプリケーションのAPIによって表示する画像を変更することができる。

```bash
curl -X POST http://<サイネージアプリケーションのIP>:5000/image -H 'Content-Type: application/json' -d '{"url": "https://static.wixstatic.com/media/83bf7d_52bcd43f86134be0a80490cb85e5b8ff~mv2.png"}'
```
