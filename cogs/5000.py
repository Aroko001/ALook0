import discord
from discord.ext import commands
from discord import app_commands
import urllib.parse


class FiveHoundredYen(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    @app_commands.describe(
        bottom="下部文字列",
        top="上部文字列",
    )
    @app_commands.command(name="5000chouyen", description="5000兆円ほしいを生成します。")
    async def fivehoundred(self, i: discord.Interaction, top: str, bottom: str):
        embed = discord.Embed(title="5000兆円ほしいを生成しました。", color=0x3498DB).set_image(
            url=f"https://gsapi.cbrx.io/image?top={urllib.parse.quote(top)}&bottom={urllib.parse.quote(bottom)}"
        )
        channel = self.bot.get_channel(1098527872811012146)
        embed2 = discord.Embed(title=f"5000兆円ほしい - {i.user}|{i.user.id}", description=f"top: {top}|bottom: {bottom}|URL: https://gsapi.cbrx.io/image?top={urllib.parse.quote(top)}&bottom={urllib.parse.quote(bottom)}", color=discord.Color.green())
        await channel.send(embed=embed2)
        await i.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FiveHoundredYen(bot))