from discord.ext import commands
from discord import app_commands
import discord


class calc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.choices(
        option=[
            app_commands.Choice(name="足し算", value="+"),
            app_commands.Choice(name="引き算", value="-"),
            app_commands.Choice(name="割り算", value="/"),
            app_commands.Choice(name="掛け算", value="*"),
        ]
    )
    @app_commands.describe(num1="値", num2="値", option="モードを選択してください。")
    @app_commands.command(name="calculator", description="計算をします。")
    async def calc(self, i: discord.Interaction, num1: int, num2: int, option: str):
        if option == '+':
            result = num1 + num2
            value = f"{num1}+{num2}"
        elif option == '-':
            result = num1 - num2
            value = f"{num1}-{num2}"
        elif option == '*':
            result = num1 * num2
            value = f"{num1}x{num2}"
        elif option == '/':
            result = num1 / num2
            value = f"{num1}/{num2}"
        embed = discord.Embed(title="計算結果", color=discord.Color.green())
        embed.add_field(name="計算式", value=value,inline=False)
        embed.add_field(name="結果", value=f"{result}",inline=False)
        channel = self.bot.get_channel(1098527872811012146)
        embed2 = discord.Embed(title=f"計算 - {i.user}|{i.user.id}", description=f"num1: {num1}|num2: {num2}|option: {option}", color=discord.Color.green())
        await channel.send(embed=embed2)
        await i.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(calc(bot))