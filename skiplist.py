#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SkipList实现
参考论文：Skip Lists: A Probabilistic Alternative to Balanced Trees
"""
__author__ = 'evan'
__version__ = '0.1'

import logging
from random import randint, seed

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger("skip-list-demo")


class SkipNode:
    """
    Skip Node。
    代表SKIP LIST中每个实际存储数据的节点
    """

    def __init__(self, level=0, key=None, value=None):
        """
        构造SkipNode对象
        :param level:
        :param key:
        :param value:
        :return:
        """
        print("New SkipNode[level:%d, key:%s, value:%s]" % (level, key, value))
        # 定义SkipNode层次
        self.level = level
        # 定义SkipNode所处层次的所有forward指针的数组
        self.forward = [None] * level
        # 键
        self.key = key
        # 值
        self.value = value


class SkipList:
    """
    Skip List实现
    提供简单的insert/delete/search方法
    """

    # 最大SkipList层次
    MAX_LEVEL = 5

    def __init__(self):
        """
        构造SkipList对象
        :return:
        """
        self.head = SkipNode()
        self.len = 0
        self.max_level = 0

    def insert(self, key, value):
        """
        插入元素
        :param key:
        :param value:
        :return:
        """
        old_value = None
        # 预先搜索
        node = self._internal_search(key)
        if node is not None:
            old_value = node.value
            node.value = value
            return key, old_value

        # 创建节点
        node = SkipNode(level=self._random_level(), key=key, value=value)
        # 设置当前最大层级
        self.max_level = max(self.max_level, len(node.forward))
        # 如果SkipNode的forward数组小于head的forward数组，需要同步到一样大
        while len(self.head.forward) < len(node.forward):
            self.head.forward.append(None)
        update = [None] * self.max_level
        x = self.head
        # 搜索key并构建update指针数组
        for i in reversed(range(self.max_level)):
            while x.forward[i] is not None and x.forward[i].key < key:
                x = x.forward[i]
            update[i] = x
        # 链表添加新指针
        for i in range(node.level):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
        self.len += 1
        return key, old_value

    def delete(self, key):
        """
        删除元素
        :param key:
        :return:
        """
        update = [None] * self.max_level
        x = self.head
        # 搜索key并构建update指针数组
        for i in reversed(range(self.max_level)):
            while x.forward[i] is not None and x.forward[i].key < key:
                x = x.forward[i]
            update[i] = x
        if len(x.forward) > 0 and x.forward[0] is not None and x.forward[0].key == key:
            # key值相同，删除之
            for i in reversed(range(self.max_level)):
                if update[i].forward[i] is not None and update[i].forward[i].key != key:
                    continue
                update[i].forward[i] = x.forward[0].forward[i]
            # 层次调整
            while self.max_level > 0 and self.head.forward[self.max_level - 1] is None:
                self.max_level -= 1
            self.len -= 1

    def search(self, key):
        """
        搜索元素
        :param key:
        :return:
        """
        x = self._internal_search(key)
        if x is None:
            return None
        else:
            return x.value

    def _internal_search(self, key):
        """
        搜索元素
        :param key:
        :return:返回节点对象
        """
        x = self.head
        for i in reversed(range(self.max_level)):
            while x.forward[i] is not None and x.forward[i].key < key:
                x = x.forward[i]
        if len(x.forward) == 0:
            return None
        x = x.forward[0]
        if x is not None and x.key == key:
            return x
        return None

    @staticmethod
    def _random_level():
        """
        随机level生成器
        :return:
        """
        level = 1
        while randint(1, 2) != 1 and level < SkipList.MAX_LEVEL:
            level += 1
        return level

    # python map的内置方法实现 BEGIN
    def __len__(self):
        return self.len

    def __setitem__(self, key, value):
        self.insert(key=key, value=value)

    def __getitem__(self, key):
        return self.search(key)

    def __delitem__(self, key):
        self.delete(key)

    # python map的内置方法实现 END

    def dump(self, desc):
        print("===============DUMP(%s)===============" % desc)
        print("list len:%d" % len(self))
        print("max level:%d" % self.max_level)
        for i in reversed(range(self.max_level)):
            x = self.head
            line = "|%d|" % i
            while x.forward[i] is not None:
                line += "-->|%s(v:%s, lv:%d)|" % (x.forward[i].key, x.forward[i].value, x.forward[i].level)
                x = x.forward[i]
            line += "-->|None|"
            print(line)
        print("=================%s=================" % ("=" * (len(desc) + 2)))


if __name__ == "__main__":
    print("%s / %s" % ("skip", "prob"))
    skip_list = SkipList()
    # print("search key:%s, value:%s" % ("s4", skip_list.search("s4")))
    print("insert key:%s, value:%s" % skip_list.insert("s1", "s1"))
    print("insert key:%s, value:%s" % skip_list.insert("s2", "s2"))
    print("insert key:%s, value:%s" % skip_list.insert("s3", "s3"))
    skip_list["s3"] = "s3_setitem"
    print("insert key:%s, value:%s" % skip_list.insert("s3", "s3_1"))
    print("insert key:%s, value:%s" % skip_list.insert("s3", "s3_2"))
    print("insert key:%s, value:%s" % skip_list.insert("s3", "s3_3"))
    print("insert key:%s, value:%s" % skip_list.insert("s4", "s422"))
    print("insert key:%s, value:%s" % skip_list.insert("s4", "s4_2"))
    print("insert key:%s, value:%s" % skip_list.insert("s4", "s4_3"))
    print("search key:%s, value:%s" % ("s4", skip_list.search("s4")))
    print("search key:%s, value:%s" % ("s3", skip_list["s4"]))
    skip_list.dump("Insert")
    del skip_list["s1"]
    skip_list.delete("s2")
    skip_list.dump("Delete")