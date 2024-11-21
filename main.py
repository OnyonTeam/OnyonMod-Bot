import discord, json, os, asyncio, nest_asyncio
from discord.ext import commands
nest_asyncio.apply()

f = open('config.json')
data = json.load(f)
bot_token = data['bot_token']
bot_prefix = data['bot_prefix']
discord_bot_access_role_id = data['discord_bot_access_role_id']
f.close()

f = open("botstatus.txt")
bot_status = f.readline()
f.close()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(
        name = bot_status,
        type = discord.ActivityType.listening
    ))
    try:
        synced = await bot.tree.sync()
        print(f"Синхронизирован(а/о) {len(synced)} команд(а)")
    except Exception as e:
        print(e)
    print('Бот запущен! ' + str(bot.user))

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'cogs.{filename[:-3]} загружен.')
        elif filename != "__pycache__":
            print(f'Ошибка при загрузке ' + filename)
    print('Все коги были загружены')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        error_msg = 'Команда не найдена'
    elif isinstance(error, commands.errors.CheckFailure):
        error_msg = 'Недостаточно прав'
    elif isinstance(error, commands.errors.UserInputError):
        error_msg = 'Неправильное использование'
    else:
        raise error
    embed = discord.Embed(
        title = error_msg
    )
    #await ctx.send(embed=embed)

# command to reload cogs
@bot.tree.command(name='reload', description='Перезагрузить бота (Только Onyon)')
@commands.has_role(discord_bot_access_role_id)
async def reload(interaction: discord.Interaction):
    await interaction.response.defer();

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.reload_extension(f'cogs.{filename[:-3]}')
            print(f'cogs.{filename[:-3]} перезагружен.')
        elif filename != "__pycache__":
            print(f'Ошибка при перезагрузке ' + filename)
    try:
        synced = await bot.tree.sync()
        print(f"Синхронизирован(а/о) {len(synced)} команд(а)")
    except Exception as e:
        print(e)
    embed = discord.Embed(
        title = 'Бот успешно перезагружен!'
    )
    await interaction.followup.send(embed=embed)

async def main():
  async with bot:
    await load_extensions()
    await bot.run(bot_token) # runs the bot.

# run main()
asyncio.run(main())