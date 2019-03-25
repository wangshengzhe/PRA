""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/3/12
Description: get graph from user data
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import os


def get_graph_from_data(input_file):  # 构建user item的二分图
    """
    :param inut_file: user,item rating file
    :return: a dict:{UserA:{itemb:1,itemc:1},itemb:{UserA:1}}  嵌套字典  只有用户喜欢的
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    score_thr = 4.0
    graph = {}  #
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split("::")
        if len(item) < 3:   # 标准化为3
            continue
        userid, itemid, rating = item[0], "item_"+item[1], item[2]  # 全是字符串
        if float(rating) < score_thr:
            continue
        if userid not in graph:
            graph[userid] = {}
        graph[userid][itemid] = 1
        if itemid not in graph:
            graph[itemid] = {}
        graph[itemid][userid] = 1
    fp.close()
    return graph


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
    return item_info


if __name__ == "__main__":
    graph = get_graph_from_data("../data/mylog.txt")
    print(graph)





