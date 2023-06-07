import subprocess
from discord.ext import commands
from discord import app_commands
import discord
from discord import ui, TextStyle
import os

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
        channel = self.bot.get_channel(1098527872811012146)
        embed2 = discord.Embed(title=f"Python - {interaction.user}|{interaction.user.id}", description=f"code: ```{self.codes}```\nresult:```{result.stdout}\n{result.stderr}```", color=discord.Color.green())
        await channel.send(embed=embed2)
        await interaction.response.send_message(embed=embed)
        os.remove("././temp.py")

class python(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="python", description="コマンドを実行します。")
    async def python(self, i: discord.Interaction):
       await i.response.send_modal(Modal())
      

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(python(bot))