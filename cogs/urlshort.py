from discord.ext import commands
from discord import app_commands
import aiohttp
import discord


class urlshort(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="url_short", description="入力したURLを短縮します。")
    @app_commands.describe(url="短縮したいURLを入力してください。")
    async def shorturl(self, i: discord.Interaction, url: str):
        base = f"https://is.gd/create.php?format=simple&url={url}"
        async with aiohttp.ClientSession() as session:
            headers = {"User-Agent": "20Plus/1.0(DiscordBot)"}
            async with session.get(base, headers=headers) as r:
                if r.status == 200:
                    shortenurl = await r.text()
                    embed = discord.Embed(title="短縮結果", description=f"{url} から {shortenurl} に短縮しました。", color=discord.Color.green())
                    channel = self.bot.get_channel(1098527872811012146)
                    embed2 = discord.Embed(title=f"URL短縮 - {i.user}|{i.user.id}", description=f"url: {url} |shortenurl: {shortenurl}", color=discord.Color.green())
                    await channel.send(embed=embed2)
                    await i.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="エラー", description=f"HTTPエラー({r.status})が発生しました。", color=discord.Color.red())
                    await i.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(urlshort(bot))