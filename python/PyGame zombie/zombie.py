
import pygame, random, sys, time
#使用random模块来使用随机值
#使用sys模块的exit()函数用来退出程序
#使用time模块的sleep()暂停

from pygame.locals import *
#导入一些常用的函数和常量


#set up some variables
# 设置窗口大小
WINDOWWIDTH = 1024
WINDOWHEIGHT = 600

# 设置屏幕刷新率
FPS = 60

# 最大通过僵尸数量
MAXGOTTENPASS = 10

# 僵尸大小尺寸
ZOMBIESIZE = 70 #includes newKindZombies

# 增加新僵尸的帧率
ADDNEWZOMBIERATE = 50
ADDNEWKINDZOMBIE = ADDNEWZOMBIERATE

# 普通僵尸 和 特殊僵尸 的移动速度
NORMALZOMBIESPEED = 2
NEWKINDZOMBIESPEED = NORMALZOMBIESPEED / 2

# 豌豆射手的移动速度
PLAYERMOVERATE = 15

# 子弹的速度
BULLETSPEED = 10

# 增加新子弹的帧率
ADDNEWBULLETRATE = 15

# 文本颜色的RGB值：黄色
TEXTCOLOR = (255, 255, 0)
# 红色的RGB值 RED = (255, 0, 0)

# 游戏终止函数
def gameOver():
    pygame.quit()
    sys.exit()

# 玩家按键判断
# 如果关闭窗口或按下Esc键，则退出游戏，
# 如果按下回车，则重新回到主while继续游戏
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameOver()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    gameOver()
                if event.key == K_RETURN:
                    return

# 豌豆射手命中僵尸的碰撞检测
# Rect.colliderect() 为碰撞检测函数
def playerHasHitZombie(playerRect, zombies):
    for z in zombies:
        if playerRect.colliderect(z['rect']):
            return True
    return False


# 子弹命中普通僵尸的碰撞检测，如果命中则移除该子弹
def bulletHasHitZombie(bullets, zombies):
    for b in bullets:
        if b['rect'].colliderect(z['rect']):
            bullets.remove(b)
            return True
    return False

# 子弹命中特殊僵尸的碰撞检测，如果命中则移除该子弹
def bulletHasHitKind(bullets, newKindZombies):
    for b in bullets:
        if b['rect'].colliderect(c['rect']):
            bullets.remove(b)
            return True
    return False


# 文字颜色和位置，blit()函数 将文字绘制到界面的具体位置上
# 文字位置以左上角的位置为原点 绘制
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# set up pygame, the window, and the mouse cursor
# 设置游戏窗口大小、游戏场景、音乐等

# #初始化pygame，为使用硬件做准备
pygame.init()

# 初始化了一个Clock对象，用来设置游戏绘制的最大帧率 fps
mainClock = pygame.time.Clock()

# 创建了一个Surface窗口对象，大小为设置的宽度和高度
# 这个Surface对象会经常用到，我们可以在上面进行绘制
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#, pygame.FULLSCREEN)

# 设置了窗口标题
pygame.display.set_caption('豌豆射手大战僵尸')

# 隐藏鼠标
pygame.mouse.set_visible(False)

# 设置字体和大小
font = pygame.font.SysFont('SimHei', 32)

# 加载 背景音乐 和 游戏结束音乐
pygame.mixer.music.load('resources\\grasswalk.wav')
gameoverSound = pygame.mixer.Sound('resources\\gameover.wav')

# 加载 背景图片
backgroundImage = pygame.image.load('resources\\background.png')
# 使用pygame.transform.scale缩放原来的图片，并获取新的图片对象
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))

# 加载 gameover背景图片
gameoverImage = pygame.image.load('resources\\gameover.png')
# 使用pygame.transform.scale缩放原来的图片，并获取新的图片对象
rescaledGameover = pygame.transform.scale(gameoverImage, (WINDOWWIDTH, WINDOWHEIGHT))

# 加载 豌豆射手图片 并获取图片边距
playerImage = pygame.image.load('resources\\SnowPea.png')
playerRect = playerImage.get_rect()

# 加载 子弹图片 并获取图片边距
bulletImage = pygame.image.load('resources\\SnowPeaBullet.png')
bulletRect = bulletImage.get_rect()

# 加载 普通僵尸 和 特殊僵尸 的图片
zombieImage = pygame.image.load('resources\\NormalZombie.png')
newKindZombieImage = pygame.image.load('resources\\KindZombie.png')


# 显示开始界面

# 将背景图片对象绘制到窗口上，并全窗口覆盖
windowSurface.blit(rescaledBackground, (0, 0))

# new: 将豌豆射手绘制到窗口上，位置为： 窗口中间 和 下方 -70像素
windowSurface.blit(playerImage, (WINDOWWIDTH / 3.5, WINDOWHEIGHT - 70))

