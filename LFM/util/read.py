""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/1/9
Description:  util function
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

import os


def get_item_info(input_file):
    """
    get item info : [title,genre]
    :param input_file: item info file
    :return: a dict : key : itemid ,value:[title,genre]
    """
    if not os.path.exists(input_file):  #
        return {}
    item_info = {}
    linenum = 0                                           # 行号
    fp = open(input_file, encoding="utf-8")
    print(fp, type(fp))
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split("::")  # 去掉首尾空格，再分割成列表，引号里面也有逗号
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemid, title, genre = item[0], item[1], item[2]
        elif len(item) > 3:  # 引号里面也有逗号
            itemid = item[0]
            genre = item[-1]
            title = ",".join(item[1:-1])  # 返回一个字符串，元素间用逗号隔开
        item_info[itemid] = [title, genre]  #
    fp.close()
    return item_info  # {iid：[title,genre],...}


def get_ave_score(input_file):
    """
    get item ave rating score
    :param input_file: user rating file
    :return: a dict  key itemid ,value:ave_score
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}   # 中间结果{iid:[人数(评分次数)：总分]}
    score_dict = {}   # 最终结果  {iid：ave_rating}
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue  # 过滤掉
        item = line.strip().split("::")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], item[2]   # str
        if itemid not in record_dict:
            record_dict[itemid] = [0, 0]
        record_dict[itemid][0] += 1   # 人数    int
        record_dict[itemid][1] += float(rating)  # 总分数  float
    fp.close()
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][0], 3)  # 保留三位小数
    return score_dict              # 最终结果  {iid：ave_rating}


def get_train_data(input_file):
    """
    get train data for LFM model train
    :param input_file: user item rating file
    :return: a list [(userid,itemid ,label),(userid1,itemid1,label)]
    """
    if not os.path.exists(input_file):
        return []
    score_dict = get_ave_score(input_file)   # ave_score 的dict:{iid:ave_rating,...}
    neg_dict = {}  # {uid:[iid,ave_sc],...}  负样本提取规则：用户评分，并且是低分
    pos_dict = {}  # {uid:[iid,1],...}
    train_data = []  # 最终输出
    linenum = 0
    score_thr = 4.0  # 正负样本的阈值
    fp = open(input_file)
    for line in fp:
        if linenum == 0:   # 第一行不能用
            linenum += 1
            continue
        item = line.strip().split("::")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])  # 注意：ranting 是数字
        if userid not in pos_dict:  #
            pos_dict[userid] = []
        if userid not in neg_dict:
            neg_dict[userid] = []   #
        if rating >= score_thr:                    # 正样本  大于等于4.0分
            pos_dict[userid].append((itemid, 1))   # 1 代表有行为  1 是正样本，0 是负样本
        else:     # 负样本,注意此时虽然小于4分，但是平均分可能大于4分，作为负样本的依据，
            score = score_dict.get(itemid, 0)         # 获取分数，负样本，平均分数,get不能新建k-v
            neg_dict[userid].append((itemid, score))  # {uid:[iid,ave_sc,iid1,ave_sc1,...],...}
    fp.close()
# 正负样本的均衡和负采样
    for userid in pos_dict:  # 对每个用户来说 {uid:[(iid,1),...],...}
        data_num = min(len(pos_dict[userid]), len(neg_dict.get(userid, [])))  # 该用户爱好电影的个数与负样本中的电影个数的较小值 正负均衡
        if data_num > 0:  # 对每个user来说，正负样本个数一样
            train_data += [(userid, zuhe[0], zuhe[1]) for zuhe in pos_dict[userid]][:data_num]  # list  正样本
        else:
            continue
        sorted_neg_list = sorted(neg_dict[userid], key=lambda element: element[1], reverse=True)[:data_num]  # 按平均得分降序 默认升序
        train_data += [(userid, zuhe[0], 0) for zuhe in sorted_neg_list]  #

        if userid =="27":  # 测试
            print(len(pos_dict[userid]))
            print(len(neg_dict[userid]))
            print(neg_dict)
            print(sorted_neg_list)

    return train_data   # [(uid0,iid0,1),(uid1,iid1,0),....]


if __name__ == "__main__":

    # 测试get_item_info
    # item_dict = get_item_info("../data/mymovies.txt")
    # print(len(item_dict))    # 3883个电影
    # print(item_dict["1"])
    # print(item_dict["11"])

    # 测试2
    # score_dict = get_ave_score("../data/myratings.txt")
    # print(len(score_dict))   # {iid:[人数，总分],...}
    # print(score_dict["31"])  # {iid:ave sc,...}

    # 测试3
    train_data = get_train_data("../data/myratings.txt")
    print(len(train_data))
    print(train_data[:20])
