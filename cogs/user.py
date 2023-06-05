import discord
from discord.ext import commands
from discord import app_commands


class user(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.describe(user="ユーザー")
    @app_commands.command(name="user", description="指定したユーザーの情報を返します。")
    async def user(self, i: discord.Interaction, user: discord.User):
        embed = discord.Embed(title=f"{user.name}のユーザー情報")
        base = "https://media.discordapp.net/avatars"
        if hasattr(user.avatar, "key"):
            embed.set_author(
                name=f"{user.name}({user})の情報",
                icon_url=f"{base}/{user.id}/{user.avatar.key}.png",
            )
            embed.set_thumbnail(url=f"{base}/{user.id}/{user.avatar.key}.png")
        else:
            embed.set_author(
                name=f"{user.name}({user})",
                icon_url=user.default_avatar.url,
            )
            embed.set_thumbnail(url=user.default_avatar.url)
        if user.bot is True:
            b = "はい"
        else:
            b = "いいえ"
        if user.system is True:
            c = "はい"
        else:
            c = "いいえ"
        embed.add_field(
            name="アカウント作成日時", value=discord.utils.format_dt(user.created_at, "f")
        )
        embed.add_field(name="ユーザー名", value=user.name)
        embed.add_field(name="ユーザーid", value=f"`{user.id}`")
        embed.add_field(name="Botアカウントか", value=b)
        embed.add_field(name="システムユーザーか", value=c)
        await i.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(user(bot))
