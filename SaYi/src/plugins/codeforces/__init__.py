from nonebot.rule import to_me
from nonebot.plugin import on_command

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.rule import is_type

from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.exception import MatcherException
from nonebot.params import CommandArg
import random
import time
from nonebot.adapters import Bot, Event
from ..dataset_controller import DataSetControl
from ..time_freezer import delay
from .data_source import webshot, webcheck, get_contest_list, get_user_info

group_rule = is_type(GroupMessageEvent)
cf = on_command("cf", aliases={"codeforces"}, priority=10, block=True)
cf_bind = on_command("cf绑定", rule=to_me(), aliases={"cfbind", "绑定cf"}, priority=10, block=True)
cf_check = on_command("我的cf", rule=to_me(), aliases={"mycf"}, priority=10, block=True)
cf_check_others = on_command("查cf", rule=to_me(), aliases={"开cf盒"}, priority=10, block=True)
cf_contest_info = on_command("cf击杀榜", aliases={"hack统计"}, priority=10, block=True)
message_list = ["启动了？", "可以挑战今天上50分", "可以挑战今天掉50分", "启动！", "今晚又是一个不眠之夜...",
                "期望听到你的好消息", "期望听到你的坏消息", "随时准备hack！", "今天挑战一下超越jiangly", "D题盲猜1900分"]
dataset_control = DataSetControl()


@cf_contest_info.handle()
async def _():
    if delay():
        return
    try:

        await cf.finish(random.choice(message_list))
    except MatcherException:
        raise
    except Exception as e:
        print("error")
        pass


@cf.handle()
async def handle_function():
    if delay():
        return
    try:
        await cf.finish(random.choice(message_list))
    except MatcherException:
        raise
    except Exception as e:
        print("error")
        pass


image_id = 'C:\\Users\\DZYCD\\PycharmProjects\\SaYibot\\SaYi\\src\\plugins\\codeforces\\codeforces_user.png'


@cf_bind.handle()
async def handle_function(event: Event, args: Message = CommandArg()):
    if delay():
        return
    try:
        name = str(args.extract_plain_text())
        user_check = get_user_info(name)
        if not user_check:
            await cf_bind.finish("你的cf用户名貌似有问题")
        else:
            try:
                effector_id = event.get_session_id().split('_')[2]
            except:
                effector_id = event.get_session_id()
            dataset_control.update_value(effector_id, "cf_bind", name)
            await cf_bind.finish(MessageSegment.text("绑定成功"))
    except MatcherException:
        raise
    except:
        await cf_bind.finish("绑定账号是？")


@cf_check.handle()
async def handle_function(event: Event):
    if delay():
        return
    try:
        name = event.get_session_id()
        name = dataset_control.get_value(name, "cf_bind")
        if not name:
            await cf_bind.finish(MessageSegment.text("你貌似还没有绑定账号呢，使用’cf绑定 xxx'来绑定账号!"))
        user = get_user_info(name)
        if not user:
            await cf_bind.finish("error:发生了未知错误")
        msg = MessageSegment.text(">>>{}个人信息\n".format(user["handle"]))
        msg += MessageSegment.text("注册时间:{0}\n上次在线时间:{1}\nranting: {2}[{3}]>>>MAX: {4}[{5}]\n加了{6}位好友\n社区贡献度:[{7}]\n"
                                   .format(user["registrationTimeSeconds"], user["lastOnlineTimeSeconds"], user["rating"], user["rank"], user["maxRating"], user["maxRank"], user["friendOfCount"], user["contribution"]))
        msg += MessageSegment.image(user["titlePhoto"])
        await cf_bind.finish(msg)
    except MatcherException:
        raise
    except:
        await cf_bind.finish("error:发生了未知错误")


@cf_check_others.handle()
async def handle_function(event: Event, args: Message = CommandArg()):
    if delay():
        return
    try:
        t = time.time()
        name = str(args)
        if not name:
            await cf_bind.finish(MessageSegment.text("？你要查谁"))
        webshot(name, image_id)
        im_id = 'file:///{}'.format(image_id)
        await cf_bind.finish(
            MessageSegment.image(im_id) + MessageSegment.text("花费：{:.2f}秒".format(float(time.time() - t))))
    except MatcherException:
        raise
    except:
        await cf_bind.finish("貌似没找到")



