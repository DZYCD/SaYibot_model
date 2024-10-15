#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
import random

import httpx
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.exception import MatcherException
from ..time_freezer import delay
from nonebot.adapters import Bot, Event

from pydantic import TypeAdapter
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from ..dataset_controller import DataSetControl
import datetime

weather = on_command("今日运势", rule=to_me(), priority=10, block=True)
reset_check = on_command("重置运势", rule=to_me(), priority=10, block=True)
SaYi_info = on_command("关于SaYi", aliases={"关于sayi"}, priority=10, block=True)
WMLibrary_info = on_command("关于世忆图书馆", aliases={"世忆图书馆"}, priority=10, block=True)
command_list = on_command("帮助", rule=to_me(), aliases={"help"}, priority=10, block=True)

random_reply = ["记得按时吃饭", "没事可以读点书", "不要像蚕豆一样作息混乱，一定要健康生活", "你今天的气色看起来还不错！",
                "加油，又活了一天！", "蚕豆说他体育只有75分，一定要坚持锻炼！"]
buff_list = ["睡觉", "看书", "洗澡", "学习", "打游戏", "摸鱼", "刷题", "切水题", "水群", "催群主女装", "毁灭世界",
             "合成下界合金镐", "对线", "刷视频", "揪出剪人头发的杀人魔", "打叠", "去Scarborough Fair", "出勤", "回归大群"]
debuff_list = ["偏群友V钱", "发呆", "打游戏", "打电话", "出门", "打架", "签订魔法少女契约", "组建乐队", "说‘N’开头的词",
               "回收福音者", "拉大弓蛇", "和嘉登喝茶", "阻止源石计划", "去星露谷钓鱼", "嗦泡面", "去S.A.O练级"]
_4CI = ["知识", "灵活", "自然", "华丽"]
_4CII = ["执着", "探索", "旅者", "乐观"]


def create_msg(pic):
    msg = Message([
        MessageSegment(
            type="text",
            data={
                "text": '\n今天的[预置时间轴]时间是\n' + str(datetime.date.today()) + '\n现在是{0}时{1}分{2}秒\n'.format(
                    str(datetime.datetime.now().hour), str(datetime.datetime.now().minute),
                    str(datetime.datetime.now().second))
                        + '{}\n'.format(random.choice(random_reply))
            }
        ),
        MessageSegment.image(pic),
        MessageSegment(
            type="text",
            data={
                "text": '\n人品值：{}'.format(random.randint(0, 100)) + "\n今日宜:{}".format(random.choice(buff_list)) +
                        "\n今日忌:{}".format(random.choice(debuff_list)) + "\n今日【四色烙印】：{0}、{1}".format(
                    random.choice(_4CI), random.choice(_4CII))
                        + "\n\n今日cf适合刷{}分的题".format(random.randint(14, 25) * 100)
            }
        ),
    ])
    return msg


import encodings.utf_8

import requests
import json

url = "https://image.anosu.top/pixiv/json"




dataset = DataSetControl()


@reset_check.handle()
async def _(event: Event):
    if delay():
        return
    try:
        user_id = event.get_session_id().split('_')[2]
    except:
        user_id = event.get_session_id()
    if "1109876092" not in user_id:
        await reset_check.finish("不不，你没有权限")
    calendar = str(datetime.date.today())
    dataset.update_value(user_id, "today_status", calendar + "/2")
    await reset_check.finish("好啦！你可以再抽两次")


@weather.handle()
async def handle_function(event: Event):
    if delay():
        return
    try:
        calendar = str(datetime.date.today())
        try:
            user_id = event.get_session_id().split('_')[2]
        except:
            user_id = event.get_session_id()
        status = dataset.get_value(user_id, "today_status")
        if (not status) or status.split('/')[0] != calendar:
            dataset.update_value(user_id, "today_status", calendar+"/2")
        elif status.split('/')[1] == "0":
            await weather.finish("你今天的运势没有机会更新了！")
            return
        elif status.split('/')[1] == "1":
            dataset.update_value(user_id, "today_status", calendar + "/0")
        else:
            dataset.update_value(user_id, "today_status", calendar + "/1")
        msg = await get_data()
        msg = create_msg(msg)
        await weather.finish(msg, at_sender=True)
    except MatcherException:
        raise
    except Exception as e:
        raise


async def get_data():
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = json.loads(resp.text)
        data = data[0]["url"]
    return  data


