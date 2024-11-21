import discord
from discord import app_commands, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View
import json

f = open('config.json')
data = json.load(f)
ban_reason_prefix = data['ban_reason_prefix']
f.close()

class OBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        customId = interaction.data.get('custom_id')
        if customId == None:
            return
        await interaction.response.defer()

        if customId == "banButton":
            embed = interaction.message.embeds[0].description
            user = await interaction.client.fetch_user(embed.partition('**Пользователь:** <@')[2].split('> (', 1)[0])
            reason = embed.partition('**Причина:** ')[2].split('\n', 1)[0]
            try:
                entry = await interaction.guild.fetch_ban(user)
                embed = discord.Embed(title = f"Этот пользователь уже забанен! {user.mention} (Тег: {user.name}, Ник: {user.display_name}) \nПричина: {entry.reason}")
                await interaction.followup.send(interaction.user.mention, embed=embed, ephemeral=True)
            except discord.NotFound:
                await interaction.guild.ban(user, reason=ban_reason_prefix + ": " + reason)
                embed = discord.Embed(title =  f"Успешно забанил пользователя! {user.mention} (Тег: {user.name}, Ник: {user.display_name}) \nПричина: {reason}")
                await interaction.followup.send(interaction.user.mention, embed=embed)
        elif customId == "disableAutoBanButton":
            f = open('servers.json')
            try:
                data = json.load(f)
            except ValueError as e:
                embed = discord.Embed(title = "servers.json сломан! (Отправьте ошибку нам)\nОшибка:\n" + str(e))
                await interaction.followup.send(interaction.user.mention, embed=embed)
                return
            f.close()

            if str(interaction.guild_id) not in data:
                return
            if data[str(interaction.guild_id)]["AutoBan"] == False:
                embed = discord.Embed(title = "Автобан уже выключен")
                await interaction.followup.send(interaction.user.mention, embed=embed, ephemeral=True)
                return
            data[str(interaction.guild_id)]["AutoBan"] = False
            json.dump(data, open('servers.json', 'w'))

            embed = discord.Embed(title = "Автобан был успешно выключен")
            await interaction.followup.send(interaction.user.mention, embed=embed)

    @app_commands.command(name="oban", description="Отправить запрос на бан определённого пользователя в другие сервера")
    @commands.has_permissions(ban_members=True)
    async def oban(self, interaction: discord.Interaction, user: discord.User, reason: str, image: discord.Attachment):
        await interaction.response.defer()

        if 'image' not in image.content_type:
            embed = discord.Embed(title = "Поддерживаются только картинки!")
            await interaction.followup.send(embed=embed)
            return

        try:
            await user.ban(reason=ban_reason_prefix+": "+reason)
        except discord.Forbidden as e:
            embed = discord.Embed(title = "У бота не хватает прав на этом сервере чтобы забанить этого пользователя! \n" + str(e))
            await interaction.followup.send(embed=embed)
            return
        banRequestMessage = f"**С:** {interaction.guild.name} | **Админ:** {interaction.user.mention} (Тег: {interaction.user.name}, Ник: {interaction.user.display_name}) \n**Пользователь:** {user.mention} (Тег: {user.name}, Ник: {user.display_name}) \n**Причина:** {reason}"

        f = open('servers.json')
        data = json.load(f)
        f.close()
        for server in data.keys():
            guild = await self.bot.fetch_guild(server)
            channel = await guild.fetch_channel(data[server]["ChannelId"])
            embed = discord.Embed(description = banRequestMessage)
            if data[server]["AutoBan"]:
                embed = discord.Embed(description = "(Вы можете игнорировать так как у вас включен автобан /autoban)\n" + banRequestMessage)
                await guild.ban(user, reason=ban_reason_prefix+": "+reason)
            embed.set_image(url="attachment://" + image.filename)
            view = View()
            button = Button(custom_id = 'banButton', label = "Забанить", style = ButtonStyle.red, emoji = '🔨')
            if data[server]["AutoBan"]:
                button = Button(custom_id = 'disableAutoBanButton', label = "Убрать автобан", style = ButtonStyle.red, emoji = '❌')
            view.add_item(item=button)
            await channel.send(embed=embed, file=await image.to_file(), view=view)

        embed = discord.Embed(description = "Запрос отправлен!\nВаш запрос:\n" + banRequestMessage)
        embed.set_image(url="attachment://" + image.filename)
        await interaction.followup.send(embed=embed, file=await image.to_file())

async def setup(bot): # a extension must have a setup function
	await bot.add_cog(OBan(bot)) # adding a cog