from discord.ext import commands
from discord import app_commands, ui, TextStyle
import discord
import subprocess
import os
import random
import urllib.parse

class Modal(ui.Modal, title="コード実行"):
    codes = ui.TextInput(label="コード", style=TextStyle.long, placeholder="実行するコード", max_length=4000, required=True,)

    async def on_submit(self, interaction: discord.Interaction):
        if "import os" in str(self.codes) or "import sys" in str(self.codes):
          return await interaction.response.send_message(embed=discord.Embed(title="エラー", description="コード内に`os`と`sys`はインポートできません。", color=discord.Color.red()), ephemeral=True)
        if "open" in str(self.codes):
          return await interaction.response.send_message(embed=discord.Embed(title="エラー", description="ファイルの操作はできません。", color=discord.Color.red()),ephemeral=True)
        if str(self.codes) == "juusou":
          return await interaction.response.send_message("https://media.discordapp.net/attachments/1015482770845335652/1104262558338273411/DDLVID.COM-1648698069645680641_1.gif", ephemeral=True)
        if str(self.codes) == "bocchitherock":
          return await interaction.response.send_message("https://tenor.com/view/bocchi-bocchitherock-hitori-gotou-%E3%81%BC%E3%81%A3%E3%81%A1%E3%81%96%E3%82%8D%E3%81%A3%E3%81%8F-anime-gif-26895035", ephemeral=True)
        with open("././temp.py", "w") as f:
          f.write(str(self.codes))
        result = subprocess.run(["python", "temp.py"], capture_output=True, text=True)
        embed = discord.Embed(title="Python", color=discord.Color.green())
        embed.add_field(name="コード", value=f"```python\n{str(self.codes)}```", inline=False)
        embed.add_field(name="出力", value=f"```{result.stdout}\n{result.stderr}```")
        await interaction.response.send_message(embed=embed)
        os.remove("././temp.py")

class 遊びやネタ(commands.Cog):
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

    @app_commands.command(name="reverse", description="入力した文字を逆文字にして表示します。")
    @app_commands.describe(input_string="逆文字にしたい文字を入力してください。")
    async def reverse(self, i: discord.Interaction, input_string: str):
        embed = discord.Embed(title="逆文字結果", description=f"{input_string[::-1]}", color=discord.Color.green())
        channel = self.bot.get_channel(1098527872811012146)
        embed2 = discord.Embed(title=f"逆文字 - {i.user}|{i.user.id}", description=f"input_string: {input_string}", color=discord.Color.green())
        await channel.send(embed=embed2)
        await i.response.send_message(embed=embed)

    @app_commands.command(name="kuji", description="おみくじができます。")
    async def kuji(self, i: discord.Interaction):
        result = ["大吉", "中吉", "小吉", "末吉", "凶", "大凶"]
        embed = discord.Embed(title="おみくじ結果", description=random.choice(result), color=discord.Color.green())
        await i.response.send_message(embed=embed)

    @app_commands.describe(
        bottom="下部文字列",
        top="上部文字列",
    )
    @app_commands.command(name="5000chouyen", description="5000兆円ほしいを生成します。")
    async def fivehoundred(self, i: discord.Interaction, top: str, bottom: str):
        embed = discord.Embed(title="5000兆円ほしいを生成しました。", color=0x3498DB).set_image(
            url=f"https://gsapi.cbrx.io/image?top={urllib.parse.quote(top)}&bottom={urllib.parse.quote(bottom)}"
        )
        channel = self.bot.get_channel(1098527872811012146)
        embed2 = discord.Embed(title=f"5000兆円ほしい - {i.user}|{i.user.id}", description=f"top: {top}|bottom: {bottom}|URL: https://gsapi.cbrx.io/image?top={urllib.parse.quote(top)}&bottom={urllib.parse.quote(bottom)}", color=discord.Color.green())
        await channel.send(embed=embed2)
        await i.response.send_message(embed=embed)

    @app_commands.command(name="python", description="コマンドを実行します。")
    async def python(self, i: discord.Interaction):
       await i.response.send_modal(Modal())
    
    @app_commands.command(name="uptime", description="Botの起動時刻を表示します。")
    async def uptime(self, i: discord.Interaction):
        await i.response.send_message(f"起動時刻: <t:{self.bot.kidoutime}:F>")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(遊びやネタ(bot))