#!/usr/bin/python

import sys
import os
import numpy as np
import copy
import random

cards_in_hands = []
status = [[] for i in range(9)]
r_status = [[] for i in range(9)]
#global_status = {}
#global_color = {'A': 0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0}
#global_number = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
real_global_status = np.ones((6, 10), dtype='int32') * -1
def main():
    global cards_in_hands, real_global_status, status, r_status
    while True:
        n = int(sys.stdin.readline())
        #sys.stderr.write("demo %d n: %d\n" % (os.getpid(), n))
        over = False
        for i in range(n):
            cmd = sys.stdin.readline()
            #sys.stderr.write("demo %d cmd: " % os.getpid()+ cmd)
            items = cmd.split()
            if items[0] == 'cardget':
                cards_in_hands.append(items[1])
                real_global_status[ord(items[1][0]) - ord('A'), int(items[1][1:])-1] = 1
            elif items[0] == 'rival':
                r_status[int(items[1])].append(items[2])
                real_global_status[ord(items[2][0]) - ord('A'), int(items[2][1:])-1] = 0
            else:
                over = True
        if over:
            break
        else:
            max_priority = 0
            region = 0
            for i in range(9):
                if len(status[i])<3 and len(status[i]) >= 1 and len(r_status[i]) >= 2:
                    priority, card = compute_priority(copy.deepcopy(status[i]), copy.deepcopy(r_status[i]))
                    if max_priority < priority:
                        max_priority = priority
                        region = i
            if max_priority >= 4:
                sys.stdout.write("act %d %s\n" % (region, card))
                sys.stdout.flush()
                status[region].append(card)
                real_global_status[ord(card[0]) - ord('A'), int(card[1:])-1] = 0
                cards_in_hands.remove(card) 
            else:
                acted = False
                idx = 0
                for i in range(9):
                    if len(status[i]) == 2:
                        for card in cards_in_hands:
                            r1 = copy.deepcopy(status[i])
                            r1.append(card)
                            lev = judge_level(r1)
                            r1.remove(card)
                            if lev == 5:
                                sys.stdout.write("act %d %s\n" % (i, card))
                                sys.stdout.flush()
                                status[i].append(card) 
                                real_global_status[ord(card[0]) - ord('A'), int(card[1:])-1] = 0
                                cards_in_hands.remove(card) 
                                acted = True
                                break
                        if acted:
                            break
                if acted == False:
                    for i in range(9):
                        if len(status[i]) == 2:
                            for card in cards_in_hands:
                                r1 = copy.deepcopy(status[i])
                                r1.append(card)
                                lev = judge_level(r1)
                                r1.remove(card)
                                if lev == 4:
                                    sys.stdout.write("act %d %s\n" % (i, card))
                                    sys.stdout.flush()
                                    status[i].append(card) 
                                    real_global_status[ord(card[0]) - ord('A'), int(card[1:])-1] = 0
                                    cards_in_hands.remove(card) 
                                    acted = True
                                    break
                            if acted:
                                break
                if acted == False:
                    for i in range(9):
                        if len(status[i]) == 2:
                            for card in cards_in_hands:
                                r1 = copy.deepcopy(status[i])
                                r1.append(card)
                                lev = judge_level(r1)
                                r1.remove(card)
                                if lev == 3:
                                    sys.stdout.write("act %d %s\n" % (i, card))
                                    sys.stdout.flush()
                                    status[i].append(card) 
                                    real_global_status[ord(card[0]) - ord('A'), int(card[1:])-1] = 0
                                    cards_in_hands.remove(card) 
                                    acted = True
                                    break
                            if acted:
                                break
                if acted == False:
                    for i in range(9):
                        if len(status[i]) == 1:
                            for card in cards_in_hands:
                                r1 = copy.deepcopy(status[i])
                                r1.append(card)
                                my_level = compute_prob_2_card(r1, real_global_status)
                                r1.remove(card)
                                if my_level[5] + my_level[4] + my_level[3] > 0.2:
                                    sys.stdout.write("act %d %s\n" % (i, card))
                                    sys.stdout.flush()
                                    status[i].append(card)
                                    real_global_status[ord(card[0]) - ord('A'), int(card[1:])-1] = 0
                                    cards_in_hands.remove(card) 
                                    acted = True
                                    break
                            if acted:
                                break
                if acted == False:
                    for i in range(9):
                        if len(status[i]) == 0 and len(r_status[i]) == 3:
                            lev = judge_level(r_status[i])
                            numbers = [int(card[1:]) for card in cards_in_hands]
                            if lev >= 4:
                                idx = numbers.index(min(numbers))
                                sys.stdout.write("act %d %s\n" % (i, cards_in_hands[idx]))
                                sys.stdout.flush()
                                status[i].append(cards_in_hands[idx])   
                                real_global_status[ord(cards_in_hands[idx][0]) - ord('A'), int(cards_in_hands[idx][1:])-1] = 0
                                cards_in_hands.remove(cards_in_hands[idx]) 
                            else:
                                idx = numbers.index(max(numbers))
                                sys.stdout.write("act %d %s\n" % (i, cards_in_hands[idx]))
                                sys.stdout.flush()
                                status[i].append(cards_in_hands[idx])   
                                real_global_status[ord(cards_in_hands[idx][0]) - ord('A'), int(cards_in_hands[idx][1:])-1] = 0
                                cards_in_hands.remove(cards_in_hands[idx]) 
                            acted = True
                            break
                if acted == False:
                    for i in range(9):
                        if len(status[i])==0 and len(r_status[i]) == 2:
                            r2 = copy.deepcopy(r_status[i])
                            rival_level = compute_prob_2_card(r2, real_global_status)
                            if rival_level[5] + rival_level[4] + rival_level[3] < 0.2:
                                numbers = [int(card[1:]) for card in cards_in_hands]
                                idx = numbers.index(max(numbers))
                                sys.stdout.write("act %d %s\n" % (i, cards_in_hands[idx]))
                                sys.stdout.flush()
                                status[i].append(cards_in_hands[idx])   
                                real_global_status[ord(cards_in_hands[idx][0]) - ord('A'), int(cards_in_hands[idx][1:])-1] = 0
                                cards_in_hands.remove(cards_in_hands[idx]) 
                                acted = True
                                break
                if acted == False:
                    for i in range(9):
                        if len(status[i]) == 0 and len(r_status[i]) == 0:
                            numbers = [int(card[1:]) for card in cards_in_hands]
                            idx = numbers.index(max(numbers))
                            sys.stdout.write("act %d %s\n" % (i, cards_in_hands[idx]))
                            sys.stdout.flush()
                            status[i].append(cards_in_hands[idx])   
                            real_global_status[ord(cards_in_hands[idx][0]) - ord('A'), int(cards_in_hands[idx][1:])-1] = 0
                            cards_in_hands.remove(cards_in_hands[idx]) 
                            acted = True
                            break
                if acted == False:
                    numbers = [int(card[1:]) for card in cards_in_hands]
                    idx = numbers.index(max(numbers))
                    for i in range(9):
                        if len(r_status[i]) == 0 and len(status[i]) < 3:
                            sys.stdout.write("act %d %s\n" % (i, cards_in_hands[idx]))
                            sys.stdout.flush()
                            status[i].append(cards_in_hands[idx])
                            real_global_status[ord(cards_in_hands[idx][0]) - ord('A'), int(cards_in_hands[idx][1:])-1] = 0
                            cards_in_hands.remove(cards_in_hands[idx]) 
                            acted = True
                            break
                if acted == False:
                    numbers = [int(card[1:]) for card in cards_in_hands]
                    idx = numbers.index(max(numbers))
                    for i in range(9):
                        if len(status[i]) < 3:
                            sys.stdout.write("act %d %s\n" % (i, cards_in_hands[idx]))
                            sys.stdout.flush()
                            status[i].append(cards_in_hands[idx])
                            real_global_status[ord(cards_in_hands[idx][0]) - ord('A'), int(cards_in_hands[idx][1:])-1] = 0
                            cards_in_hands.remove(cards_in_hands[idx]) 
                            acted = True
                            break
   
