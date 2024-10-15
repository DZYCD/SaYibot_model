#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
api_key = "e0fa72f1e0e433cfd42a27b16be036af5d8340df"
minsim = '80!'

import io
import requests
from PIL import Image
import json
from collections import OrderedDict

thumbSize = (250, 250)

# enable or disable indexes
index_hmags = '0'
index_reserved = '0'
index_hcg = '0'
index_ddbobjects = '0'
index_ddbsamples = '0'
index_pixiv = '1'
index_pixivhistorical = '1'
index_seigaillust = '1'
index_danbooru = '0'
index_drawr = '1'
index_nijie = '1'
index_yandere = '0'
index_animeop = '0'
index_shutterstock = '0'
index_fakku = '0'
index_hmisc = '0'
index_2dmarket = '0'
index_medibang = '0'
index_anime = '0'
index_hanime = '0'
index_movies = '0'
index_shows = '0'
index_gelbooru = '0'
index_konachan = '0'
index_sankaku = '0'
index_animepictures = '1'
index_e621 = '0'
index_idolcomplex = '0'
index_bcyillust = '0'
index_bcycosplay = '0'
index_portalgraphics = '0'
index_da = '1'
index_pawoo = '0'
index_madokami = '0'
index_mangadex = '0'

# generate appropriate bitmask
db_bitmask = int(
    index_mangadex + index_madokami + index_pawoo + index_da + index_portalgraphics + index_bcycosplay + index_bcyillust + index_idolcomplex + index_e621 + index_animepictures + index_sankaku + index_konachan + index_gelbooru + index_shows + index_movies + index_hanime + index_anime + index_medibang + index_2dmarket + index_hmisc + index_fakku + index_shutterstock + index_reserved + index_animeop + index_yandere + index_nijie + index_drawr + index_danbooru + index_seigaillust + index_anime + index_pixivhistorical + index_pixiv + index_ddbsamples + index_ddbobjects + index_hcg + index_hanime + index_hmags,
    2)

def search(fname = "C:\\Users\\DZYCD\\OneDrive\\Pictures\\0e12bcf6fb149d904d82eac55454751c.jpg"):
    image = Image.open(fname)
    image = image.convert('RGB')
    imageData = io.BytesIO()
    image.save(imageData, format='PNG')
    url = 'http://saucenao.com/search.php?output_type=2&numres=1&minsim=' + minsim + '&dbmask=' + str(
    db_bitmask) + '&numres=5' + '&api_key=' + api_key
    files = {'file': ("image.jpg", imageData.getvalue())}
    imageData.close()
    r = requests.post(url, files=files)
    results = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(r.text)
    if int(results['header']['user_id']) == 0:
        return '有可能你这个找不到，也有可能是蚕豆网络爆炸了...等会再试试'
    if(results['header']['results_returned'])==0:
        return '我翻遍所有站点都没有找到你这个,sorry'
    msg = "找到以下结果！\n"
    for i in range (results['header']['results_returned']):
        # get vars to use
        service_name = ''
        illust_id = 0
        index_id = results['results'][i]['header']['index_id']

        if index_id == 5 or index_id == 6:
            # 5->pixiv 6->pixiv historical
            service_name = 'pixiv'
            illust_id = results['results'][i]['data']['pixiv_id']
        elif index_id == 8:
            # 8->nico nico seiga
            service_name = 'seiga'
            illust_id = results['results'][i]['data']['seiga_id']
        elif index_id == 10:
            # 10->drawr
            service_name = 'drawr'
            illust_id = results['results'][i]['data']['drawr_id']
        elif index_id == 11:
            # 11->nijie
            service_name = 'nijie'
            member_id = results['results'][i]['data']['member_id']
            illust_id = results['results'][i]['data']['nijie_id']
        elif index_id == 28:
            # 28->animepictures
            service_name = 'animepictures'
            illust_id = results['results'][i]['data']['animepictures_id']
        elif index_id == 34:
            # 34->da
            service_name = 'da'
            illust_id = results['results'][i]['data']['da_id']
        msg = msg+"{}-->站点：{}\nid：{}\n相似度：{}\n".format(i+1, service_name, illust_id, results['results'][i]['header']['similarity'])
    return msg