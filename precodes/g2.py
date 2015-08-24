#!/usr/bin/python

import sys
import os

def get_color(card):
    if card == '': return -1
    return ord(card[0]) - ord('A')

def get_num(card):
    if card == '': return -1
    return int(card[1:])

def ths(cards):
    color = [[False for i in range(10)] for i in range(6)]
    res = []
    for i in range(len(cards)):
        c = get_color(cards[i][0])
        num = int(cards[i][1:]) - 1
        color[c][num] = True
    k = 0
    maxnum = 0
    maxc = 0
    for i in range(6):
        for j in range(1, 9)[::-1]:
            if color[i][j - 1] and color[i][j] and color[i][j + 1]:
                k = j
                break
        if maxnum < k:
            maxnum = k
            maxc = i
    if maxnum != 0:
        card = chr(maxc + ord('A')) + str(maxnum)
        res.append(card)
        card = chr(maxc + ord('A')) + str(maxnum + 1)
        res.append(card)
        card = chr(maxc + ord('A')) + str(maxnum + 2)
        res.append(card)

    if len(res) > 0: return res
    for i in range(6):
        for j in range(9):
            if color[i][j] and color[i][j + 1]:
                card = chr(i + ord('A')) + str(j + 1)
                res.append(card)
                card = chr(i + ord('A')) + str(j + 2)
                res.append(card)
            if j + 2 < 10 and color[i][j] and color[i][j + 2]:
                card = chr(i + ord('A')) + str(j + 1)
                res.append(card)
                card = chr(i + ord('A')) + str(j + 3)
                res.append(card)

    return res

def find_ths(card1, card2, card_in_use):
    c = card1[0]
    if get_num(card1) > get_num(card2):
        t = card1
        card1 = card2
        card2 = t
    num1 = get_num(card1)
    num2 = get_num(card2)
    if num2 - num1 == 1:
        f1 = True
        f2 = True
        p1 = num1 - 1
        p2 = num2 + 1
        if p1 > 0:
            card3 = c + str(p1)
            if card3 in card_in_use: f1 = False
        if p2 <= 10:
            card3 = c + str(p2)
            if card3 in card_in_use: f2 = False
        if f1 or f2: return card3
        return ''
    else:
        flag = True
        p = num1 + 1
        card3 = c + str(p)
        if card3 in card_in_use: flag = False
        if flag: return card3
        else: return ''

def find_region(card, status):
    for i in range(0, 9):
        if card in status[i]: return i

def zd(card):
    res = []
    zd_cards = [[] for i in range(10)]
    for i in range(len(card)):
        num = get_num(card[i])
        zd_cards[num - 1].append(card[i])
    for i in range(10)[::-1]:
        if len(zd_cards[i]) >= 3:
            for j in range(len(zd_cards[i])):
                res.append(zd_cards[i][j])
    for i in range(10)[::-1]:
        if len(zd_cards[i]) == 2:
            for j in range(len(zd_cards[i])):
                res.append(zd_cards[i][j])
    return res

def th(card):
    res = []
    zd_cards = [[] for i in range(6)]
    color_max = [-1 for i in range(6)]
    for i in range(len(card)):
        color = get_color(card[i])
        zd_cards[color].append(card[i])
    for i in range(6):
        if len(zd_cards[i]) >= 2:
            res.append(zd_cards[i])
    return res


def printFile(region, card_put, status, cards_in_hands, card_in_use):
    #print 'status', status
    #print 'card_put', card_put
    #print 'region', region
    #print 'cards_in_hands', cards_in_hands
    #print 'card_in_use', card_in_use
    status[region].append(card_put)
    card_in_use.append(card_put)
    cards_in_hands.remove(card_put)
    sys.stdout.write('act %d %s\n' % (region, card_put))
    sys.stdout.flush()

def work_for_first(cnt, offensive, status, rival_status, cards_in_hands, card_in_use):

    region = -1
    card_put = ''

########
    if cnt == 1:
        if offensive: region = 4
        else:
            if len(rival_status[4]) > 0: region = 3
            else: region = 4
    else:
        flag = False
        for i in range(5):
            region = 4 + i
            if len(status[region]) == 0:
                flag = True
                break
            region = 4 - i
            if len(status[region]) == 0:
                flag = True
                break
        if not flag: return []

################
    cards = ths(cards_in_hands)
    tmp = ''
    posths = ''
    if len(cards) == 3:
        card_put = cards[2]
        return [region, card_put]

    cards = zd(cards_in_hands)
    if len(cards) >= 2:
        card_put = cards[0]
        return [region, card_put]

    cards = ths(cards_in_hands)
    if len(cards) > 0:
        for i in range(len(cards)):
            if i % 2 == 1: continue
            tmp = find_ths(cards[i], cards[i + 1], cards_in_use)
            if tmp != '': tmp = cards[i + 1]
            if card_put == '' or get_num(card_put) < get_num(tmp):
                    #print get_num(card_put)
                    #print get_num(tmp)
                card_put = tmp
                posths = cards[i]

            #region = find_region(posths, status)
        if card_put != '':
            return [region, card_put]


