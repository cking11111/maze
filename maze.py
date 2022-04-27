# @skyclear
# -*-coding:utf-8 -*-
import time
import os, sys, pygame
from pygame import font
from pygame.locals import *
import numpy as np
class Button():
    def __init__(self,msg):
        self.width=200
        self.height=50
        self.button_color=(0,0,0)
        self.text_color=(255,255,255)
        self.font=font.SysFont('Arial',50)
        # self.rect=pygame.Rect(700,70,self.width,self.height)
        self.prep_msg(msg)
    def prep_msg(self,msg):
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)

    def draw_button(self,screen,location):
        self.rect=pygame.Rect(location[0],location[1],self.width,self.height)
        screen.blit(self.msg_image,self.rect)
        pygame.display.update()
    def set_msg(self,msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)

def isequal(rect1,rect2):
  if rect1.left==rect2.left and rect1.right==rect2.right:
      if rect1.top==rect2.top and rect2.bottom==rect2.bottom:
          return True
  return False
# 游戏主角是机器人android
class Android:
    # 初始化类
    def __init__(self, img, rect, speed):
        # rect 是机器人的位置，speed则是移动速度
        self.ful_img = img
        self.rect = rect
        self.speed = speed
        self.steps=0
    def draw(self,screen):
        screen.blit(self.ful_img, self.rect)
    def setrect(self,g,h,screen):
        self.rect.left=h*20
        self.rect.top=g*20
        screen.blit(self.ful_img,self.rect)
        self.draw(screen)
        pygame.display.update()
        # 定时装置
    # 当按下键盘时，移动机器人
    def update(self, screen, press_keys):
        global isOver  # 声明这是全局变量
        # 根据按下的方向键来移动机器人
        if press_keys==pygame.K_LEFT:
            temp=self.rect.left
            self.rect.left -= self.speed
            # 如果碰壁则无法再移动
            if self.rect.left <= 0:
                self.rect.left = 0
            # 判断是否碰撞，70是一个基数是障碍物方块边长
            for block in block_group:
                if isequal(self.rect,block.rect):
                    self.rect.left+=self.speed
                    break
            # 接下来的if...else用于使机器人产生向左移动时的动画
            screen.blit(self.ful_img, self.rect)
            if isequal(self.rect,sf[1].rect):
                isOver=True
            if temp!=self.rect.left:
                self.steps+=1
        if press_keys==pygame.K_RIGHT:
            temp = self.rect.left
            self.rect.left += self.speed

            # 如果碰壁则无法再移动
            if self.rect.right >= 700:
                self.rect.right = 700
            # 判断是否碰撞，70是一个基数是障碍物方块边长
            for block in block_group:  # block_group列表记录所有的方块，最后一位记录终点方块，判断胜利调用最后一位，除此之外不涉及最后一位
                # 此后两个if判断与某一方块是否碰撞
                if isequal(self.rect,block.rect):
                        self.rect.left -= self.speed
                        break
            if temp != self.rect.left:
                self.steps += 1
            screen.blit(self.ful_img, self.rect)
            # 判断是否胜利
            if isequal(self.rect,sf[1].rect):
                    isOver = True
            # 接下来的if...else用于使机器人产生向右移动时的动画


        if press_keys==pygame.K_UP:
            temp = self.rect.top
            self.rect.top -= self.speed

            # 如果碰壁则无法再移动
            if self.rect.top <= 0:
                self.rect.top = 0
            # 判断是否碰撞，70是一个基数是障碍物方块边长
            for block in block_group:  # block_group列表记录所有的方块，最后一位记录终点方块，判断胜利调用最后一位，除此之外不涉及最后一位
                # 此后两个if判断与某一方块是否碰撞
                if isequal(self.rect, block.rect):
                    self.rect.top += self.speed
                    break
            screen.blit(self.ful_img, self.rect)
            # 判断是否胜利
            if isequal(self.rect, sf[1].rect):
                isOver = True
            if temp!=self.rect.top:
                self.steps+=1
        if press_keys==pygame.K_DOWN:
            temp = self.rect.top
            self.rect.top += self.speed

            # 如果碰壁则无法再移动
            if self.rect.bottom >= 700:
                self.rect.bottom = 700
            # 判断是否碰撞，70是一个基数是障碍物方块边长
            for block in block_group:  # block_group列表记录所有的方块，最后一位记录终点方块，判断胜利调用最后一位，除此之外不涉及最后一位
                # 此后两个if判断与某一方块是否碰撞
                if isequal(self.rect, block.rect):
                    self.rect.top -= self.speed
                    break
            screen.blit(self.ful_img, self.rect)

            # 判断是否胜利
            if isequal(self.rect, sf[1].rect):
                isOver = True
            if temp!=self.rect.top:
                self.steps+=1


