from datetime import datetime, timedelta
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (Bot起動完了)")


# 指定時刻にミュートするコマンド (!mute_at 22:00 @ユーザー)
@bot.command()
async def mute_at(ctx, time_str: str, member: discord.Member):
    await process_mute_setting(ctx, time_str, member, do_mute=True)


# 指定時刻にミュート解除するコマンド (!unmute_at 22:30 @ユーザー)
@bot.command()
async def unmute_at(ctx, time_str: str, member: discord.Member):
    await process_mute_setting(ctx, time_str, member, do_mute=False)


# 共通処理関数
async def process_mute_setting(ctx, time_str: str, member: discord.Member, do_mute: bool):
    action_name = "ミュート" if do_mute else "ミュート解除"
    try:
        target_time_obj = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        await ctx.send("時刻のフォーマットが正しくありません。`22:00` の形式で入力してください。")
        return

    now = datetime.now()
    target_datetime = datetime.combine(now.date(), target_time_obj)

    if target_datetime <= now:
        target_datetime += timedelta(days=1)

    wait_seconds = (target_datetime - now).total_seconds()
    formatted_time = target_datetime.strftime("%Y-%m-%d %H:%M")

    await ctx.send(f"[{member.display_name}] さんを `{formatted_time}` に{action_name}予約しました。")

    await asyncio.sleep(wait_seconds)

    if member.voice:
        await member.edit(mute=do_mute)
        await ctx.send(f"指定の時間（{time_str}）になりました。[{member.display_name}] さんの{action_name}を完了しました。")
    else:
        await ctx.send(f"[{member.display_name}] さんがVCにいないため、{action_name}処理をスキップしました。")


# ★一番下のダブルクォーテーションの中にDeveloper Portalでリセット取得したトークンを貼り付けます
bot.run（環境変数から読み込む安全な書き方）
TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("エラー: DISCORD_TOKEN が設定されていません。")
