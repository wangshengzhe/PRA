""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/2/5
Description: item cf main Algo
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
from __future__ import division
# 导入python未来支持的语言特征division(精确除法)，py2
# 当我们没有在程序中导入该特征时，"/"操作符执行的是截断除法(Truncating Division),
# 当我们导入精确除法之后，"/"执行的是精确除法
import sys
import os

os.getcwd()
sys.path.append("../utill")  #

import utill.reader as reader
import math
import operator


def base_contribute_score():
    """"
    item cf base sim contribution score by user
    """
    return 1


def update_one_contribute_score(user_total_click_num):  # 升级1
    """
    item cf update sim contribution score by user
    """
    return 1/math.log10(1+user_total_click_num)


def update_two_contribute_score(click_time_one,click_time_two):
    """
    item cf update two sim contribution score by user
    """
    delata_time = abs(click_time_one - click_time_two)
    total_sec = 60*60*24
    delata_time = delata_time/total_sec
    return 1/(1+delata_time)


def cal_item_sim(user_click, user_click_time):   # 计算相似度
    """
    :param user_click: dict,key userid value [itemid1,itemid2。。。]
    :return: dict,key:itemid i ,value_key itemid j ,value_value simscore  用户个数
    """
    co_appear = {}   # {i1:{j1:1,j2:1,...}}存放每部电影i，以及该电影与其他电影有共同喜欢的分数（人数）j:u(i)&u(j)
    item_user_click_time = {}  # itemid: usernum 存放每部电影：喜欢的人数  i:u(i)
    for user, itemlist in user_click.items():  # user = userid  itemlist = [itemid1,itemid2...]
        for index_i in range(0, len(itemlist)):
            itemid_i = itemlist[index_i]       #
            item_user_click_time.setdefault(itemid_i, 0)  # 对不存在的key，进行一个初值的设定，增加k-v
            item_user_click_time[itemid_i] += 1
            for index_j in range(index_i + 1, len(itemlist)):
                itemid_j = itemlist[index_j]
                if user+"_"+itemid_i not in user_click_time:
                    click_time_one = 0
                else:
                    click_time_one = user_click_time[user+"_"+itemid_i]
                if user+"_"+itemid_j not in user_click_time:
                    click_time_two = 0
                else:
                    click_time_two = user_click_time[user+"_"+itemid_j]
                co_appear.setdefault(itemid_i, {})  #
                co_appear[itemid_i].setdefault(itemid_j, 0)
                # co_appear[itemid_i][itemid_j] += base_contribute_score()  #
                # co_appear[itemid_i][itemid_j] += update_one_contribute_score(len(itemlist))  # 升级1
                co_appear[itemid_i][itemid_j] += update_two_contribute_score(click_time_one,click_time_two)  # 升级2
                co_appear.setdefault(itemid_j, {})
                co_appear[itemid_j].setdefault(itemid_i, 0)
                # co_appear[itemid_j][itemid_i] += base_contribute_score()
                # co_appear[itemid_i][itemid_j] += update_one_contribute_score(len(itemlist))   # 升级1
                co_appear[itemid_i][itemid_j] += update_two_contribute_score(click_time_one,click_time_two)  # 升级1
    item_sim_score = {}  # 相似度矩阵  {i:{J:sij}...}
    item_sim_score_sorted = {}  # {i:[（J:sij），...],...}排序
    for itemid_i, relate_item in co_appear.items():   # relate_item = {}
        for itemid_j, co_time in relate_item.items():   # co_time = u(i)&u(j)
            sim_score = co_time/math.sqrt(item_user_click_time[itemid_i]*item_user_click_time[itemid_j])  # 相似度分数
            item_sim_score.setdefault(itemid_i, {})
            item_sim_score[itemid_i].setdefault(itemid_j, 0)
            item_sim_score[itemid_i][itemid_j] = sim_score  # {i:{J:sij}...}
    for itemid in item_sim_score:
        item_sim_score_sorted[itemid] = sorted(item_sim_score[itemid].items(), key=\
                                    operator.itemgetter(1), reverse=True)  # 按相似度分数排序  降序
        # {i:[（J,sij），...],...}
    return item_sim_score_sorted  # {i:[J:sij]...}  排序后的


def cal_recom_result(sim_info, user_click, user_click_time):
    """
    recom by itemcf
    :param sim_info: item sim dict
    :param user_click: user click dict
    :return: dict,key:userid value_key itemid,value_value recom_score
    """
    recent_click_num = 3   # 用user最近的3个item
    topk = 5
    recom_info = {}  # 存储推荐的结果
    for user in user_click:  # {uid:[iid1,iid2....]}
        click_list = user_click[user]  # user  喜欢的item 列表
        recom_info.setdefault(user, {})       # 对于不存在的key 进行一个初值的设定
        for itemid in click_list[:recent_click_num]:  # 将user喜欢item列表（没有排序）的前3个取出
            if itemid not in sim_info:    # {i:{J:sij}...}  排序后的
                continue
            for itemsimzuhe in sim_info[itemid][:topk]:  # 排序后字典变成了元组组成的列表
                itemsimid = itemsimzuhe[0]  #
                itemsimscore = itemsimzuhe[1]  #
                recom_info[user][itemsimid] = itemsimscore   # 新增k-v
    return recom_info  # {uid:{iid1:sc,...}}


def debug_itemsim(item_info, sim_info):
    """
    show itemsim info
    :param item_info: dict,key itemid value:[title,gen]
    :param sim_info: dict,key itemid,value list[(itemid1,simscore),(itemid2,simscore)]
    :return:
    """
    fixd_itemid = "1"
    if fixd_itemid not in item_info:
        print("invalid itemid")
        return
    [title_fix, genres_fix] = item_info[fixd_itemid]
    for zuhe in sim_info[fixd_itemid][:5]:
        itemid_sim = zuhe[0]
        sim_score = zuhe[1]
        if itemid_sim not in item_info:
            continue
        [title, genres] = item_info[itemid_sim]
        print(title_fix +"\t"+genres_fix + "\tsim:" + title + "\t" + genres + "\t" + str(sim_score))


def debug_recomresult(recom_result, item_info):
    """
    debug recomresult
    :param recom_result: key userid value:dict,value-key:itemid,vlue_value:recom_score {uid:{iid1:sc,...}}
    :param item_info:key itemid value:[title,genre]
    :return:
    """
    user_id = "1"
    if user_id not in recom_result:
        print("invalid result")
        return
    for zuhe in sorted(recom_result[user_id].items(),key = operator.itemgetter(1), reverse=True):
        itemid,score = zuhe
        if itemid not in item_info:
            continue
        print(",".join(item_info[itemid])+"\t" + str(score))

def main_flow():
    """
    main flow of itemcf
    """
    user_click, user_click_time = reader.get_user_click("../data/myratings.txt")   # 用户的点击序列
    item_info = reader.get_item_info("../data/mymovies.txt")
    sim_info = cal_item_sim(user_click)                         # 相似度
    #debug_itemsim(item_info, sim_info)
    recom_result = cal_recom_result(sim_info, user_click)       # 推荐结果
    # print(recom_result["1"])                                    # 打印出userid1的推荐结果
    debug_recomresult(recom_result,item_info)


if __name__ =="__main__":
    main_flow()
