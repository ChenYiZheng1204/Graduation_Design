'''
GameEngine.py description
游戏类：代表游戏状态和进度的类
__init__：获取三个玩家名称/id并初始化游戏信息
sortHelper：通过返回虚拟值对扑克进行排序的助手函数
encodeGame：获取可选的游戏状态（正在进行、教授获胜、学生获胜），并将游戏对象编码为字符串
shuffleDeck：创建并搅乱初始牌组
dealCard：将牌发给玩家
chooseLandlord：取玩家的名字，让玩家成为教授
assignPlayOrder：指定播放顺序
whichPattern：标识所玩的牌型和等级
isValidPlay：检查所选播放是否为有效播放
makePlay：接收选定的牌，当前玩家玩这些牌
checkWin：检查是否有人获胜
createAI：取2个名字，创建2个AI玩家
AIMakePlay：选择的AI根据选择的landlord打牌或呼叫房东
玩家等级：游戏中玩家的等级
__init__：取一个名称并创建对象
playCard：从玩家身上移除卡片
AI类：游戏中AI玩家的类
__init__：取一个名称并创建对象
playCard：从AI播放器中移除卡片
getAllMoves：返回AI可能做出的所有移动
'''


import random

import pygame

import utils
import tkinter.messagebox
from pygameWidgets import *
pygame.init()
pygame.font.init()