# 由于需要判断碰撞，所以无法简单绘制障碍物，需设置障碍物类
class Block:
    def __init__(self, img, rect):
        self.img = img
        self.rect = rect

    # 绘制障碍物方块
    def draw(self, screen):
        screen.blit(self.img, self.rect)


# 绘制背景方块
def drawBackground(screen):
    global start_location
    # 清空列表,初始化
    block_group.clear()

    # 定义障碍物
    block1_img = pygame.image.load('block1.png').convert()
    final1_img=pygame.image.load('final1.png').convert()
    # 通过background_group这个二维List进行迷宫的绘制
    for i in range(35):
        for j in range(35):
            if background_group[i][j] == 1:
                block = Block(block1_img, Rect(20 * j, 20 * i, 20, 20))  # 初始化障碍物方块
                block.draw(screen)  # 绘制障碍物方块
                block_group.append(block)  # 向列表中加入该方块
            elif background_group[i][j]=='f':
                final=Block(final1_img,Rect(20*j,20*i,20,20))

                final.draw(screen)
                sf[1]=final

            elif background_group[i][j]=='s':
                start=Block(final1_img,Rect(20*j,20*i,20,20))
                start.draw(screen)
                sf[0]=start


def seekpath(i,j,Andr,screen):
    global flag
    if flag==False:
        return
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # 当有按键按下时调用机器人类进行更新
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flag=False
            return
    global label_steps
    background1 = pygame.image.load('bgp.png').convert()
    screen.fill(white,(0,0,700,700))
    # 屏幕填充为背景图
    screen.blit(background1, (0, 0))
    # 调用方法绘制背景障碍物方块
    drawBackground(screen)
    Andr.draw(screen)
    pygame.display.update()
    if background_group[i][j]=='f':
        return True
    for n in range(4):
        g=i+mover[n].a
        h=j+mover[n].b
        d=mover[n].dir
        if 0<=g<=34 and 0<=h<=34 and background_group[g][h] in [0,'f'] and mark[g][h]==0 :
            mark[g][h]=1
            Andr.steps+=1
            label_steps.set_msg(str(Andr.steps))
            label_steps.draw_button(screen,(750,560))
            screen.fill(white,(0,0,700,700))
            # 屏幕填充为背景图
            screen.blit(background1, (0, 0))
            # 调用方法绘制背景障碍物方块
            drawBackground(screen)
            Andr.setrect(g,h, screen)
            Andr.draw(screen)
            pygame.display.update()
            # os.system('pause')
            time.sleep(0.1)
            if seekpath(g,h,Andr,screen):
                res.append((g,h))
                return True
    Andr.steps-=1
    return False
class move:
    def __init__(self,a,b):
        self.a=a
        self.b=b
        if a==0 and b==1:
            self.dir='right'
        elif a==1 and b==0:
            self.dir='down'
        elif a==-1 and b==0:
            self.dir='up'
        elif a==0 and b==-1:
            self.dir='left'
