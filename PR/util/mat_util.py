""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/3/12
Description:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
from scipy.sparse import coo_matrix
import numpy as np
import util.read as read
import sys


def graph_to_m(graph):  # 求稀松矩阵M
    """

    :param graph:  user item graph
    :return: a coo_matrix, parse mat M
             a list, total user item point
             a dict ,map all the point to row index
    """
    vertex = list(graph.keys())  # py2中返回列表 py3:dict_keys[user,item...] 用list（）转换
    address_dict = {}
    total_len = len(vertex)
    for index in range(len(vertex)):
        address_dict[vertex[index]] = index  # {'user':num ,'item':num}
    row =[]
    col = []
    data = []
    for element_i in graph:
        weight = round(1/len(graph[element_i]), 3)
        row_index = address_dict[element_i]
        for element_j in graph[element_i]:
            col_index = address_dict[element_j]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    m = coo_matrix((data, (row, col)), shape=(total_len, total_len))
    return m, vertex, address_dict


def mat_all_point(m_mat, vertex, alpha):
    """
    get E-alpha*m_mat.T
    :param m_mat:
    :param vertex: total item and user point
    :param alpha:  the prob for random walking
    :return:  a parse
    """
    total_len = len(vertex)  # 所有顶点的个数
    row = []
    col = []
    data = []
    for index in range(total_len):  # 获得单位阵，np.eye() 容易溢出
        row.append(index)
        col.append(index)
        data.append(1)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    eye_t = coo_matrix((data, (row, col)), shape=(total_len, total_len))  # 单位阵
    # print(eye_t.todense())
    # sys.exit()  # 程序退出，用于测试第二个函数
    return eye_t.tocsr() - alpha*m_mat.tocsr().transpose()


if __name__ == "__main__":
    graph = read.get_graph_from_data("../data/mylog.txt")
    m, vertex, address_dict = graph_to_m(graph)

    # print(address_dict)  # 测试第一个函数
    # print(m)
    # print(m.todense())  # todense() 是将m 按矩阵的形式输出

    mat_all_point(m, vertex, 0.8)  # 测试第二个函数


