""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/1/24
Description:  train lr model
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import numpy as np
from sklearn.linear_model import LogisticRegressionCV as LRCV
from sklearn.externals import joblib


def train_lr_model(train_file, model_coef, model_file):
    """

    :param train_file: process file for lr train
    :param model_coef:  w1,w2,
    :param model_file:  model pkl
    """
    total_feature_num = 118  # 离散化后的特征维度
    train_label = np.genfromtxt(train_file, dtype=np.int32, delimiter=",", usecols=-1)  # delimiter=","声明分隔符是，
    feature_list = range(total_feature_num)
    train_feature = np.genfromtxt(train_file,dtype=np.int32, delimiter=",", usecols=feature_list)  # 118 维是样本特征
    lr_cf = LRCV(Cs=[1, 10, 100], penalty="l2", tol=0.0001, max_iter=500, cv=5,).fit(train_feature,train_label)  # 正则化相关的参数 Cs是正则项系数，求倒数，tol=0.0001，残差收敛条件
    scores = lr_cf.scores_.values()[0]  # shape=[5,3]
    print(",".join([str(ele) for ele in scores.mean(axis=0)]))  # 对每列求平均
    print("diff:%s"%(",".join([str(ele) for ele in scores.mean(axis=0)])))  # 三个平均值
    print("Accurcy:%s%(+-%0.2f)"%(scores.mean(),scores.std()*2))  # 一个平均值  正态分布，+-2*std 就是90%
    lr_cf = LRCV(Cs=[1, 10, 100], penalty="l2", tol=0.0001, max_iter=500, cv=5,scoring="roc_auc").fit(train_feature,train_label)  # 正则化相关的参数 Cs是正则项系数，求倒数，tol=0.0001，残差收敛条件
    scores = lr_cf.scores.values()[0]
    print("diff:%s" % (",".join([str(ele) for ele in scores.mean(axis=0)])))  # 三个平均值
    print("Auc:%s%(+-%0.2f)" % (scores.mean(), scores.std() * 2))  # 一个平均值
    coef = lr_cf.coef_[0]
    fw = open(model_coef,)
    fw.write(",".join(str(ele) for ele in coef))
    fw.close()

    joblib.dump(lr_cf,model_file)