import discord
import itertools
from datetime import datetime
from os import environ, listdir
from discord.ext import commands, tasks
from keep_alive import keep_alive

Token = environ['Token']

class ALookZ(commands.Bot):
  async def setup_hook(self):
    keep_alive()
    for name in listdir("ALook0/cogs"):
      if not name.startswith(("_", ".")):
        await bot.load_extension(
          f"cogs.{name[:-3] if name.endswith('.py') else name}"
        )
    await self.tree.sync()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = ALookZ(command_prefix="A0+", intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="起動中..",),status=discord.Status.dnd, help_command=None,)

@tasks.loop(seconds=10)
async def StatusSwap(cycle_d):
  activity = discord.Game(next(cycle_d))
  await bot.change_presence(activity=activity, status=discord.Status.online)

@bot.listen(name="on_ready")
async def bot_ready():
  print("起動完了")
  print("------------------------------------")
  print(f"ユーザーネーム: {bot.user}")
  print(f"アプリケーションID: {bot.application_id}")
  print(f"招待リンク: https://discord.com/api/oauth2/authorize?client_id={bot.application_id}&permissions=8&scope=bot%20applications.commands")
  print("------------------------------------")
  bot.kidoutime = int(datetime.now().timestamp())
  channel = bot.get_channel(1096598013322989631)
  embed = discord.Embed(title=":white_check_mark: 起動完了", description=f"{bot.user.name}が正常に起動しました。",color=discord.Color.green())
  embed.set_footer(text=bot.user, icon_url=bot.user.avatar,)
  await channel.send(embed=embed)
  await StatusSwap.start(
    itertools.cycle(
      [
        f"/help | {len(bot.guilds)} サーバー",
        f"/help | {len(bot.users)} ユーザー",
        f"/help | {round(bot.latency * 1000)} ms",
      ]
    )
  )

@bot.listen(name="on_command_error")
async def cmderror(ctx, errors):
  embed = discord.Embed(title="おっと...", description="文字コマンドにはサポートしていないようです。", color=discord.Color.red())
  await ctx.send(embed=embed)

try:
  bot.run(Token)
except discord.HTTPException:
  print("RateLimit Error.")