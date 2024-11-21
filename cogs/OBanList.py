import discord
from discord import app_commands
from discord.ext import commands
import json

f = open('config.json')
data = json.load(f)
ban_reason_prefix = data['ban_reason_prefix']
f.close()

class OBanList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="obanlist", description="Получить список людей забаненных с помощью этого бота")
    @commands.has_permissions(ban_members=True)
    async def obanlist(self, interaction: discord.Interaction):
        await interaction.response.defer()

        number = 0
        ban_list = "**Пользователь | Причина**\n"
        async for entry in interaction.guild.bans():
            if entry.reason != None and entry.reason.startswith(ban_reason_prefix + ": "):
                number += 1
                ban_list += str(number) + ". Тег: " + entry.user.name + " | " + entry.reason.replace(ban_reason_prefix + ": ", "") + "\n"
        embed = discord.Embed(description = ban_list)
        await interaction.followup.send(embed=embed)

async def setup(bot): # a extension must have a setup function
	await bot.add_cog(OBanList(bot)) # adding a cog