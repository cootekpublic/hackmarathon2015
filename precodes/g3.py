#!/usr/bin/python

import sys
import os
import random
from itertools import combinations


def value(card):
    val = 0
    if card[0] == 'A':
        val = 0
    elif card[0] == 'B':
        val = 10
    elif card[0] == 'C':
        val = 20
    elif card[0] == 'D':
        val = 30
    elif card[0] == 'E':
        val = 40
    else:
        val = 50
    return val + int(card[1:]) - 1

def val_2_char(num):
    a = num/10
    b = (num%10) + 1
    arr = ['A','B','C','D','E','F']
    return arr[a]+str(b)

def is_th(arr):
    return (arr[0]/10 == arr[1]/10 and arr[1]/10 == arr[2]/10 )

def is_sz(arr):
    tmp = sorted(arr)
    return (tmp[2]%10 - tmp[1]%10 == 1 and tmp[1] - tmp[0] == 1)

def is_zd(arr):
    return (arr[2]%10 == arr[1]%10 and arr[1]%10 == arr[0]%10)

def is_ths(arr):
    return is_th(arr) and is_sz(arr)

def get_level(arr):
    if (is_ths(arr)):
        return 5
    elif is_zd(arr):
        return 4
    elif is_th(arr):
        return 3
    elif is_sz(arr):
        return 2
    else:
        return 1

def get_three_card(arr):
    num_arr = []
    max_level = 0
    max_three = []
    its_num = 0
    for item in arr:
        num_arr.append(value(item))
    for item in list(combinations(num_arr, 3)):
        level = get_level(item)
        if level >= max_level:
            max_level = level
            max_three = item
    ch_max_three = []
    for item in max_three:
        ch_max_three.append(val_2_char(item))
    return max_level,ch_max_three





if __name__ == '__main__':
    cards_in_hands = []
    status = [[] for i in range(9)]
    linesLeft = 9
    emptyLine = 9

    # 0:empty 1:wait_tonghuashun 2:wait_zhadan 3:giveup
    special_status = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 0:zhengchang 1:youpaifang
    my_state = 0

    # cards on tablee
    card_appear = []

    # GOOD CARD
    good_card = []
    good_card_pos = 0

    # whick line my wait card should be
    pos_wait = {}

    # his status
    his_status = [[] for i in range(9)]
    his_levels = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
    his_sum = [10,10,10,10,10,10,10,10,10]

    send = False
    color = ['','','','','','','','','']
    #fw = open("info.txt", 'w+')

    while True:
        n = int(sys.stdin.readline())
        over = False
        for i in range(n):
            cmd = sys.stdin.readline()
            items = cmd.split()
            if items[0] == 'cardget':
                cards_in_hands.append(items[1])
                cards_in_hands.sort(key=lambda x:int(x[1:]))
                cards_in_hands = list(reversed(cards_in_hands))
            elif items[0] == 'rival':
                #card_appear.append(items[2])
                #his_status[int(items[1])].append(items[2])
                #if len(his_status[int(items[1])]) == 3:
                    #his_levels = get_level(his_status[i])
                    #his_sum = value(his_status[item[1]][0]) + value(his_status[item[1]][1]) + value(his_status[item[1]][2]) 
                pass
            else:
                over = True
        if over:
            break
        else:
            if len(good_card) == 0:
                send = False
                max_level,ch_max_three = get_three_card(cards_in_hands)
                if max_level >= 3:
                    #fw.write("#1")
                    #fw.write("\nmaxLevel : "+str(max_level))
                    
                    
                    #fw.write("\ngmax_3_c: ")
                    #for item in ch_max_three:
                        #fw.write(item+' ')

                    #fw.write("\n")
                    #for i in range(9):
                        #fw.write(str(len(status[i]))+' ')

                    for i in range(9):
                        if len(status[i]) == 0:
                            good_card_pos = i
                            good_card = ch_max_three
                            #fw.write("\n!--"+str(len(status[i]))+" "+str(i))
                            status[i].append(good_card[0])
                            color[i] = good_card[0][0]

                            #fw.write("\n GoodCardBegin:act %d %s\n" % (good_card_pos, good_card[0]))

                            sys.stdout.write("act %d %s\n" % (good_card_pos, good_card[0]))
                            sys.stdout.flush()
                            cards_in_hands.remove(good_card[0])
                            card_appear.append(good_card[0])
                            good_card.remove(good_card[0])
                            send = True
                            break
                if send == False:
                    for i in [8,7,6,5,4,3,2,1,0]:
                        if  len(status[i]) < 3 and color[i] != '':
                            #fw.write("#2")
                            for card in cards_in_hands:
                                if card[0] == color[i]:
                                    status[i].append(card)

                                    
                                    #fw.write("act %d %s\n" % (i, card))

                                    sys.stdout.write("act %d %s\n" % (i, card))
                                    sys.stdout.flush()
                                    card_appear.append(card)
                                    cards_in_hands.remove(card)
                                    send = True

                                    #fw.write("\n")
                                    #for i in range(9):
                                        #fw.write(str(len(status[i]))+' ')
                                    break
                            if send:
                                break
                        elif color[i] == '':
                            #fw.write("#3 i ="+str(i)+' color[i]:'+color[i])
                            color[i] = cards_in_hands[0][0]
                            status[i].append(cards_in_hands[0])

                            #fw.write("act %d %s\n" % (i, cards_in_hands[0]))

                            sys.stdout.write("act %d %s\n" % (i, cards_in_hands[0]))
                            sys.stdout.flush()
                            card_appear.append(cards_in_hands[0])
                            cards_in_hands = cards_in_hands[1:]
                            send = True

                            #fw.write("\n")
                            #for i in range(9):
                                #fw.write(str(len(status[i]))+' ')

                            break
                else:
                    pass
                if (not send):
                    #fw.write("#4")
                    for i in [8,7,6,5,4,3,2,1,0]:
                        if len(status[i]) < 3:
                            status[i].append(cards_in_hands[0])

                            #fw.write("act %d %s\n" % (i, cards_in_hands[0]))

                            sys.stdout.write("act %d %s\n" % (i, cards_in_hands[0]))
                            sys.stdout.flush()
                            card_appear.append(cards_in_hands[0])
                            cards_in_hands = cards_in_hands[1:]
                            #fw.write("\n")
                            #for i in range(9):
                                #fw.write(str(len(status[i]))+' ')
            else:
                #fw.write("#5")
                status[good_card_pos].append(good_card[0])
                
                #fw.write("act %d %s\n" % (good_card_pos, good_card[0]))
                

                sys.stdout.write("act %d %s\n" % (good_card_pos, good_card[0]))
                sys.stdout.flush()
                cards_in_hands.remove(good_card[0])
                card_appear.append(good_card[0])
                good_card.remove(good_card[0])

                #fw.write("\n")
                #for i in range(9):
                    #fw.write(str(len(status[i]))+' ')

                continue