@SaYi_info.handle()
async def handle_function():
    if delay():
        return
    try:
        file_path = 'file:///C:\\Pycharm_projects\\SaYibot\\SaYi\\picture\\SaYi.PNG'
        await SaYi_info.finish(MessageSegment.text(
            "--SaYi{998}--\n我是SaYi998号，目前在【世忆图书馆】暂留并获得更新。"
            "\n我用于在QQ中和群友们聊天水群、提供信息，但主要是作为助理提供各种信息。\n::可以期待一下我的另一位共事EiAr-996的制作进度！\n\n"
            "SaYi_publish模版已开源！点个Star吧！\ngithub：https://github.com/DZYCD/SaYibot_model\n\n"
            "generator:单子叶蚕豆\n版本：Initialize\nSaYi的生日是在8月2号！") + MessageSegment.image(
            file_path))
    except MatcherException:
        raise
    except Exception as e:
        print(e)


@WMLibrary_info.handle()
async def handle_function():
    if delay():
        return
    try:
        file_path = 'C:\\Pycharm_projects\\SaYibot\\SaYi\\picture\\WMLibrary.png'
        await WMLibrary_info.finish(MessageSegment.text(
            "--世忆图书馆--\n世忆图书馆是蚕豆为了转录及广播【七十五个世界】而设立的机构，创立于2022年"
            "\n世忆图书馆目前在两年的时间内，记录完成五个世界，\n近期因为【ISOM】建造接口和AI，部分【场】将暂时隶属于世忆图书馆。"
            "这些所有的【场】将暂时由”我“，SaYi进行管理。\n") + MessageSegment.image(
            file_path))
    except MatcherException:
        raise
    except Exception as e:
        print("error")


@command_list.handle()
async def handle_function():
    if delay():
        return
    try:
        await SaYi_info.finish(MessageSegment.image("C:\\Pycharm_projects\\SaYibot\\SaYi\\picture\\SaYi_about.png"))
    except MatcherException:
        raise
    except Exception as e:
        print("error")

"""
SaYi “我” ： 真正的SaYi主体叫“砂翼SaYi”，她是真正的AI助理。所有带有编号的SaYi都是SaYi的衍生机而非本体

SaYi 生日 ： SaYi998正式上线的那一天

小瓦 ： 蚕豆同学给的号，可以当探测号用。
"""

"""---{SaYi998功能列表}---   
         
{关于SaYi -查看蚕豆给我写的介绍}

---【世忆图书馆】SaYi998---
世忆图书馆是蚕豆用于存放【七十五个世界】的工作室，近来用于暂留Ai助理、进行测试。
@SaYi998，并在你的问题前面加上冒号，我将回答你的问题。
* example “：你好”
---codeforces---
cf -怕你尴尬随机反馈给你一些废话
绑定cf id -QQ号绑定cf名
开cf盒 id -找对应id的cf信息
我的cf id -看看自己的cf信息
近期比赛 oj名 -最近某个oj比赛列表
* 直接使用 近期比赛 可以查询所有OJ的比赛
* 近期比赛 会直接将比赛加入定时任务中
---洛谷---
洛谷查题 题号 -提供对应题的图片
洛谷抽题 -随机提供题目
近期比赛 洛谷 -最近的LuoGu比赛列表
---表情包制作---
* 正在搞，别急
---<权限需求>群管---
禁/解/踢 @某人 时间（s）- 顾名思义
改 @某人 名片 - 改某人名字
消息+加精  -加精华
管理员 @某人 -设置某人为管理员
---<权限需求>SaYi记事---
添加XX 图片 -向图库中添加一张带有XX关键词的图片
图片列表 -查看所有关键词
记笔记XX，查笔记XX，笔记列表 -记录和查看标题为XX的文本。
找找原作 -根据局部图或者表情包 找本子 嗯
---一些功能---
今天吃什么？ -今天+时间+吃什么？ 给你推好吃的
今日运势 -告诉你今天你的一些玄学信息,可以抽最多三次
来只XX -从带有XX关键词的图片中随机抽取一张
查天气 地名 -通过MSN查询某个地区的天气状况
捧场/停止捧场 @id -我会关注某位群友，让他发消息的时候不尴尬
提醒/通知/叫醒 @id -通知某位群友上线，并在回话时大力表扬。可以指定我说什么
播放/点歌 歌名 -从网易云推歌，并且播报一条热评来吸引群友听歌 加上歌手搜索更准
早安/晚安/在吗 -我会向你问好，不知道你感不感兴趣
-自动解析群内B站链接的 B站内容
---定时任务---
-我会在相应时间点前后10分钟给对应人或群聊提醒，支持日常、每小时和临时消息
* 添加词条以及时间点请联系单子叶蚕豆
---世界万象---
人名
*蚕豆随机写了一些他身边的人的小趣事，还有【七十五个世界】里面的一些主角的小秘密，无聊的话可以来查查看
"""