import os
import sqlite3
import asyncio
import discord
from discord.ext import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import random
from dotenv import load_dotenv

# 各自設定
load_dotenv()

# トークンとか設定
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
FOLDER_TO_WATCH = os.getenv("FOLDER_TO_WATCH")
DB_PATH = "uploaded_images.db" 

# discord botの設定
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# DB初期化
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploaded_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()


# すでにある画像をDBに登録
def register_existing_images():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for root, _, files in os.walk(FOLDER_TO_WATCH):
        for file_name in files:
            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                file_path = os.path.relpath(os.path.join(root, file_name), FOLDER_TO_WATCH)
                cursor.execute("INSERT OR IGNORE INTO uploaded_images (file_name) VALUES (?)", (file_path,))
    conn.commit()
    conn.close()

# 画像アップロード処理
class ImageHandler(FileSystemEventHandler):
    def __init__(self, bot):
        self.bot = bot

    # スクショが取られたときの処理
    async def process_event(self, event):
        if event.is_directory:
            return
        
        print(f"スクショ取られたよ: {event.src_path}")
        file_path = os.path.relpath(event.src_path, FOLDER_TO_WATCH)
        if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            # すでに上げられてなければアップロード
            if not self.is_already_uploaded(file_path):
                await self.upload_image(event.src_path, file_path)

    # なんか大事な処理らしい
    def on_created(self, event):
        asyncio.run_coroutine_threadsafe(self.process_event(event), bot.loop)

    # すでにアップロードされているかDBから確認
    def is_already_uploaded(self, file_path):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM uploaded_images WHERE file_name = ?", (file_path,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    # アップロードした画像をDBに登録
    def mark_as_uploaded(self, file_path):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO uploaded_images (file_name) VALUES (?)", (file_path,))
        conn.commit()
        conn.close()

    # 画像をアップロード
    async def upload_image(self, absolute_path, relative_path):
        await asyncio.sleep(1)
        channel = self.bot.get_channel(CHANNEL_ID)
        print(f"アップロード中だよちょっと待ってね: {relative_path}")
        if channel:
            try:
                await channel.send(file=discord.File(absolute_path))
                print(f"アップロードしたよ: {relative_path} at {CHANNEL_ID}")
                self.mark_as_uploaded(relative_path)
            except Exception as e:
                print(f"アップロード失敗したよ {relative_path}: {e}")
                await channel.send(f"アップロード失敗したよ: {relative_path}")

# 隠し要素
kidou = ["いつでもかかってこい!", "まかせな!", "今日もがんばるよ!", "いっぱいスクショ取ってきてね!"]


# ボットが起動したときの処理
@bot.event
async def on_ready():
    print(f"{bot.user}が起動しました")
    print("---------------------")
    print("")
    print("")
    print("無事起動しました")
    print("")
    print("")
    print("Crtl+Cで終了するよ")
    print("---------------------")
    print(f"bot「{kidou[random.randint(0, len(kidou)-1)]}」")
    

    # DB初期化
    initialize_db()

    # すでにある画像をDBに登録
    register_existing_images()

    # フォルダ監視開始
    observer = Observer()
    handler = ImageHandler(bot)
    observer.schedule(handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()

    # botを動かし続ける
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    bot.run(TOKEN)
