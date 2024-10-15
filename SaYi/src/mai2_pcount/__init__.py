#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
from nonebot import on_command, on_endswith, on_regex, require
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, Message, MessageEvent
from nonebot.typing import T_State
from nonebot.params import CommandArg, Endswith, RegexMatched
from nonebot.permission import SUPERUSER

require("nonebot_plugin_localstore")

import json
from datetime import datetime
import nonebot_plugin_localstore as store


# 获取插件数据目录
def get_data_file(group_id):
    return store.get_data_file("mai2_pcount", f"{group_id}.json")


# 读取写入数据通用
def load_data(group_id):
    data_file = get_data_file(group_id)
    if data_file.exists():
        return json.loads(data_file.read_text(encoding='utf-8'))
    return {"enabled": False}


def save_data(group_id, data):
    data_file = get_data_file(group_id)
    data_file.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding='utf-8')


# 插件开关状态检查
def is_plugin_enabled(data):
    return data.get("enabled", False)


# 开启插件功能
pcount_on = on_command(
    "pcount on",
    aliases={"开启pcount", "开启pcount插件"},
    priority=90,
    permission=SUPERUSER,
    block=True
)


@pcount_on.handle()
async def handle_pcount_on(bot: Bot, event: Event, state: T_State):
    group_id = str(event.group_id)
    data = load_data(group_id)
    if not is_plugin_enabled(data):
        data["enabled"] = True
        save_data(group_id, data)
        await pcount_on.finish("插件功能已开启，数据文件已初始化")
    else:
        await pcount_on.finish("插件功能已开启，数据文件已存在")


# 关闭插件功能
pcount_off = on_command(
    "pcount off",
    aliases={"关闭pcount", "关闭pcount插件"},
    priority=90,
    permission=SUPERUSER,
    block=True
)


@pcount_off.handle()
async def handle_pcount_off(bot: Bot, event: Event, state: T_State):
    group_id = str(event.group_id)
    data = load_data(group_id)
    if is_plugin_enabled(data):
        data["enabled"] = False
        save_data(group_id, data)
        await pcount_off.finish("插件功能已关闭")
    else:
        await pcount_off.finish("插件功能已经是关闭状态")


def check_plugin_status(data, event):
    if not is_plugin_enabled(data):
        return f"插件功能未开启，无法执行指令"
    return None


# 帮助
help = on_command(
    "机厅帮助",
    aliases={"舞萌机厅人数帮助", "pcounthelp", "mphelp", "mmphelp"},
    priority=90,
    block=True
)


@help.handle()
async def handle_help(event: Event):
    help_message = (
        "线上机厅人数查询、修改帮助\n"
        "[机厅代号]+ - =[数字]: 使用类似于 'cy=6' 的指令来修改机厅人数\n"
        "[机厅代号]几: 使用类似于 'cy几' 的指令来查询机厅人数\n"
        "jt: 查看所有机厅的人数~\n"
        "注意注意~！各个群聊的数据都是不一样的，需要自行配置机厅哦\n"
        "蚕豆说这是Miaowing大佬做的插件！orz orz"
    )
    await help.finish(help_message)


# 添加机厅
add_hall = on_command(
    "add",
    aliases={"addjt"},
    priority=90,
    permission=SUPERUSER,
    block=True
)


