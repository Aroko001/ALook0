from discord.ext import commands
from discord import app_commands
import discord

class HelpSelect(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        super().__init__(
            placeholder="カテゴリを選択してください",
            options=[
                discord.SelectOption(
                    label=cog_name, description=cog.__doc__
                ) for cog_name, cog in bot.cogs.items() if cog.__cog_app_commands__ and cog_name not in ['Jishaku']
            ]
        )

        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.bot.get_cog(self.values[0])
        assert cog

        commands_mixer = []
        for i in cog.walk_commands():
            commands_mixer.append(i)
        
        for i in cog.walk_app_commands():
            commands_mixer.append(i)

        embed = discord.Embed(
            title=f"{cog.__cog_name__} コマンド",
            description='\n'.join(
                f"**{command.name}**: `{command.description}`"
                for command in commands_mixer
            )
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

class help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name='help', description='コマンドの一覧を表示します。')
    async def help(self, i: discord.Interaction):
        embed = discord.Embed(
            title="ヘルプ",
            description=f"多機能なBot, **ALook0**\n\nお問い合わせや要望は[Ar0ko192](https://discord.com/users/790489873957781536)へお願いします。\n\n起動時刻: <t:{self.bot.kidoutime}:F>\n\n招待はこちらから↓\n[管理者権限](https://discord.com/oauth2/authorize?client_id=1107181590695645294&scope=bot+applications.commands&permissions=8)\n[権限なし](https://discord.com/oauth2/authorize?client_id=1107181590695645294&scope=bot+applications.commands)"
        )
        view = discord.ui.View().add_item(HelpSelect(self.bot))
        await i.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(help(bot))