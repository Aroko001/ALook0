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

class 情報(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name='help', description='コマンドの一覧を表示します。')
    async def help(self, i: discord.Interaction):
        embed = discord.Embed(
            title="ヘルプ",
            description=f"多機能なBot, **ALook0**\n\nお問い合わせや要望は/feature_suggestionコマンドでお願いします。\n\n起動時刻: <t:{self.bot.kidoutime}:F>\n\n招待はこちらから↓\n[管理者権限](https://discord.com/oauth2/authorize?client_id=1107181590695645294&scope=bot+applications.commands&permissions=8)\n[権限なし](https://discord.com/oauth2/authorize?client_id=1107181590695645294&scope=bot+applications.commands)"
        )
        view = discord.ui.View().add_item(HelpSelect(self.bot))
        await i.response.send_message(embed=embed, view=view)

    @app_commands.command(name="ping", description="BotのPing値を表示します。")
    async def ping(self, i: discord.Interaction):
        embed = discord.Embed(title="Pong! :ping_pong:", description=f"現在のBotのPing値は{round(self.bot.latency * 1000)}msです。", color=discord.Color.green())
        await i.response.send_message(embed=embed)

    @app_commands.command(name="bug_report", description="バグ報告をします。")
    @app_commands.describe(description="報告する内容を入力してください。")
    async def bugreport(self, i: discord.Interaction, description: str):
        channel = self.bot.get_channel(1095604986051842138)
        embed = discord.Embed(title=f"バグ報告 - {i.user}|{i.user.id} - {i.guild}", description=description, color=discord.Color.green())
        await channel.send(embed=embed)
        await i.response.send_message("送信しました。ご協力ありがとうございます。", ephemeral=True)

    @app_commands.command(name="feature_suggestion", description="機能提案をします。")
    @app_commands.describe(description="提案する内容を入力してください。")
    async def featuresuggestion(self, i: discord.Interaction, description: str):
        channel = self.bot.get_channel(1095609040589037648)
        embed = discord.Embed(title=f"機能提案 - {i.user}|{i.user.id} - {i.guild}", description=description, color=discord.Color.green())
        await channel.send(embed=embed)
        await i.response.send_message("送信しました。ご協力ありがとうございます。", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(情報(bot))