##################

    cards = th(cards_in_hands)
    card_put = ''
    for i in range(len(cards)):
        if len(cards[i]) == 2: pass
        for j in range(len(cards[i])):
            if get_num(card_put) < get_num(cards[i][j]): card_put = cards[i][j]
    if card_put == '':
        for i in range(len(cards)):
            if len(cards[i]) == 2:
                for j in range(len(cards[i])):
                    if get_num(card_put) < get_num(cards[i][j]):
                        card_put = cards[i][j]
    if card_put != '':
        return [region, card_put]
    return []


def find_ths_in_hand(card1, card2, card_in_hand):
    c = card1[0]
    if get_num(card1) > get_num(card2):
        t = card1
        card1 = card2
        card2 = t
    num1 = get_num(card1)
    num2 = get_num(card2)
    if num2 - num1 == 1:
        f1 = False
        f2 = False
        p1 = num1 - 1
        p2 = num2 + 1
        if p1 > 0:
            card3 = c + str(p1)
            if card3 in card_in_hand: f1 = True
        if p2 <= 10:
            card4 = c + str(p2)
            if card4 in card_in_hand: f2 = True
        if f2: return card4
        elif f1: return card3
        else: return ''
    else:
        flag = False
        p = num1 + 1
        card3 = c + str(p)
        if card3 in card_in_hand: flag = True
        if flag: return card3
        else: return ''


def two_ths(status, rival_status, cards_in_hands, cards_in_use, tag):
    standard = 4
    region = standard + tag
    if len(status[region]) != 2: return []
    cards = ths(status[region])
    tmp = ''
    posths = ''
    if len(cards) == 2:
        card_put = ''
        for i in range(len(cards) - 1):
            if i % 2 == 0: pass
            tmp = find_ths_in_hand(cards[i], cards[i + 1], cards_in_hands)
            if card_put == '' or get_num(card_put) < get_num(tmp):
                #print get_num(card_put)
                #print get_num(tmp)
                card_put = tmp
                posths = cards[i]

        if card_put != '':
            return [region, card_put]
    return []


def work_two_ths(status, rival_status, cards_in_hands, cards_in_use):
    res = []
    for i in range(5):
        res = two_ths(status, rival_status, cards_in_hands, cards_in_use, i)
        if len(res) == 2: return res
        if i != 0: flag = two_ths(status, rival_status, cards_in_hands, cards_in_use, -i)
        if len(res) == 2: return res
    return []

def two_zd(status, rival_status, cards_in_hands, cards_in_use, tag):
    standard = 4
    region = standard + tag
    if len(status[region]) != 2: return []
    cards = zd(status[region])
    if len(cards) == 2:
        num = get_num(cards[0])
        for i in range(6):
            card = chr(i + ord('A')) + str(num)
            if card in cards_in_hands:
                return [region, card]
    return []

def work_two_zd(status, rival_status, cards_in_hands, cards_in_use):
    res = []
    for i in range(0, 5):
        res = two_zd(status, rival_status, cards_in_hands, cards_in_use, i)
        if len(res) == 2: return res
        if i != 0: res = two_zd(status, rival_status, cards_in_hands, cards_in_use, -i)
        if len(res) == 2: return res
    return res

def two_th(status, rival_status, cards_in_hands, cards_in_use, tag):
    standard = 4
    region = standard + tag
    if len(status[region]) != 2: return []
    cards = th(status[region])
    if len(cards) == 1 and len(cards[0]) == 2:
        color = get_color(cards[0][0])
        num = -1
        card_put = ''
        for card in cards_in_hands:
            if get_color(card) == color:
                tmp_num = get_num(card)
                if (num < tmp_num):
                    num = tmp_num
                    card_put = card
        if card_put != '':
            return [region, card_put]
    return []
def work_two_th(status, rival_status, cards_in_hands, cards_in_use):
    res = []
    for i in range(5):
        res = two_th(status, rival_status, cards_in_hands, cards_in_use, i)
        if len(res) == 2: return res
        if i != 0: flag = two_th(status, rival_status, cards_in_hands, cards_in_use, -i)
        if len(res) == 2: return res
    return res

def sz(status):
    res = []
    a = get_num(status[0])
    b = get_num(status[1])
    if a == b - 1:
        res.append(status[0])
        res.append(status[1])
    elif a == b + 1:
        res.append(status[1])
        res.append(status[0])
    return res
