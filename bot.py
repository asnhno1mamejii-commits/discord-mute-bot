import os
import asyncio
from datetime import datetime
import pytz
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 日本時間に設定
JST = pytz.timezone('Asia/Tokyo')

# --- 毎日実行したい時間を設定（24時間表記） ---
MUTE_TIME = "1:00"    # 毎日1時00分にミュート
UNMUTE_TIME = "8:00"  # 毎日8時00分にミュート解除

# 実行対象のボイスチャンネルID（※自分のチャンネルIDに書き換えてください）
TARGET_CHANNEL_ID = yomo00987_92333

@tasks.loop(seconds=60)
async def daily_schedule():
    now = datetime.now(JST).strftime("%H:%M")
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    
    if channel is None:
        return

    if now == MUTE_TIME:
        for member in channel.members:
            await member.edit(mute=True)
        print(f"[{now}] 毎日のミュートを実行しました")

    elif now == UNMUTE_TIME:
        for member in channel.members:
            await member.edit(mute=False)
        print(f"[{now}] 毎日のミュート解除を実行しました")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (Bot起動完了)")
    if not daily_schedule.is_running():
        daily_schedule.start()

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("エラー: DISCORD_TOKEN が設定されていません。")
