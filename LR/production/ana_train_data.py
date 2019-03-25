""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/1/24
Description: feature selection and data selection
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import pandas as pd
import numpy as np
import operator
import sys


def get_input(input_train_file, input_test_file):
    """
    指定某些数据为int 类型，样本选择，选择某些特征，
    :param input_train_file: 原始数据
    :param input_test_file:  原始数据
    :return: pd.DataFrame train_data
             pd.Dataframe  test_data
    """
    dtype_dict = {"age": np.int32,
                  "education-num": np.int32,
                  "capital-gain": np.int32,
                  "capital-loss": np.int32,
                  "hours - per - week": np.int32,
                  }  # 指定哪些列是数字
    use_list = range(15)  # 15 个特征
    use_list.remove(2)   # 去掉第3列
    train_data_df = pd.read_csv(input_train_file, sep=",", header=0, dtype=dtype_dict, na_values="?", usecols=use_list) # header表示第0行是列索引
    train_data_df = train_data_df.dropna(axis=0, how="any")  # 样本选择，只要是有NaN的行都不要
    test_data_df = pd.read_csv(input_test_file, sep=",", header=0, dtype=dtype_dict, na_values="?", usecols=use_list)  # header表示第0行是列索引
    test_data_df = test_data_df.dropna(axis=0, how="any")  # 样本选择，只要是有NaN的行都不要
    return train_data_df, test_data_df


def lable_trans(x):
    """
    :param x: each element
    :return:
    """
    if x == "<=50k":
        return "0"
    if x == " >50k":
        return "1"
    return "0"


def process_lable_feature(lable_feature_str, df_in):  #
    """
    :param lable_feature_str: "label"  文件中的这一列叫"lable"
    :param df_in: DataFrameIne
    """
    df_in.loc[:, lable_feature_str] = df_in.loc[:, lable_feature_str].apply(lable_trans)  # loc是根据dataframe的具体标签选取列
    # 将lable 转换成"0" 或"1"


def dict_trans(dict_in):  #
    """

    :param dict_in: key str,value int
    :return: a dict, key str value index for example 0,1,2
    """
    output_dict = {}
    index = 0
    for zuhe in sorted(dict_in.items(), key=operator.itemgetter(1), reverse=True):
        output_dict[zuhe[0]] = index  #
        index += 1
    return output_dict    # 将dict中的每个key 都赋予一个坐标值  {"类别”：1,...}


def dis_to_feature(x, feature_dict):  # 对特征进行离散化
    """

    :param x: element
    :param feature_dict: pos dict   {"名称":0,...}
    :return: a str as "0,1,0,0"
    """
    output_list = [0]*len(feature_dict)
    if x not in feature_dict:  # x 是指定列的所有元素,
        return ",".join([str(ele) for ele in output_list])  # 全部为0组成的字符串
    else:
        index = feature_dict[x]  # 该类所对应的索引，
        output_list[index] = 1  #
    return ",".join([str(ele) for ele in output_list])  # 将一个list转化成str


def process_dis_feature(feature_str, df_train, df_test):  # 处理离散特征
    """
    process dis feature for lr train
    :param feature_str:  label_in    指定某一列
    :param df_train: train_data_df  将“lable" 列转换为”0“ 和”1“ 之后的dataframe
    :param df_test:  test_data_df
    return : the dim of the feature for lr train
    """
    origin_dict = df_train.loc[:, feature_str].value_counts().to_dict()  # {名称：数目，...}
    feature_dict = dict_trans(origin_dict)  # {"名称0":0,"名称1":1,..}
    df_train.loc[:, feature_str] = df_train.loc[:, feature_str].apply(dis_to_feature, args=(feature_dict,))
    df_test.loc[:, feature_str] = df_test.loc[:, feature_str].apply(dis_to_feature, args=(feature_dict,))
    print(df_train.loc[:3, feature_str])  #
    return len(feature_dict)  # 返回每个特征离散化的维度


def list_trans(input_dict):
    """

    :param input_dict: {"count":num,"std":num,"min":num,...}
    :return: a list, [0.1,0.2,0.3,0.4,0.5]  依次传入"min", "25%", "50%", "75%", "max"对应的数值
    """
    output_list = [0]*5
    key_list = ["min", "25%", "50%", "75%", "max"]
    for index in range(len(key_list)):
        fix_key = key_list[index]  # "min", "25%", "50%", "75%", "max"
        if fix_key not in input_dict:
            print("error")
            sys.exit()
        else:
            output_list[index] = input_dict[fix_key]  #
    return output_list


def con_to_feature(x, feature_list):
    """
    :param x: element
    :param feature_list: list for feature trans
    :return: str,"1_0_0_1
    """
    feature_len = len(feature_list)-1
    result = [0] * feature_len
    for index in range(feature_len):
        if x >= feature_list[index] and x <= feature_list[index+1]:
            result[index] = 1
            return ",".join([str(ele) for ele in result])


def process_con_feature(feature_str, df_train, df_test):   # 处理连续特征
    """
    process con feature for lr train
    :param feature_str:  label_in    指定某一列
    :param df_train: train_data_df  将“lable" 列转换为”0“ 和”1“ 之后的dataframe
    :param df_test:  test_data_df
    return : the dim of the feature for lr train
    """
    origin_dict = df_train.loc[:, feature_str].destribe().todict()  # 根据destribe（）将连续特征分段，
    feature_list = list_trans(origin_dict)  # [0.1,0.2,0.3,0.4,0.5]  依次传入"min", "25%", "50%", "75%", "max"对应的数值
    df_train.loc[:, feature_str] =df_train.loc[:, feature_str].apply(con_to_feature, args=(feature_list,))
    df_test.loc[:, feature_str] =df_test.loc[:, feature_str].apply(con_to_feature, args=(feature_list,))
    print(df_train.loc[:3, feature_str])
    return len(feature_list)-1  # 返回特征的维度


def output_file(df_in, out_file):
    """
   write data of df_in to out_file
    """
    fw = open(out_file, "w+",encoding="utf-8")
    for row_index in df_in.index:
        outline = ",".join([str(ele) for ele in df_in.loc[row_index].valures])
        fw.write(outline+"\n")
    fw.close()


def ana_train_data(input_train_data, input_test_data, out_train_file, out_test_file):
    """
    :param input_train_data:  原始数据
    :param input_test_data:   原始数据
    :param out_train_file:
    :param out_test_file:
    :return:
    """
    train_data_df, test_data_df = get_input(input_train_data, input_test_data)  # 返回样本选择后的dataframe
    lable_feature_str = "lable"  #
    dis_feature_list = [
        "workclass", "education", "marital-status",
        "occupation", "relationship", "race", "sex", "native-country"
    ]  # 离散特征的列表
    con_feature_list = [
        "age", "education-num", "capital-gain", "capital-loss", "hours-per-week"
    ]
    process_lable_feature(lable_feature_str, train_data_df)  # 将dataframe 中的“lable" 列中的内容转换成 "0" "1"
    process_lable_feature(lable_feature_str, test_data_df)
    dis_feature_num = 0
    con_feature_num = 0
    for dis_feature in dis_feature_list:
        dis_feature_num += process_dis_feature(dis_feature, train_data_df, test_data_df)
    for con_feature in con_feature_list:
        con_feature_num += process_con_feature(con_feature, train_data_df, test_data_df)
    output_file(train_data_df, out_train_file)  #
    output_file(test_data_df, out_test_file)   # 将离散化后的数据持久化导本地


if __name__ == "__main__":
    ana_train_data("../data/train.txt", "../data/test.txt")