def two_sz(status, rival_status, cards_in_hands, card_in_use, tag):
    standard = 4
    region = standard + tag
    if len(status[region]) != 2: return[]
    card = sz(status[region])
    if len(card) == 2:
        card_put = ''
        for i in range(len(cards_in_hands)):
            num = get_num(cards_in_hands[i])
            if num == get_num(card[1]) + 1:
                card_put = cards_in_hands[i]
                break
            elif num == get_num(card[0]) - 1:
                card_put = cards_in_hands[i]
                break
        if card_put != '':
            return [region, card_put]
    return []
def work_two_sz(status, rival_status, cards_in_hands, cards_in_use):
    res = []
    for i in range(5):
        res = two_sz(status, rival_status, cards_in_hands, cards_in_use, i)
        if len(res) == 2: return res
        if i != 0: res = two_sz(status, rival_status, cards_in_hands, cards_in_use, -i)
        if len(res) == 2: return res
    return res

def find_one_zd(card, cards_in_hands, card_in_use):
    one_num=str(get_num(card)-1)
    num_hand =''
    num_use=''
    res = []
    for i in range(len(card_in_use)):
        num_use += str(get_num(card_in_use[i])-1)
    for i in range(len(cards_in_hands)):
        num_hand+=str(get_num(cards_in_hands[i])-1)
    k = num_hand.count(one_num)
    k_use = num_use.count(one_num)

    if k>=2:
	 for i in range(len(cards_in_hands)):
            if str(get_num(cards_in_hands[i])-1) == one_num:
                 res.append(cards_in_hands[i])
                 return res[0]
    elif k==1 and k_use <=3:
         for i in range(len(cards_in_hands)):
            if str(get_num(cards_in_hands[i])-1) ==one_num:
                 res.append(cards_in_hands[i])
                 return res[0]
    else:
        return ''

def find_one_th(card, cards_in_hands,card_in_use):
    color_hand =''
    for i in range(len(cards_in_hands)):
        color_hand+=str(get_color(cards_in_hands[i]))

    one_color=str(get_color(card))
    res = []
    card_put = ''

    k = color_hand.count(one_color)
    if k >= 2:
        max=0
        for i in range(len(cards_in_hands)):
            if str(get_color(cards_in_hands[i])) == one_color:
                res.append(cards_in_hands[i])
        for i in range(len(res)):
            if get_num(res[i]) >= get_num(res[max]):
                max=i
        card_put=res[max]
        return card_put
    elif k == 1:
        for i in range(len(cards_in_hands)):
            if str(get_color(cards_in_hands[i])) ==one_color:
                res.append(cards_in_hands[i])
        card_put = res[0]
        return card_put
    else:
        return ''

def one_special(status, rival_status, card_in_hand, card_in_use, name):
    region = -1
    ret = ''
    for i in range(5):
        if len(status[4 + i]) == 1 :
            card = status[4 + i][0]
            if name == 'one_ths':
                ret = find_one_ths(card, card_in_hand, card_in_use)
            elif name == 'one_zd':
                ret = find_one_zd(card, card_in_hand, card_in_use)
            elif name == 'one_th':
                ret = find_one_th(card, card_in_hand, card_in_use)
            elif name == 'one_sz':
                ret = find_one_sz(card,status, card_in_hand, card_in_use)
            if ret != '':
                if type(ret) == str:
                    region = 4 + i
                    break
                if type(ret) == tuple:
                    region = ret[0]
                    ret = ret[1]
                    break
        if i != 0 and len(status[4 - i]) == 1:
            card = status[4 - i][0]
            if name == 'one_ths':
                ret = find_one_ths(card, card_in_hand, card_in_use)
            elif name == 'one_zd':
                ret = find_one_zd(card, card_in_hand, card_in_use)
            elif name == 'one_th':
                ret = find_one_th(card, card_in_hand, card_in_use)
            elif name == 'one_sz':
                ret = find_one_sz(card,status, card_in_hand, card_in_use)
            if ret != '':
                if type(ret) == str:
                    region = 4 - i
                    break
                if type(ret) == tuple:
                    region = ret[0]
                    ret = ret[1]
                    break
    if region == -1:
        return []
    else:
        return [region,ret]

def th_or_zd(card, card_in_hand):
    one_num = str(get_num(card)-1)
    num_hand = ''
    for i in range(len(cards_in_hands)):
        num_hand += str(get_num(cards_in_hands[i])-1)
    k = num_hand.count(one_num)
    if k>=2:
        return 1
    else:
        return 0



