# -*- coding = utf-8 -*-
# @Time :2020/11/13 12:22 上午
# @Author: XZL
# @File : wolf_colony.py
# @Software: PyCharm
import numpy as np
from artificial_wolf import artificial_wolf


class wolf_colony(artificial_wolf):

    def __init__(self, min_d, max_d, Xsize, wolf_num, alpha, S):
        self.lead_wolf = artificial_wolf(min_d, max_d, Xsize)
        self.you_wolfs
        self.meng_wolfs
