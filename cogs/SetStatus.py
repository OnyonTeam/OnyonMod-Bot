import discord
from discord import app_commands
from discord.ext import commands
import json

f = open('config.json')
data = json.load(f)
discord_bot_access_role_id = data['discord_bot_access_role_id']
f.close()

class SetStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='setstatus', description='Установить статус бота (Только Onyon)')
    @commands.has_role(discord_bot_access_role_id)
    async def setstatus(self, interaction: discord.Interaction, status_name: str):
        await interaction.response.defer();

        await self.bot.change_presence(status=discord.Status.online,
                                 activity=discord.Game(name=status_name, type=discord.ActivityType.listening))

        f = open("botstatus.txt", "w")
        f.write(status_name)
        f.close()

        embed = discord.Embed(title = 'Статус бота изменён на ' + status_name)
        await interaction.followup.send(embed=embed)
    
async def setup(bot): # a extension must have a setup function
	await bot.add_cog(SetStatus(bot)) # adding a cog