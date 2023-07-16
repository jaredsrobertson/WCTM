import json

import asyncio
import aiohttp
from dotenv import dotenv_values

config = dotenv_values('.env')

async def get_steam_id(discord_id):
    file = './steam_ids.json'
    with open(file, 'r') as f:
        steam_ids_dict = json.load(f)
    if str(discord_id) in steam_ids_dict.keys():
        result = steam_ids_dict[discord_id]
    else:
        async with aiohttp.ClientSession() as session:
            headers = {'authorization' : config['discord_api_token']}
            url = f'https://discord.com/api/v9/users/{discord_id}/profile'
            #response = requests.get(url, headers=headers)
            async with session.get(url, headers=headers) as response:
                data = response.json()
                steam_id_check = next((x for x in data['connected_accounts'] if x.get('type') == 'steam'), dict()).get('id')
                if steam_id_check:
                    data = {discord_id : steam_id_check}
                    steam_ids_dict.update(data)
                    with open(file, 'w') as f:
                        json.dump(steam_ids_dict, f)
                    result = steam_id_check
                else:
                    result = False
    return result

async def get_owned_games(steam_ids):
    for steam_id in steam_ids:
        async with aiohttp.ClientSession() as session:
            steaminfo = {'include_appinfo': '1'}
            url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={config['steam_key']}&steamid={steam_id}"
            async with session.get(url, params=steaminfo) as response:
                data = await response.json()
        games_appid_dict, appids_match_list = await get_shared_games(data)
        match_list = await get_mp_games(appids_match_list, games_appid_dict)
    return match_list

async def get_shared_games(data):
    games_data = data['response']['games']
    games_appid_dict = {}
    data_lists = []
    #for games in games_data:
        #games_appid_dict[games['name']] = games['appid']
        #data_list = [k['appid'] for k in games_data]
        #data_lists.append(data_list)
    #num_lists = len(data_lists)
    #appids_match_list = set(data_lists[0])
    #for i in range(1, num_lists):
        #appids_match_list = appids_match_list.intersection(set(data_lists[i]))
    games_appid_dict = {games['name']: games['appid'] for games in games_data}
    data_lists = [[k['appid'] for k in games_data] for _ in range(len(games_data))]
    appids_match_list = set(data_lists[0]).intersection(*data_lists[1:])
    return games_appid_dict, appids_match_list

async def get_mp_games(appids_match_list, games_appid_dict):
    mp_appids_list = []
    async with aiohttp.ClientSession() as session:
        #counter = 0
        tasks = []
        for appid in appids_match_list:
            url = f"https://store.steampowered.com/api/appdetails/?appids={appid}&filters=categories"
            #async with session.get(url) as response:
            tasks.append(session.get(url))
        responses = await asyncio.gather(*tasks)
        for response in responses:
                #mp_data = await response.text()
                data = await response.json()
                appid = list(data.keys())[0]
                categories = data[appid]['data'].get('categories', [])
                #if 'Multi-player' in mp_data:
                if any(category['description'] == 'Multi-player' for category in categories):             
                    mp_appids_list.append(appid)
                    #counter += 1
    match_list = [v for v, k in games_appid_dict.items() if k in appids_match_list]
    #match_list = sorted(match_list, key=str.lower)
    match_list.sort(key=str.lower)
    return match_list
