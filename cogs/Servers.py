import discord
from discord import app_commands, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View
import json

f = open('config.json')
data = json.load(f)
discord_bot_access_role_id = data['discord_bot_access_role_id']
f.close()

class Servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addserver", description="Добавить сервер в учёт (Только Onyon)")
    @commands.has_role(discord_bot_access_role_id)
    async def addserver(self, interaction: discord.Interaction, server_id: str, channel_id: str):
        await interaction.response.defer()

        try:
            guild = await self.client.fetch_guild(server_id)
            channel = await guild.fetch_channel(channel_id)
        except Exception as e:
            embed = discord.Embed(title = "Произошла ошибка! \nОшибка:\n" + str(e))
            await interaction.followup.send(embed=embed)
            return

        f = open('servers.json')
        try:
            data = json.load(f)
        except ValueError as e:
            embed = discord.Embed(title = "Ваш servers.json сломан! (если ваш servers.json пустой то добавьте  в него эти 2 символа {} )\nОшибка:\n" + str(e))
            await interaction.followup.send(embed=embed)
            return
        f.close()

        data.update({server_id: {"ServerName": guild.name, "ChannelId": int(channel_id), "AutoBan": False}})
        json.dump(data, open('servers.json', 'w'))

        embed = discord.Embed(title = f"Сервер {guild.name} ({server_id}) учитывается с этого момента!")
        await interaction.followup.send(embed=embed)
        embed = discord.Embed(title = "Ваш сервер учитывается с этого момента!")
        await channel.send(embed=embed)

    @app_commands.command(name="removeserver", description="Удалить сервер из учёта (Только Onyon)")
    @commands.has_role(discord_bot_access_role_id)
    async def removeserver(self, interaction: discord.Interaction, server_id: str):
        await interaction.response.defer()

        f = open('servers.json')
        try:
            data = json.load(f)
        except ValueError as e:
            embed = discord.Embed(title = "Ваш servers.json сломан! (если ваш servers.json пустой то добавьте  в него эти 2 символа {} )\nОшибка:\n" + str(e))
            await interaction.followup.send(embed=embed)
            return
        f.close()

        if server_id not in data:
            embed = discord.Embed(title = "Сервер с айди " + server_id + " не найден в servers.json, убедитесь что вы ввели имя сервера правильно")
            await interaction.followup.send(embed=embed)
            return
        err = ""
        try:
            guild = await self.client.fetch_guild(server_id)
            #await guild.leave()
        except Exception as e:
            err = "Но произошла ошибка при выходе из сервера: \n" + str(e)
        del data[server_id]
        json.dump(data, open('servers.json', 'w'))
        embed = discord.Embed(title = f"Сервер {guild.name} ({server_id}) больше не учитывается! "+err)
        await interaction.followup.send(embed=embed)

async def setup(bot): # a extension must have a setup function
	await bot.add_cog(Servers(bot)) # adding a cog