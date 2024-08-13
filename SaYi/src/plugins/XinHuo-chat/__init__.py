from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.exception import MatcherException

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = 'bdf37372'
SPARKAI_API_SECRET = 'NGFkYTBmYWQxMDM0MGUxZWE0ZjlkZjdi'
SPARKAI_API_KEY = 'd0d90bd21e1eb0ad2c116928e38ad72b'
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'


msg = on_command(":", aliases={"："}, rule=to_me(), priority=30, block=True)

spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )


@msg.handle()
async def _(event: Event, args: Message = CommandArg()):
    text = args.extract_plain_text()
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
        user = "访客"
    text = "作为【世忆图书馆】司书兼助理SaYi_998号，你的职责是帮助查询任何知识。" \
           "你的主人叫单子叶蚕豆。我是" + user + ",请你用平等，客观，保护自己尊严的前提下用最多三句话回答:" + text
    messages = [ChatMessage(
            role="user",
            content=text
        )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    p = a.dict()
    token_count = p["llm_output"]["token_usage"]
    print("token_decrease : {0}({1}/{2} + {3})".format(token_count["total_tokens"], token_count["question_tokens"],
                                                       token_count["prompt_tokens"], token_count["completion_tokens"]))
    p = p["generations"][0][0]["text"]
    await msg.finish(p)
