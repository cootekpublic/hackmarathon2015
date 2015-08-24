#!/usr/bin/python

import sys


class Situation:
    def __init__(self):
        self.card_pool = LocalCardPool()
        self.first_full = [-1] * 9
        pass
    def update_situation(self, command):
        retflag = self.card_pool.update_by_command(command)
        if retflag == True:
            return retflag
        cmds = command.split()
        region = ''
        if cmds[0] == 'act':
            region = 'M'
        elif cmds[0] == 'rival':
            region = 'Y'
        region += str(cmds[1])
        if len(self.get_region_cards(region))==3 and self.first_full[int(region[1])] == -1:
            self.first_full[int(region[1])] = ('0' if region[0]=='M' else '1')
        return retflag
    def deal_card(self, region, card):
        cmd = 'act '+str(region)+' '+str(card.value)+'\n'
        self.update_situation(cmd)

        sys.stdout.write(cmd)
        sys.stdout.flush()

    def get_region_cards(self, region):
        '''
        here region has several options Mx,Yx
        '''
        ret_cards = []
        for card in self.card_pool.cards:
            if card.region == region:
                ret_cards.append(card)
        return ret_cards

    def judge_level(self, cards):
        assert(len(cards)==3)
        r = [cards[0].value, cards[1].value, cards[2].value]

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
        pass

    def judge_sum(self, Mcards, Ycards, n):
        c0 = 0
        c1 = 0
        for card in Mcards:
            c0 += int(card.value[1])
        for card in Ycards:
            c1 += int(card.value[1])
        if c0 > c1:
            return 0
        elif c1 > c0:
            return 1
        elif n != -1:
            return self.first_full[n]
        else:
            return -1

    def judge_region(self ,region):
        '''
        o means we win.
        :param situation:
        :param region:
        :return:
        '''
        level0 = self.judge_level(self.get_region_cards('M'+str(region)))
        level1 = self.judge_level(self.get_region_cards('Y'+str(region)))
        if level0 < level1:
            return 1
        elif level0 > level1:
            return 0
        else:
            return self.judge_sum(self.get_region_cards('M'+str(region)), self.get_region_cards('Y'+str(region)), int(region))
        pass
    def get_all_unshow_cards(self):
        ret = []
        for card in self.card_pool.cards:
            if card.status == CardStatus.UNSHOWN:
                ret.append(card)
        return ret


    def get_cards_in_hand(self):
        cards_inhand = []
        for card in self.card_pool.cards:
            if card.status == CardStatus.INHAND:
                cards_inhand.append(card)

        return cards_inhand

    def get_all_group_3_cards(self):
        cards = self.get_cards_in_hand()
        num = len(cards)
        ret_card_group = []
        num_group = []
        for i in range(num-2):
            one_group = []
            one_group.append(i)
            for j in range(i+1,num-1):
                one_group.append(j)
                for k in range(j+1,num):
                    one_group.append(k)
                    num_group.append(list(one_group))
                    one_group.remove(k)
                one_group.remove(j)
            one_group.remove(i)

        for group in num_group:
           ret_card_group.append([cards[group[0]],cards[group[1]],cards[group[2]]])
        return ret_card_group

    def get_all_group_2_cards(self):
        cards = self.get_cards_in_hand()
        num = len(cards)
        ret_card_group = []
        num_group = []
        for i in range(num-1):
            one_group = []
            one_group.append(i)
            for j in range(i+1,num):
                one_group.append(j)
                num_group.append(list(one_group))
                one_group.remove(j)
            one_group.remove(i)

        for group in num_group:
           ret_card_group.append([cards[group[0]],cards[group[1]]])
        return ret_card_group

    def get_best_card_group(self, card_groups):

        best_card_group = card_groups[0]
        for i in range(len(card_groups)):
            if Comparator.cards_compare(best_card_group, card_groups[i], self) == 1:
                best_card_group = card_groups[i]
        return best_card_group

class LocalCardPool:
    def __init__(self):
        '''
        todo
        '''
        self.cards = []
        for c in range(6):
            for i in range(1, 11):
                card = Card(chr(ord('A') + c) + str(i))
                self.cards.append(card)
    def get(self, value):
        for card in self.cards:
            if card.value == value:
                return card
    def update_by_command(self, cmd):
        items = cmd.split()
        if items[0]=='cardget':
            card_get = Card(items[1])
            card_get.status = CardStatus.INHAND
            self.update_by_card(card_get)
            return False
        elif items[0]=='rival':
            card_rival = Card(items[2])
            card_rival.region = 'Y'+items[1]
            card_rival.status = CardStatus.ONREGION
            self.update_by_card(card_rival)
            return False
        elif items[0] == 'act':
            card_act = Card(items[2])
            card_act.region = 'M'+items[1]
            card_act.status = CardStatus.ONREGION
            self.update_by_card(card_act)
            return False
        else:
            return True
    def update_by_card(self, card):
        for i in range(len(self.cards)):
            if self.cards[i].value == card.value:
                self.cards[i] = card




