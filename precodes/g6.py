#!/usr/bin/python
#coding=utf-8

import sys
import os
import copy

arr_all_list = []
for arr_se_item in ['A','B','C','D','E','F']:
    for arr_son_item in [0,1,2,3,4,5,6,7,8,9]:
        arr_all_list.append(arr_se_item+str(arr_son_item))

weightDict = {"tonghuashun":4,"zhadan":3,"tonghua":2,"shunzi":1,"qita":0}

cards_in_hands = []
myStatus = [[] for i in range(9)]
hisStatus = [[] for i in range(9)]

win_weight = 1.1
los_weight = 1.1

#fout = open("test.out",'a')
#tout = open("result.out","a")

def getSeries(input_arr):
    #判断三个数字是否连续
    arr_series = input_arr[:]
    arr_series.sort(key=lambda x:x[1])
    return (int(arr_series[1][1])==int(arr_series[0][1])+1 \
            and int(arr_series[2][1])==int(arr_series[1][1])+1)

def getType(arr_type):
    detail_type = getSeries(arr_type)
    if arr_type[0][1] == arr_type[1][1] and arr_type[1][1] == arr_type[2][1]:
        return "zhadan"
    elif arr_type[0][0] == arr_type[1][0] and arr_type[1][0] == arr_type[2][0]:
        if detail_type:
            return "tonghuashun"
        else:
            return "tonghua"
    else:
        if detail_type:
            return "shunzi"
        else:
            return "qita"

def estimate(state):
    # Precondition: state must be a 3-element list!
    score = int(state[0][1])+int(state[1][1])+int(state[2][1])
    return weightDict[getType(state)]*28+score

def compare(state_1,state_2):
    # Precondition: both state_1 and state_2 must be 3-element lists!
    score_1 = estimate(state_1)
    score_2 = estimate(state_2)
    if score_1>score_2:
        return 1
    elif score_1==score_2:
        return 0
    else:
        return -1

def getStatus(arr_A,arr_B):
    if len(arr_A) == 0 and len(arr_B) == 0: #两队在这一列未放置
        return -2
    elif len(arr_A) < 3 and len(arr_B) < 3: #两队均未满三个棋子
        return 0
    elif len(arr_A) == 3 and len(arr_B) == 3:
        return compare(arr_A,arr_B)
    else:
        if len(arr_A) == 3:
            if len(arr_B) <= 1:
                return 0
            else:
                for item in arr_all_list:
                    new_arr_B = arr_B[:]
                    new_arr_B.append(item)
                    if compare(new_arr_B,arr_A)>0:
                        return 0
                return 1
        else:
            if len(arr_A) <= 1:
                return 0
            else:
                for item in arr_all_list:
                    new_arr_A = arr_A[:]
                    new_arr_A.append(item)
                    if compare(new_arr_A,arr_B)>0:
                        return 0
                return -1

def findNum(status, num):
    count = 0
    for i in xrange(len(status)):
        if status[i] == num:
            count += 1
    return count

def selectCard(status, lineScore, lineCard):
        sta_len = len(status)
        winNum = findNum(status, 1)
        losNum = findNum(status, -1)
        listZero = [0]
        security = listZero * 9
        danger = listZero * 9
        result = 0
        maxScore = 0
        for i in xrange(sta_len):
            if status[i] == 1 or status[i] == -1:
                continue
            elif len(myStatus[i]) < 3:
                result = i
                maxScore = lineScore[i]
                break
        if winNum >= 5:
            return (result,lineCard[result])
        if losNum >= 5:
            return (result,lineCard[result])
        for i in xrange(sta_len-2):
            temp = (status[i],status[i+1],status[i+2])
            if temp == (1,1,1):
                return (result,lineCard[result])
            elif temp == (-1,-1,-1):
                return (result,lineCard[result])
            if temp == (0,-1,-1) and not danger[i]:
                danger[i] = 1
                lineScore[i] *= los_weight
            elif temp == (-1,0,-1) and not danger[i+1]:
                danger[i+1] = 1
                lineScore[i+1] *= los_weight
            elif temp == (-1,-1,0) and not danger[i+2]:
                danger[i+2] = 1
                lineScore[i+2] *= los_weight
            if temp == (0,1,1) and not security[i]:
                security[i] = 1
                lineScore[i] *= win_weight
            elif temp == (1,0,1) and not security[i+1]:
                security[i+1] = 1
                lineScore[i+1] *= win_weight
            elif temp == (1,1,0) and not security[i+2]:
                security[i+2] = 1
                lineScore[i+2] *= win_weight
        for j in xrange(sta_len):
            if (status[j] == 0 and myStatus[i]<3) or status[j] == -2:
                if lineScore[j] > maxScore:
                    result = j
                    maxScore = lineScore[j]
        return (result, lineCard[result])


