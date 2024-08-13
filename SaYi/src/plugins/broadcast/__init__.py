from nonebot import on_command, require, get_bots
from nonebot.adapters.cqhttp import MessageSegment
import os
from random import randint, choice
from ..time_freezer import scheduler
from ..dataset_controller import DataSetControl
from ..web_processor import webshot
import time
import datetime

__plugin_name__ = 'timing'
__plugin_usage__ = '用法：在规定时间触发发送的信息。'

img_path = 'file:///' + os.path.split(os.path.realpath(__file__))[0] + '/img/'


# 发送图片时用到的函数, 返回发送图片所用的编码字符串
def send_img(img_name):
    global img_path
    return MessageSegment.image(img_path + img_name)


async def say_about_contests(info):
    bot, = get_bots().values()
    path = "E:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\codeforces\\codeforces_main.png"
    webshot(info[3], path)
    path = "file:///" + path
    # 发送一条私聊信息
    await bot.send_msg(
        message_type="group",
        # user_id , "private
        group_id=455953679,
        message=MessageSegment.text('下一场{0}比赛:\n[{1}]\n马上就要开始了!\nlink:[{2}]'.format(info[1].split("_contest_annotation")[0], info[2], info[3]))+
                MessageSegment.image(path)
    )


async def say_to_target(info, user):
    bot, = get_bots().values()
    for target in user:
        time.sleep(1)
        rule, user_id = target.split('_')
        if rule == "private":
            await bot.send_msg(
                message_type="private",
                # 私聊用户QQ号
                user_id=user_id,
                message=info
            )
        else:
            await bot.send_msg(
                message_type="group",
                # 私聊用户QQ号
                group_id=user_id,
                message=info
            )

job_path = "E:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\job_list.json"
dataset = DataSetControl(job_path)
greetings = [["一日之计在于晨，有多少群友起床了?", "早上吃一个面包，楼下有卖包子的来个纯肉包好了", "这个时间点可能是大部分群友的回笼觉时间",
              "醒来的同学看一眼,今天有没有早八？", "你不起大爷大妈都起了，应该庆幸楼下没有广场舞的声音", "让我看看有多少群友醒过来了?"],
             ["下午适合睡个午觉，有条件的可以躺下了", "打瞌睡的可以补一杯咖啡！蚕豆天天只喝拿铁", "要来开个茶话会吗?",
              "按理说现在是最困的时候，蚕豆说他推荐睡午觉"],
             ["睡前不要听特别燥的音乐，不过如果你是硬核爱好者，当我没说", "小朋友请睡觉，大朋友请随便", "仰望星空，思考人生。你对未来的打算...是什么?",
              "忙碌了一天，可以去阳台看看夜空。", "睡前回顾一下一天的时光，今天学到了什么?有没有什么进步?是不是又摸鱼了?"],
             ["大伙都知道，CFK的大鸡腿饭 非常好吃（爱来自塔塔开）", "不舒服就去喝粥，开心了就去吃烧烤，没啥想法就去美团转转。一直以来都是这样。",
              "想吃点啥？可以对我问‘今天晚上吃什么’哦", "机房里的同志、在宿舍里的同志、可能还有在外出差的同志们，出去吃饭吧", "猜猜现在几点？今天打算吃啥？",
              "我有个建议！吃点焖锅怎么样？不然来份地锅鸡！", "虽然不知道你上一顿是几点解决的，但是这个点...多少吃一点吧。"]]


def update_daily_inform(i):
    if "早上好!" in i[2]:
        i[2] = "早上好!今天是{0}\n{1}".format(datetime.date.fromtimestamp(i[0]), choice(greetings[0]))
    if "下午好!" in i[2]:
        i[2] = "下午好!现在是下午一点\n{0}".format(choice(greetings[1]))
    if "晚上好!" in i[2]:
        i[2] = "晚上好!现在是晚上十一点\n{0}".format(choice(greetings[2]))
    if "晚饭时间!" in i[2]:
        i[2] = "晚饭时间!\n{0}".format(choice(greetings[3]))
    return i


async def search_job():
    times = int(time.time())+600
    print("[定时任务检查]>>>\nfrom", times-600, "to", times, "seconds, search about the job from {}".format(job_path))
    cnt = 0
    job_list = dataset.get_value("result", "job_list")

    for i in job_list:
        if times > i[0] > times-600:
            cnt += 1
            time.sleep(1)
            if "contest_annotation" in i[1]:  # cf事件
                await say_about_contests(i)
            if i[1] == "daily_round":
                await say_to_target(i[2], i[3:])
            if i[1] == "template":
                await say_to_target(i[2], i[3:])

    new_job_list = []
    for i in job_list:
        if times < i[0]:
            new_job_list.append(i)
        if times > i[0]:
            if i[1] == "daily_round":  # 每日循环事件
                i[0] += 60 * 60 * 24
                i = update_daily_inform(i)
                new_job_list.append(i)
            elif i[1] == "hours_round":  # 每小时循环事件
                i[0] += 60 * 60
                new_job_list.append(i)

    dataset.update_value("result", "job_list", new_job_list)
    dataset.update_value("result", "job_count", len(new_job_list))
    print("定时任务检查完毕, 执行了{}个事件".format(cnt))


# 设置一个定时器
timing = scheduler


@timing.scheduled_job("interval", minutes=5, id="check_board")
async def see_in_list():
    await search_job()
