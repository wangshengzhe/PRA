""""
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Author: 王圣哲
date:   2019/2/4
Description:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
import os
def get_item_info(item_file):
    """
    get item info[title,genes]
    Args:
       item_file:input iteminfo file
    Return :
       a dict,key:itemid,value:[title,genres]
    """

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
    fp = open(item_file)  # 打开文件句柄
    for line in fp:
        print(line, type(line))

        if num == 0:
            num += 1
            continue
        item = line.strip().split("::")
        if len(item) < 3:
            continue
        [itemid, title, genres] = item
        if itemid not in item_info:
            item_info[itemid] = [title, genres]
            continue
        fp.close()
    return item_info

os.getcwd()
item_info = get_item_info("../data/moviestest.txt")
print(item_info)
