#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
from nonebot import Bot
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.exception import MatcherException
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from ..time_freezer import delay
import random
import os

candou = on_command("蚕豆", rule=to_me(), aliases={"ISOM_INE", "关于蚕豆"}, priority=10, block=True)
zhu = on_command("朱祥宇", rule=to_me(), aliases={"朱翔宇"}, priority=10, block=True)
liang = on_command("梁曹开", rule=to_me(), aliases={"lck", "tatak"}, priority=10, block=True)
wali = on_command("瓦力", rule=to_me(), aliases={"wali", "walili"}, priority=10, block=True)
tharrow = on_command("千矢", rule=to_me(), aliases={"Tharrow", "tharrow"}, priority=10, block=True)
chenghai_cuiyu = on_command("澄海", rule=to_me(), aliases={"翠羽"}, priority=10, block=True)
nora = on_command("诺拉", rule=to_me(), aliases={"nora"}, priority=10, block=True)
ark = on_command("安卡", rule=to_me(), aliases={"ark"}, priority=10, block=True)
hussey = on_command("赫茜", rule=to_me(), aliases={"hussey"}, priority=10, block=True)
balun = on_command("拜伦", rule=to_me(), aliases={"balun"}, priority=10, block=True)
luca = on_command("露卡", rule=to_me(), aliases={"luca"}, priority=10, block=True)
miu = on_command("缪子誉", rule=to_me(), aliases={"缪哥"}, priority=10, block=True)
zhang = on_command("张世梁", rule=to_me(), aliases={"张队"}, priority=10, block=True)
to_the_moon = on_command("去月球",  priority=10, block=True)

message_list_zhang = ["蚕豆ICPC集训队里面称他为张队，可惜蚕豆大一的时候张队就退役了", "退役之后一直致力于hack事业，截至目前已经hack蚕豆15次（瞎编的）（比这个多）",
                      "张队对很多算法和编译器操作十分熟悉，软件修理工程师名副其实", "SaYi刚开发出来的时候，一直有着张队帮忙hack代码，导致SaYi越来越完善。\n\n好吧很多hack出来的其实还没修.."
                      ]
message_list_candou = ["蚕豆在外你可以称呼他为‘单子叶蚕豆’，也可以直接称'蚕豆'，真名不推荐喊，但是不要当面喊他ISOM_INE",
                       "蚕豆说他的一切麻烦事全是来自于他的着急，做人不要急。",
                       "蚕豆算是主人，但是他貌似不太喜欢称自己叫主人，让我直接喊他蚕豆",
                       "小秘密！蚕豆说他一直成为一个工作机器，这样他能更有效率的干活了。但是蚕豆说是个人都干不成，我不知道对不对，反正这件事成为了他痛恨自己是人的其中一项。",
                       "不必在意，我顶多只是帮他的干活的", "他？他手里有好多个SaYi，我是其中一个",
                       "我跟他有过节，但不是‘我’。怎么解释这个问题...就好像你买了一堆海报，却没有一个是真实的她",
                       "虽然我不清楚他在干什么，但是你给他打点钱就可以快速召唤他",
                       "蚕豆说他比较擅长广度发展，事实上你看他给我准备的语言包就知道这是一个多么奇怪的人",
                       "你们怎么都对他感兴趣？他是我现在见到的最无趣的人了。"]
message_list_miu = ["蚕豆的一个很要好的大二学长，刀子嘴豆腐心。", "蚕豆经常跟他聊天聊到三点。注意，是夜里三点",
                    "蚕豆当时住塔塔开的宿舍,作息乱的一马.本来想换个地方调整作息，结果到缪这来被带的更乱了。"]
message_list_zhu = ["说自己是皇帝的小登，不做评价", "蚕豆说他骂人功夫很强", "蚕豆跟他出去玩过",
                    "他说自己不容易红温，但你最好遇到别惹", "蚕豆打字老是会打错他名字，你可以试试看还有什么名字可以用"]