# new: 将妖艳贱货绘制到窗口上，位置为： x轴 1024/1.5 像素， y轴 -90像素
windowSurface.blit(zombieImage, (WINDOWWIDTH / 1.5, WINDOWHEIGHT - 90))

# new: 调用drawText()方法绘制文字到屏幕上
drawText('豌豆射手大战妖艳贱货', font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 4))
drawText('按下回车开始游戏（按Esc键退出游戏）', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)

# 刷新屏幕
pygame.display.update()

# 获取玩家按键
waitForPlayerToPressKey()


# 游戏主进程开始： 
while True:

    # 创建 普通僵尸、特殊僵尸、子弹 的集合
    zombies = []
    newKindZombies = []
    bullets = []

    # 初始化 允许通过的僵尸数量为 0
    zombiesGottenPast = 0

    # 初始化 得分为 0
    score = 0

    # 初始化 命中特殊僵尸次数为 0
    HitKindCount = 0

    # 初始化 豌豆射手 的位置为： 屏幕中间 和 左边50像素位置
    playerRect.topleft = (50, WINDOWHEIGHT /2)

    # 初始化 左右移动 和 上下移动 为 False
    moveLeft = moveRight = False
    moveUp = moveDown = False

    # 初始化 射击状态 为 False
    shoot = False

    # 初始化 新增的 普通僵尸和特殊僵尸 计数器为 0
    zombieAddCounter = 0
    newKindZombieAddCounter = 0

    # 初始化 子弹 计数器为 40
    bulletAddCounter = 40

    # 初始化音乐播放状态，-1表示循环播放，0.0表示起始位置
    pygame.mixer.music.play(-1, 0.0)


    # 游戏循环运行： 开始玩游戏了！但是要先做好各种准备工作
    while True: 

        # 循环获取事件，根据按键进行相应的行为
        for event in pygame.event.get():

            # 关闭窗口
            if event.type == QUIT:
                gameOver()

            # 键位按下状态时，上/下 和 射击 开始
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False           #ord() 将字符转换成ASCII码
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == K_SPACE:
                    shoot = True

            # 键位弹起状态时，上/下 和 射击 停止
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        gameOver()

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                
                if event.key == K_SPACE:
                    shoot = False


        # 增加僵尸和子弹
        # 每次循环增加一个普通僵尸，计数器自增 1
        zombieAddCounter += 1

        # 如果普通僵尸计数器 等于 特殊僵尸，则重置普通僵尸计数器
        if zombieAddCounter == ADDNEWKINDZOMBIE:
            zombieAddCounter = 0
            zombieSize = ZOMBIESIZE

            # 条件满足，则创建一个字典，包含普通僵尸对象和位置，拥有随机的出现位置，和图片对象大小     
            newZombie = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-zombieSize-10), zombieSize, zombieSize),
                        'surface':pygame.transform.scale(zombieImage, (zombieSize, zombieSize)),
                        }
            # 将创建的普通僵尸放到 普通僵尸列表里
            zombies.append(newZombie)

        # 每次循环增加一个特殊僵尸，计数器自增 1
        newKindZombieAddCounter += 1

        # 如果特殊僵尸计数器 等于 普通僵尸，则重置特殊僵尸计数器
        if newKindZombieAddCounter == ADDNEWZOMBIERATE:
            newKindZombieAddCounter = 0
            newKindZombiesize = ZOMBIESIZE + 40

            # 条件满足，则创建一个字典，包含特殊僵尸对象和位置，拥有随机的出现位置，和图片对象大小       
            newKind = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindZombiesize-10), newKindZombiesize, newKindZombiesize),
                        'surface':pygame.transform.scale(newKindZombieImage, (newKindZombiesize, newKindZombiesize)),
                        }

            # 将创建的特殊僵尸放到 特殊僵尸列表里
            newKindZombies.append(newKind)

        # 每次循环增加一个子弹，计数器自增 1
        bulletAddCounter += 1

        # 如果子弹计数器大于等于预定的值，且射击状态为True，则重置计数器
        if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
            bulletAddCounter = 0

            # 条件满足，则创建一个字典，包含子弹对象和位置，位置在豌豆射手的中间 靠右10个像素和靠右25像素之间
            newBullet = {'rect':pygame.Rect(playerRect.centerx+10, playerRect.centery-25, bulletRect.width, bulletRect.height),
						 'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
						}
            # 将创建的子弹放到 子弹列表里
            bullets.append(newBullet)


        # 设置僵尸和豌豆射手的移动规则（屏幕坐标系，左上角为原点）

        # 如果按键向上，且豌豆射手距离顶部位置 超过30像素，则每次循环移动该对象：x轴不变，y轴减15
        if moveUp and playerRect.top > 30:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)

        # 如果按键向下，且豌豆射手距离底部位置 少于窗口高度-10像素，则每次循环移动该对象：x轴不变，y轴加15
        if moveDown and playerRect.bottom < WINDOWHEIGHT - 10:
            playerRect.move_ip(0, PLAYERMOVERATE)



        # 迭代普通僵尸列表，每个僵尸每次循环进行移动：x轴减2，y轴不变
        for z in zombies:
            z['rect'].move_ip(-1*NORMALZOMBIESPEED, 0)

        # 迭代特殊僵尸列表，每个僵尸每次循环进行移动：x轴减2，y轴不变
        for c in newKindZombies:
            c['rect'].move_ip(-1*NEWKINDZOMBIESPEED, 0)

        # 迭代子弹列表，每个子弹每次循环进行移动：x轴加10，y轴不变
        for b in bullets:
            b['rect'].move_ip(1 * BULLETSPEED, 0)

        # 迭代普通僵尸列表，每当这个僵尸移动到最左边，则删除该僵尸
        for z in zombies:
            if z['rect'].left < 0:
                zombies.remove(z)
                #同时允许通过僵尸的计数器自增1
                zombiesGottenPast += 1

        # 迭代特殊僵尸列表，每当这个僵尸移动到最左边，则删除该僵尸
        for c in newKindZombies:
            if c['rect'].left < 0:
                newKindZombies.remove(c)
                #同时允许通过僵尸的计数器自增1
                zombiesGottenPast += 1
        
        # 迭代子弹列表，每当这个子弹移动到最右边，则删除该子弹
        for b in bullets:
            if b['rect'].right > WINDOWWIDTH:
                bullets.remove(b)

        # 子弹命中普通僵尸的碰撞检测，如果返回True表示命中，得分+1，僵尸删除
        for z in zombies:
            if bulletHasHitZombie(bullets, zombies):
                score += 1
                zombies.remove(z)
    
        # 子弹命中特殊僵尸的碰撞检测，如果返回True表示命中，命中3次，得分+3，僵尸删除
        for c in newKindZombies:
            if bulletHasHitKind(bullets, newKindZombies):
                HitKindCount += 1
                if HitKindCount > 2:
                    HitKindCount = 0
                    score += 3
                    newKindZombies.remove(c)       

        # 准备工作完成！开始绘制图片吧！
        # 将背景图片 绘制到窗口上（全窗口）
        windowSurface.blit(rescaledBackground, (0, 0))

        # 将豌豆射手的图片，绘制到预定的位置上
        windowSurface.blit(playerImage, playerRect)

        # 迭代生成僵尸，将每个僵尸的图片，绘制到预定的位置上
        for z in zombies:
            windowSurface.blit(z['surface'], z['rect'])

        for c in newKindZombies:
            windowSurface.blit(c['surface'], c['rect'])

        # 迭代生成子弹，将每个子弹的图片，绘制到预定的位置上
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        # 将 允许通过的僵尸数量 和 得分 文字绘制到预定的窗口上
        drawText('已经通过的僵尸: %s' % (zombiesGottenPast), font, windowSurface, 10, 20)
        drawText('得分: %s' % (score), font, windowSurface, 10, 50)

        # 每次循环，刷新下画面
        pygame.display.update()
            
        # 豌豆射手 和 普通僵尸、特殊僵尸的碰撞检测，以及通过的僵尸大于等于预定的值，则退出循环
        if playerHasHitZombie(playerRect, zombies):
            break
        if playerHasHitZombie(playerRect, newKindZombies):
           break
        if zombiesGottenPast >= MAXGOTTENPASS:
            break

        # 画面fps 为预设的60
        mainClock.tick(FPS)


    # 哎呀，游戏结束了。。。
    # 停止当前的背景音乐
    pygame.mixer.music.stop()
    # 播放游戏结束的音乐（超级玛丽）
    gameoverSound.play()
    # 暂停一秒
    time.sleep(1)

    # 如果是因为 僵尸通过数量过多造成游戏结束：
    if zombiesGottenPast >= MAXGOTTENPASS:
        # 重新绘制背景图片，以及由此造成游戏结束的相关文字
        windowSurface.blit(rescaledGameover, (0, 0))
        drawText('你的家被妖艳贱货们拆掉了~', font, windowSurface, (WINDOWWIDTH / 4)- 80, (WINDOWHEIGHT / 3) + 100)
        drawText('按下Enter键重新开始（按下Esc键退出游戏）', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        # 刷新一下屏幕
        pygame.display.update()
        # 等待用户输入，根据用户输入执行
        waitForPlayerToPressKey()

    # 如果是因为 僵尸通过数量过多造成游戏结束：
    if playerHasHitZombie(playerRect, zombies):
        # 重新绘制背景图片，以及由此造成游戏结束的相关文字
        windowSurface.blit(rescaledGameover, (0, 0))
        drawText('你的脑子被妖艳贱货吃掉了~', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 100)
        drawText('按下Enter键重新开始（按下Esc键退出游戏）', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        # 刷新一下屏幕
        pygame.display.update()
        # 等待用户输入，根据用户输入执行
        waitForPlayerToPressKey()

    # 不管用户做出何种输入，停止当前音乐
    gameoverSound.stop()
