# -*- coding = utf-8 -*-
# @Time :2020/11/12 7:47 下午
# @Author: XZL
# @File : WPA.py
# @Software: PyCharm
import math as m
import numpy as np
import function
import heapq

α = 4  # 探狼比例因子
β = 6  # 狼群更新比例因子
ω = 500  # 距离判定因子
S = 1000  # 步长因子
T_max = 30  # 最大游走次数
wolf_num = 50  # 狼群数量
max_iteration = 300  # 最大迭代次数
number_T = np.random.randint(wolf_num / (α + 1), wolf_num / α)  # 探狼数量

# 待寻优变量的取值范围
min_d = -200
max_d = 200

# 探狼探寻方向
h_max = 15
h_min = 2

step_a = (max_d - min_d) / S  # 探狼游走步长
step_b = 2 * step_a  # 猛狼奔袭步长
step_c = step_a / 2  # 围攻步长

Xsize = 6  # 维度(方程的参数维度)

# 初始化狼群以及计算猎物浓度(取值范围均匀分布)
wolf_colony_X = np.random.uniform(min_d, max_d, (wolf_num, Xsize))

# 迭代 每次迭代都是完整一次狼群行为
for it in range(0, max_iteration):
    print("------开始第 %d 次迭代--------" % (it + 1))

    wolf_colony_V = function.func6(wolf_colony_X)
    # 初始化头狼
    L_Wolf_V = np.min(wolf_colony_V)
    L_Wolf_index = np.argmin(wolf_colony_V)
    L_Wolf_X = wolf_colony_X[L_Wolf_index]
    L_Wolf = [L_Wolf_V, L_Wolf_index]
    print(" > 初始化头狼:%f" % L_Wolf_V)
    # 初始化探狼
    T_Wolf_V = heapq.nsmallest(number_T, wolf_colony_V.copy())
    T_Wolf = function.find_index(T_Wolf_V, wolf_colony_V.tolist())  # 0:探狼在狼群中位置 1:解
    # 初始化猛狼
    M_Wolf_V = heapq.nlargest(wolf_num - number_T - 1, wolf_colony_V.copy())
    M_Wolf = function.find_index(M_Wolf_V, wolf_colony_V.tolist())  # 0:探狼在狼群中位置 1:解

    # 探狼开始游走
    for i in range(0, T_Wolf.shape[0]):
        H = np.random.randint(h_min, h_max)  # 尝试的方向
        single_T_Wolf = wolf_colony_X[int(T_Wolf[i][0])]  # 当前探狼
        optimum_value = T_Wolf[i][1]  # 解
        optimum_position = single_T_Wolf.copy()
        find = False

        # 探狼游走行为 一旦探狼发现目标 -> 开始召唤
        for t in range(0, T_max):

            # 在初始位置朝H个方向试探，直到找到一个优解
            for p in range(1, H + 1):
                single_T_Wolf_trial = single_T_Wolf.copy()
                # single_T_Wolf_trial = single_T_Wolf_trial + int(m.cos(m.pi * p / H)) * step_a
                single_T_Wolf_trial = single_T_Wolf_trial + np.random.uniform(-1, 1,
                                                                              (single_T_Wolf_trial.shape[0],)) * step_a

                single_T_Wolf_V = function.func6(single_T_Wolf_trial)[0]

                # 探狼转变为头狼
                if L_Wolf_V > single_T_Wolf_V:
                    find = True
                    L_Wolf_V = single_T_Wolf_V  # 更新头狼解
                    L_Wolf_X = single_T_Wolf_trial
                    L_Wolf_index = int(T_Wolf[i][0])  # 更新头狼下标
                    wolf_colony_X[L_Wolf_index] = single_T_Wolf_trial  # 更新头狼位置参数

                    T_Wolf = np.delete(T_Wolf, i, axis=0)  # 探狼转为头狼，发起召唤，删除探狼
                    break

                elif optimum_value > single_T_Wolf_V:
                    optimum_value = single_T_Wolf_V
                    optimum_position = single_T_Wolf_trial

            else:
                print(" > 第%d只探狼完成第%d游走,未发现猎物" % ((i + 1), (t + 1)))
                # 记录上次的最优位置
                single_T_Wolf = optimum_position

            if find is True:
                break

        if find is True:
            print("第%d只探狼发现猎物 %f" % (i, single_T_Wolf_V))
            break

        else:
            # 若游走完成探狼没找到猎物，更新所有游走过程中最优的一次位置
            wolf_colony_X[int(T_Wolf[i][0])] = optimum_position

    d_near = (1 / (1 * ω)) * Xsize * (max_d - min_d)  # dnear值，判定距离

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
                single_M_Wolf_V = function.func6(single_M_Wolf)[0]

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
                ready += 1  # 围攻就绪态+1
            else:
                break

        # 所有猛狼是否就位
        if ready == M_Wolf.shape[0]:
            print(" > 所有猛狼已进入围攻状态")
            break

    # 围攻行为
    for m in range(0, M_Wolf.shape[0]):
        s_m_index = int(M_Wolf[m][0])
        single_M_Wolf = wolf_colony_X[s_m_index]
        # 发起围攻，计算围攻后位置
        single_M_Wolf = single_M_Wolf + np.random.uniform(-1, 1) * step_c * np.abs(L_Wolf_X - single_M_Wolf)
        single_M_Wolf_V = function.func6(single_M_Wolf)[0]

        if L_Wolf_V > single_M_Wolf_V:
            print(" > 发起围攻!目标更新 原值:%f 现值:%f" % (L_Wolf_V, single_M_Wolf_V))
            # 头狼变猛狼
            M_Wolf[m][0] = L_Wolf_index
            M_Wolf[m][1] = L_Wolf_V
            wolf_colony_X[L_Wolf_index] = L_Wolf_X

            # 猛狼变头狼
            L_Wolf_V = single_M_Wolf_V
            L_Wolf_X = single_M_Wolf
            L_Wolf_index = s_m_index
            wolf_colony_X[L_Wolf_index] = single_M_Wolf
    print(" > 围攻完成")

    # 强者生存行为
    wolf_colony_V = function.func6(wolf_colony_X)  # 重新计算现在所有狼狩猎的状态
    eliminate_number = np.random.randint(wolf_num / (2 * β), wolf_num / β)
    Bad_Wolf_V = heapq.nlargest(eliminate_number, wolf_colony_V.copy())
    Bad_Wolf = function.find_index(Bad_Wolf_V, wolf_colony_V.tolist())
    # 生成新的人工狼
    new_wolf = np.random.uniform(min_d, max_d, (eliminate_number, Xsize))
    # 淘汰最弱的狼
    for n in range(0, len(Bad_Wolf_V)):
        wolf_colony_X[int(Bad_Wolf[n][0])] = new_wolf[n]

    print(wolf_colony_X[L_Wolf_index])
    print(" > 头狼:%f" % L_Wolf_V)
