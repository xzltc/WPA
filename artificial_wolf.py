# -*- coding = utf-8 -*-
# @Time :2020/11/12 8:37 下午
# @Author: XZL
# @File : artificial_wolf.py
# @Software: PyCharm
import numpy as np


class artificial_wolf:
    def __init__(self, mind, maxd, Xsize):
        self.X_size = Xsize  # 有几个参数
        self.X_position = np.random.uniform(mind, maxd, Xsize)  # 初始化参数
        self.Y = None  # 人工狼闻到猎物的浓度 Y=f(X)

    def X(self):
        return self.X_position

    def Y(self):
        return self.Y


aw = artificial_wolf(5)
print(aw.X())
