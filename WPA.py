# -*- coding = utf-8 -*-
# @Time :2020/11/12 7:47 下午
# @Author: XZL
# @File : WPA.py
# @Software: PyCharm
import math as m
import numpy as np
import function
import heapq

wolf_num = 20  # 狼群数量
max_iteration = 300  # 最大迭代次数
α = 4  # 探狼比例因子
β = 6  # 狼群更新比例因子
T_max = 30  # 最大游走次数
ω = 500  # 距离判定因子
S = 1000  # 步长因子
number_T = np.random.randint(wolf_num / (α + 1), wolf_num / α)  # 探狼数量

# 带寻优变量的取值范围
min_d = -5
max_d = 5

# 探狼探寻方向
h_max = 15
h_min = 2

step_a = (max_d - min_d) / S  # 探狼游走步长
step_b = 2 * step_a  # 猛狼奔袭步长
step_c = step_a / 2  # 围攻步长

# 维度(每只人工狼的参数)
Xsize = 2

# 初始化狼群以及计算猎物浓度
wolf_colony_X = np.random.uniform(min_d, max_d, (wolf_num, Xsize))
wolf_colony_Y = function.func2(wolf_colony_X)

# 初始化头狼
L_Wolf_V = np.min(wolf_colony_Y)
L_Wolf_index = np.argmin(wolf_colony_Y)
L_Wolf_X = wolf_colony_X[L_Wolf_index]
L_Wolf = [L_Wolf_V, L_Wolf_index]
print("头狼:%f" % L_Wolf_V)
# 初始化探狼
T_Wolf_V = heapq.nsmallest(number_T, wolf_colony_Y.copy())
T_Wolf = function.find_index(T_Wolf_V, wolf_colony_Y.tolist())  # 0:群中下标 1:解
# 初始化猛狼
M_Wolf_V = heapq.nlargest(wolf_num - number_T - 1, wolf_colony_Y.copy())
M_Wolf = function.find_index(M_Wolf_V, wolf_colony_Y.tolist())  # 0:群中下标 1:解

# 发起召唤的狼


# 迭代 执行几次
for it in range(0, max_iteration):

    for i in range(0, T_Wolf.shape[0]):  # 从第一头探狼开始
        H = np.random.randint(h_min, h_max)  # 当前探狼每次尝试的方向
        single_T_Wolf = wolf_colony_X[int(T_Wolf[i][0])]  # 变量
        optimum_value = T_Wolf[i][1]  # 解
        optimum_position = single_T_Wolf.copy()
        find = False

        # 探狼游走行为
        for t in range(0, T_max):

            for p in range(1, H + 1):
                single_T_Wolf_trial = single_T_Wolf.copy()  # 每次在初始位置朝H个方向试探，直到找到一个优解
                # single_T_Wolf_trial = single_T_Wolf_trial + m.cos(m.pi * p / H) * step_a
                single_T_Wolf_trial = single_T_Wolf_trial + np.random.uniform(-1, 2,
                                                                              (single_T_Wolf_trial.shape[0],)) * step_a

                single_T_Wolf_V = function.func2(single_T_Wolf_trial)[0]

                # 探狼转变为头狼
                if L_Wolf_V > single_T_Wolf_V:
                    find = True
                    L_Wolf_V = single_T_Wolf_V  # 更新头狼解
                    L_Wolf_X = single_T_Wolf_trial
                    L_Wolf_index = int(T_Wolf[i][0])  # 更新头狼下标
                    wolf_colony_X[L_Wolf_index] = single_T_Wolf_trial  # 更新头狼位置参数

                    break

                elif optimum_value > single_T_Wolf_V:
                    optimum_value = single_T_Wolf_V
                    optimum_position = single_T_Wolf_trial
            else:
                print("探狼完成第%d游走,未找到猎物" % (t + 1))
                single_T_Wolf = optimum_position

            if find is True:
                break

        if find is True:
            print("探狼发现猎物 %f" % single_T_Wolf_V)
            break

    d_near = (1 / (Xsize * ω)) * Xsize * (max_d - min_d)  # dnear值，判定距离

    # 召唤行为
    surrounded = False
    # 所有猛狼进入围攻范围才能结束
    while ~surrounded:
        ready = 0
        for m in range(0, M_Wolf.shape[0]):
            s_m_index = int(M_Wolf[m][0])  # 猛狼在狼群中下标
            single_M_Wolf = wolf_colony_X[s_m_index]  # 猛狼变量
            d = np.abs(L_Wolf_X - single_M_Wolf)
            dd = np.sum(d)

            while d_near < dd:
                single_M_Wolf = single_M_Wolf + step_b * (L_Wolf_X - single_M_Wolf) / np.abs(L_Wolf_X - single_M_Wolf)
                single_M_Wolf_V = function.func2(single_M_Wolf)[0]

                # 更新猛狼位置
                wolf_colony_X[s_m_index] = single_M_Wolf
                M_Wolf[m][1] = single_M_Wolf_V

                d = np.abs(L_Wolf_X - single_M_Wolf)
                dd = np.sum(d)

                if L_Wolf_V > single_M_Wolf_V:
                    # 头狼变猛狼
                    M_Wolf[m][0] = L_Wolf_index
                    M_Wolf[m][1] = L_Wolf_V
                    wolf_colony_X[L_Wolf_index] = L_Wolf_X

                    # 猛狼变头狼
                    L_Wolf_V = single_M_Wolf_V
                    L_Wolf_X = single_M_Wolf
                    L_Wolf_index = s_m_index
                    wolf_colony_X[L_Wolf_index] = single_M_Wolf
                    break

            if d_near > dd:
                ready += 1  # 围攻就绪态
            else:
                break

        if ready == M_Wolf.shape[0]:
            print("所有猛狼已进入围攻状态")
            break

    # 围攻行为
    # for

    # 一次结束后，去掉wolf_colony_X中最后的几个狼，生成新的人工狼
    # 重新分配头狼、探狼、猛狼

    print(wolf_colony_X[L_Wolf_index])
    print(L_Wolf_V)
print("111")
