from discord.ext import commands
from discord import app_commands, ui, TextStyle
import aiohttp
import async_google_trans_new
import discord
import string
import secrets

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
        embed = discord.Embed(title=self.titles, description=self.description)
        embed.set_thumbnail(url=self.picture)

        await interaction.response.send_message(embed=embed)

class 便利(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="url_short", description="入力したURLを短縮します。")
    @app_commands.describe(url="短縮したいURLを入力してください。")
    async def shorturl(self, i: discord.Interaction, url: str):
        base = f"https://is.gd/create.php?format=simple&url={url}"
        async with aiohttp.ClientSession() as session:
            headers = {"User-Agent": "ALook0/1.0(DiscordBot)"}
            async with session.get(base, headers=headers) as r:
                if r.status == 200:
                    shortenurl = await r.text()
                    embed = discord.Embed(title="短縮結果", description=f"{url} から {shortenurl} に短縮しました。", color=discord.Color.green())
                    channel = self.bot.get_channel(1098527872811012146)
                    embed2 = discord.Embed(title=f"URL短縮 - {i.user}|{i.user.id}", description=f"url: {url} |shortenurl: {shortenurl}", color=discord.Color.green())
                    await channel.send(embed=embed2)
                    await i.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="エラー", description=f"HTTPエラー({r.status})が発生しました。", color=discord.Color.red())
                    await i.response.send_message(embed=embed)

    @app_commands.command(name="url_check", description="URLを検査します。")
    @app_commands.describe(url="検査したいURLを入力してください。")
    async def url(self, i: discord.Interaction, url: str):
        base = f"https://safeweb.norton.com/report/show?url={url}&ulang=jpn"
        async with aiohttp.ClientSession() as session:
            headers = {"User-Agent": "20Plus/1.0(DiscordBot)"}
            async with session.get(base, headers=headers) as r:
                if r.status == 200:
                    data = await r.content.read()
                    if "安全".encode() in data:
                        embed = discord.Embed(title="結果は安全です。", description=f"Norton Safewebが{url} を分析して安全性とセキュリティの問題を調べました。", color=discord.Color.green())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 安全", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                    elif "注意".encode() in data:
                        embed = discord.Embed(title="結果は注意です。", description="注意の評価を受けた Web サイトは少数の脅威または迷惑を伴いますが、赤色の警告に相当するほど危険とは見なされません。サイトにアクセスする場合には注意が必要です。", color=discord.Color.yellow())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 注意", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                    elif "警告".encode() in data:
                        embed = discord.Embed(title="結果は警告です。", description="これは既知の危険な Web ページです。このページを表示**しない**ことを推奨します。", color=discord.Color.red())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 警告", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                    elif "未評価".encode() in data:
                        embed = discord.Embed(title="結果は未評価です。", description="このURLは未分類に当たるので、評価がありません。", color=discord.Color.dark_gray())
                        embed.set_footer(text="Powered by Norton Safeweb")
                        channel = self.bot.get_channel(1098527872811012146)
                        embed2 = discord.Embed(title=f"URL検査 - {i.user}|{i.user.id}", description=f"url: {url} |評価: 未評価", color=discord.Color.green())
                        await channel.send(embed=embed2)
                        await i.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="エラー", description="エラーが発生しました。", color=discord.Color.red())
                    await i.response.send_message(embed=embed)

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

    @app_commands.describe(text="翻訳するテキストを入力してください。", lang="翻訳をする言語を選択してください。")
    @app_commands.choices(
        lang=[
            app_commands.Choice(name="アルメニア語", value="hy"),
            app_commands.Choice(name="中国語（簡体）", value="zh"),
            app_commands.Choice(name="オランダ語", value="nl"),
            app_commands.Choice(name="英語", value="en"),
            app_commands.Choice(name="エスペラント語", value="eo"),
            app_commands.Choice(name="フランス語", value="fr"),
            app_commands.Choice(name="グルジア語", value="ka"),
            app_commands.Choice(name="ドイツ語", value="de"),
            app_commands.Choice(name="ギリシャ語", value="el"),
            app_commands.Choice(name="イタリア語", value="it"),
            app_commands.Choice(name="日本語", value="ja"),
            app_commands.Choice(name="韓国語", value="ko"),
            app_commands.Choice(name="クルド語", value="ku"),
            app_commands.Choice(name="ペルシャ語", value="fa"),
            app_commands.Choice(name="ポーランド語", value="pl"),
            app_commands.Choice(name="ポルトガル語（ポルトガル、ブラジル）", value="pt"),
            app_commands.Choice(name="ルーマニア語", value="ro"),
            app_commands.Choice(name="スペイン語", value="es"),
            app_commands.Choice(name="スウェーデン語", value="sv"),
            app_commands.Choice(name="トルコ語", value="tr"),
            app_commands.Choice(name="ウルドゥー語", value="ur"),
        ]
    )
    @app_commands.command(name="translate", description="翻訳をします。")
    async def translate(self, i: discord.Interaction, lang: str, text: str):
        g = async_google_trans_new.AsyncTranslator()
        embed = discord.Embed(title="翻訳結果", description=f"{lang}へ翻訳: {await g.translate(text, lang)}", color=discord.Color.green())
        channel = self.bot.get_channel(1098527872811012146)
        embed2 = discord.Embed(title=f"翻訳 - {i.user}|{i.user.id}", description=f"lang: {lang}|text: {text}", color=discord.Color.green())
        await channel.send(embed=embed2)
        await i.response.send_message(embed=embed)

    @app_commands.command(name="embed", description="Embedを作ります。（管理者権限所有者専用）")
    @app_commands.checks.has_permissions(administrator=True)
    async def embed_create(self, i: discord.Interaction):
      await i.response.send_modal(Modal())

    @app_commands.command(name="purge", description="メッセージを一括削除します。（メッセージ管理権限所有者専用）")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, i: discord.Interaction, number: int):
      channel = i.channel
      deleted = await channel.purge(limit=number)
      await i.response.send_message(f"{len(deleted)}メッセージを削除しました。")

    @app_commands.command(name="rolelist", description="ロールの一覧を表示します。")
    async def rolelist(self, i: discord.Interaction):
        guild = i.guild
        if len(guild.roles) > 1:
            role = "\n".join([r.mention for r in guild.roles][1:])
            embed = discord.Embed(title="ロール一覧", description=f"{role}")
            await i.response.send_message(embed=embed)
        else:
            await i.response.send_message("ロールが見つかりませんでした。")

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

    @app_commands.describe(botuser="ボットを選択してください。")
    @app_commands.command(name="botinv", description="選択したBotの招待を返します。")
    async def botinv(self, i: discord.Interaction, botuser: discord.User):
      if botuser.bot == True:
        embed = discord.Embed(title=f"{botuser}の招待リンク")
        embed.add_field(name="管理者権限", value=f"https://discord.com/oauth2/authorize?client_id={botuser.id}&scope=bot+applications.commands&permissions=8", inline=False)
        embed.add_field(name="選択可能権限", value=f"https://discord.com/oauth2/authorize?client_id={botuser.id}&scope=bot+applications.commands&permissions=70368744177655", inline=False)
        embed.add_field(name="権限なし", value=f"https://discord.com/oauth2/authorize?client_id={botuser.id}&scope=bot+applications.commands")
        await i.response.send_message(embed=embed)
      else:
        await i.response.send_message("選択したユーザーはBotではありません。", ephemeral=True)

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

    @app_commands.choices(
        地域=[
            app_commands.Choice(name="札幌", value="016010"),
            app_commands.Choice(name="青森", value="020010"),
            app_commands.Choice(name="秋田", value="050010"),
            app_commands.Choice(name="山形", value="060010"),
            app_commands.Choice(name="福島", value="070010"),
            app_commands.Choice(name="埼玉", value="110010"),
            app_commands.Choice(name="千葉", value="120010"),
            app_commands.Choice(name="東京", value="130010"),
            app_commands.Choice(name="新潟", value="150010"),
            app_commands.Choice(name="金沢", value="170010"),
            app_commands.Choice(name="福井", value="180010"),
            app_commands.Choice(name="長野", value="200010"),
            app_commands.Choice(name="岐阜", value="210010"),
            app_commands.Choice(name="静岡", value="220010"),
            app_commands.Choice(name="京都", value="260010"),
            app_commands.Choice(name="大阪", value="270000"),
            app_commands.Choice(name="神戸", value="280010"),
            app_commands.Choice(name="奈良", value="290010"),
            app_commands.Choice(name="和歌山", value="300010"),
            app_commands.Choice(name="鳥取", value="310010"),
            app_commands.Choice(name="岡山", value="330010"),
            app_commands.Choice(name="広島", value="340010"),
            app_commands.Choice(name="山口", value="350020"),
            app_commands.Choice(name="徳島", value="360010"),
            app_commands.Choice(name="福岡", value="400010"),
        ]
    )
    @app_commands.describe(地域="地域を選択してください。")
    @app_commands.command(name="weather", description="天気を表示します。")
    async def weather(self, i: discord.Interaction, 地域: str):
        base = "https://weather.tsukumijima.net/api/forecast/city"
        async with aiohttp.ClientSession() as session:
            headers = {"User-Agent": "ALook0/1.0(DiscordBot)"}
            async with session.get(f"{base}/{地域}", headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    f = js["forecasts"][0]
                    embed = discord.Embed(
                        title=js["title"],
                        description=js["description"]["bodyText"],
                        color=0x3498DB,
                    )
                    embed.add_field(
                        name=f["date"] + "の天気。", value="天気は" + f["telop"] + "です。"
                    )
                    await i.response.send_message(embed=embed)
                else:
                    await i.response.send_message("取得できません。")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(便利(bot))