class Card:
    def __init__(self, value):
        self.value = value
        '''
        the other region starts with Y, for example Y3
        our region starts with M, for example M2
        default region is N
        '''
        self.region = 'N'
        self.status = CardStatus.UNSHOWN
        pass

class CardStatus:
    UNSHOWN = 'unshown'
    ONREGION = 'onregion'
    INHAND = 'inhand'

class Comparator:
    '''
    return 0, if cards1>cards2
    return 1, if cards1<cards2
    '''
    @staticmethod
    def cards_compare(cards1, cards2, situation):
        level0 = situation.judge_level(cards1)
        level1 = situation.judge_level(cards2)
        if level0 < level1:
            return 1
        elif level0 > level1:
            return 0
        else:
            return Comparator.judge_sum(cards1, cards2)
        pass
    @staticmethod
    def judge_sum(Mcards, Ycards):
        c0 = 0
        c1 = 0
        for card in Mcards:
            c0 += int(card.value[1])
        for card in Ycards:
            c1 += int(card.value[1])
        if c0 > c1:
            return 0
        elif c1 > c0:
            return 1
        else:
            return -1


    @staticmethod
    def extend_best_cards(your_cards, situation):
        if len(your_cards) == 2:
            test_group = []
            pool = []
            for card in situation.card_pool.cards:
                if card.status == CardStatus.UNSHOWN:
                    pool.append(card)
            for card in pool:
                temp = []
                temp.append(your_cards[0])
                temp.append(your_cards[1])
                temp.append(card)
                test_group.append(temp)
            return situation.get_best_card_group(test_group)
        pass


