'''
single.py description
singleGUI类：用于创建游戏窗口的类
__init__：获取游戏对象并初始化对象和GUI
confirmIdentity：确认教授身份
passIdentity：放弃成为教授的机会
selectCard：将卡对象标记为选中
取消选择卡：取消选择已选择的卡
confirmCard：确认打牌
passCard：通过转弯
updateScreen：使用游戏对象更新游戏屏幕
initGUI:初始化pygame GUI和游戏对象
run：运行pygame窗口和所有需要运行的内容
可以直接调用此文件来创建单人游戏窗口
'''

import tkinter
import pygame
from chatComm import *
import tkinter.messagebox
from pygameWidgets import *
from GameEngine import *
import time
import threading
pygame.init()
pygame.font.init()

# class for the single player game window
class singleGUI:
    def __init__(self, Game):
        # initialize main parameters
        self.name = Game.p1.name
        self.width = 800
        self.height = 600
        self.fps = 20
        self.title = "斗地主残局对战系统"
        self.bgColor = (255, 255, 255)
        self.bg = pygame.image.load('./imgs/bg/tartanbg.png')
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        # initialize game object
        self.Game = Game
        self.Game.p2 = AI(self.Game.p2.name)
        # self.Game.p3 = AI(self.Game.p3.name)
        #总的出牌顺序
        self.Game.playerDict = {self.Game.p1.name: self.Game.p1,
                                self.Game.p2.name: self.Game.p2}
        self.player = self.Game.p1
        self.objs = []
        self.AIcardDict = {}
        self.cardDict = {}
        self.selectedCards = []
        self.chosenLandlord = False
        self.prevPlayTime = time.time()
        pygame.init()
        self.run()

    # confirm proofessor identity
    def confirmIdentity(self):#确认身份
        self.Game.chooseLandlord(self.name)
        self.chosenLandlord = True
        self.Game.assignPlayOrder()
        self.prevPlayTime = time.time()
        self.updateScreen()

    # pass professor identity
    def passIdentity(self):
        self.Game.makePlay([])
        self.prevPlayTime = time.time()
        self.updateScreen()

    # select cards
    def selectCard(self, cardVal):
        if cardVal not in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.append(cardVal)

    # deselect cards
    def deSelect(self, cardVal):
        if cardVal in self.selectedCards and cardVal in self.player.cards:
            self.selectedCards.remove(cardVal)

    # confirm card play
    def confirmCard(self):
        pygame.init()
        if self.selectedCards != [] and self.Game.isValidPlay(self.selectedCards):
            self.Game.makePlay(self.selectedCards)
            self.selectedCards = []
            mod = self.Game.checkWin()
            print(mod)
            if mod == 1:  # current player wins as professor
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {self.Game.prevPlayer}', '恭喜你，成功通过此关卡!')
                pygame.quit()
            elif mod == 2:  # current player wins as student
                tkinter.Tk().wm_withdraw()  # to hide the main window
                tkinter.messagebox.showinfo(
                    f'Winner is: {self.Game.prevPlayer}', '恭喜你，成功通过此关卡!')
                pygame.quit()
            self.prevPlayTime = time.time()
            self.updateScreen()
        elif self.Game.prevPlay == []:  # show error
            tkinter.Tk().wm_withdraw()
            tkinter.messagebox.showwarning('Warning', 'Invalid play!')

    # pass turn
    def passCard(self):
        if self.selectedCards == []:
            self.Game.makePlay([])
            self.prevPlayTime = time.time()
            self.updateScreen()

    # update screen from game object
    def updateScreen(self):
        # clear everything
        self.objs.clear()#初始化
        # update hand cards更新手牌
        #cardDict 分发的初始卡牌 player.cards 对局中的卡牌，随着对局进行变化
        for i in self.cardDict:
            if i not in self.player.cards:
                self.cardDict[i] = None
        for i in self.AIcardDict:
            if i not in self.Game.maingame2:
                self.AIcardDict[i] = None
        xStart = 50
        AIStart = 50
        #手牌长度
        cardCnt = len(self.player.cards)
        AIcardCnt = len(self.Game.maingame2)
        for card in self.player.cards:
            if card not in self.cardDict:
                cardObj = Card(self.screen, card, xStart, 430, 50, 70, lambda x=card: self.selectCard(
                    x), lambda x=card: self.deSelect(x))
                self.cardDict[card] = cardObj
            else:
                cardObj = self.cardDict[card]
                cardObj.x = xStart
            # print(self.Game.prevPlay[1])#当前对局出的牌
            if cardObj not in self.objs:
                self.objs.append(cardObj)
            xStart += 700/cardCnt

        for card in self.Game.maingame2:
            if card not in self.AIcardDict:
                AIcardObj = Card(self.screen, card, AIStart, 40, 50, 70, lambda x=card: self.selectCard(
                    x), lambda x=card: self.deSelect(x))
                self.AIcardDict[card] = AIcardObj
            else:
                AIcardObj = self.AIcardDict[card]
                AIcardObj.x = AIStart
            # print(self.Game.prevPlay[1])#当前对局出的牌
            if AIcardObj not in self.objs:
                self.objs.append(AIcardObj)
            AIStart += 700/AIcardCnt

        xStart = 230
        cardCnt = len(self.Game.prevPlay[1])
        #!=0 出了至少一张牌
        if cardCnt != 0:
            for card in self.Game.prevPlay[1]:
                prevPlayObj = Card(self.screen, card, xStart, 180, 50, 70)
                self.objs.append(prevPlayObj)
                xStart += 350/cardCnt
        # update landlord cards#更新地主牌
        if self.chosenLandlord == True:
            xStart = 320
            for card in self.Game.landLordCards:
                landlordCardObj = Card(self.screen, card, xStart, 40, 50, 70)
                # self.objs.append(landlordCardObj)
                xStart += 200/3
        # update current player
        text = f"Current playing: {self.Game.currentPlayer}"

        currentPlayerTextObj = Text(self.screen, text, 230, 120, 350, 50)
        self.objs.append(currentPlayerTextObj)
        # update avatars and positions
        myPos = 0
        if myPos == 0:
            #玩家做地主后进行的设置
            self.prevPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[1]], 700, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.prevPlayer)
            self.nextPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[1]], 700, 70, 60, 20, self.chosenLandlord)
            self.objs.append(self.nextPlayer)
            self.myPlayer = Player(
                self.screen, self.Game.playerDict[self.Game.playOrder[0]], 370, 570, 60, 20, self.chosenLandlord)
            self.objs.append(self.myPlayer)
            self.prevImg = Img(
                self.screen, self.Game.playerDict[self.Game.playOrder[1]], 700, 10, 60, 60)
            self.objs.append(self.prevImg)
            self.afterImg = Img(
                self.screen, self.Game.playerDict[self.Game.playOrder[1]], 700, 10, 60, 60)
            self.objs.append(self.afterImg)
            self.myImg = Img(
                self.screen, self.Game.playerDict[self.Game.playOrder[0]], 370, 510, 60, 60)
            self.objs.append(self.myImg)
            self.prevCardCnt = Text(
                self.screen, str(len(self.Game.playerDict[self.Game.playOrder[1]].cards)), 720, 90, 20, 20)
            self.objs.append(self.prevCardCnt)
            self.afterCardCnt = Text(
                self.screen, str(len(self.Game.playerDict[self.Game.playOrder[1]].cards)), 720, 90, 20, 20)
            self.objs.append(self.afterCardCnt)
        # elif myPos == 1:
        #     #AI1做地主后进行的设置
        #     self.prevPlayer = Player(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[0]], 50, 70, 60, 20, self.chosenLandlord)
        #     self.objs.append(self.prevPlayer)
        #     self.nextPlayer = Player(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[2]], 700, 70, 60, 20, self.chosenLandlord)
        #     self.objs.append(self.nextPlayer)
        #     self.myPlayer = Player(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[1]], 370, 570, 60, 20, self.chosenLandlord)
        #     self.objs.append(self.myPlayer)
        #     self.prevImg = Img(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[0]], 50, 10, 60, 60)
        #     self.objs.append(self.prevImg)
        #     self.afterImg = Img(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[2]], 700, 10, 60, 60)
        #     self.objs.append(self.afterImg)
        #     self.myImg = Img(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[1]], 370, 510, 60, 60)
        #     self.objs.append(self.myImg)
        #     self.prevCardCnt = Text(
        #         self.screen, str(len(self.Game.playerDict[self.Game.playOrder[0]].cards)), 70, 90, 20, 20)
        #     self.objs.append(self.prevCardCnt)
        #     self.afterCardCnt = Text(
        #         self.screen, str(len(self.Game.playerDict[self.Game.playOrder[2]].cards)), 720, 90, 20, 20)
        #     self.objs.append(self.afterCardCnt)
        # else:
        #     #AI2做地主进行的设置
        #     self.prevPlayer = Player(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[1]], 50, 70, 60, 20, self.chosenLandlord)
        #     self.objs.append(self.prevPlayer)
        #     self.nextPlayer = Player(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[0]], 700, 70, 60, 20, self.chosenLandlord)
        #     self.objs.append(self.nextPlayer)
        #     self.myPlayer = Player(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[2]], 370, 570, 60, 20, self.chosenLandlord)
        #     self.objs.append(self.myPlayer)
        #     self.prevImg = Img(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[1]], 50, 10, 60, 60)
        #     self.objs.append(self.prevImg)
        #     self.afterImg = Img(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[0]], 700, 10, 60, 60)
        #     self.objs.append(self.afterImg)
        #     self.myImg = Img(
        #         self.screen, self.Game.playerDict[self.Game.playOrder[2]], 370, 510, 60, 60)
        #     self.objs.append(self.myImg)
        #     self.prevCardCnt = Text(
        #         self.screen, str(len(self.Game.playerDict[self.Game.playOrder[1]].cards)), 70, 90, 20, 20)
        #     self.objs.append(self.prevCardCnt)
        #     self.afterCardCnt = Text(
        #         self.screen, str(len(self.Game.playerDict[self.Game.playOrder[0]].cards)), 720, 90, 20, 20)
        #     self.objs.append(self.afterCardCnt)
        # print(self.chosenLandlord)
        # print(self.Game.currentPlayer)
        # print(self.name)
        # update buttons
        if self.chosenLandlord and self.Game.currentPlayer == self.name:
            # print(self.Game.playerDict['human'].cards)
            self.passCardButton = Button(
                self.screen, 100, 350, 100, 50, 'Pass turn', self.passCard)
            self.objs.append(self.passCardButton)
            self.confirmCardButton = Button(
                self.screen, 600, 350, 100, 50, 'Confirm Play', self.confirmCard)
            self.objs.append(self.confirmCardButton)
            # test = Text(self.screen, '', 230, 120, 350, 50,self.confirmIdentity)
            # self.objs.append(test)