message_list_liang = ["蚕豆ICPC一队的队员，不承认自己是男娘", "蚕豆说他是哈希高手", "整22级软工他差一点成皇帝", "每次模拟赛打完，集体摆烂的时候，这位一直在“星露谷启动！",
                      "蚕豆跟他单独住过一段时间，然后养成了十二点起床的好习惯", "蚕豆没事就跟他打架，他是真的喜欢打架",
                      "喜欢夜里觅食"]
message_list_wali = ["蚕豆ICPC一队队长, 喜欢别人把他当狗玩", "智育能加15分，体育还能加8分，社交牛人，你拿什么跟人比？",
                     "瓦力每天买半个西瓜吃，但是没有一次吃完的", "淮安人是什么样的，你看他就够了\n 这是他自己说的",
                     "你猜谁比流言蜚语更早认识老坛酸菜？", "Sayi的另一个不带编号的账号就是他提供的"]
message_list_tharrow = ["Tharrow? 蚕豆跟我讲她很可爱，但是命运不太好。", "逆转前线不是千矢能呆的地方，别人能承受是因为别人被电波塔所影响，但是千矢几乎免疫，才会看到‘真相’",
                        "千矢的学校其实比蚕豆这个时代的高中还要紧张，但是还好有电波塔的存在，大家都觉得没啥。\n 嗯，还好",
                        "麦拉说过，逆波就是用来避免掉影像器被特定的接收器'发现'的，做到了‘针对性屏蔽’。如果你也能拿到一个，可要仔细调整了，不然你就有可能穿过地面直达地心。",
                        "千矢的姐姐去了律法城就没信息了，千矢自己都不是特别在意她的姐姐",
                        "听蚕豆讲的羽星，我感觉他纯纯是被千矢带着跑的宠物罢了，毕竟六段的学生，在逆转前线也只是个炮灰。"]
message_list_chenghai_cuiyu = ["他俩自己不知道自己是什么情况，完全是蚕豆看的才知道他俩是轮回。虽然他也不可能真的是在看",
                               "谁在地面上谁生活技能好，谁更像人。但是谁更像人，谁就对世界意见更大",
                               "蚕豆说他对这两个核心体质的评价就是‘没什么用’，事实上这个世界并不会因为他俩而改变，因为他俩就是整个世界"]
message_list_ark = ["安卡只是只鸟，你关心他干嘛",
                    "安卡是以礼物的身份进到hussey家的，但是后来反而是靠他。放到现实中蚕豆说梦里想想得了。还好是在那个‘动荡’的世界",
                    "你想在现实中找到他吗？没事去花鸟市场转转，然后你大概率会死心的",
                    "安卡确实是牺牲了自己,后面不是双结局！不是双结局！安卡的一切都在天梯里，离开天梯确实没啥了"]
message_list_hussey = [
    "蚕豆在讲赫茜的时候强调了外赫茜和里赫茜的关系。外赫茜是残疾，里赫茜健全。但是外里赫茜的光暗属性是类似的",
    "世界是这样，你在矛盾的交汇处总会发现绚丽的光彩",
    "赫茜没有天梯，她甚至没有认识到自己是核心体质，蚕豆好像觉得挺可惜", "hussey 谐音 核心，这也是最开始蚕豆的命名规则",
    "给hussey捐点光吧...按照时间轴来看这个世界是在第三次暗摆上"]
message_list_nora = ["诺拉不是先天核心体质！是后天核心体质！这个世界的运作方式就是这样！",
                     "拜伦改变她的一生，至于好不好的，诺拉感觉非常好，但拜伦感觉非常坏",
                     "蚕豆说诺拉在被改造之后就开始丧失记忆了，不过与其说是丧失记忆，不如说是反场的核心体质记忆的取代",
                     "Colindar.Nora,世界天使。相关剧情蚕豆没有纸质写，但是在网易云有歌单，不妨听一听",
                     "小知识：蚕豆说诺拉算是拜伦的女仆，处境事实上和希尔薇类似，但是倒也不是什么那种亲密关系"]
