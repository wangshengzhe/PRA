""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/1/21
Description:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import math
import operator
import sys

sys.path.append("../utill")
import utill.reader as reader


def transfer_user_click(user_click):  # 将用户点击序列转变位被用户点击的商品序列
    """
    get item by user_click
    :param user_click: key uid value :[iid1,iid2]
    :return:dict key itemid value :[uid1,uid2...]   {iid:[uid1,uid2....]}
    """
    item_click_by_user = {}   #
    for user in user_click:   # {uid：[iid0,iid1,...],...}
        item_list = user_click[user]   #
        for itemid in item_list:
            item_click_by_user.setdefault(itemid, [])
            item_click_by_user[itemid].append(user)
    return item_click_by_user   # {iid:[uid1,uid2....]}


def base_contribution_score():
    """
    base usercf user contribution score
    :return:  1
    """
    return 1


def cal_user_sim(item_click_by_user):         # 计算用户的相似度
    """
    get user sim info
    :param item_click_by_user: dict ,key: itemid value [iid1,iid2,...]
    :return: dict,key :iid value :dict ,value_key:itemid_j,value_value:sim  {iid:{iidj:sc}}
    """
    co_appear = {}         # {uidi:{}} # {每个user：{其他各个用户：累加分数}}
    user_click_count = {}  # {uid:num,...}  每个用户及行为次数
    for itemid, user_list in item_click_by_user.items():
        for index_i in range(0, len(user_list)):  # 相似度矩阵
            user_i = user_list[index_i]
            user_click_count.setdefault(user_i, 0)
            user_click_count[user_i] += 1
            for index_j in range(index_i+1, len(user_list)):
                user_j = user_list[index_j]
                co_appear.setdefault(user_i, {})
                co_appear[user_i].setdefault(user_j, 0)
                co_appear[user_i][user_j] += base_contribution_score()
                co_appear.setdefault(user_j, {})
                co_appear[user_j].setdefault(user_i, 0)
                co_appear[user_j][user_i] += base_contribution_score()

    user_sim_info = {}  # {uid：{uidj：sc，uidj1：sc,...},...}
    user_sim_info_sorted = {}  # {uid:[(uid,sc)...],...}
    for user_i, relate_user in co_appear.items():  # 取user 以及该user有交集的user集合
        user_sim_info.setdefault(user_i, {})
        for user_j, cotime in relate_user.items():  # cotime :分数
            user_sim_info[user_i].setdefault(user_j, 0)
            user_sim_info[user_i][user_j] = cotime/math.sqrt(user_click_count[user_i]*user_click_count[user_j])  # float
    for user in user_sim_info:
        user_sim_info_sorted[user] = sorted(user_sim_info[user].items(), key=
                                            operator.itemgetter(1), reverse=True)
        return user_sim_info_sorted


def cal_recom_result(user_click, user_sim):
    """
    recom by usercf algo
    :param usr_click: dict key uid value [iid0,iid1...]
    :param user_sim:  key uid value:[(uid0,score0)(uid1,score1)...]
    :return: dict ,key:userid value:dict  v-k:iid,v-v:reom_score
    """
    recom_result = {}
    topk_user = 3  # 最相近的3个user
    item_num = 5
    for user, item_list in user_click.items():
        tmp_dict = {}   # 临时dict 完成过滤
        for itemid in item_list:
            tmp_dict.setdefault(itemid, 1)  #
        recom_result.setdefault(user, {})   #
        for zuhe in user_sim[user][:topk_user]:  #
            userid_j, sim_score = zuhe
            if userid_j not in user_click:
                continue
            for itemid_j in user_click[userid_j][:item_num]:  #
                recom_result[user].setdefault(itemid_j, sim_score)  # 将user的sc 作为item的sc
    return recom_result  # {userid:{iid:sc,...},....}


def main_flow():
    """
     main flow
    """
    user_click, user_click_time = reader.get_user_click("../data/myratings.txt")
    item_click_by_user = transfer_user_click(user_click)   # 将用户点击序列转变成item 被点击序列
    user_sim = cal_user_sim(item_click_by_user)            # 计算用户的相似度
    recom_result = cal_recom_result(user_click, user_sim)
    print(recom_result["1"])


if __name__ =="__main__":
    main_flow()