def play(status):
    [lineScore,lineCard] = computeLineScore(myStatus,hisStatus,status,arr_all_list,cards_in_hands)
    [region,card] = selectCard(status,lineScore,lineCard)
    if not card:
        for i in range(9):
            if len(myStatus[i])<3:
                return [i,cards_in_hands[0]]
    else:
        return [region,card]


#typeWeigthDict={"tonghuashun":4,"zhadan":3,"tonghua":2,"shunzi":1,"qita":0}
posWeigthDict={0:1.2,1:1.8,2:2.4,3:3} # hand 1 left 0
score=0.0
preMaxScore=0
maxCard=""
count=0

def getType(arr_type):
    detail_type = getSeries(arr_type)
    if arr_type[0][1] == arr_type[1][1] and arr_type[1][1] == arr_type[2][1]:
        return "zhadan"
    elif arr_type[0][0] == arr_type[1][0] and arr_type[1][0] == arr_type[2][0]:
        if detail_type:
            return "tonghuashun"
        else:
            return "tonghua"
    else:
        if detail_type:
            return "shunzi"
        else:
            return "qita"




def search(cur,cardToSearch,cardsOnLine,cardsOnHand,cardsLeft,probList):
    global score,count,maxCard,preMaxScore
    if cur==3:
        # print cardToSearch
        prob=0.0
        for i in probList:
                   # prob*=i
                prob+=i
                # posTypeInt+=1.0/(len(cardsLeft)+1)
        # print probList
        count+=1
        cardsType=getType(cardToSearch)
        sum=0
        for i in range(len(cardToSearch)):
            sum += int(cardToSearch[i][1])
        curScore = (weightDict[cardsType]*28+sum)*posWeigthDict[prob]
        score += curScore
        if curScore>preMaxScore:
            preMaxScore=curScore
            maxCard=cardToSearch[len(cardsOnLine)]
        # print score,sum,posType
        return
    if cur==len(cardsOnLine):
        cardsOnHandTemp=copy.deepcopy(cardsOnHand)
        for card in cardsOnHand:
            cardsOnHandTemp.remove(card)
            probList[cur]=1.0
            search(cur+1,cardToSearch+[card],cardsOnLine,cardsOnHandTemp,cardsLeft,probList)
            probList[cur]=0.0
    else:
        cardsOnHandTemp=copy.deepcopy(cardsOnHand)
        for card in cardsOnHand:
            cardsOnHandTemp.remove(card)
            probList[cur]=1.0
            search(cur+1,cardToSearch+[card],cardsOnLine,cardsOnHandTemp,cardsLeft,probList)
            probList[cur]=0.0

        cardsLeftTemp=copy.deepcopy(cardsLeft)
        for card in cardsLeft:
            # probList[cur]=1.0/(len(cardsLeft))
            cardsLeftTemp.remove(card)
            search(cur+1,cardToSearch+[card],cardsOnLine,cardsOnHand,cardsLeftTemp,probList)
            # probList[cur]=0.0


def getMyScore(cardsOnLine,cardsLeft,cardsOnHand):
    global score,count,preMaxScore
    cur=len(cardsOnLine);
    probList=[0.0]*3
    for i in range(cur):
        probList[i]=1.0
    # print cur,probList
    count=0
    score=0.0
    preMaxScore=0  
    search(cur,cardsOnLine,cardsOnLine,cardsOnHand,cardsLeft,probList)
    # score=score/count
    score=preMaxScore

