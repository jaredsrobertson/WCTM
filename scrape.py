import requests
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import constants


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless=new')
driver = webdriver.Chrome(options=chrome_options)


async def get_owned_games(steam_ids):
    steam_key = constants.steam_key
    steaminfo = {'include_appinfo': '1'}

    for steam_id in steam_ids:
        url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_key}&steamid={steam_id}'
        response = requests.get(url, params=steaminfo)

        data = response.json()
        games_data = data['response']['games']
        games_appid_dict = {}

        for games in games_data:
            games_appid_dict[games['name']] = games['appid']

            data_list = [k['appid'] for k in games_data]

            if steam_id == "76561198037294606":
                window = data_list
            elif steam_id == "76561198413196075":
                sharp = data_list
            elif steam_id == "76561198114679719":
                rocky = data_list
            elif steam_id == "76561198119027474":
                richy = data_list

    return await match_games(window, sharp, rocky, richy, games_appid_dict)

async def match_games (window, sharp, rocky, richy, games_appid_dict):
    appids_match_list = list(set(window) & set(sharp) & set(rocky) & set(richy))
    return await get_games(appids_match_list, games_appid_dict)


async def get_games(appids_match_list, games_appid_dict):
    async with aiohttp.ClientSession() as session:
        mp_appids_list = []
        counter = 0
        for appid in appids_match_list:
            url = f"https://store.steampowered.com/api/appdetails/?appids={appid}&filters=categories"
            async with session.get(url) as response:
                mp_data = await response.text()
                if 'Multi-player' in mp_data:

                    mp_appids_list.append(appid)
                    counter += 1

    match_list = [v for v, k in games_appid_dict.items() if k in appids_match_list]
    match_list = sorted(match_list, key=str.lower)
    #print(games_appid_dict.items())


    return match_list