def dfs():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # 定义机器人移动速度
    speed_android = 20
    # 定义间隔时间，没过一个间隔时间进行一次循环判断
    dwTime = 100
    # 定义机器人所占的空间，为一个矩形,Rect(左上角位置横坐标，左上角位置纵坐标，长，宽)
    r_android = Rect(20, 20, 20, 20)
    # 初始化pygame
    pygame.init()
    # 定义时钟
    clock = pygame.time.Clock()
    # 定义屏幕
    screen = pygame.display.set_mode(size)
    # 定义机器人图画
    android = pygame.image.load('mover1.png').convert_alpha()
    # 定义背景
    background1 = pygame.image.load('bgp.png').convert()
    # 定义一个Android
    Andr = Android(android, r_android, speed_android)
    # 设置窗口标题
    pygame.display.set_caption("迷宫游戏")
    # 开始循环
    mover.append(move(0,-1))
    mover.append(move(0,1))
    mover.append(move(-1,0))
    mover.append(move(1,0))
    seekpath(1,1,Andr,screen)
    screen.fill(white)
    # 屏幕填充为背景图
    screen.blit(background1, (0, 0))
    # 调用方法绘制背景障碍物方块
    drawBackground(screen)
def auto_game():


    dfs()
    list.reverse(res)
    for i in res:
        if res.index(i) == len(res) - 1:
            print(i)
        else:
            print(i, end='->')
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
def check_button(button,mouse_x,mouse_y):
    if button.rect.collidepoint(mouse_x,mouse_y):
        return True
    else:
        return False
def get_0_1_array(array):
    '''按照数组模板生成对应的 0-1 矩阵，默认rate=0.2'''
    zeros_num = int(array.size * 0.7)#根据0的比率来得到 0的个数
    new_array = np.ones(array.size)#生成与原来模板相同的矩阵，全为1
    new_array[:zeros_num] = 0 #将一部分换为0
    new_array[zeros_num]=2
    new_array[zeros_num+1]=3
    np.random.shuffle(new_array)#将0和1的顺序打乱
    re_array = new_array.reshape((35,35)).astype(int)#重新定义矩阵的维度，与模板相同
    return re_array
def mark_init(mark):
    for i in range(len(mark)):
        for j in range(len(mark[0])):
            mark[i][j]=0
