from discord.ext import commands
from discord import app_commands
import discord

class rolelist(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="rolelist", description="ロールの一覧を表示します。")
    async def rolelist(self, i: discord.Interaction):
        guild = i.guild
        if len(guild.roles) > 1:
            role = "\n".join([r.mention for r in guild.roles][1:])
            embed = discord.Embed(title="ロール一覧", description=f"{role}")
            await i.response.send_message(embed=embed)
        else:
            await i.response.send_message("ロールが見つかりませんでした。")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(rolelist(bot))