def search2(cur,cardToSearch,cardsOnLine,cardsLeft,probList):
    global score,count,preMaxScore
    if cur==3:
        # print cardToSearch
        prob=0.0
        for i in probList:
                   # prob*=i
                prob+=i
                # posTypeInt+=1.0/(len(cardsLeft)+1)
        # print probList
        count+=1
        cardsType=getType(cardToSearch)
        sum=0
        for i in range(len(cardToSearch)):
            sum += int(cardToSearch[i][1])
        curScore = (weightDict[cardsType]*28+sum)*posWeigthDict[prob]
        score += curScore
        if curScore>preMaxScore:
            preMaxScore=curScore
        # print curScore,maxCard
        return
    cardsLeftTemp=copy.deepcopy(cardsLeft)
    for card in cardsLeft:
        # probList[cur]=1.0/(len(cardsLeft))
        cardsLeftTemp.remove(card)
        search2(cur+1,cardToSearch+[card],cardsOnLine,cardsLeftTemp,probList)
        # probList[cur]=0.0


def getRivalScore(cardsOnLine,cardsLeft):
    global score,count,preMaxScore
    cur=len(cardsOnLine);
    probList=[0.0]*3
    for i in range(cur):
        probList[i]=1.0
    # print cur,probList
    count=0
    score=0.0
    preMaxScore=0
    search2(cur,cardsOnLine,cardsOnLine,cardsLeft,probList)
    # score=score/count
    score=preMaxScore
    

def computeLineScore(myCardsOnline,opponentCardsOnline,linesStatus,cardsLeft,cardsOnHand):
    firstEmpty=True
    firstEmptyPos=0
    lineScores=[0.0]*9
    maxScoreCards=['']*9
    #fout.write(str(status)+"\n")
    for i in range(9):
            if linesStatus[i]==0:
                if len(myCardsOnline[i])<3:
                    getMyScore(myCardsOnline[i], cardsLeft, cardsOnHand)
                    myScore=score
                    getRivalScore(opponentCardsOnline[i], cardsLeft)
                    rivalScore=score
                    lineScores[i]=float(myScore)/rivalScore
                    maxScoreCards[i]=maxCard
                    #fout.write(str(int(myScore))+","+str(int(rivalScore))+";")
                else:
                    pass
                    #fout.write("*** ;")
            elif linesStatus[i]==-2:
                if firstEmpty:
                    getMyScore(myCardsOnline[i], cardsLeft, cardsOnHand)
                    myScore=score
                    getRivalScore(opponentCardsOnline[i], cardsLeft)
                    rivalScore=score
                    lineScores[i]=float(myScore)/rivalScore
                    maxScoreCards[i]=maxCard
                    firstEmpty=False
                    firstEmptyPos=i
                    #fout.write(str(int(myScore))+","+str(int(rivalScore))+";")
                else:
                    lineScores[i]=lineScores[firstEmptyPos]
                    maxScoreCards[i]=maxScoreCards[firstEmptyPos]
                    #fout.write("*** ;")
            else:
                pass
                #fout.write("*** ;")
    #fout.write("\n")
    return lineScores,maxScoreCards

def decode(card):
    return card[0]+str(int(card[1:])-1)

def encode(card):
    return card[0]+str(int(card[1:])+1)

if __name__ == '__main__':
    status = [-2]*9
    while True:
        n = int(sys.stdin.readline())
        #sys.stderr.write("demo %d n: %d\n" % (os.getpid(), n))
        over = False
        for i in range(n):
            cmd = sys.stdin.readline()
            #sys.stderr.write("demo %d cmd: " % os.getpid()+ cmd)
            items = cmd.split()
            if items[0] == 'cardget':
                items[1] = decode(items[1])
                arr_all_list.remove(items[1])
                cards_in_hands.append(items[1])
            elif items[0] == 'rival':
                items[2] = decode(items[2])
                arr_all_list.remove(items[2])
                hisStatus[int(items[1])].append(items[2])
                status[int(items[1])] = getStatus(myStatus[int(items[1])],hisStatus[int(items[1])])
                pass
            else:
                '''
                if items[0]=="youwin":
                    tout.write("1\n")
                else:
                    tout.write("0\n")
                '''
                #tout.close()
                #fout.write(items[0]+"\n\n")
                #fout.close()
                over = True
        if over:
            break
        else:
            [region,card] = play(status) 
            myStatus[region].append(card)
            cards_in_hands.remove(card)
            status[region] = getStatus(myStatus[region],hisStatus[region])
            sys.stdout.write("act %d %s\n" % (region,encode(card)))
            sys.stdout.flush()
 

