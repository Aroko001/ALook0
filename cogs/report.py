from discord.ext import commands
from discord import app_commands
import discord


class report(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="bug_report", description="バグ報告をします。")
    @app_commands.describe(description="報告する内容を入力してください。")
    async def bugreport(self, i: discord.Interaction, description: str):
        channel = self.bot.get_channel(1095604986051842138)
        embed = discord.Embed(title=f"バグ報告 - {i.user}|{i.user.id} - {i.guild}", description=description, color=discord.Color.green())
        await channel.send(embed=embed)
        await i.response.send_message("送信しました。ご協力ありがとうございます。", ephemeral=True)

    @app_commands.command(name="feature_suggestion", description="機能提案をします。")
    @app_commands.describe(description="提案する内容を入力してください。")
    async def featuresuggestion(self, i: discord.Interaction, description: str):
        channel = self.bot.get_channel(1095609040589037648)
        embed = discord.Embed(title=f"機能提案 - {i.user}|{i.user.id} - {i.guild}", description=description, color=discord.Color.green())
        await channel.send(embed=embed)
        await i.response.send_message("送信しました。ご協力ありがとうございます。", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(report(bot))