def compute_priority(r1, r2):
    global cards_in_hands, real_global_status, status, r_status
    rival_level = compute_rival_level(r2)
    max_priority = -100;
    max_card = None
    if len(r1) == 3:
        pass
    elif len(r1) == 2:
        for card in cards_in_hands:
            r1.append(card)
            lev = judge_level(r1)
            if lev == 5:
                #todo
                p = 10 - 10 * rival_level[5]
            elif lev == 4:
                p = 10 - 20 * rival_level[5] - 10 * rival_level[4]
            elif lev == 3:
                p = 10 - 30 * rival_level[5] - 20 * rival_level[4] - 10 * rival_level[3]
            elif lev == 2:
                p = 10 - 40 * rival_level[5] - 30 * rival_level[4] - 20 * rival_level[3] - 10 * rival_level[2]
            else:
                p = 10 - 50 * rival_level[5] - 40 * rival_level[4] - 30 * rival_level[3] - 20 * rival_level[2] - 10 * rival_level[1]
            if len(r2)==3 and (judge_level(r2) > lev or judge_level(r2) == lev and sum_number(r1) <= sum_number(r2)):
                p = 0                
            if max_priority < p:
                max_card = card
                max_priority = p
            r1.remove(card)
    elif len(r1) == 1:
        for card in cards_in_hands:
            r1.append(card)
            my_level = compute_prob_2_card(r1, real_global_status)
            p = pk_with_rival(my_level, rival_level)
            if max_priority < p:
                max_card = card
                max_priority = p
            r1.remove(card)
    else:
        for card in cards_in_hands:
            r1.append(card)
            numbers = int(r1[0][1:])
            p = 0
            if numbers >= 7 and numbers < 10:
                if list(global_status[:, numbers - 2]).count(1) + list(global_status[:, numbers]).count(1) >= 1:
                    p = 2
                if list(global_status[char2index(r1[0][0]),:]).count(1) >= 1:
                    p = 4
                if list(global_status[:, numbers - 1]).count(1) >= 1:
                    p = 5
                if list(global_status[char2index(r1[0][0]), numbers - 2]).count(1) + list(global_status[char2index(r1[0][0]), numbers]).count(1) >= 1:
                    p = 6
            if max_priority < p:
                max_card = card
                max_priority = p
            r1.remove(card)
    return max_priority, max_card


