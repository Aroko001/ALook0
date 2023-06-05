import discord
from discord.ext import commands
from discord import app_commands


class avatar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.describe(user="ユーザー")
    @app_commands.command(name="avatar", description="選択したユーザーのアバターを表示します。")
    async def avatar(self, i: discord.Interaction, user: discord.User):
        embed = discord.Embed()
        base = "https://media.discordapp.net/avatars"
        if hasattr(user.avatar, "key"):
            embed.set_author(
                name=f"{user.name}({user})のアバター",
                icon_url=f"{base}/{user.id}/{user.avatar.key}.png",
            )
            embed.set_image(url=f"{base}/{user.id}/{user.avatar.key}.png")
        else:
            embed.set_author(
                name=f"{user.name}({user})のアバター",
                icon_url=user.default_avatar.url,
            )
            embed.set_image(url=user.default_avatar.url)
        await i.response.send_message(embed=embed, ephemeral=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(avatar(bot))