@add_hall.handle()
async def handle_add_hall(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return

    try:
        hall_name, hall_id = args.extract_plain_text().split()
        hall_id = hall_id.strip()
        if hall_id not in data:
            data[hall_id] = {"name": hall_name, "count": 0}
            save_data(group_id, data)
            await add_hall.finish(f"机厅 {hall_name} ({hall_id}) 已添加")
        else:
            await add_hall.finish(f"机厅 {hall_id} 已存在")
    except ValueError:
        await add_hall.finish("输入格式错误，请使用 `添加机厅 机厅名 机厅代号`")


# 删除机厅
remove_hall = on_command(
    "删除机厅",
    aliases={"removejt", "移除机厅"},
    priority=90,
    permission=SUPERUSER,
    block=True
)


@remove_hall.handle()
async def handle_remove_hall(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return

    hall_id = args.extract_plain_text().strip()

    if hall_id in data:
        del data[hall_id]
        save_data(group_id, data)
        await remove_hall.finish(f"机厅 {hall_id} 已删除")
    else:
        await remove_hall.finish(f"机厅 {hall_id} 不存在")


# 修改人数
edit_count = on_regex(
    r'([a-zA-Z]+)([+-=])(\d+)',
    priority=90,
    block=True
)


@edit_count.handle()
async def handle_edit_count(event: Event, match=RegexMatched()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return

    user_name = event.sender.card or event.sender.nickname
    hall_id = match.group(1).strip()
    operation = match.group(2)
    count_delta = int(match.group(3))

    if hall_id not in data:
        return

    current_time = datetime.now().strftime("%H:%M")

    if operation == "+":
        data[hall_id]["count"] += count_delta
    elif operation == "-":
        if data[hall_id]["count"] - count_delta < 0:
            await edit_count.finish(
                f"不是哥们，0419来机厅打领土战争了？")
            return
        if data[hall_id]["count"] - count_delta > 15:
            await edit_count.finish(
                f"?今天机厅限时免费还是大猩猩攻过来了?")
            return
        data[hall_id]["count"] -= count_delta
    else:
        if count_delta < 0:
            await edit_count.finish("不是哥们，0419来机厅打领土战争了？")
            return
        if count_delta > 15:
            await edit_count.finish(
                f"?今天机厅限时免费还是大猩猩攻过来了?")
            return
        data[hall_id]["count"] = count_delta

    data[hall_id]["upload_time"] = current_time
    data[hall_id]["uploader"] = user_name

    save_data(group_id, data)
    await edit_count.finish(f"修改成功，当前 {data[hall_id]['name']} ({hall_id}) 共有 {data[hall_id]['count']} 人")


# 查询人数
look_count = on_endswith(
    "几",
    priority=90,
    block=True
)


@look_count.handle()
async def handle_look_count(event: Event):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return

    hall_id = event.get_plaintext().rstrip("几").strip()

    if hall_id in data:
        hall_name = data[hall_id]['name']
        count = data[hall_id]['count']
        upload_time = data[hall_id].get('upload_time', '2001年')
        uploader = data[hall_id].get('uploader', '世贸双子塔')

        response = f"{hall_name} ({hall_id}): {count}人（{uploader} 于 {upload_time}更新）"
        await look_count.finish(response)
    else:
        return


# 查询所有机厅人数
jt = on_command(
    "jt",
    aliases={"!jt", "！jt", "/jt"},
    priority=90,
    block=True
)


@jt.handle()
async def handle_jt(bot: Bot, event: Event):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return

    region_name = data.get("region", "邳州")  # 默认城市名 北京
    total_count = 0
    message_lines = ["机厅在线人数:"]

    for hall_id in data.keys():
        if hall_id in ["region", "enabled"]:  # 跳过 "region" 和 "enabled" 字段
            continue
        hall_name = data[hall_id]['name']
        count = data[hall_id]['count']
        upload_time = data[hall_id].get('upload_time', '2001年')
        uploader = data[hall_id].get('uploader', '世贸双子塔')

        total_count += count
        message_lines.append(f"{hall_name} ({hall_id}): {count}人（{uploader} 于 {upload_time}更新）")

    message_lines.append(f"{region_name}一共有{total_count}人正在出勤")

    await jt.finish("\n".join(message_lines))


# 查询所有机厅人数（简洁）
jjt = on_command(
    "jjt",
    aliases={"!jjt", "！jjt", "/jjt", "#jjt"},
    priority=90,
    block=True
)


@jjt.handle()
async def handle_jjt(bot: Bot, event: Event):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return

    region_name = data.get("region", "邳州")  # 默认城市名 北京
    total_count = 0
    message_lines = ["当前机厅人数："]

    for hall_id, hall_info in data.items():
        if isinstance(hall_info, dict) and "count" in hall_info:
            message_lines.append(f"{hall_info['name']} ({hall_id}): {hall_info['count']}人")
            total_count += hall_info['count']

    message_lines.append(f"\n区域名: {region_name}\n合计人数: {total_count}人")
    await jjt.finish("\n".join(message_lines))


# 修改地区名
edit_region_name = on_command(
    "修改地区名",
    aliases={"edit_region_name", "bind region", "edit region name", "修改地区"},
    priority=90,
    block=True
)


@edit_region_name.handle()
async def handle_edit_region_name(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return

    region_name = args.extract_plain_text().strip()

    if not region_name:
        await edit_region_name.finish("使用方式：修改地区名 wmc聚集地（自定义地区名）")

    data["region"] = region_name
    save_data(group_id, data)

    await edit_region_name.finish(f"地区名已成功修改为：{region_name}")
