from discord.ext import commands
from discord import app_commands
import discord
import aiohttp
import tracemalloc

tracemalloc.start()


class urlcheck(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="url_check", description="URLを検査します。")
    @app_commands.describe(url="検査したいURLを入力してください。")
    async def url(self, i: discord.Interaction, url: str):
        base = f"https://safeweb.norton.com/report/show?url={url}&ulang=jpn"
        async with aiohttp.ClientSession() as session:
            headers = {"User-Agent": "20Plus/1.0(DiscordBot)"}
            async with session.get(base, headers=headers) as r:
                if r.status == 200:
                    data = await r.content.read()
                    if "安全".encode() in data:
                        embed = discord.Embed(title="結果は安全です。", description=f"Norton Safewebが{url} を分析して安全性とセキュリティの問題を調べました。", color=discord.Color.green())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 安全", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                    elif "注意".encode() in data:
                        embed = discord.Embed(title="結果は注意です。", description="注意の評価を受けた Web サイトは少数の脅威または迷惑を伴いますが、赤色の警告に相当するほど危険とは見なされません。サイトにアクセスする場合には注意が必要です。", color=discord.Color.yellow())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 注意", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                    elif "警告".encode() in data:
                        embed = discord.Embed(title="結果は警告です。", description="これは既知の危険な Web ページです。このページを表示**しない**ことを推奨します。", color=discord.Color.red())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 警告", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                    elif "未評価".encode() in data:
                        embed = discord.Embed(title="結果は未評価です。", description="このURLは未分類に当たるので、評価がありません。", color=discord.Color.dark_gray())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 未評価", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="エラー", description="エラーが発生しました。", color=discord.Color.red())
                    await i.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(urlcheck(bot))