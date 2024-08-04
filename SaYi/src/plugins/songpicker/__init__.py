import random

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot import on_command
from ..time_freezer import delay
from .data_source import DataGet, DataProcess

songpicker = on_command("点歌", aliases={"播放", "歌曲", "查歌"}, priority=9)

dataGet = DataGet()


@songpicker.handle()
async def _(state: T_State, args: Message = CommandArg()):
    if delay():
        return
    song_name = args.extract_plain_text()
    if len(song_name) < 1:
        await songpicker.reject("歌名?")
    song_ids = await dataGet.song_ids(song_name=song_name)
    song_com = await dataGet.song_comments(song_id=song_ids[0])
    if not song_ids:
        await songpicker.finish("这曲子貌似不在曲库中，你最好去网易云看一眼")
    else:
        await songpicker.send(MessageSegment.music("163", int(song_ids[0])))
        await songpicker.finish(MessageSegment.text(str(song_com[random.randint(0, 4)])))

