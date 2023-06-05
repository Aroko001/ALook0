from discord.ext import commands
from discord import app_commands
import discord


class purge(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="purge", description="メッセージを削除します。")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, i: discord.Interaction, number: int):
      channel = i.channel
      deleted = await channel.purge(limit=number)
      await i.response.send_message(f"{len(deleted)}メッセージを削除しました。")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(purge(bot))