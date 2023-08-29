import itertools
from time import *
from sys import *
import easygui as g
import os
s = sleep

def yd_one_print(text,f):
    stdout.write("\r"+""*60+"\r")
    stdout.flush()
    for i in text:
        stdout.write(i)
        stdout.flush()
        s(f)
def twenty_two_p(a,b,c,d):
    class CardGaming:
        def __init__(self):
            self.formula_list = list()
            for marks in itertools.product(["+", "-", "*", "/"], repeat=3):
                for bracket in ["{0}%s{1}%s{2}%s{3}", "({0}%s{1})%s{2}%s{3}", "({0}%s{1}%s{2})%s{3}",
                                "{0}%s({1}%s{2})%s{3}",
                                "{0}%s({1}%s{2}%s{3})", "({0}%s{1})%s({2}%s{3})", "{0}%s{1}%s({2}%s{3})"]:
                    self.formula_list.append((bracket % marks))
     
        def solve(self, card_probability):
            answer = []
            for card_order in set(itertools.permutations(card_probability, 4)):
                for formula in self.formula_list:
                    final_formula = formula.format(*card_order)
                    try:
                        if round(eval(final_formula), 3) == 24:
                            answer.append(final_formula)
                    except ZeroDivisionError:
                        continue
            return answer
    print(CardGaming().solve((a,b, c, d)))
def yd_help():
    yd_one_print('''共21个功能                        
    twenty_two(a,b,c,d)为求24点abcd为四个数值中间要加英文逗号,                  yd_zs()求质数括号内求范围,                                      
    yd_one_print(text,time)文字一个一个输出括号里先填文字（字符串）后面逗号写间隔                            yd_zhengchu(a,b)a能否整除b(没啥用)          
    yd_pf(a)求a的平方                                                            yd_cf(a,b)求a的b次方                                                yd_abs(a)求a的绝对值                                     
    yd_d_qz(a)a向下取整                   yd_u_qz(a)a向上取整                yd_sswr(a)四舍五入                                               
    功能为返回值，加上_p为print出来                       
    yd_cont(a,b)a为列表，b为字符串or数值求b在a里重复出现了几次                               
    yd_clear_win()清屏（windows系统）                                       
    yd_clear_mac()清屏（mac系统）''',0.05)
def yd_zs_p(aaa):
    qqq = 0
    for i in range(2,aaa):
        kkk = 0
        for j in range(1,i+1):
            if i % j == 0:
                kkk += 1
        if kkk == 2:
            nnuumm.append(i)
    nnuumm2.append(nnuumm[0])
    for x in nnuumm:
        if x == nnuumm2[-1]:
            qqq += 1
        else:
            nnuumm2.append(x)
    print(nnuumm2)
    print(len(nnuumm2))

def yd_zs(aaa):
    qqq = 0
    for i in range(2,aaa):
        kkk = 0
        for j in range(1,i+1):
            if i % j == 0:
                kkk += 1
        if kkk == 2:
            nnuumm.append(i)
    nnuumm2.append(nnuumm[0])
    for x in nnuumm:
        if x == nnuumm2[-1]:
            qqq += 1
        else:
            nnuumm2.append(x)
    return nnuumm2
def yd_zhengchu_p(yd_zhenchu,ydzhenchu):
    if yd_zhenchu % ydzhenchu == 0:
        print("Yes")
    else:
        print("No")
def yd_zhengchu_yn(yd_zhenchu,ydzhenchu):
    if yd_zhenchu % ydzhenchu == 0:
        return "Yes"
    else:
        return "No"
def yd_zhengchu_tf(yd_zhenchu,ydzhenchu):
    if yd_zhenchu % ydzhenchu == 0:
        return True
    else:
        return False

def yd_pf_p(ydaaaaa):
    print(ydaaaaa*ydaaaaa)
def yd_pf(ydaaaaa):
    return ydaaaaa*ydaaaaa
def yd_cf_p(ydaaaaaa,ydaaaaaa2):
    ydaaaaaa3 = ydaaaaaa
    for ydaaaaaaforzy in range(ydaaaaaa2-1):
        ydaaaaaa = ydaaaaaa * ydaaaaaa3
    print(ydaaaaaa)
def yd_cf(ydaaaaaa,ydaaaaaa2):
    ydaaaaaa3 = ydaaaaaa
    for ydaaaaaaforzy in range(ydaaaaaa2-1):
        ydaaaaaa = ydaaaaaa * ydaaaaaa3
    return ydaaaaaa
def twenty_two(a,b,c,d):
    class CardGaming:
        def __init__(self):
            self.formula_list = list()
            for marks in itertools.product(["+", "-", "*", "/"], repeat=3):
                for bracket in ["{0}%s{1}%s{2}%s{3}", "({0}%s{1})%s{2}%s{3}", "({0}%s{1}%s{2})%s{3}",
                                "{0}%s({1}%s{2})%s{3}",
                                "{0}%s({1}%s{2}%s{3})", "({0}%s{1})%s({2}%s{3})", "{0}%s{1}%s({2}%s{3})"]:
                    self.formula_list.append((bracket % marks))
     
        def solve(self, card_probability):
            answer = []
            for card_order in set(itertools.permutations(card_probability, 4)):
                for formula in self.formula_list:
                    final_formula = formula.format(*card_order)
                    try:
                        if round(eval(final_formula), 3) == 24:
                            answer.append(final_formula)
                    except ZeroDivisionError:
                        continue
            return answer
    return (CardGaming().solve((a,b, c, d)))
def yd_abs(num):
    if num < 0:
        num_j = num * -1
    elif num > 0:
        num_j = num
    elif num == 0:
        num_j = 0
    return num_j
def yd_abs_p(num):
    if num < 0:
        num_j = num * -1
    elif num > 0:
        num_j = num
    elif num == 0:
        num_j = 0
    print(num_j)
def yd_d_qz(aaa):
    return aaa - (aaa - int(aaa))
def yd_d_qz_p(aaa):
    print(aaa - (aaa - int(aaa)))
def yd_u_qz(aaa):
    return aaa - (aaa - int(aaa)) + 1
def yd_u_qz_p(aaa):
    print(aaa - (aaa - int(aaa)) + 1)
def yd_sswr(aaa):
    if(aaa - int(aaa) <= 0.4):
        return aaa - (aaa - int(aaa))
    else:
        return aaa - (aaa - int(aaa))+1

def yd_sswr_p(aaa):
    if(aaa - int(aaa) <= 0.4):
        print(aaa - (aaa - int(aaa)))
    else:
        print(aaa - (aaa - int(aaa))+1)
def yd_cont(lb,zf):
    ydcnt = 0
    for fw in lb:
        if fw == zf:
            ydcnt += 1
    return ydcnt
def yd_cont_p(lb,zf):
    ydcnt = 0
    for fw in lb:
        if fw == zf:
            ydcnt += 1
    print(ydcnt)
def yd_clear_win():
    os.system('cls')
def yd_clear_mac():
    os.system('clear')