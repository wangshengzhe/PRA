""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/1/11
Description: lfm model train main function
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import numpy as np
import sys
sys.path.append("..//util")
import util.read as read
import operator


def lfm_train(train_data, F, alpha, beta, step):
    """
    :param train_data: train_data for lfm
    :param F:  user vector len item vector len
    :param alpha:  regularization factor  正则化的参数
    :param beta:   learning rate
    :param step:   iteration num  迭代次数
    :return:dict:key itemid,value:list     np.ndarray
            dict :key userid ,value :list  np.ndarray
    """
    user_vec = {}   # 所有user向量的集合  {uid0:[v1,v2,...],uid1:[v1,v2,...],...}
    item_vec = {}   # 所有item向量的集合 {iid：[v1,v2,...],iid1:[v1,v2,...],...}
    for step_index in range(step):  # 每一次迭代 ，指导迭代次数结束跳出循环
        for data_instance in train_data:  # 一个tuple
            userid, itemid, label = data_instance  #
            if userid not in user_vec:   #
                user_vec[userid] = init_model(F)  # 初始化向量
            if userid not in item_vec:
                item_vec[userid] = init_model(F)  #

        delta = label - model_predict(user_vec[userid], item_vec[itemid])  # 预测值与真实值的差
        for index in range(F):  # 每一维，循环一遍就是梯度下降一次
            user_vec[userid][index] += beta*(delta*item_vec[itemid][index]-alpha*user_vec[userid][index])  # 梯度下降
            item_vec[itemid][index] += beta*(delta*user_vec[userid][index]-alpha*item_vec[itemid][index])
        beta = beta*0.9  # 快收敛的时候，速度慢一点
    return user_vec, item_vec


def init_model(vector_len):
    """
    :param vector_len: the len of vector
    :return: a ndarray
    """
    return np.random.randn(vector_len)  # 标准正态分布初始化


def model_predict(user_vector, item_vector):
    """
    user_vector and item_vector distance   cos 值   距离远近，推荐强度
    :param user_vector: model produce user vector
    :param item_vector:  model produce item vector
    :return: a num
    """
    res = np.dot(user_vector, item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
    # 求cos  np.linalg.norm() 范数，模
    return res


def model_train_process():
    """
    test lfm model train
    :return:
    """
    train_data = read.get_train_data("../data/myratings.txt")
    user_vec, item_vec = lfm_train(train_data, 50, 0.01, 0.1, 50)

    recom_result = give_recom_result(user_vec, item_vec, "1")
    print(recom_result)

    ana_recom_result(train_data, "1", recom_result)

    # print(len(user_vec["1"]))
    # print(item_vec["2455"])


def give_recom_result(user_vec, item_vec, userid):
    """
    use lfm model result give fix userid recom result

    :param user_vec:  lfm model result
    :param item_vec:
    :param userid:  fix userid   推荐结果
    :return:a list [(itemid,score),(itemid1,score1)]
    """
    fix_num = 10
    if userid not in user_vec:
        return []
    record = {}  # 存放 输入的u_v与所有的i_v的cos值{iid:cos,...}
    recom_list = []  # 排序后的[(iid0,cos0),(iid1,cos1),...]
    user_vector = user_vec[userid]  # 根据userid 获得对应的vector
    for itemid in item_vec:  # 遍历每个 item 向量
        item_vector = item_vec[itemid]
        res = np.dot(user_vector, item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))  # cos，
        record[itemid] = res  # {iid：与user向量的cos值，...} u_v 与每个i_v的cos值
    for zuhe in sorted(record.items(), key=operator.itemgetter(1), reverse=True)[:fix_num]:  # iteritems()-->items()
        # [(iid,cos),(),...]
        itemid = zuhe[0]
        score = round(zuhe[1], 3)
        recom_list.append((itemid, score))
    return recom_list  # list  [(iid,score),...]


def ana_recom_result(train_data, userid, recom_list):  # 分析评估推荐结果
    """
    :param train_data: train data for lfm model
    :param userid: fix userid
    :param recom_list: reeom result by lfm
    """
    item_info = read.get_item_info("../data/mymovies.txt")
    for data_instance in train_data:
        tmp_userid, itemid, label = data_instance
        if tmp_userid == userid and label == 1:  # 训练集中，该user喜欢的电影详情
            print(item_info[itemid])
        print("recom result")
        for zuhe in recom_list:    # 组合是元组
            print(item_info[zuhe[0]])  # 打印 推荐列表的电影详情


if __name__ == "__main__":
    model_train_process()


