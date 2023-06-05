from discord.ext import commands
from discord import app_commands
import discord


class searchengine(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="searchengines", description="選択した検索エンジンのURLを送ります。")
    @app_commands.describe(select="検索エンジンを選択してください。")
    @app_commands.choices(
        select=[
            app_commands.Choice(name="DuckDuckGo", value="DuckDuckGo"),
            app_commands.Choice(name="Yahoo", value="Yahoo"),
            app_commands.Choice(name="Google", value="Google"),
            app_commands.Choice(name="Bing", value="Bing"),
            app_commands.Choice(name="YahooJP", value="YahooJP"),
        ]
    )
    async def searchengine(self, i: discord.Interaction, select: str):
        if select == "DuckDuckGo":
            await i.response.send_message("https://duckduckgo.com/", ephemeral=True)
        elif select == "Yahoo":
            await i.response.send_message("https://yahoo.com/", ephemeral=True)
        elif select == "Google":
            await i.response.send_message("https://www.google.co.jp/", ephemeral=True)
        elif select == "Bing":
            await i.response.send_message("https://www.bing.com/", ephemeral=True)
        elif select == "YahooJP":
            await i.response.send_message("https://www.yahoo.co.jp/", ephemeral=True)
        else:
            await i.response.send_message("エラーが発生しました。", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(searchengine(bot))