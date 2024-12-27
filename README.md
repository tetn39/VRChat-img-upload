# 取ったスクショをDiscordにアップロードしてくれるbot

VRChat用に作ったので、ほかのゲームには対応してません

---
## 使い方(初回)

### 1. .envを作る
ルートディレクトリに`.env`を作り中身は以下のように書き込んでください
```
DISCORD_TOKEN=AAABBBCCC
DISCORD_CHANNEL_ID=123456123456
FOLDER_TO_WATCH=C:/Users/username/Pictures/VRChat
```
- `DISCORD_TOKEN`はdiscord botのトークン
- `DISCORD_CHANNEL_ID`はアップロードしたいチャンネルID
- `FOLDER_TO_WATCH`はVRChatのスクショフォルダを指定 (バックスラッシュだとバグる可能性があるので、普通のスラッシュで)

### 2. VRChat-image-start.batを実行
実行して「無事起動しました」が出ればOK

---
## 使い方(2回目以降)

### 1. VRChat-image-start.batを実行
実行して「無事起動しました」が出ればOK