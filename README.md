# HardwareLogForPi5

このプロジェクトは、Raspberry Pi 5のハードウェア情報を定期的にログに記録するためのものです。
- [HardwareLogForPi5](#hardwarelogforpi5)
  - [セットアップ手順](#セットアップ手順)
  - [サービスとして実行する](#サービスとして実行する)
  - [ログの確認](#ログの確認)
  - [トラブルシューティング](#トラブルシューティング)
  - [注意事項](#注意事項)
  
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

   # write your install path
   [Service]
   ExecStart=.venv/bin/python logging.py
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
