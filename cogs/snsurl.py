from discord.ext import commands
from discord import app_commands
import discord


class snsurl(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="snsurl", description="選択したSNSのURLを送ります。")
    @app_commands.describe(select="SNSを選択してください。")
    @app_commands.choices(
        select=[
            app_commands.Choice(name="Discord", value="Discord"),
            app_commands.Choice(name="Facebook", value="Facebook"),
            app_commands.Choice(name="Instagram", value="Instagram"),
            app_commands.Choice(name="Reddit", value="Reddit"),
            app_commands.Choice(name="TikTok", value="TikTok"),
            app_commands.Choice(name="Twitter", value="Twitter"),
            app_commands.Choice(name="Youtube", value="Youtube"),
        ]
    )
    async def snsurl(self, i: discord.Interaction, select: str):
        if select == "Discord":
            await i.response.send_message("https://discord.com/", ephemeral=True)
        elif select == "Facebook":
            await i.response.send_message("https://ja-jp.facebook.com/", ephemeral=True)
        elif select == "Instagram":
            await i.response.send_message("https://www.instagram.com/", ephemeral=True)
        elif select == "Reddit":
            await i.response.send_message("https://www.reddit.com/", ephemeral=True)
        elif select == "TikTok":
            await i.response.send_message("https://www.tiktok.com/ja-JP", ephemeral=True)
        elif select == "Twitter":
            await i.response.send_message("https://twitter.com/", ephemeral=True)
        elif select == "Youtube":
            await i.response.send_message("https://www.youtube.com/", ephemeral=True)
        else:
            await i.response.send_message("エラーが発生しました。", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(snsurl(bot))