""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/2/23
Description:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import os
import operator


def get_ave_score(input_file):
    """
    求item的平均分
    :param int_file: user rating file
    :return:  a dict key:itemid , value :ave_score
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record = {}  # {iid:[sc,num],...}
    ave_score = {}  # {iid:ave_sc,...}

    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split("::")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if itemid not in record:
            record[itemid] = [0, 0]
        record[itemid][0] += rating
        record[itemid][1] += 1
    fp.close()

    for itemid in record:
        ave_score[itemid] = round(record[itemid][0]/record[itemid][1], 3)
    return ave_score   # {iid:ave_sc,...}


def get_item_cate(ave_score, input_file):
    """
    得到每个item的类别，统计每个类别的item，并按照平均分倒排
    :param ave_score: a dict,key itemid value ave_rating score
    :param input_file:  item_info file
    :return:  a dict key  iid, value a dict ,key cate value ration
               a dict key cate value[iid0,iid1,...]

    """
    if not os.path.exists(input_file):
        return {}, {}
    linenum = 0
    item_cate = {}   # {iid：{种类：ratio，...},...}
    record = {}      #
    topk = 100
    cate_item_sort = {}
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split("::")
        if len(item) < 3:
            continue
        itemid = item[0]
        cate_str = item[-1]
        cate_list = cate_str.strip().split("|")  # 种类列表
        ratio = round(1/len(cate_list), 3)  # 根据类别数量，均等分权重
        if itemid not in item_cate:
            item_cate[itemid] = {}
        for fix_cate in cate_list:
            item_cate[itemid][fix_cate] = ratio    # {iid：{种类：ratio，...},...}
    fp.close()
    for itemid in item_cate:  # 对于某个iid
        for cate in item_cate[itemid]:  # cate :{种类：retio,... }中的种类
            if cate not in record:
                record[cate] = {}    # record：{种类：{iid：ave_sc，}}
            itemid_rating_score = ave_score.get(itemid, 0)
            record[cate][itemid] = itemid_rating_score

    for cate in record:
        if cate not in cate_item_sort:
            cate_item_sort[cate] = []
        for zuhe in sorted(record[cate].items(), key=operator.itemgetter(1), reverse=True)[:topk]:
            cate_item_sort[cate].append(zuhe[0])
    return item_cate, cate_item_sort


if __name__ == "__main__":
    res = get_ave_score("../data/myratings.txt")
    print(res)
    item_cate, cate_item_sort = get_item_cate(res, "../data/mymovies.txt")
    print(item_cate["1"])
    print(cate_item_sort["Children"])