# class for the Game object
class Game:
    def __init__(self, p1id, p2id,levelid):
        print(levelid)
        if levelid == 1:
            #level1 难度1 第一个是玩家的手牌 第二个是AI的手牌
            level1 = [['heart 2', 'heart J', 'spade J', 'heart 5', 'diamond 5', 'diamond 4','club 4','club 3'],['X', 'heart 10', 'diamond 10','diamond 7']]
        # for generating and comparing cards
        #关卡2
        elif levelid == 2:
            level1 = [['heart A', 'spade A', 'spade K', 'spade 6', 'spade 2', 'diamond 2','heart Q','club 2'],['club J', 'heart 10', 'diamond 10', 'club 10', 'club 8', 'diamond 3', 'diamond 9', 'club Q']]
        elif levelid == 3:
            level1 = [['club 2','heart 2','spade 2','diamond 2','club J'],['spade 3','club 4','club A','heart A','spade A','diamond A','D','X']]
        elif levelid == 4:
            level1 = [['heart 2','club K','heart K','spade 10','heart 10','heart 7','club 7','heart 5','diamond 5','heart 4'],['spade A','heart A','heart 8']]
        # self.tp = ['spade 2']
        # self.game1 = ['heart Q', 'heart A', 'spade 8', 'heart 6', 'diamond 8', 'diamond 2', 'spade 4', 'spade 9', 'heart K', 'heart 5', 'club K', 'spade 6', 'club 9', 'club 5', 'diamond Q', 'diamond 4', 'diamond A']
        # self.game2 = ['spade A', 'heart 9', 'diamond 6', 'spade J', 'diamond 5', 'heart 7', 'spade 7', 'club 6', 'club 4', 'spade 3', 'spade 10', 'spade K', 'club A', 'heart J', 'X', 'diamond K', 'D']
        self.maingame2 = level1[1]
        self.game1 = level1[0]
        self.game2 = level1[1]
        # self.game3 = ['spade 3']
        self.colors = ['heart', 'spade', 'diamond', 'club']
        self.nums = ['A', '2', '3', '4', '5', '6',
                     '7', '8', '9', '10', 'J', 'Q', 'K']
        self.specials = ['X', 'D']
        self.cardOrder = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8,
                          'J': 9, 'Q': 10, 'K': 11, 'A': 12, '2': 13, 'X': 14, 'D': 15}
        # player objects and dictionary
        self.p1 = player(p1id)
        self.p2 = player(p2id)
        # self.p3 = player(p3id)
        #每个人的手牌集合
        self.playerDict = {p1id: self.p1, p2id: self.p2}
        # some game states
        self.currentPlayer = ''
        self.prevPlayer = ''
        self.prevPlay = ['', []]
        self.playOrder = []
        self.landLordCards = []

    # helper function for sorting card
    def sortHelper(self, x):
        if x[-1] == '0':
            return self.cardOrder['10']
        return self.cardOrder[x[-1]]

    # encode game to a message
    def encodeGame(self, mod=0):
        return f'''#{str(mod)}#{self.p1.name}#{self.p1.identity}#{self.p1.cards}
        #{self.p2.name}#{self.p2.identity}#{self.p2.cards}
        #{self.p3.name}#{self.p3.identity}#{self.p3.cards}
        #{self.currentPlayer}#{self.prevPlay}#{self.playOrder}#{self.landLordCards}'''

    # generate and distribute the initial cards
    #生成和分发初始卡
    def shuffleDeck(self):
        self.deck = []
        for i in self.colors:
            for j in self.nums:
                self.deck.append(i+' '+j)
        self.deck.append(self.specials[0])
        self.deck.append(self.specials[1])
        random.shuffle(self.deck)

    # deal the initial cards randomly
    #随机分牌
    def dealCard(self):
        # self.landLordCards = []
        # #分三张给地主
        # for i in range(3):
        #     choice = random.choice(self.deck)
        #     self.landLordCards.append(choice)
        #     self.deck.remove(choice)
        #     print(self.landLordCards)
        # self.p1Card = []
        # for i in range(17):
        #     choice = random.choice(self.deck)
        #     self.p1Card.append(choice)
        #     self.deck.remove(choice)
        #     print(self.p1Card)
        #     for x in range(17):
        #         print(self.game1[x])
        #         self.p1Card.append(self.game1[x])
        #         self.deck.remove(self.game1[x])
        #         print(self.p1Card)
        # self.p2Card = []
        # for i in range(17):
        #     choice = random.choice(self.deck)
        #     self.p2Card.append(choice)
        #     self.deck.remove(choice)
        #     print(self.p2Card)
        # self.p3Card = []
        # for i in range(17):
        #     choice = random.choice(self.deck)
        #     self.p3Card.append(choice)
        #     self.deck.remove(choice)
        #     print(self.p3Card)
        self.p1.cards = self.game1
        self.p2.cards = self.game2
        # self.p3.cards = self.game3
        self.p1.cards.sort(key=lambda x: self.sortHelper(x))
        self.p2.cards.sort(key=lambda x: self.sortHelper(x))
        # self.p3.cards.sort(key=lambda x: self.sortHelper(x))
        print(self.p2.cards)


    # assign landlord
    #分配地主
    def chooseLandlord(self, name):
        self.playerDict[name].identity = 'p'
        # for card in self.tp:
        #     self.playerDict[name].cards.append(card)
        # self.playerDict[name].cards.sort(key=lambda x: self.sortHelper(x))

    # assign play sequence
    #决定出牌顺序
    def assignPlayOrder(self):
        #playorder:出牌顺序
        self.p1.identity = 'p'
        #这里指定了玩家直接为地主，从玩家开始出牌
        if self.p1.identity == 'p':
            self.playOrder = [self.p2.name]
            # random.shuffle(self.playOrder)
            self.playOrder.insert(0, self.p1.name)
        # elif self.p2.identity == 'p':
        #     self.playOrder = [self.p1.name]
        #     # random.shuffle(self.playOrder)
        #     self.playOrder.insert(0, self.p2.name)
        # elif self.p3.identity == 'p':
        #     self.playOrder = [self.p1.name, self.p2.name]
        #     random.shuffle(self.playOrder)
        #     self.playOrder.insert(0, self.p3.name)
        else:
            self.playOrder = [self.p1.name, self.p2.name]
            random.shuffle(self.playOrder)
        self.currentPlayer = self.playOrder[0]

    # identify pattern of played card
    def whichPattern(self, selectedCards):
        cardValues = []
        for i in selectedCards:
            if i[-1] == '0':  # special case of 10
                cardValues.append(self.cardOrder['10'])
            else:
                cardValues.append(self.cardOrder[i[-1]])
        pattern = utils.get_move_type(cardValues)
        return pattern

    # check play validity
    def isValidPlay(self, selected):
        selectedCards = sorted(selected, key=lambda x: self.sortHelper(x))
        if self.prevPlay[0] == self.currentPlayer:
            return True
        pattern1 = self.whichPattern(self.prevPlay[1])
        pattern2 = self.whichPattern(selectedCards)
        if pattern2['type'] == 15 or pattern1['type'] == 5:
            return False  # previous kingbomb or current invalid
        elif pattern2['type'] == 5 or pattern1['type'] == 0:
            return True  # current kingbomb or previous pass
        else:
            if pattern1['type'] == pattern2['type'] and\
                    pattern1['rank'] < pattern2['rank']:
                try:
                    if pattern1['len'] == pattern2['len']:
                        return True
                    return False
                except:
                    return True
            else:
                return False

    # make a play
    def makePlay(self, selectedCards):
        if selectedCards == [] and self.prevPlay != []:
            pass
        else:
            self.playerDict[self.currentPlayer].playCard(selectedCards)
            self.prevPlay = [self.currentPlayer, selectedCards]
        self.prevPlayer = self.currentPlayer
        if self.playerDict['AI1'].cards == []: #判断AI1 是否打完了手牌
            pygame.init()
            tkinter.Tk().wm_withdraw()  # to hide the main window
            tkinter.messagebox.showinfo(
                f'Winner is: AI', '很遗憾，通关失败!')
            pygame.init()
            pygame.quit()
        playerIndex = self.playOrder.index(self.currentPlayer)
        if playerIndex == 1:
            self.currentPlayer = self.playOrder[0]
        else:
            self.currentPlayer = self.playOrder[1]

    # check who wins
    def checkWin(self):
        print(self.playerDict['AI1'].cards)
        if self.playerDict[self.prevPlayer].cards == []:
            if self.playerDict[self.prevPlayer].identity == 'p':
                return 1  # player wins as professor
            else:
                return 2  # player wins as students
        elif self.playerDict['AI1'].cards == []:
            return 3 # AI1赢
        else:
            return 0  # 一直循环

    # create AI players
    def createAI(self, name2, name3):
        self.p2 = AI(name2)
        self.p3 = AI(name3)
        self.playerDict[name2] = self.p2
        self.playerDict[name3] = self.p3

    # AI makes a play
    def AIMakePlay(self, name, chosenLandLord):
        AIplayer = self.playerDict[name]
        print('+++++++++++')
        print(AIplayer.cards)#当前AI的手牌
        print('++++++++')
        if chosenLandLord:
            moves = AIplayer.getAllMoves()
            #moves 电脑这个回合可以出的所有牌型组合
            possibleMoves = []
            for move in moves:
                realcards = []
                for card in move:
                    for hand in AIplayer.cards:
                        if hand[-1] == card[-1] and hand not in realcards:
                            realcards.append(hand)
                if self.isValidPlay(realcards):
                    possibleMoves.append(realcards)
            possibleMoves.append([])
            move = random.choice(possibleMoves)
            print(move)
            self.makePlay(move)
        else:
            self.chooseLandlord(name)
            self.assignPlayOrder()


# class for a game player
class player:
    def __init__(self, name):
        self.name = name
        self.identity = 's'
        self.cards = []

    # make a play
    def playCard(self, selectedCards):
        for i in selectedCards:
            self.cards.remove(i)


# class for an AI player
class AI:
    def __init__(self, name):
        self.name = name
        self.identity = 's'
        self.cards = []

    # make a play
    def playCard(self, selectedCards):
        for i in selectedCards:
            self.cards.remove(i)

    # get all possible moves
    def getAllMoves(self):
        envmoves = utils.MovesGener(self.cards).gen_moves()
        EnvCard2RealCard = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                            8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q',
                            13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'}
        realmoves = []
        for move in envmoves:
            realmove = []
            for card in move:
                realmove.append(EnvCard2RealCard[card])
            realmoves.append(realmove)
        return realmoves