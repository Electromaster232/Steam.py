import aiohttp


class Utils:

    def vanitytosteamid(vanityurl):
        """Convert a vanity url to SteamID64"""

        async with aiohttp.get(
            "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FF0EEF99E5BD63F29FC0F938A56F115C&vanityurl=" + vanityurl) as r:
            resjson = r.json()
        if resjson['response']['success'] != 1:
            return False
        return resjson['response']['steamid']

    def gametoid(gamename):
        """Convert a game name to its ID"""

        async with aiohttp.get("http://api.steampowered.com/ISteamApps/GetAppList/v2") as r:
            response = r.json()
        response = response['applist']['apps']
        try:
            gameid = next((item for item in response if item["name"] == gamename))
        except StopIteration:
            return False
        gameid = gameid['appid']
        return gameid

    def idtogame(gameid):
        """Convert game ID to game name"""

        async with aiohttp.get("http://api.steampowered.com/ISteamApps/GetAppList/v2") as r:
            response = r.json()
        response = response['applist']['apps']
        try:
            gamename = next((item for item in response if item["appid"] == gameid))
        except StopIteration:
            return False
        gamename = gamename['name']
        return gamename

    def setup(self):
        pass