if __name__ == "__main__":
    size = (900, 700)  # 对话框大小
    res = []
    flag=True
    white = (255, 255, 255)  # 定义白色
    mark = []
    for i in range(35):
        c = []
        for j in range(35):
            c.append(0)
        mark.append(c)
    block_group = []  # 障碍物组
    sf = [0 for i in range(2)]
    isOver = False  # 判断游戏是否结束
    mover = []
    # 定义迷宫的二维list,0为可走为空，1为填充砖块处
    temp = get_0_1_array(np.ones(35 * 35)).astype(int).tolist()

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # 定义机器人移动速度
    speed_android = 20
    # 定义间隔时间，没过一个间隔时间进行一次循环判断
    dwTime = 30
    # 定义机器人所占的空间，为一个矩形,Rect(左上角位置横坐标，左上角位置纵坐标，长，宽)

    r,c=list(np.argwhere(np.array(temp)==2))[0]
    for i in range(35):
        for j in range(35):
            if temp[i][j] == 2:
                temp[i][j] = 's'
                start_location = (i, j)
            if temp[i][j] == 3:
                temp[i][j] = 'f'
    background_group = temp
    r_android = Rect(c*20, r*20, 20, 20)
    # 初始化pygame
    pygame.init()
    # 定义时钟
    start_rect=pygame.Rect(c*20,r*20,20,20)   #机器人起始位置
    start_location=r_android
    clock = pygame.time.Clock()
    # 定义屏幕
    screen = pygame.display.set_mode(size)
    # 定义机器人图画
    android = pygame.image.load('mover1.png').convert_alpha()
    # 定义背景
    background1 = pygame.image.load('bgp.png').convert()
    # 定义一个Android
    Andr = Android(android, r_android, speed_android)
    # 定义按钮
    button_play = Button('play')
    button_auto = Button('auto')
    button_reset = Button('reset')
    button_steps = Button('steps:')
    label_steps=Button(str(Andr.steps))
    label_win=Button('You win!')
    label_fail=Button("Don't find a right path!")
    label_caption=Button('Welcome to maze ')
    # 设置窗口标题
    pygame.display.set_caption("迷宫游戏")

    button_play.draw_button(screen, (750, 70))
    button_reset.draw_button(screen, (750, 210))
    button_auto.draw_button(screen, (750, 350))
    button_steps.draw_button(screen, (750, 490))
    label_steps.draw_button(screen,(750,560))
    label_caption.draw_button(screen,(280,300))
    play=False
    reset=False
    while True:
        if play:

            screen.fill(white, (0, 0, 700, 700))
            # 屏幕填充为背景图
            screen.blit(background1, (0, 0))
            # 调用方法绘制背景障碍物方块
            drawBackground(screen)
            Andr.draw(screen)

            pygame.display.update()


        if isOver:
            # screen.fill(white,(0,0,700,700))
            label_win.draw_button(screen,(300,300)) # 绘制胜利背景
            pygame.display.update()

            play=False
            # clock.tick(1000)
            Andr.setrect(start_rect.top // 20, start_rect.left // 20, screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # 当有按键按下时调用机器人类进行更新
            elif event.type==KEYDOWN:
                press_keys=event.key
        # press_keys = pygame.key.get_pressed()
                Andr.update(screen, press_keys)
                label_steps.set_msg(str(Andr.steps))
                label_steps.draw_button(screen,(750,560))
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y=pygame.mouse.get_pos()
                if check_button(button_play,mouse_x,mouse_y) and play==False:
                    # 屏幕填充为白色
                    screen.fill((0,0,0),(750,560,100,50))
                    Andr.steps=0
                    label_steps.set_msg(str(0))
                    label_steps.draw_button(screen,(750,560,100,50))
                    screen.fill(white, (0, 0, 700, 700))
                    # 屏幕填充为背景图
                    screen.blit(background1, (0, 0))
                    # 调用方法绘制背景障碍物方块
                    drawBackground(screen)
                    pygame.display.update()
                    play=True
                    isOver=False
                elif check_button(button_reset,mouse_x,mouse_y):
                    screen.fill(white, (0, 0, 700, 700))
                    # 屏幕填充为背景图
                    screen.fill((0, 0, 0), (750, 560, 100, 50))
                    Andr.steps = 0
                    label_steps.set_msg(str(0))
                    label_steps.draw_button(screen, (750, 560, 100, 50))
                    screen.blit(background1, (0, 0))
                    # 调用方法绘制背景障碍物方块
                    temp=get_0_1_array(np.ones(35*35)).astype(int).tolist()
                    for i in range(35):
                        for j in range(35):
                            if temp[i][j]==2:
                                temp[i][j]='s'
                                start_location=(i,j)
                            if temp[i][j]==3:
                                temp[i][j]='f'
                    background_group=temp
                    width=(start_location[1])*20
                    height=(start_location[0])*20
                    start_rect=pygame.Rect(width,height,20,20)
                    Andr.setrect(start_location[0],start_location[1],screen)
                elif check_button(button_auto,mouse_x,mouse_y):
                    flag=True
                    screen.fill((0, 0, 0), (750, 560, 100, 50))
                    Andr.steps = 0
                    label_steps.set_msg(str(0))
                    label_steps.draw_button(screen, (750, 560, 100, 50))
                    play=False
                    mover.append(move(0, -1))
                    mover.append(move(0, 1))
                    mover.append(move(-1, 0))
                    mover.append(move(1, 0))
                    if seekpath(start_rect.top//20, start_rect.left//20, Andr, screen):
                        screen.fill(white,(0,0,700,700))

                    # 屏幕填充为背景图
                    #     screen.blit(background1, (0, 0))
                        label_win.draw_button(screen,(300,300))
                        pygame.display.update()

                    # 调用方法绘制背景障碍物方块

                    else:
                            label_fail.draw_button(screen,(300,300))
                            pygame.display.update()
                    mark_init(mark)
                    Andr.setrect(start_rect.top//20,start_rect.left//20,screen)


        if play:
            Andr.draw(screen)
            pygame.display.update()
            # 定时装置
            clock.tick(dwTime)
