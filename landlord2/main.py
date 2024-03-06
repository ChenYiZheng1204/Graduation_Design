'''
main.py description
goMulti：启动mutliplayer窗口
goHost：以主机身份开始游戏
goClient：以客户端身份启动游戏
goSolo：以单人身份开始游戏
goHome：启动主屏幕
这可以直接调用以启动主游戏
'''


import os
from consql import conn
import tkinter
import tkinter.font as font
import host
import client
import single
from GameEngine import Game
from PIL import Image,ImageTk

from imgs import bg
# go to mutliplayer window
def goMulti(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("500x400")
    wnd.title("Fight the Professor!")
    mainframe = tkinter.Frame(wnd)
    mainframe.pack()
    lab = tkinter.Label(
        mainframe, text="Choose whether you're a\n host or a client:\n")
    lab['font'] = font.Font(size=20)
    lab.pack()
    btn1 = tkinter.Button(mainframe, text="Play as host",
                          width=18, height=5, command=lambda: goHost(wnd))
    btn1['font'] = font.Font(size=14)
    btn1.pack()
    btn2 = tkinter.Button(mainframe, text="Play as client",
                          width=18, height=5, command=lambda: goClient(wnd))
    btn2['font'] = font.Font(size=14)
    btn2.pack()
    wnd.mainloop()


# start game as host
def goHost(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("500x400")
    wnd.title("与教授战斗！")
    #wnd.resizable(0, 0)
    loginGUIObj = host.loginGUI(wnd)
    wnd.mainloop()


# start game as client
def goClient(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("500x400")
    wnd.title("与教授战斗！")
    wnd.resizable(0, 0)
    loginGUIObj = client.loginGUI(wnd)
    wnd.mainloop()


# start game as single player
def goSolo(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("与教授战斗！")
    wnd.resizable(0, 0)
    # game = Game('human', 'AI1', 'AI2',1)
    game = Game('human', 'AI1',1)
    singleGUIObj = single.singleGUI(game)
    wnd.mainloop()

def goSolo2(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("与教授战斗！")
    wnd.resizable(0, 0)
    # game = Game('human', 'AI1', 'AI2',2)
    game = Game('human', 'AI1',2)
    singleGUIObj = single.singleGUI(game)
    wnd.mainloop()

def goSolo3(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("与教授战斗！")
    wnd.resizable(0, 0)
    # game = Game('human', 'AI1', 'AI2',3)
    game = Game('human', 'AI1',3)

    singleGUIObj = single.singleGUI(game)
    wnd.mainloop()
def goSolo4(parent=None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("与教授战斗！")
    wnd.resizable(0, 0)
    # game = Game('human', 'AI1', 'AI2',4)
    game = Game('human', 'AI1',4)
    singleGUIObj = single.singleGUI(game)
    wnd.mainloop()

#屏幕居中函数
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
    screenheight = root.winfo_screenheight()  # 获取显示屏高度
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)  # 设置窗口居中参数
    root.geometry(size)  # 让窗口居中显示

def selectlevel(parent = None):
    if parent:
        parent.destroy()
    wnd = tkinter.Tk()
    wnd.geometry("800x600")
    wnd.title("请选择游戏难度:")
    center_window(wnd,800,600)
    wnd.resizable(0, 0)
    mainframe = tkinter.Frame(wnd)
    mainframe.pack()
    titleLab = tkinter.Label(mainframe, text="选择游戏关卡")
    titleLab['font'] = font.Font(size=24, weight='bold', slant='italic')
    titleLab.pack()
    lab = tkinter.Label(mainframe, text="选择游戏模式\n")
    lab['font'] = font.Font(size=20)
    lab.pack()
    btn1 = tkinter.Button(mainframe, text="关卡1",
                          height=5, width=15, command=lambda: goSolo(wnd))
    btn1['font'] = font.Font(size=14)
    btn1.pack()
    btn2 = tkinter.Button(mainframe, text="关卡2",
                          height=5, width=15, command=lambda: goSolo2(wnd))
    btn2['font'] = font.Font(size=14)
    btn2.pack()
    btn3 = tkinter.Button(mainframe, text="关卡3",
                          height=5, width=15, command=lambda: goSolo3(wnd))
    btn3['font'] = font.Font(size=14)
    btn3.pack()
    btn4 = tkinter.Button(mainframe, text="关卡4",
                          height=5, width=15, command=lambda: goSolo4(wnd))
    btn4['font'] = font.Font(size=14)
    btn4.pack()
    wnd.mainloop()

# open the main window
def goHome(parent=None):
    class User:
        def __init__(self):
            self.username = None
            self.pwd = None
    Nowuser = User()
    pwd = tkinter.Tk()
    # pwd.geometry("400x300")
    pwd.title("登陆界面")
    mainpwd = tkinter.Frame(pwd,bg="skyblue")
    center_window(pwd,450,300)
    mainpwd.pack(fill='both',ipadx=10,ipady=10,expand=True)
    tkinter.Label(mainpwd,text = "账户名",width=8,height=2).grid(row = 0,column=0,padx=(10,0),pady=10)
    tkinter.Label(mainpwd,text = "密码",width=8,height=2).grid(row = 1,column=0,padx=(10,0))
    nameinput = tkinter.Entry(mainpwd)
    passinput = tkinter.Entry(mainpwd)
    nameinput.grid(row=0, column=1,columnspan=3,padx=(0,10),ipadx=60)
    passinput.grid(row=1, column=1,columnspan=3,padx=(0,10),ipadx=60)
    # nametitle['font'] = font.Font(size = 24,weight='bold',slant='italic')
    # nametitle.pack()
    # passtitle['font'] = font.Font(size=24, weight='bold', slant='italic')
    # passtitle.pack()
    # nameinput.pack()

    def getmess():
        print("用户名:%s" % nameinput.get())
        print("密码:%s" % passinput.get())
        Nowuser.username = nameinput.get()
        Nowuser.pwd = passinput.get()
        def send_data(na,pw):
            from consql import conn
            a = conn.get_name_id(na,pw)
            return a
        result = send_data(Nowuser.username,Nowuser.pwd)
        print(result)
        if result == 0:
            nameinput.delete(0, "end")
            passinput.delete(0, "end")
            pwd.destroy()
            if parent:
                parent.destroy()
            wnd = tkinter.Tk()
            wnd.geometry("800x800")
            wnd.title("斗地主残局系统")
            mainframe = tkinter.Frame(wnd, bg='pink')
            center_window(wnd,800,800)
            mainframe.pack(fill='both', ipadx=10, ipady=10, expand=True)
            titleLab = tkinter.Label(mainframe, text="斗地主残局系统")
            titleLab['font'] = font.Font(size=24, weight='bold', slant='italic')
            titleLab.pack()
            lab = tkinter.Label(mainframe, text="选择游戏模式\n")
            lab['font'] = font.Font(size=20)
            lab.pack()
            btn1 = tkinter.Button(mainframe, text="选择游戏关卡",
                                  height=5, width=15, command=lambda: selectlevel(wnd))
            btn1['font'] = font.Font(size=14)
            btn1.pack()
            btn2 = tkinter.Button(mainframe, text="从第一关开始游戏",
                                  height=5, width=15, command=lambda: goSolo(wnd))
            btn2['font'] = font.Font(size=14)
            btn2.pack()
            wnd.mainloop()
        else:
            if Nowuser.username == '' or Nowuser.pwd == '':
                warn = tkinter.Tk()
                center_window(warn, 300, 150)
                warn.title("提示")
                warntitle = tkinter.Label(warn, text="用户名和密码不允许为空")
                warntitle.pack()
            else:
                warn = tkinter.Tk()
                center_window(warn, 300, 150)
                warn.title("提示")
                warntitle = tkinter.Label(warn, text="用户名或者密码错误，登陆失败")
                warntitle.pack()


    def enroll():
        pwd.withdraw()
        en = tkinter.Tk()
        center_window(en,400,250)
        en.title("注册页面")
        mainen = tkinter.Frame(en, bg="skyblue")
        mainen.pack(fill='both', ipadx=10, ipady=10, expand=True)
        tkinter.Label(mainen, text="设置您的账户名", width=8, height=2).grid(row=0, column=0, padx=(10, 0), pady=10)
        tkinter.Label(mainen, text="设置您的密码", width=8, height=2).grid(row=1, column=0, padx=(10, 0))
        ennameinput = tkinter.Entry(mainen)
        enpassinput = tkinter.Entry(mainen)
        ennameinput.grid(row=0, column=1, columnspan=3, padx=(0, 10), ipadx=60)
        enpassinput.grid(row=1, column=1, columnspan=3, padx=(0, 10), ipadx=60)
        #返回登陆页面函数
        def get_rs():
            en.destroy()
            pwd.deiconify()
        def User_enroll():
            from consql import conn
            na = ennameinput.get()
            pw = enpassinput.get()
            a = conn.resgin_name_id(na, pw)
            print(a)
            if a == 0:
                warn = tkinter.Tk()
                center_window(warn, 300, 150)
                warn.title("提示")
                warntitle = tkinter.Label(warn, text="用户名已存在")
                warntitle.pack()
            elif a == 1:
                warn = tkinter.Tk()
                center_window(warn, 300, 150)
                warn.title("提示")
                warntitle = tkinter.Label(warn, text="用户名或者密码不可为空")
                warntitle.pack()
            elif a == 2:
                ms = tkinter.Tk()
                center_window(ms, 300, 150)
                ms.title("提示")
                warntitle = tkinter.Label(ms, text="注册成功")
                warntitle.pack()


        tkinter.Button(mainen, text="确认", command=User_enroll, width=8, height=2).grid(row=2, column=1, sticky="w",padx=30, pady=10)
        tkinter.Button(mainen, text="返回", command=get_rs, width=8, height=2).grid(row=2, column=2, sticky="w",padx=30, pady=10)


    tkinter.Button(mainpwd, text="登录", command=getmess,width=8,height=2).grid(row=2, column=1, sticky="w", padx=30, pady=10)
    tkinter.Button(mainpwd,text="注册",command=enroll,width=8,height=2).grid(row=2,column=2,sticky="w",padx=30)
    tkinter.Button(mainpwd, text="退出", command=mainpwd.quit,width=8,height=2).grid(row=2, column=3, sticky="e", padx=30)

    mainpwd.mainloop()


if __name__ == '__main__':
    goHome()