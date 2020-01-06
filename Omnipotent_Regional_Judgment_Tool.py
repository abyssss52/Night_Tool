#! /usr/bin/env python
# coding=utf-8
#================================================================
#
#   Editor      : Pycharm
#   File name   : Omnipotent_Regional_Judgment_Tool.py
#   Author      : night
#   Description : 用于判断点与区域的位置关系函数(目前已有算法：射线法)
#   Date        : 2020.01.06
#
#================================================================

def Ray_Segment(point, point_s, point_e):
    '''
    判断射线与多边形边的相对位置关系
    :param point: 要被判断的目标点，也是该方法的射线起点  eg. [(x1,y1),(x2,y2)]
    :param point_s: 多边形的边的假定起点  eg. (x1,y1)
    :param point_e: 多边形的边的假定结束点  eg. (x1,y1)
    :return: True or False: 表示是否point发出的射线与多边形的边相交
    '''
    # 排除多边形边是水平的情况，该情况下，射线有可能与多边形的边平行，重叠或者多边形这条边实着为一个点
    if point_s[1] == point_e[1]:
        return False

    # 排除射线在多边形边的下方
    if point_s[1] > point[1] and point_e[1] > point[1]:
        return False

    # 排除射线在多边形边的上方
    if point_s[1] < point[1] and point_e[1] < point[1]:
        return False

    # 排除多边形边的起点在射线上
    if point_s[1] == point[1] and point_e[1] > point[1]:
        return False

    # 排除多边形边的结束点在射线上
    if point_e[1] == point[1] and point_s[1] > point[1]:
        return False

    # 排除多边形的边完全在射线左侧
    if point_s[0] < point[0] and point_e[0] < point[0]:
        return False

    # 求射线与多边形边的交点
    intersec_point = point_e[0] - (point_e[0] - point_s[0]) * (point_e[1] - point[1]) / (point_e[1] - point_s[1])
    if intersec_point < point[0]:
        return False

    return True


def Point_in_Ploy(point, poly):
    '''
    判断点是否在多边形内 （单向射线法）
    :param point: 要被判断的目标点  eg. (x1,y1)
    :param poly: 多边形的坐标点集合  eg. [[x1,y1], [x2,y2], [x3,y3],[x1,y1]] 一个多边形  [[[x1,y1], [x2,y2], [x3,y3],[x1,y1]],[[],[],[],[],[]]]  多个多边形
    :return: True or False: 表示point是否在多边形内
    '''

    intersec_num = 0   # 交点数
    for each_poly in poly:
        for i in range(len(each_poly)-1):
            point_s = each_poly[i]
            point_e = each_poly[i+1]
            if Ray_Segment(point, point_s, point_e):
                intersec_num += 1

        # 验证多边形最后一个点与第一个点组成的边
        point_s = each_poly[-1]
        point_e = each_poly[0]
        if Ray_Segment(point, point_s, point_e):
            intersec_num += 1

    return True if intersec_num % 2 == 1 else False