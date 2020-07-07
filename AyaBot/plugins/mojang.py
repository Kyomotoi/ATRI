import json
import base64
import nonebot
import requests
from mcstatus import MinecraftServer
from nonebot import on_command, CommandSession


@on_command('mc_server_status', aliases=['服务器状态查询'], only_to_me=False)
async def _(session: CommandSession):
    ip = session.current_arg.strip()
    if not ip:
        ip = session.get('server', prompt='请告诉吾辈服务器ip，或输入服务器名(如需添加请联系作者)')

    if ip == '南外手艺':
        ip = str('mc.nflsedition.com:26164')

    elif ip == 'hypixel':
        ip = str('mc.hypixel.net')
        
    elif ip == 'shotbow':
        ip = str('us.shotbow.net')

    elif ip == 'potterworld':
        ip = str('potterworldmc.com')
    
    else:
        pass

    server = MinecraftServer.lookup(ip)
    status = server.status()
    await session.send(f'IP:{ip}\nPlayers: {0}\nms: {1}'.format(status.players.online, status.latency))


@on_command('check_mc_id', aliases=['mc正版查询', 'MC正版查询'], only_to_me=False)
async def check_mc_id(session: CommandSession):
    player = session.current_arg.strip()
    if not player:
        player = session.get('player', prompt='请告诉吾辈需要查询的id')
    
    url = f'https://api.mojang.com/users/profiles/minecraft/{player}'
    print(url)

    try:
        response = requests.request("GET", url)

        try:
            html = response.text
            ms = json.loads(html)

            name = ms["name"]
            uuid = ms["id"]

            await session.send(f'status: success!\nPlayer: {name}\nuuid: {uuid}\nNamemc: https://mine.ly/{name}.1')

        except:
            await session.send(f'{player}可能为非正版玩家，无法查询到其信息')

    except:
        await session.send('mojang似乎炸了...等一会吧')