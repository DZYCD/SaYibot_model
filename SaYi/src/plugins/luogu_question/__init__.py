from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot import on_command
from nonebot.exception import MatcherException
from ..time_freezer import delay
import random
import time

from .data_source import webshot

ques_picker = on_command("洛谷查题", aliases={"洛谷搜题"}, priority=10, block=True)
random_picker = on_command("洛谷抽题", priority=10, block=True)
image_id = 'E:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\luogu_question\\image.png'


@ques_picker.handle()
async def _(args: Message = CommandArg()):
    if delay():
        return
    try:
        qus_id = str(args.extract_plain_text())
        t = time.time()
        webshot(qus_id, image_id)
        im_id = 'file:///{}'.format(image_id)
        await ques_picker.finish(MessageSegment.image(im_id) +
                                 MessageSegment.text("花费：{:.2f}秒".format(float(time.time() - t))))
    except MatcherException:
        raise
    except:
        await ques_picker.finish("没有查到对应的题")


@random_picker.handle()
async def _():
    if delay():
        return
    try:
        qus_id = 'P' + str(random.randint(1001, 10080))
        t = time.time()
        webshot(qus_id, image_id)
        im_id = 'file:///{}'.format(image_id)
        await ques_picker.finish(MessageSegment.image(im_id) + MessageSegment.text(
            "来做做这题! 花费：{:.2f}秒".format(float(time.time() - t))))
    except MatcherException:
        raise
    except:
        await ques_picker.finish("貌似抽到了一片虚无...")
