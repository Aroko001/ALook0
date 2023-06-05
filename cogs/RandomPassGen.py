from discord.ext import commands
from discord import app_commands
import secrets
import discord
import string


class passgen(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="generatepassword", description="ランダムなパスワードを生成します。")
    @app_commands.describe(length="パスワードの長さを入力してください。")
    async def generate_password(self, i: discord.Interaction, length: int = 8):
        if length > 50:
            embed = discord.Embed(title='エラー', color=0xE74C3C) 
            embed.add_field(name='エラー内容', value="パスワードの長さは50より大きくできません。")
            await i.response.send_message(embed=embed, ephemeral=True)
            return
        user = i.user
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*()'
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        embed = discord.Embed(title='ランダムなパスワードを生成しました。', color=0x00ff00)
        embed.add_field(name='生成されたパスワード', value=password)
        await user.send(embed=embed)
        channel = self.bot.get_channel(1098527872811012146)
        if length == 8:
          description = "length = default(8)"
        else:
          description = f"length = {length}"
        embed2 = discord.Embed(title=f"generatepassword - {i.user}|{i.user.id}", description=description,color=discord.Color.green())
        await channel.send(embed=embed2)
        await i.response.send_message("DMにランダム生成したパスワードを送信しました。", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(passgen(bot))