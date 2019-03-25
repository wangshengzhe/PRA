""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/2/4
Description:公共信息提取函数代码实现
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import os


def get_user_click(rating_file):
    """
    get user click list
    :param rating_file:
    :return: dict, key: userid, value : [ itemid1, itemid2] 所有 评分>=3 的itemid
    """
    if not os.path.exists(rating_file):
        return{}               # 如果不存在返回一个空字典
    fp = open(rating_file)     # 打开一个句柄
    num = 0                    #
    user_click = {}            # 用户的点击序列
    user_click_time = {}       # {uid_iid :time}
    for line in fp:
        if num == 0:
            num += 1
            continue
        item = line.strip().split("::")
        # Python strip() 方法用于就地移除字符串头尾指定的字符（默认为空格）或字符序列。item是list
        if len(item) < 4:         # 过滤掉
            continue
        [userid, itemid, rating, timestamp] = item   # uid,iid,rating,time 都是str
        if userid +"_"+ itemid not in user_click_time:
            user_click_time[userid+"_"+itemid] = int(timestamp)
        if float(rating) < 3.0:
            continue
        if userid not in user_click:
            user_click[userid] = []
        user_click[userid].append(itemid)
    fp.close()  # 关闭文件句柄
    return user_click, user_click_time


def get_item_info(item_file):
    """
    get item info[title,genes]
    Args:
       item_file:input iteminfo file
    Return :
       a dict,key:itemid,value:[title,genres]
    """
    if not os.path.exists(item_file):  # 如果不存在文件
        return {}
    num = 0
    item_info = {}
    fp = open(item_file, encoding="utf-8")  # 打开文件句柄
    for line in fp:
        if num == 0:
            num += 1
            continue
        item = line.strip().split("::")
        if len(item) < 3:
            continue
        if len(item) == 3:
           [itemid, title, genres] = item
        if len(item) > 3:
            itemid = item[0]
            genres = item[-1]
            title = ",".join(item[1:-1])  # 返回通过指定字符连接序列中元素后生成的新字符串。
        if itemid not in item_info:
            item_info[itemid] = [title, genres]
    fp.close()
    return item_info


if __name__ == "__main__":
    os.getcwd()                               # 返回当前的工作目录
    # user_click = get_user_click("../data/myratings.txt")
    # print(len(user_click), type(user_click), )   # usernum ,dict
    # print(user_click["1"])

    item_info = get_item_info("../data/mymovies.txt")
    print(item_info["11"])
    print(len(item_info), item_info)






