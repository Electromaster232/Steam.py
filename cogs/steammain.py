import discord
from discord.ext import commands
import requests

class Steammain:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, vanityurl):
        """Get information on a user (requires VanityURl)"""

        message = await self.bot.say("Getting Information...")
        # Convert VanityURL to SteamID64
        response = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FF0EEF99E5BD63F29FC0F938A56F115C&vanityurl=" + vanityurl)
        resjson = response.json()
        if resjson['response']['success'] != 1:
            await self.bot.say("There was an error contacting the Steam API (Converting URL to SteamID64). Error Message: " + resjson['response']['message'])
            return
        steamid = resjson['response']['steamid']
        # Get player Info
        userinfo = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=FF0EEF99E5BD63F29FC0F938A56F115C&steamids=" + steamid)
        userjson = userinfo.json()
        userjson = userjson['response']['players'][0]

        try:
            realname = userjson['realname']
        except KeyError:
            realname = "None Set"
        # Print Embed
        embed = discord.Embed(title="Steam User Information", url=userjson['profileurl'],
                              description="Information on Requested User (SteamID) " + userjson['steamid'], color=0x1ea632)
        embed.set_thumbnail(url=userjson['avatarfull'])
        embed.add_field(name="Username:", value = userjson['personaname'], inline=True)
        embed.add_field(name="Real Name:", value = realname, inline = True)
        embed.add_field(name="Primary Group ID:", value = userjson['primaryclanid'], inline = False)
        await self.bot.edit_message(message, new_content=None, embed=embed)


def setup(bot):
    bot.add_cog(Steammain(bot))
