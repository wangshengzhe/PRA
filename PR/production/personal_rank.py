""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/3/12
Description:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
from __future__ import division  # py2 中的 py3 不需要
import operator
import sys
sys.path.append("../util")
import util.read as read
import util.mat_util as mat_util


def personal_rank(graph, root, alpha, iter_num, recom_num=10):
    """

    :param graph: user item graph
    :param root:  the fixed user for which to recom  目标user  固定顶点
    :param alpha: the prob to go to random walk
    :param iter_num:  iteration num
    :param recom_num: recom item num  默认的推荐个数
    :return:  a dict key itemid ,value pr
    """

    rank = {}
    rank = {point: 0 for point in graph}  # 字典生成式
    rank[root] = 1                        # 目标user为1，其余顶点pr为0
    recom_result = {}                     #

    for iter_index in range(iter_num):  # 迭代
        tmp_rank = {}
        tmp_rank = {point: 0 for point in graph}                 # {user：重要度}

        for out_point, out_dict in graph.items():                # out_dict 出度，out_point:uid or iid
            for inner_point, value in graph[out_point].items():  # inner_point是与out_point 连接的顶点user or item  value =1
                tmp_rank[inner_point] += round(alpha*rank[out_point]/len(out_dict), 4)
                if inner_point == root:
                    tmp_rank[inner_point] += round(1-alpha, 4)

        if tmp_rank == rank:   # 迭代充分
            print("out"+str(iter_index))
            break
        rank = tmp_rank

    right_num = 0
    for zuhe in sorted(rank.items(), key=operator.itemgetter(1), reverse=True):  # 根据pr值排序
        point, pr_score = zuhe[0], zuhe[1]
        if len(point.split("_")) < 2:  # 若该顶点不是item顶点，str没有"_"就还是原来的字符串
            continue
        if point in graph[root]:   # 若该顶点被固定顶点行为过
            continue
        recom_result[point] = pr_score   # pr值
        right_num += 1
        if right_num > recom_num:
            break
    return recom_result


def personal_rank_mat(graph, root, alpha,recom_num = 10):  # 矩阵形式
    """

    :param graph: user item graph
    :param root: the fix user to recom
    :param alpha: the prob to random walk
    :param recom_num: recom iem num
    :return: a dick : itemid, value:pr score
    """


def get_one_user_recom():
    """
    give one fix_user recom result
    :return:
    """
    user = "A"
    alpha = 0.6
    graph = read.get_graph_from_data("../data/mylog.txt")
    iter_num = 100   # 随机写一个迭代数目

    recom_result = personal_rank(graph, user, alpha, iter_num)
    print(recom_result)

    item_info = read.get_item_info("../data/mymovies.txt")
    for itemid in graph[user]:
        pure_itemid = itemid.split("_")[1]
        print(item_info[pure_itemid])
    print("result-------")
    for itemid in recom_result:
        pure_itemid = itemid.split("_")[1]

        print(item_info[pure_itemid])
        print(recom_result[itemid])


if __name__ =="__main__":
    get_one_user_recom()
