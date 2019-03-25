""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/2/23
Description:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import os
import operator
import sys
sys.path.append("../")
import util.read as read



def get_up(item_cate, input_file):
    """

    :param item_cate: dict key iid value: dict  v_k:category,v_v :ratio   {iid:{cat:ratio,...},...}
    :param input_file: user rating file
    :return: a dict key:uid value :[(cate,ratio),(cate,ratio),..]
    """
    if not os.path.exists(input_file):
        return {}
    record = {}
    up = {}
    linenum = 0
    score_thr = 4.0
    topk = 2
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split("::")
        if len(item) < 4:
            continue
        userid, itemid, rating, timestamp = item[0], item[1], float(item[2]), int(item[3])
        if rating < score_thr:
            continue
        if itemid not in item_cate:  # 若该电影找不到相应的类别
            continue
        time_score = get_time_score(timestamp)
        if userid not in record:
            record[userid] = {}
        for fix_cate in item_cate[itemid]:
            if fix_cate not in record[userid]:
                record[userid][fix_cate] = 0  #
            record[userid][fix_cate] += rating * time_score*item_cate[itemid][fix_cate]
    fp.close()
    for userid in record:
        if userid not in up:
            up[userid] = []
        total_score = 0
        for zuhe in sorted(record[userid].items(), key=operator.itemgetter(1), reverse=True)[:topk]:
            up[userid].append((zuhe[0], zuhe[1]))
            total_score += zuhe[1]
        for index in range(len(up[userid])):
            up[userid][index] = (up[userid][index][0],round(up[userid][index][1]/total_score, 3))   # 归一化
    return up  # 用户刻画


def get_time_score(timestampe):
    """

    :param timestampe: int
    :return: time score
    """
    fix_time_stamp = 1476086345  # 最大的时间戳，表示最近的时间
    total_sec = 24 * 60*60
    delta = (fix_time_stamp - timestampe)/total_sec/100 # 转化为天
    return round(1/(1+delta), 3)  # 时间分数，时间越短，分数越高，最高为1，时间越长分数越低


def recom(cate_item_sort, up, userid, topk=10):
    """

    :param cat_item_sort: reverse sort
    :param up: user profile
    :param userid:  fix userid to recom
    :param topk:  recom num
    :return:  a dict key userid value [itemid1,itemid2]
    """
    if userid not in up:  # 找不到用户画像，就不推荐
        return {}
    recom_result = {}
    if userid not in recom_result:
        recom_result[userid] = []
    for zuhe in up[userid]:
        cate = zuhe[0]
        ratio = zuhe[1]
        num = int(topk*ratio)+1
        if cate not in cate_item_sort:
            continue
        recom_list = cate_item_sort[cate][:num]
        recom_result[userid] += recom_list
    return recom_result


def run_main():
    ave_score = read.get_ave_score("../data/myratings.txt")
    item_cate, cate_item_sort = read.get_item_cate(ave_score,"../data/mymovies.txt")
    up = get_up(item_cate, "../data/ratings.txt")
    print(len(up))


if __name__ =="__main__":
    run_main()