def compute_rival_level(r):
    global cards_in_hands, real_global_status, status, r_status
    rival_prop = {5:0.0, 4:0.0, 3:0.0, 2:0.0, 1:1.0}
    if len(r) == 3:
        rival_prop[judge_level(r)] = 1
        return rival_prop
    elif len(r) == 2:
        other_global_status = copy.deepcopy(real_global_status)
        for i in range(6):
            for j in range(10):
                if other_global_status[i][j] == 1:
                    other_global_status[i][j] = 0
        return compute_prob_2_card(r[0:2], other_global_status)
    



def compute_prob_2_card(r, global_status):
    global cards_in_hands, real_global_status, status, r_status
    numbers = [int(card[1:]) for card in r]
    if numbers[0] > numbers[1]:
        r[0], r[1] = r[1], r[0]
        numbers[0], numbers[1] = numbers[1], numbers[0]
    level_prob = {5:0.0, 4:0.0, 3:0.0, 2:0, 1:1.0}
    card_num = 0
    for i in range(9):
        card_num += len(status[i])
        card_num += len(r_status[i])
    card_num += 7
    left_cards = 60 - card_num
    same_color = r[0][0] == r[1][0]
    order_numbers = numbers[1] - numbers[0] == 1 or numbers[1] - numbers[0] == 2
    same_numbers = numbers[0] == numbers[1]
    if same_color:
        if order_numbers:
            if numbers[1] - numbers[0] == 1:
                if numbers[0] == 1: #and global_status.get(r[0][0]+'3', -1) == 1 or numbers[1] == 10 and global_status.get(r[0][0]+'8', -1) == 1:
                    if global_status[char2index(r[0][0]),2] == 1:
                        level_prob[5] = 1
                        return level_prob
                    elif global_status[char2index(r[0][0]),2] == 0:
                        level_prob[5] = 0
                        if list(global_status[char2index(r[0][0]),:]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = list(global_status[char2index(r[0][0]), :]).count(-1) / float(left_cards)
                        if list(global_status[:, 2]).count(1) >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = list(global_status[:, 2]).count(-1) / float(left_cards)
                    else:
                        level_prob[5] = 1.0 / left_cards
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = (list(global_status[char2index(r[0][0]), :]).count(-1) - 1) / float(left_cards)
                        if list(global_status[:, 2]).count(1) >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = (list(global_status[:, 2]).count(-1) - 1) / float(left_cards)
                elif numbers[1] == 10:
                    if global_status[char2index(r[0][0]),7] == 1:
                        level_prob[5] = 1
                        return level_prob
                    elif global_status[char2index(r[0][0]),7] == -1:
                        level_prob[5] = 1.0 / left_cards 
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = (list(global_status[char2index(r[0][0]), :]).count(-1) - 1) / float(left_cards)
                        if list(global_status[:, 7]).count(1) >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = (list(global_status[:, 7]).count(-1) - 1) / float(left_cards)
                    else:
                        level_prob[5] = 0
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = (list(global_status[char2index(r[0][0]), :]).count(-1)) / float(left_cards)
                        if list(global_status[:, 7]).count(1) >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = (list(global_status[:, 7]).count(-1)) / float(left_cards)
                else:
                    if global_status[char2index(r[0][0]), numbers[0]-2] == 1 or global_status[char2index(r[0][0]), numbers[1]] == 1:
                        level_prob[5] = 1
                        return level_prob
                    elif global_status[char2index(r[0][0]), numbers[0]-2] == 0 and global_status[char2index(r[0][0]), numbers[1]] == -1 or \
                        global_status[char2index(r[0][0]), numbers[0]-2] == -1 and global_status[char2index(r[0][0]), numbers[1]] == 0:
                        level_prob[5] = 1.0 / left_cards
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = (list(global_status[char2index(r[0][0]), :]).count(-1) - 1)/ float(left_cards)
                        if list(global_status[:, numbers[0]-2]).count(1) + list(global_status[:, numbers[1]]).count(1)  >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = (list(global_status[:, numbers[0]-2]).count(-1) + list(global_status[:, numbers[1]]).count(-1) - 1) / float(left_cards) 
                    elif global_status[char2index(r[0][0]), numbers[0]-2] == -1 and global_status[char2index(r[0][0]), numbers[1]] == -1:
                        level_prob[5] = 2.0 / left_cards
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = (list(global_status[char2index(r[0][0]), :]).count(-1) - 2)/ float(left_cards)
                        if list(global_status[:, numbers[0]-2]).count(1) + list(global_status[:, numbers[1]]).count(1)  >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = (list(global_status[:, numbers[0]-2]).count(-1) + list(global_status[:, numbers[1]]).count(-1) - 2) / float(left_cards) 
                    else:
                        level_prob[5] = 0
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = (list(global_status[char2index(r[0][0]), :]).count(-1))/ float(left_cards)
                        if list(global_status[:, numbers[0]-2]).count(1) + list(global_status[:, numbers[1]]).count(1)  >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = (list(global_status[:, numbers[0]-2]).count(-1) + list(global_status[:, numbers[1]]).count(-1)) / float(left_cards) 
            elif numbers[1] - numbers[0] == 2:
                    if global_status[char2index(r[0][0]), numbers[0]] == 1:
                        level_prob[5] = 1
                        return level_prob
                    elif global_status[char2index(r[0][0]),numbers[0]] == 0:
                        level_prob[5] = 0
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = list(global_status[char2index(r[0][0]), :]).count(-1) / float(left_cards)
                        if list(global_status[:, numbers[0]]).count(1) >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = list(global_status[:, numbers[0]]).count(-1) / float(left_cards)
                    else:
                        level_prob[5] = 1.0 / left_cards
                        if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                            level_prob[3] = 1
                        else:
                            level_prob[3] = (list(global_status[char2index(r[0][0]), :]).count(-1) - 1) / float(left_cards)
                        if list(global_status[:, numbers[0]]).count(1) >= 1:
                            level_prob[2] = 1
                        else:
                            level_prob[2] = (list(global_status[:, numbers[0]]).count(-1) - 1) / float(left_cards)
        else:
            if list(global_status[char2index(r[0][0]), :]).count(1) >= 1:
                level_prob[3] = 1
                return level_prob
            else:
                level_prob[3] = list(global_status[char2index(r[0][0]), :]).count(-1) / float(left_cards)
    else:
        if order_numbers:
            if numbers[1] - numbers[0] == 1:
                if numbers[0] == 1:
                    if list(global_status[:, 2]).count(1) >= 1:
                        level_prob[2] = 1
                    else:
                        level_prob[2] = list(global_status[:, 2]).count(-1) / float(left_cards)
                elif numbers[1] == 10:
                    if list(global_status[:, 7]).count(1) >= 1:
                        level_prob[2] = 1
                    else:
                        level_prob[2] = list(global_status[:, 7]).count(-1) / float(left_cards) 
                else:
                    if list(global_status[:, numbers[0] - 2]).count(1) + list(global_status[:, numbers[1]]).count(1) >= 1:
                        level_prob[2] = 1
                    else:
                        level_prob[2] = list(global_status[:, numbers[0] - 2]).count(-1) + list(global_status[:, numbers[1]]).count(-1) / float(left_cards) 
            elif numbers[1] - numbers[0] == 2:
                if list(global_status[:, numbers[0]]).count(1) >= 1:
                    level_prob[2] = 1
                else:
                    level_prob[2] = list(global_status[:, numbers[0]]).count(-1) / float(left_cards)
        else:
            if same_numbers:
                if list(global_status[:, numbers[0] - 1]).count(1) >= 1:
                    level_prob[4] = 1
                else:
                    level_prob[4] = list(global_status[:, numbers[0] - 1]).count(-1) / float(left_cards)
    return level_prob         


def sum_number(r):
    numbers = [int(card[1:]) for card in r]
    return sum(numbers)

def char2index(c):
    return ord(c) - ord('A')


def pk_with_rival(my_level, rival_level):
    if my_level[5] == 1:
        return 10
    elif my_level[4] == 1:
        return 7
    elif my_level[3] == 1:
        return 5
    elif my_level[2] == 1:
        return 3
    prob = my_level[5] * (rival_level[1]+rival_level[2]+rival_level[3]+rival_level[4]) + \
                my_level[4] * (rival_level[1]+rival_level[2]+rival_level[3]) + \
                my_level[3] * (rival_level[1]+rival_level[2]) + \
                my_level[2] * (rival_level[1])
    return prob * 10

def judge_level(r):
    same_color = (r[0][0] == r[1][0] and r[0][0] == r[2][0])
    numbers = [int(card[1:]) for card in r]
    numbers.sort()
    order_numbers = (numbers[1] - numbers[0] == 1 and numbers[2] - numbers[0] == 2)
    same_numbers = (numbers[0] == numbers[1] and numbers[0] == numbers[2])
    if same_color and order_numbers:
        return 5
    elif same_numbers:
        return 4
    elif same_color:
        return 3
    elif order_numbers:
        return 2
    else:
        return 1


if __name__ == '__main__':
    main()

