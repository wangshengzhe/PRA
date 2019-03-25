""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/3/13
Description:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import os


def produce_train_data(input_file, out_file):
    """

    :param input_file: user behavior file
    :param out_file:output file
    """
    if not os.path.exists(input_file):
        return   #
    record = {}    # record = {uid:[iid,iid....]}
    linenum = 0
    score_thr = 4.0
    fp = open(input_file, encoding="utf-8")
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split("::")
        if len(item) < 4:
            continue
        userid, itemid, rating, = item[0], item[1], float(item[2])
        if rating < score_thr:  # 大于等于4分的判定为喜欢
            continue
        if userid not in record:
            record[userid] = []
        record[userid].append(itemid)
    fp.close()
    fw = open(out_file, "w+")
    for userid in record:
        fw.write(" ".join(record[userid])+"\n")  # 每一行对应一个user 喜欢的item 用空格 隔开
    fw.close()


if __name__ =="__main__":
    produce_train_data("../data/mytest.txt", "../data/mytest_train_data.txt")



