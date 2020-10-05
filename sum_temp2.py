#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:41:59 2020

@author: mike
"""


def position_landscape_to_slope_landscape(a):
    out = []
    for ((x0, y0), (x1, y1)) in zip(a, a[1:]):
        m = (y1 - y0) / (x1 - x0)
        out.append((x0, m))
    out.append((a[-1][0], 0))
    return out
 
def slope_landscape_to_position_landscape(a):
    out = [(a[0][0], 0)]
    for ((x0, m0), (x1, _)) in zip(a, a[1:]):
        y0 = out[-1][1]
        y1 = y0 + (x1 - x0) * m0
        out.append((x1, y1))
    return out
 
def sum_slope_landscapes(a, b):
    assert a[-1][1] == 0
    assert b[-1][1] == 0
 
    out = []
    am, bm = 0, 0
    while len(a) > 0 or len(b) > 0:
        # if a is empty or b comes earlier...
        if len(a) == 0 or (len(a) > 0 and len(b) > 0 and a[0][0] > b[0][0]):
            # then deal with b.
            bx, bm = b[0]
            b = b[1:]
            out.append((bx, am + bm))
        # if b is empty or a comes earlier...
        elif len(b) == 0 or (len(a) > 0 and len(b) > 0 and a[0][0] < b[0][0]):
            # then deal with a.
            ax, am = a[0]
            a = a[1:]
            out.append((ax, am + bm))
        # the only remaining option is ax = bx.
        else:
            ax, am = a[0]
            bx, bm = b[0]
            a, b = a[1:], b[1:]
            assert ax == bx
            out.append((ax, am + bm))
 
        # not strictly necessary, but produces minimal landscapes
        if len(out) > 2 and out[-1][1] == out[-2][1]:
            out.pop()
 
    return out

A = [ [0,0], [4,2], [5,1.5], [7, 2.5], [9, 0] ]
B = [ [1,0], [2,2], [3,3], [6, 1.5], [8,0]]

AA = position_landscape_to_slope_landscape(A)
BB = position_landscape_to_slope_landscape(B)

ff = sum_slope_landscapes(AA, BB)

fff = slope_landscape_to_position_landscape(ff)
