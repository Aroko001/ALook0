from discord.ext import commands
from discord import app_commands
import discord


class ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="ping", description="BotのPing値を表示します。")
    async def ping(self, i: discord.Interaction):
        embed = discord.Embed(title="Pong! :ping_pong:", description=f"現在のBotのPing値は{round(self.bot.latency * 1000)}msです。", color=discord.Color.green())
        await i.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ping(bot))