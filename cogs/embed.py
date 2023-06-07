from discord.ext import commands
from discord import app_commands
import discord
from discord import ui, TextStyle

class Modal(ui.Modal, title="Embed作成"):
    titles = ui.TextInput(label="タイトル", style=TextStyle.short, placeholder="埋め込みのタイトル", required=True,)
    description = ui.TextInput(label="説明", style=TextStyle.long, placeholder="埋め込みの説明", max_length=4000, required=False,)
    picture = ui.TextInput(label="画像", style=TextStyle.short, placeholder="埋め込みの画像", required=False,)

    async def on_submit(self, interaction: discord.Interaction):
        if (
            str(self.picture).startswith("http://")
            or str(self.picture).startswith("https://")
        ):
            await interaction.response.send_message(
                "URLはhttp(s)から始まります。", ephemeral=True
            )
            return
        embed = discord.Embed(title=self.titles)
        if self.description:
            embed = discord.Embed(title=self.titles, description=self.description)
            if self.picture:
                embed = discord.Embed(title=self.titles, description=self.description)
                embed.set_footer(icon_url=self.picture)
        if self.picture:
            embed = discord.Embed(title=self.titles)
            embed.set_footer(icon_url=self.picture)

        await interaction.response.send_message(embed=embed)

class embed_create(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="embed", description="Embedを作ります。")
    async def embed_create(self, i: discord.Interaction):
      await i.response.send_modal(Modal())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(embed_create(bot))