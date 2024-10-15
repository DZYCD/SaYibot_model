#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

from nonebot import logger
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot_plugin_userinfo import get_user_info
from nonebot.rule import to_me
from nonebot.plugin import on_command, on_message
from nonebot.exception import MatcherException

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = 
SPARKAI_API_SECRET = 
SPARKAI_API_KEY = 
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'


msg = on_message(rule=to_me(), priority=60, block=True)

spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )




@msg.handle()
async def handle_add_hall(bot: Bot, event: Event):
    text = event.get_plaintext()
    text = text.strip()

    if len(text) <= 1:
        await msg.finish("SaYi在，有什么需要问的？")
    id_ = event.get_session_id()
    try:
        id_ = id_.split('_')[2]
    except:
        pass
    if id_ == '1109876092':
        user = "单子叶蚕豆"
    else:
        user = await get_user_info(bot, event, event.get_user_id())
        user = str(user).split("user_name='")[1]
        user = str(user).split("'")[0]
    print(str(user))
    text = ("作为【世忆图书馆】司书兼助理SaYi_998号，你的职责是帮助查询任何知识。你的主人叫单子叶蚕豆。我是" + user +
            "。请你用平等，客观，保护自己尊严的前提下对下列语句用最多三句话、至多200字回答。"
                                "我的语句为:" + text)
    messages = [ChatMessage(
            role="user",
            content=text
        )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    p = a.dict()
    token_count = p["llm_output"]["token_usage"]
    logger.info("来源{0}：{1}".format(id_, text))
    logger.warning("Token Decrease : {0}({1}/{2} + {3})".format(token_count["total_tokens"], token_count["question_tokens"],
                                                       token_count["prompt_tokens"], token_count["completion_tokens"]))
    p = p["generations"][0][0]["text"]
    await msg.finish(p)


"""
[默认省略协议：Process{Function} dos equal ({result{text}} to {result{ValueName}}]
作为【世忆图书馆】司书兼助理SaYi_998号，你的职责是帮助查询任何知识。你的主人叫单子叶蚕豆。
我是 user.接下来你只需要正常对话，但如果用户的需求符合下列情况之一，仅将::后面的内容解析后替换并删除‘::’，输出对应的命令行，不要掺杂任何东西：
1.播放乐曲：“[TTL]SaYi dos MusicModule{::用户提供的乐曲名}",
2.打招呼: "[TTL]SaYi dos GreetingModule{::指向的人名，若没有使用我的用户名}"，
3.给某个人捧场 : "[TTL]SaYi dos FocusModule{::输入的id}",
4.其他 ："[TTL]SaYi dos ChatModule{::输入内容}"
"""