def find_one_ths(card, card_in_hand, card_in_use):
    c = card[0]
    card_find = ''
    number = get_num(card)
    card_next = c + str(number + 1) if number < 10 else card
    card_pre = c + str(number - 1)  if (number - 1) > 0 else card
    card_next_two = c + str(number + 2) if number < 10 else card
    card_pre_two = c + str(number - 2) if (number - 2) > 0 else card
    if card_next in card_in_hand and card_pre in card_in_hand:
        card_find = card_next
    elif card_next in card_in_hand and card_next_two in card_in_hand:
        card_find = card_next_two
    elif card_pre in card_in_hand and card_pre_two in card_in_hand:
        card_find = card_pre
    elif th_or_zd(card,card_in_hand) == 1:
        return ''
    elif card_next in card_in_hand:
        if card_next_two not in card_in_use or card_pre not in card_in_use:
            card_find = card_next
    elif card_pre in card_in_hand:
        if card_pre_two not in card_in_use or card_next not in card_in_use:
            card_find = card_pre
    elif card_next_two in card_in_hand:
        if card_next not in card_in_use:
            card_find = card_next_two
    elif card_pre_two in card_in_hand:
        if card_pre not in card_in_use:
            card_find = card_pre_two
    return card_find


def find_one_sz(card, status, cards_in_hands,card_in_use):
    number = get_num(card)
    max = 1
    region = -1
    card_find = ''
    card_max = cards_in_hands[0]
    for i in range(len(cards_in_hands)):
        num = get_num(cards_in_hands[i])
        if num > max:
            max = num
            card_max = cards_in_hands[i]
        if num == number + 1 or num == number + 2:
            card_find = cards_in_hands[i]
            break
        elif num == number - 1 or num == number - 2:
            card_find = cards_in_hands[i]
            break
    if card_find == '':
        for i in range(4,-1,-1):
            if len(status[4 + i]) == 0:
                return ''
            elif len(status[4 - i]) == 0:
                return ''
        for i in range(4, -1, -1):
            if len(status[4 + i]) != 0 and len(status[4 + i]) < 3:
                region = 4 + i
                card_find = card_max
                break
            elif i != 0 and len(status[4 - i]) != 0 and len(status[4 - i]) < 3:
                region = 4 - i
                card_find = card_max
                break
    if region != -1:
        return region, card_find
    else:
        return card_find

def the_last_one(status, rival_status, cards_in_hands, cards_in_use):
    Sum = 0
    Max = -1
    region = -1
    for i in range(9):
        if len(status[i]) == 2:
            Sum = status[i][0] + status[i][1]
            if Max < Sum:
                Max = Sum
                region = i
    Max = -1
    card_put = ''
    for card in cards_in_hands:
        num = get_num(card)
        if Max < num:
            Max = num
            card_put = card
    return [region, card_put]

if __name__ == '__main__':
    cards_in_hands = []
    cards_in_use = []
    status = [[] for i in range(9)]
    rival_status = [[] for i in range(9)]
    offensive = True
    cnt = 0

    while True:
        n = int(sys.stdin.readline())
        over = False
        for i in range(n):
            cmd = sys.stdin.readline()
            items = cmd.split()
            if items[0] == 'cardget':
                cards_in_hands.append(items[1])
            elif items[0] == 'rival':
                rival_status[int(items[1])].append(items[2])
                cards_in_use.append(items[2])
            else:
                over = True

        if over:
            break
        else:
            #printFile(0, cards_in_hands[0], status, cards_in_hands, cards_in_use)
            cnt += 1
            if cnt == 1:
                if n == 8: offensive = False
                elif n == 7: offensive = True
            card_put = ''
            if cnt == 1:
                card_put = work_for_first(cnt, offensive, status, rival_status, cards_in_hands, cards_in_use)
            if len(card_put) == 0: card_put = work_two_ths(status, rival_status, cards_in_hands, cards_in_use)
            if len(card_put) == 0: card_put = work_two_zd(status, rival_status, cards_in_hands, cards_in_use)
            if len(card_put) == 0: card_put = one_special(status, rival_status, cards_in_hands, cards_in_use, 'one_ths')
            if len(card_put) == 0: card_put = one_special(status, rival_status, cards_in_hands, cards_in_use, 'one_zd')
            if len(card_put) == 0: card_put = work_two_th(status, rival_status, cards_in_hands, cards_in_use)
            if len(card_put) == 0: card_put = work_two_sz(status, rival_status, cards_in_hands, cards_in_use)
            if len(card_put) == 0: card_put = one_special(status, rival_status, cards_in_hands, cards_in_use, 'one_th')
            if len(card_put) == 0: card_put = one_special(status, rival_status, cards_in_hands, cards_in_use, 'one_sz')
            if len(card_put) == 0: card_put = work_for_first(cnt, offensive, status, rival_status, cards_in_hands, cards_in_use)
            if len(card_put) == 0: card_put = the_last_one(status, rival_status, cards_in_hands, cards_in_use)
            printFile(card_put[0], card_put[1], status, cards_in_hands, cards_in_use)

            #sys.stdout.write('act %d %s\n' % (region, card_put))
            #sys.stdout.flush()