# 选择地主环节

        elif not self.chosenLandlord and self.Game.currentPlayer == self.name:
            self.passButton = Button(
                self.screen, 350, 350, 100, 50, 'begin', self.passIdentity)
            self.objs.append(self.passButton)
            # self.confirmButton = Button(
            #     self.screen, 600, 350, 100, 50, 'Be Professor', self.confirmIdentity)
            # self.objs.append(self.confirmButton)


    # initialize game GUI

    def initGUI(self):
        pygame.init()
        # set basic variables
        self.clock = pygame.time.Clock()
        self.prevPlayTime = time.time()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.bgColor)
        pygame.display.set_caption(self.title)
        # initialize game object
        self.Game.assignPlayOrder()
        self.Game.shuffleDeck()
        self.Game.dealCard()
        # update screen
        self.updateScreen()

    # main function to be called
    def run(self):
        self.initGUI()
        playing = True
        while playing:
            self.screen.fill(self.bgColor)
            self.screen.blit(self.bg, (0, 0))
            self.clock.tick(self.fps)
            self.updateScreen()
            if time.time() - self.prevPlayTime > 3:
                if self.Game.currentPlayer == 'AI1':
                    if self.chosenLandlord:
                        self.Game.AIMakePlay('AI1', self.chosenLandlord)
                    else:
                        self.Game.AIMakePlay('AI1', self.chosenLandlord)
                        self.chosenLandlord = True
                    self.prevPlayTime = time.time()
                # elif self.Game.currentPlayer == 'AI2':
                #     if self.chosenLandlord:
                #         self.Game.AIMakePlay('AI2', self.chosenLandlord)
                #     else:
                #         self.Game.AIMakePlay('AI2', self.chosenLandlord)
                #         self.chosenLandlord = True
                #     self.prevPlayTime = time.time()
            # to show the initial screen 显示最开始的屏幕
            for obj in self.objs:
                obj.process()
            for event in pygame.event.get():
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                    for obj in self.objs:
                        obj.process()
                if event.type == pygame.QUIT:
                    playing = False
            for obj in self.objs:
                obj.process()
            pygame.display.flip()
        pygame.quit()
        exit()


# start game as single player mode
if __name__ == "__main__":
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("Fight the Professor!")
    wnd.resizable(0, 0)
    game = Game('human', 'human2')
    singleGUIObj = singleGUI(game)
    wnd.mainloop()