class oracle:

    '''
    this function dealcard directly
    '''
    next_cardandregions = []
    your_zeros_position = [1]*9
    your_ones_position = [0]*9
    your_twos_position = [0]*9
    your_threes_position = [0]*9
    @staticmethod
    def right_cmd(situation):
        if len(oracle.next_cardandregions) != 0:
            cardandregion = oracle.next_cardandregions.pop()
            situation.deal_card(cardandregion.region, cardandregion.card)
            return
        for region in range(9):
            your_regioncards = situation.get_region_cards('Y'+str(region))
            if len(your_regioncards) == 3:
                oracle.your_threes_position[region] = 1
                oracle.your_ones_position[region] = 0
                oracle.your_twos_position[region] = 0
                oracle.your_zeros_position[region] = 0

                if oracle.dohim(region, your_regioncards, situation):
                    return

            elif len(your_regioncards) == 2:
                oracle.your_twos_position[region] = 1
                oracle.your_zeros_position[region] = 0
                oracle.your_ones_position[region] = 0
                oracle.your_threes_position[region] = 0

                your_best_regioncards = Comparator.extend_best_cards(your_regioncards, situation)
                if oracle.dohim(region, your_best_regioncards, situation):
                    return

                pass
            else:
                if oracle.dome(situation):
                    return

        '''
        here there is no output. So for from 0 to 3 test
        '''
        j = 0
        for i in range(9):
            if len(situation.get_region_cards('M'+str(i)))<3:
                j = i
                break
        situation.deal_card(j,situation.get_cards_in_hand()[0])
        return


    '''
    check
    '''

    @staticmethod
    def dome(situation):
        pos = []
        group_and_region = []


        for i in range(len(oracle.your_zeros_position)):
            pos.append((oracle.your_zeros_position[i]|oracle.your_ones_position[i])*i)

    #    pos.sort()
        cards_in_my_hands = situation.get_cards_in_hand()
        unshow_cards = situation.get_all_unshow_cards()
        for region in pos:
            my_region_cards = situation.get_region_cards('M'+str(region))
            if len(my_region_cards) == 2:
                groups = []
                for card in cards_in_my_hands:
                    temp = list(my_region_cards)
                    temp.append(card)
                    groups.append(temp)
                my_best_group = situation.get_best_card_group(groups)
                group_and_region.append(CardGroupAndRegion(region, my_best_group))
                pass
            if len(my_region_cards) == 1:
                groups = []
                group = []
                group.append(my_region_cards[0])
                for handcard in cards_in_my_hands:
                    group.append(handcard)
                    for unshowcard in unshow_cards:
                        group.append(unshowcard)
                        groups.append(list(group))
                        group.remove(unshowcard)
                    group.remove(handcard)
                my_best_group = situation.get_best_card_group(groups)
                group_and_region.append(CardGroupAndRegion(region, my_best_group))
                pass
            if len(my_region_cards) == 0:
                my_2_card_group = situation.get_all_group_2_cards()
                groups = []
                for unshowcard in unshow_cards:
                    for everygroup in my_2_card_group:
                        group = list(everygroup)
                        group.append(unshowcard)
                        groups.append(group)

                my_best_group = situation.get_best_card_group(groups)
                group_and_region.append(CardGroupAndRegion(region, my_best_group))
                pass



        flags_region = []
        if len(group_and_region)==0:

            j = 0
            for i in range(9):
                if len(my_situation.get_region_cards('M'+str(i)))<3:
                    j = i
                    break
            my_situation.deal_card(j,my_situation.get_cards_in_hand()[0])
            return
        my_bbbest_region_and_group = group_and_region[0]

        for i in range(len(group_and_region)):
            if i == 0:
                continue
            if Comparator.cards_compare(my_bbbest_region_and_group.group, group_and_region[i].group,situation) == 1:
                my_bbbest_region_and_group = group_and_region[i]
            if Comparator.cards_compare(my_bbbest_region_and_group.group, group_and_region[i].group,situation) == -1:
                flags_region.append(group_and_region[i].region)
        if len(flags_region) != 0:
            same_region = []
            for card_and_region in group_and_region:
                if Comparator.cards_compare(my_bbbest_region_and_group.group, card_and_region.group,situation) == -1:
                    same_region.append(card_and_region.region)
            if len(same_region) != 1:

                same_region.sort()
                for flag in same_region:
                    if len(situation.get_region_cards('M'+str(flag)))==3:
                        same_region.remove(flag)
                best_region = same_region[len(same_region)/2]

                best_group = my_bbbest_region_and_group.group
                best_card = oracle.get_handcards(best_group).pop()

                situation.deal_card(best_region, best_card)
                return True
            else:
                best_group = my_bbbest_region_and_group.group
                best_card = oracle.get_handcards(best_group).pop()
                situation.deal_card(my_bbbest_region_and_group.region, best_card)
                return True
        else:
            best_group = my_bbbest_region_and_group.group
       	    best_card = oracle.get_handcards(best_group).pop()
            situation.deal_card(my_bbbest_region_and_group.region, best_card)
            return True


    @staticmethod
    def get_handcards(group):
        ret = []
        for card in group:
            if card.status == CardStatus.INHAND:
                ret.append(card)
        if len(ret) == 1:
            return ret
        if len(ret) == 2:
            if(ret[0].value[1]<ret[1].value[1]):
                return ret
            else:
                Card1 = ret[0]
                Card2 = ret[1]
                ret[0] = Card2
                ret[1] = Card1
                return ret





    '''
    if our best is better in region
    so do him!
    '''

    @staticmethod
    def dohim(region, your_regioncards, situation):
            my_regioncards = situation.get_region_cards('M'+str(region))
            if len(my_regioncards) == 0:
                best_card_group = situation.get_best_card_group(situation.get_all_group_3_cards())
                if Comparator.cards_compare(best_card_group, your_regioncards,situation) == 0:
                    '''
                    do him
                    '''
                    situation.deal_card(region, best_card_group[0])
                    oracle.next_cardandregions.append(CardAndRegion(region,best_card_group[1]))
                    oracle.next_cardandregions.append(CardAndRegion(region,best_card_group[2]))
                    return True
            pass
            if len(my_regioncards) == 1:
                temp_2_card_groups = situation.get_all_group_2_cards()
                groups = []
                for group in temp_2_card_groups:
                    group.append(my_regioncards[0])
                    groups.append(group)
                best_card_group = situation.get_best_card_group(groups)
                if Comparator.cards_compare(best_card_group,your_regioncards,situation) == 0:
                    '''
                    do him
                    '''
                    best_card_group.pop()
                    situation.deal_card(region, best_card_group[0])
                    oracle.next_cardandregions.append(CardAndRegion(region, best_card_group[1]))
                    return True
            if len(my_regioncards) == 2:
                cards_in_hand = situation.get_cards_in_hand()
                groups = []
                for card in cards_in_hand:
                    group = list(my_regioncards)
                    group.append(card)
                    groups.append(group)
                best_card_group = situation.get_best_card_group(groups)
                if Comparator.cards_compare(best_card_group, your_regioncards,situation) == 0:
                    '''
                    do him
                    '''
                    situation.deal_card(region, best_card_group.pop())
                    return True
            return False

class CardGroupAndRegion:
    def __init__(self, region, group):
        self.region = region
        self.group = group

class CardAndRegion:
    def __init__(self, region, card):
        self.region = region
        self.card = card




if __name__ == '__main__':
    cards_in_hands = []
    status = [[] for i in range(9)]
    my_situation = Situation();

    while True:
        n = int(sys.stdin.readline())
        #sys.stderr.write("demo %d n: %d\n" % (os.getpid(), n))
        over = False
        for i in range(n):
            cmd = sys.stdin.readline()
            #sys.stderr.write("demo %d cmd: " % os.getpid()+ cmd)
            over = my_situation.update_situation(cmd)
            '''
            items = cmd.split()
            if items[0] == 'cardget':
                cards_in_hands.append(items[1])
            elif items[0] == 'rival':

                pass
            else:
                over = True
            '''
        if over:
            break
        else:
            oracle.right_cmd(my_situation)



