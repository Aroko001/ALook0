from discord.ext import commands
from discord import app_commands
import discord


class help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="help", description="コマンドの一覧を表示します。")
    async def help(self, i: discord.Interaction):
        num = 0
        embed = discord.Embed(
            title="コマンド一覧", timestamp=i.created_at, color=discord.Color.purple()
        )

        for command in self.bot.tree.walk_commands():
            num = num + 1
            if num > 24:
                embed.add_field(name=command.name, value=command.description)
            else:
                embed.add_field(name=command.name, value=command.description)
        if i.user.avatar is None:
            embed.set_footer(
                text=f"実行者: {i.user} ",
                icon_url=i.user.defualt_avatar,
            )
        else:
            embed.set_footer(
                text=f"実行者: {i.user} ",
                icon_url=i.user.avatar,
            )
        await i.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(help(bot))