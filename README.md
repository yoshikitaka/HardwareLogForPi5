# HardwareLogForPi5

このプロジェクトは、Raspberry Pi 5のハードウェア情報を定期的にログに記録するためのものです。
- [HardwareLogForPi5](#hardwarelogforpi5)
  - [セットアップ手順](#セットアップ手順)
  - [サービスとして実行する](#サービスとして実行する)
  - [ログの確認](#ログの確認)
  - [トラブルシューティング](#トラブルシューティング)
  - [注意事項](#注意事項)
- [作者メモ](#作者メモ)
  
## セットアップ手順

1. リポジトリをクローンします：
   ```
   git clone https://github.com/yoshikitaka/HardwareLogForPi5.git
   cd HardwareLogForPi5
   ```

2. 仮想環境を作成し、アクティベートします：
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. 必要なパッケージをインストールします：
   ```
   pip install -r requirements.txt
   ```

## サービスとして実行する

1. サービスファイルを作成します：
   ```
   sudo nano /etc/systemd/system/hardwarelog.service
   ```

   以下の内容を記述します。 `<INSTALL_PATH>` をあなたの実際のインストールパスに置き換えてください。
   ```ini
   [Unit]
   Description=Hardware Log for Raspberry Pi 5
   After=network.target

   # Write your install path. Note: Relative paths are not supported, use absolute paths.
   [Service]
   ExecStart=<INSTALL_PATH>/.venv/bin/python <INSTALL_PATH>/logging.py
   WorkingDirectory=<INSTALL_PATH>
   StandardOutput=inherit
   StandardError=inherit
   User=%u

   [Install]
   WantedBy=multi-user.target
   ```

2. タイマーファイルを作成します：
   ```
   sudo nano /etc/systemd/system/hardwarelog.timer
   ```

   以下の内容を記述します：
   ```ini
   [Unit]
   Description=Run Hardware Log every minute

   [Timer]
   OnBootSec=1min
   OnUnitActiveSec=1min
   Unit=hardwarelog.service

   [Install]
   WantedBy=timers.target
   ```

3. サービスとタイマーを有効化し、開始します：
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable hardwarelog.timer
   sudo systemctl start hardwarelog.timer
   ```


## ログの確認

ログファイルは `<INSTALL_PATH>/system_log.csv` に保存されます。

## トラブルシューティング

サービスの状態を確認：
```
sudo systemctl status hardwarelog.service
```

サービスのログを確認：
```
sudo journalctl -u hardwarelog.service
```

## 注意事項

- このサービスは1分ごとにログを記録します。頻度を変更する場合は、タイマーファイルの `OnUnitActiveSec` の値を調整してください。
- ログファイルのサイズが大きくなりすぎないよう、定期的に確認し、必要に応じてローテーションを設定してください。

# 作者メモ
動作が遅い・・・1分間隔で動作させてるのにログには1分10秒くらいの感覚で記録される・・・csvファイルの作りやすさ、cpu周波数の取得等の簡易さの都合でpyton使ったけど、とにかく遅い。ラズパイに用意されてるコマンドで組みなおすかも。
