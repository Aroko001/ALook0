import discord
import itertools
from datetime import datetime
import async_google_trans_new
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

@bot.tree.context_menu()
async def ユーザー情報(i: discord.Interaction, user: discord.User):
  embed = discord.Embed(title=f"{user.name}のユーザー情報")
  base = "https://media.discordapp.net/avatars"
  if hasattr(user.avatar, "key"):
    embed.set_author(
      name=f"{user.name}({user})の情報",
      icon_url=f"{base}/{user.id}/{user.avatar.key}.png",
    )
    embed.set_thumbnail(url=f"{base}/{user.id}/{user.avatar.key}.png")
  else:
    embed.set_author(
      name=f"{user.name}({user})",
      icon_url=user.default_avatar.url,
    )
    embed.set_thumbnail(url=user.default_avatar.url)
  if user.bot is True:
    b = "はい"
  else:
    b = "いいえ"
  if user.system is True:
    c = "はい"
  else:
    c = "いいえ"
  embed.add_field(
    name="アカウント作成日時", value=discord.utils.format_dt(user.created_at, "f")
  )
  embed.add_field(name="ユーザー名", value=user.name)
  embed.add_field(name="ユーザーid", value=f"`{user.id}`")
  embed.add_field(name="Botアカウントか", value=b)
  embed.add_field(name="システムユーザーか", value=c)
  await i.response.send_message(embed=embed, ephemeral=True)

@bot.tree.context_menu()
async def 日本語に翻訳(i: discord.Interaction, message: discord.Message):
  g = async_google_trans_new.AsyncTranslator()
  embed = discord.Embed(title="翻訳結果", description=f"日本語へ翻訳: {await g.translate(message.content, 'ja')}", color=discord.Color.green())
  channel = bot.get_channel(1098527872811012146)
  embed2 = discord.Embed(title=f"翻訳（アプリ） - {i.user}|{i.user.id}", description=f"lang: ja|text: {message.content}", color=discord.Color.green())
  await channel.send(embed=embed2)
  await i.response.send_message(embed=embed, ephemeral=False)

@bot.tree.context_menu()
async def 英語に翻訳(i: discord.Interaction, message: discord.Message):
  g = async_google_trans_new.AsyncTranslator()
  embed = discord.Embed(title="翻訳結果", description=f"英語へ翻訳: {await g.translate(message.content, 'en')}", color=discord.Color.green())
  channel = bot.get_channel(1098527872811012146)
  embed2 = discord.Embed(title=f"翻訳（アプリ） - {i.user}|{i.user.id}", description=f"lang: ja|text: {message.content}", color=discord.Color.green())
  await channel.send(embed=embed2)
  await i.response.send_message(embed=embed, ephemeral=False)

@bot.tree.context_menu()
async def プロフィール画像を取得(i: discord.Interaction, user: discord.User):
  embed = discord.Embed()
  base = "https://media.discordapp.net/avatars"
  if hasattr(user.avatar, "key"):
      embed.set_author(
          name=f"{user.name}({user})のアバター",
          icon_url=f"{base}/{user.id}/{user.avatar.key}.png",
      )
      embed.set_image(url=f"{base}/{user.id}/{user.avatar.key}.png")
  else:
      embed.set_author(
          name=f"{user.name}({user})のアバター",
          icon_url=user.default_avatar.url,
      )
      embed.set_image(url=user.default_avatar.url)
  await i.response.send_message(embed=embed, ephemeral=False)

try:
  bot.run(Token)
except discord.HTTPException:
  print("RateLimit Error.")
