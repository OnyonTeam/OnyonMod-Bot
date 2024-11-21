import discord
from discord import app_commands
from discord.ext import commands
import json, typing

f = open('config.json')
data = json.load(f)
f.close()

class AutoBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='autoban', description='Автоматически банит человека когда кто-то отправляет запрос')
    @commands.has_permissions(ban_members=True)
    async def autoban(self, interaction: discord.Interaction, action: typing.Literal["статус", "включить", "выключить"]):
        await interaction.response.defer()

        f = open('servers.json')
        try:
            data = json.load(f)
        except ValueError as e:
            embed = discord.Embed(title = "servers.json сломан! (Отправьте ошибку нам)\nОшибка:\n" + str(e))
            await interaction.followup.send(embed=embed)
            return
        f.close()

        if str(interaction.guild_id) not in data:
            embed = discord.Embed(title = "Вашего сервера нету в списке, попросите нас добавить вас в него")
            await interaction.followup.send(embed=embed)
            return

        if action == "статус":
            action = {True: "включен", False: "выключен"}[data[str(interaction.guild_id)]["AutoBan"]]
            embed = discord.Embed(title = "Автобан сейчас " + action)
            await interaction.followup.send(embed=embed)
            return

        action = {"включить": [True, "включен"], "выключить": [False, "выключен"]}[action]
        data[str(interaction.guild_id)]["AutoBan"] = action[0]
        json.dump(data, open('servers.json', 'w'))

        embed = discord.Embed(title = "Автобан был успешно " + action[1])
        await interaction.followup.send(embed=embed)
    
async def setup(bot): # a extension must have a setup function
	await bot.add_cog(AutoBan(bot)) # adding a cog