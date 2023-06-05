import discord
from discord.ext import commands
from discord import app_commands


class botinv(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.describe(botuser="ボットを選択してください。")
    @app_commands.command(name="botinv", description="選択したBotの招待を返します。")
    async def botinv(self, i: discord.Interaction, botuser: discord.User):
      if botuser.bot == True:
        embed = discord.Embed(title=f"{botuser}の招待リンク")
        embed.add_field(name="管理者権限", value=f"https://discord.com/oauth2/authorize?client_id={botuser.id}&scope=bot+applications.commands&permissions=8", inline=False)
        embed.add_field(name="選択可能権限", value=f"https://discord.com/oauth2/authorize?client_id={botuser.id}&scope=bot+applications.commands&permissions=70368744177655", inline=False)
        embed.add_field(name="権限なし", value=f"https://discord.com/oauth2/authorize?client_id={botuser.id}&scope=bot+applications.commands")
        await i.response.send_message(embed=embed)
      else:
        await i.response.send_message("選択したユーザーはBotではありません。", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(botinv(bot))
