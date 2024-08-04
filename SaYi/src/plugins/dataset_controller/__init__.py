from nonebot.exception import MatcherException
import random
from ..time_freezer import check_time
from nonebot.matcher import Matcher
import json
import pandas
from nonebot.rule import to_me
from nonebot.plugin import on_command, on_type, on_message
from nonebot import on_type, on_message
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, PrivateMessageEvent


class DataSetControl:
    def __init__(self, data_path="C:\\Users\\DZYCD\\PycharmProjects\\SaYibot\\SaYi\\src\\plugins\\dataset_controller"
                                 "\\library.json"):
        self.data_file = data_path

    def get_dataset(self):
        with open(self.data_file, 'r', encoding='UTF-8') as f:
            load_dict = json.load(f)
            return load_dict

    def save_dataset(self, source):
        json_dict = json.dumps(source, indent=2, ensure_ascii=False)
        with open(self.data_file, 'w', encoding='UTF-8') as f:
            f.write(json_dict)

    def search(self, dic: dict, key: str):
        try:
            return dic[key]
        except:
            return False

    def update_value(self, key: str, target: str, value):
        dic = self.get_dataset()
        if not self.search(dic, key):
            dic[key] = {}
        dic[key][target] = value
        self.save_dataset(dic)

    def get_value(self, key: str, target: str):
        dic = self.get_dataset()
        if self.search(dic, key):
            try:
                return dic[key][target]
            except:
                return False
        return False

