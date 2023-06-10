from discord.ext import commands
from discord import app_commands
import discord

class InviteButton(discord.ui.View):
    def __init__(self, inv: str):
        super().__init__()
        self.inv = inv
        self.add_item(discord.ui.Button(label="招待ボタン", url=self.inv))

class 情報(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="ping", description="BotのPing値を表示します。")
    async def ping(self, i: discord.Interaction):
        embed = discord.Embed(title="Pong! :ping_pong:", description=f"現在のBotのPing値は{round(self.bot.latency * 1000)}msです。", color=discord.Color.green())
        await i.response.send_message(embed=embed)

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
    await bot.add_cog(情報(bot))