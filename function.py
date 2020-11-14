# -*- coding = utf-8 -*-
# @Time :2020/11/12 8:20 下午
# @Author: XZL
# @File : function.py
# @Software: PyCharm
from mpl_toolkits.mplot3d import Axes3D
import math as m
import numpy as np
from matplotlib import pyplot as plt


def func1(x):
    return 11 * m.sin(6 * x) + 7 * m.cos(5 * x)


def func2(X):
    if X.ndim == 1:
        X = np.reshape(X, (1,) + X.shape)
        # print(id(X))
    res = np.zeros((X.shape[0]))

    for i in range(0, X.shape[0]):
        x1 = X[i][0]
        x2 = X[i][1]
        res[i] = 0.26 * (pow(x1, 2) + pow(x2, 2)) + 0.5 * x1 * x2
        # res[i] = -m.cos(x1) * m.cos(x2) * m.exp(-pow((x1 - m.pi), 2) - pow((x2 - m.pi), 2))
        # res[i] = 4 * pow(x1, 2) - 2.1 * pow(x1, 4) + (1 / 3) * pow(x1, 6) + x1 * x2 - 4 * pow(x2, 2) + 4 * pow(x2, 4)
        # res[i] = x1 + x2
    return res


def find_index(value, wolf_colony):
    ret = np.zeros((len(value), 2))

    for i in range(0, len(value)):
        ret[i][0] = wolf_colony.index(value[i])
        ret[i][1] = value[i]
    return ret


fig = plt.figure()
ax = Axes3D(fig)
x = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
y = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
X, Y = np.meshgrid(x, y)  # 网格的创建，这个是关键
Z = np.sin(X) * np.cos(Y)
plt.xlabel('x')
plt.ylabel('y')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
# plt.show()