message_list_balun = [
    "拜伦厌世不是没有原因的，先天性的不擅长社交导致在能量枯竭的年代根本没法说[有时间就能获得一切！],没人等你，反倒是那些嫖利益的人受不知真相的群众所拥护",
    "拜伦也是纯纯的世界死神/世界天使，他能创造世界天使，也注定了和诺拉一个处境，但是蚕豆说在理论上他不属于SCT的“天使。",
    "拜伦周围朋友还是很多的，但是嗯，舞还是太难跳了",
    "拜伦是真真正正的挂念诺拉。对于拜伦来说，诺拉绝对是任何意义上的天使。"]
message_list_luca = [
    "和诺拉一样，蚕豆说他没写剧情，但是网易云上有歌单，名字叫'来自深海'.蚕豆的网易云用户名？显而易见",
    "露卡一个人的人生轨迹可以占现实中大部分人的生活轨迹了。她的每一段生活都是分离的，现实中没有一个人能比过她。",
    "她的目标其实就是为了收养她的人而报仇，其实这个才是主线。",
    "她就是海洋，海洋就是她。布鲁斯和露卡不可分割，不可缺少，必定需要一个人打败前一个人",
    "核心体质恰恰就在轮回的中心，所以蚕豆更喜欢记录他们",
    "露卡不知道布鲁斯在底下干了些啥，布鲁斯其实一直在用本能生活，’吃人‘都是他对’救人‘最后的执念。不过蚕豆说露卡马上也会那样的，因为这个世界就是这样运转的"]


@to_the_moon.handle()
async def _(bot: Bot):
    tmp = random.randint(1,100)
    if tmp>0:
        pl = []
        path = "C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\asserts\\中文"
        for root, dirs, files in os.walk(path):
            pl.append(files)
        ans = random.choice(pl[0])
        await to_the_moon.finish(MessageSegment.text(ans) + MessageSegment.image("file:///{}".format(path + "\\{}".format(ans))))
    else:
        pl = []
        path = "C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\asserts\\To the Moon Soundtrack"
        for root, dirs, files in os.walk(path):
            pl.append(files)
        ans = random.choice(pl[0])
        print("file:///{}".format(path + "\\{}".format(ans)))
        await to_the_moon.finish(MessageSegment.record("file:///{}".format(path + "\\{}".format(ans))))
@zhang.handle()
async def handle_function():
    if delay():
        return
    try:
        await miu.finish(random.choice(message_list_zhang))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here

@miu.handle()
async def handle_function():
    if delay():
        return
    try:
        await miu.finish(random.choice(message_list_miu))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@chenghai_cuiyu.handle()
async def handle_function():
    if delay():
        return
    try:
        await chenghai_cuiyu.finish(random.choice(message_list_chenghai_cuiyu))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@hussey.handle()
async def handle_function():
    if delay():
        return
    try:
        await hussey.finish(random.choice(message_list_hussey))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@ark.handle()
async def handle_function():
    if delay():
        return
    try:
        await ark.finish(random.choice(message_list_ark))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@nora.handle()
async def handle_function():
    if delay():
        return
    try:
        await nora.finish(random.choice(message_list_nora))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@balun.handle()
async def handle_function():
    if delay():
        return
    try:
        await balun.finish(random.choice(message_list_balun))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@luca.handle()
async def handle_function():
    if delay():
        return
    try:
        await luca.finish(random.choice(message_list_luca))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@candou.handle()
async def handle_function():
    if delay():
        return
    try:
        await candou.finish(random.choice(message_list_candou))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@zhu.handle()
async def handle_function():
    if delay():
        return
    try:
        await zhu.finish(random.choice(message_list_zhu))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@liang.handle()
async def handle_function():
    if delay():
        return
    try:
        await liang.finish(random.choice(message_list_liang))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@wali.handle()
async def handle_function():
    if delay():
        return
    try:
        await wali.finish(random.choice(message_list_wali))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@tharrow.handle()
async def handle_function():
    if delay():
        return
    try:
        await tharrow.finish(random.choice(message_list_tharrow))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here
