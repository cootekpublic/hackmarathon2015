#!/usr/bin/python

import sys
import os




def choose(my_region, rival_region, all_cards, cards_in_hands):
    max_score = [0, 0, 0, 0]   # card_index, region_index, level, value
    has_empty = False
    region_to_append = -1
    
    for my_cards_index in range( len(cards_in_hands) ):
        
        for my_region_index in range(9):
            if is_empty_region(my_region_index):
                has_empty = True
                if abs(my_region_index - 4) < abs(region_to_append - 4):
                    region_to_append = my_region_index
                continue
            
            
            elif len(my_region[my_region_index]) >= 3:
                continue
            
            else:
                level,value = judge(my_region[my_region_index], my_cards_index)
                level,value = recompute_score(my_region[my_region_index], my_cards_index, level, value)
                #sys.stderr.write("===== xichen %d, %d" % (level,value))
                max_score = compare_max(max_score, [my_cards_index, my_region_index, level, value])
        
    if (has_empty):
        for my_cards_index in range( len(cards_in_hands) ):
            for my_cards_second in range(my_cards_index+1, len(cards_in_hands)):
                level,value = judge([ cards_in_hands[my_cards_second] ], my_cards_index)
                max_score = compare_max(max_score, [my_cards_index, region_to_append, level, value])
                
                
    return max_score[0], max_score[1]


def is_empty_region(region_index):
    return len(my_region[region_index]) == 0



def judge(standard_list, cards_index):
    
    is_same_color = judge_same_color(standard_list, cards_index)
    temp_list = standard_list[:]
    temp_list.append(cards_in_hands[cards_index])
    temp_list = [int(i[1]) for i in temp_list]
    is_sequence, average = judge_sequence(temp_list)
    
    
    if is_same_color and is_sequence:
        return 5, average
    
    if judge_same_number(temp_list):
        return 4, average
    
    elif is_same_color:
        return 3, average
    
    elif is_sequence:
        return 2, average

    else:
        return 1, average


def judge_same_color(standard_list, cards_index):
    
    def judge_same_color_two_cards(standard_card, my_card):
        return standard_card[0] == my_card[0]
    
        
    if len(standard_list) == 1:
        has_same_color_card = False
        for digit in all_cards[ cards_in_hands[cards_index][0] ]:
            if digit == 1:
                has_same_color_card = True
                break
                
        if has_same_color_card:
            return judge_same_color_two_cards(standard_list[0], cards_in_hands[cards_index])
        else:
            return False
        
    elif len(standard_list) == 2:
        return judge_same_color_two_cards(standard_list[0], cards_in_hands[cards_index]) and judge_same_color_two_cards(standard_list[1], cards_in_hands[cards_index])
    
    else:
        return False


def judge_same_number(card_list):
    for i in range( len(card_list)-1 ):
        if card_list[i] != card_list[i+1]:
            return False
    return True


def judge_sequence(card_list):
    card_list.sort(key=lambda x: int(x))
    value = float(sum(card_list)) / len(card_list)
    
    if len(card_list) == 3:
        for i in range( len(card_list)-1 ):
            if (int(card_list[i]) - int(card_list[i+1])) != -1:
                return False, value
            
        return True, value
    
    elif len(card_list) == 2:
        max = int(card_list[1])
        min = int(card_list[0])
        
        if max - min == 1:
            if max+1 <= 9:
                for color in all_cards:
                    if all_cards[color][max+1] == 1:
                        return True, value
                
            if min-1 >= 0:
                for color in all_cards:
                    if all_cards[color][min-1] == 1:
                        return True, value
            
        elif max - min == 2:
            if min+1 <= 9:
                for color in all_cards:
                    if all_cards[color][min+1] == 1:
                        return True, value
        
        return False, value
    
    else:
        return False, value
    
    
    
def compare_max(max_score_list, my_score_list):
    if my_score_list[2] > max_score_list[2] or (my_score_list[2] == max_score_list[2] and my_score_list[3] > max_score_list[3]):
        return my_score_list
    else:
        return max_score_list
    

def recompute_score(region_to_append, my_cards_index, level, value):
    return level, value
    
    


if __name__ == '__main__':
    my_region = [[] for i in range(9)]
    rival_region = [[] for i in range(9)]

    all_cards = {'A': [1]*10, 'B': [1]*10, 'C': [1]*10, 'D': [1]*10, 'E': [1]*10, 'F': [1]*10}

    cards_in_hands = []

    
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
                color = items[1][0]
                num = int(items[1][1])
                all_cards[color][num-1] = 0

            elif items[0] == 'rival':
                rival_reg_idx = items[1]
                color = items[2][0]
                num = int(items[2][1])
                all_cards[color][num-1] = 0
            else:
                over = True
        if over:
            break
        else:

             
#             for i in range(9):
#                 if len(my_region[i]) < 3:
#                     reg_idx = i
#                     my_region[i].append(cards_in_hands[0])
#                     break
            

            i, reg_idx = choose(my_region, rival_region, all_cards, cards_in_hands)
            #sys.stderr.write("=======demo %d n: %d\n" % (i, len(cards_in_hands)))
            my_region[reg_idx].append(cards_in_hands[i])
            
            sys.stdout.write("act %d %s\n" % (reg_idx, cards_in_hands[i]))
            sys.stdout.flush()
            #sys.stderr.flush()
            cards_in_hands = cards_in_hands[0:i]+cards_in_hands[i+1:]
             
            
