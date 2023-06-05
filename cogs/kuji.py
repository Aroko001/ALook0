from discord.ext import commands
from discord import app_commands
import discord
import random


class kuji(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="kuji", description="おみくじができます。")
    async def kuji(self, i: discord.Interaction):
        result = ["大吉", "中吉", "小吉", "末吉", "凶", "大凶"]
        embed = discord.Embed(title="おみくじ結果", description=random.choice(result), color=discord.Color.green())
        await i.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(kuji(bot))