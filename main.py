from discord.ext import commands
import discord
import logging
import asyncio

description = '''Steam.py Alpha v0.1'''
# Set logging level
logging.basicConfig(level=logging.ERROR)

# this specifies what extensions to load when the bot starts up
startup_extensions = []

# Create the bot object
bot = commands.Bot(command_prefix=['steam.'], description=description)


@bot.event
async def on_ready():
    print("© 2017 Electromaster232")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('READY')


@bot.command()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("The extension {} was loaded.".format(extension_name))


@bot.command()
async def unload(extension_name: str):
    """Unloads an extension."""
    try:
        bot.unload_extension("cogs.{}".format(extension_name))
    except:
        await bot.say("There was an error")
    await bot.say("The extension {} was unloaded.".format(extension_name))


@bot.command()
async def reload(extension_name: str):
    """Reloads an extension"""
    bot.unload_extension("cogs.{}".format(extension_name))
    bot.load_extension("cogs.{}".format(extension_name))
    bot.say("The extension {} was reloaded.".format(extension_name))


@bot.command()
async def ping():
    """Simple Ping Command"""
    em = discord.Embed(description="Pong!", color=discord.Color.blue())
    await bot.say(embed=em)


@bot.command()
async def owner():
    """Tells you who the bot owner is"""
    owner = str((await bot.application_info()).owner)
    em = discord.Embed(description=owner, color=discord.Color.green())
    await bot.say(embed=em)


# TODO: Make this less hacky
@bot.command(pass_context=True)
async def debug(ctx, *, code):

    if ctx.message.author.id == "133353440385433600":
        global_vars = globals().copy()
        global_vars['bot'] = bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.message.author
        global_vars['channel'] = ctx.message.channel
        global_vars['server'] = ctx.message.server

        try:
            result = eval(code, global_vars, locals())
            if asyncio.iscoroutine(result):
                result = await result
            result = str(result)
            await bot.say("```" + result + "```")
        except Exception as error:
            await bot.say('```{}: {}```'.format(type(error).__name__, str(error)))
            return
    else:
        await bot.say(":no_entry: Access to this command is restricted.")

# Load extensions and start the bot
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
# Run the bot object with token
    bot.run('NDIxNDgwMzM3NDk1OTQ5MzM1.DYSo2g.yg7elym4vZV0vlIVn-cEnZMENDs')
