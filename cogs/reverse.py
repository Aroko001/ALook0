from discord.ext import commands
from discord import app_commands
import discord


class reverse(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="reverse", description="入力した文字を逆文字にして表示します。")
    @app_commands.describe(input_string="逆文字にしたい文字を入力してください。")
    async def reverse(self, i: discord.Interaction, input_string: str):
        embed = discord.Embed(title="逆文字結果", description=f"{input_string[::-1]}", color=discord.Color.green())
        channel = self.bot.get_channel(1098527872811012146)
        embed2 = discord.Embed(title=f"逆文字 - {i.user}|{i.user.id}", description=f"input_string: {input_string}", color=discord.Color.green())
        await channel.send(embed=embed2)
        await i.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(reverse(bot))