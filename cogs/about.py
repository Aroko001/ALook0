from discord.ext import commands
from discord import app_commands
import discord

class InviteButton(discord.ui.View):
    def __init__(self, inv: str):
        super().__init__()
        self.inv = inv
        self.add_item(discord.ui.Button(label="招待ボタン", url=self.inv))

class about(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="about", description="このbotの情報を表示します。")
    async def about(self, i: discord.Interaction):
        embed = discord.Embed(title="このボットの情報", description=f"このbotは[Ar0ko192#0059](https://discord.com/users/790489873957781536)という人物に作られました。\n起動時刻: <t:{self.bot.kidoutime}:F>\n\n関連リンク\n[招待リンク](https://dsc.gg/alook)",color=discord.Color.green())
        embed.set_thumbnail(url=f"https://media.discordapp.net/avatars/{self.bot.user.id}/{self.bot.user.avatar.key}.png")
        await i.response.send_message(embed=embed,view=InviteButton(str("https://discord.com/api/oauth2/authorize?client_id=1107181590695645294&permissions=8&scope=bot%20applications.commands")))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(about(bot))