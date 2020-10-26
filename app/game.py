try:
    import pygame
    import random as r
    import time as t
    import os
    import pyautogui as pg
    import PIL
except:
    os.system('install.py')

score = 0
healpoints = 3
display_w = 880
display_h = 600
game_exit = False
time1 = t.time() - 3
time2 = t.time() - 1
time3 = t.time()
# глобальные переменные будут здесь
class background:

    image1 = pygame.image.load('images\\background.png')
    image2 = pygame.image.load('images\\background.png')
    image3 = pygame.image.load('images\\background_night.png')
    image4 = pygame.image.load('images\\background_night.png')
    y = -2352+display_h
    speed = 5
    max_speed = 10
    min_speed = 0

    def draw(self,display,handbrake,boost):
        global time3
        if handbrake and self.speed > self.min_speed:
            self.speed -= 1

        if boost and self.speed < self.max_speed:
            self.speed += 1

        if boost and self.speed == self.max_speed:
            boost = False

        if handbrake and self.speed == self.min_speed:
            handbrake = False

        self.y += self.speed
        if time3 + 180 > t.time():
            display.blit(self.image1,(0,self.y))
            display.blit(self.image2,(0,self.y-2352))
        elif time3 + 180 < t.time() < time3 + 360:
            display.blit(self.image3,(0,self.y))
            display.blit(self.image4,(0,self.y-2352))
        else:
            time3 = t.time()

        if self.y >= display_h:
            self.y = -2352+display_h
            display.blit(self.image1,(0,self.y))

class car:
    image = pygame.image.load('images\\car_skins\\Porsche.png')
    image_name = 'main'
    x = 335
    y = 350
    height = PIL.Image.open('images\\car_skins\\Porsche.png').size[1]
    line = 1

    def draw(self,display):
        global score,objects,time1,time2,healpoints,game_exit,hearts
        for i in bonuses:
            if self.y < i.y < self.y + self.height and i.line == self.line:
                if i.type == 'heart'and healpoints < 3:
                    healpoints += 1
                    hearts[healpoints-1] = heart(healpoints-1,True)
                if i.type == 'money':
                    score += 100
                bonuses.remove(i)

        for i in objects:
            if (i.y < self.y+self.height < i.y+i.height or i.y < self.y < i.y+i.height) and i.line == self.line and t.time() - 3 >= time1:
                score -= 100
                time1 = t.time()
                healpoints -= 1
                for i in range(3-healpoints):
                    hearts[2-i] = heart(2-i,False)
                if healpoints == 0:
                    txt = font1.render('GAME OVER',False,(255,255,255))
                    display.blit(txt,(display_w//2 - 100,display_h//2-50))
                    scoreboard = {}
                    with open('log.txt','w') as f:
                        f.write('{}\n{}'.format(name,str(max(score,record))))
                        f.close()
                    game_exit = True



        if t.time() - 3 < time1:
            if self.image_name == 'main' and time2 + 0.25 < t.time():
                self.image_name = 'zero'
                display.blit(self.image,(self.x + 80 * self.line,self.y))
                time2 = t.time()
            if self.image_name == 'zero' and time2 + 0.25 > t.time():
                self.image_name = 'main'
                time2 = t.time()

        else:
            display.blit(self.image,(self.x + 80 * self.line,self.y))

class npc:
    global objects

    def __init__(self,line):
        path = os.listdir(path = 'images\\npc_cars')
        rnum = r.randint(0,len(path)-1)
        self.image = pygame.image.load('images\\npc_cars\\{}'.format(path[rnum]))
        self.height = PIL.Image.open('images\\npc_cars\\{}'.format(path[rnum])).size[1]
        self.line = line-1
        if background.speed > 6:
            self.y = -100 - (95 * (r.randint(0,1)))
            self.speed = (r.randint(-8+self.line,-7+self.line))*-1
        else:
            self.y = display_h + 100 + (95 * (r.randint(0,1)))
            self.speed = (r.randint(-8+self.line,-7+self.line))*-1

        self.x = 335


    def draw(self,display):
        self.y += background.speed - self.speed
        display.blit(self.image,(self.x + self.line * 80,self.y))
        if self.y > display_h + 250 or self.y < -250:
            objects.remove(self)

class bonus:
    def __init__(self,num):
        path = os.listdir(path = 'images\\bonuses')
        rnum = r.randint(0,len(path)-1)
        self.type = path[rnum].split('.')[0]
        self.image = pygame.image.load('images\\bonuses\\{}'.format(path[rnum]))
        self.height = PIL.Image.open('images\\bonuses\\{}'.format(path[rnum])).size[1]
        s = [0,1,2]
        s.pop(car.line)
        self.line = r.choice(s)
        self.x = 335 + 80*self.line
        self.y = r.randint(-400-1500*num,-250-1500*num)

    def draw(self,display):
        global bonuses
        self.y += background.speed
        if self.y > display_h:
            bonuses.remove(self)
        display.blit(self.image,(self.x,self.y))

class heart:
    def __init__(self,position,live):
        if live:
            self.image1 = pygame.image.load('images\\heart.png')
        else:
            self.image1 = pygame.image.load('images\\heart1.png')
        self.x = 50 + 55*position
        self.y = display_h - 100

    def draw(self,display):
        display.blit(self.image1,(self.x,self.y))



# здесь можно смело поменять название

pygame.init()
pygame.font.init()
font1 = pygame.font.Font("Pixel.ttf",45)
font2 = pygame.font.Font("Pixel.ttf",120)


game_display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Need For Speed Light')
clock = pygame.time.Clock()

def process_keyboard(event):
    global line,handbrake,boost,game_exit
    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and car.line > 0 and background.speed != background.min_speed:
            car.line -= 1

        if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and car.line < 2 and background.speed != background.min_speed:
            car.line +=1

        if (event.key == pygame.K_w or event.key == pygame.K_UP) and background.speed < background.max_speed:
            background.speed +=1

        if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and background.speed > background.min_speed:
            background.speed -= 1

        if event.key == pygame.K_SPACE and background.speed > background.min_speed:
            handbrake = True

        if event.key == pygame.K_LSHIFT and background.speed < background.max_speed:
            boost = True

        if event.key == pygame.K_ESCAPE:
            answ = pg.confirm('Exit to main menu?', title = 'P A U S E', buttons = ['Continue', 'Exit'])
            if answ == 'Exit':
                game_exit = True



# самая важная функция в ней все и происходит
def game_loop(update_time):
    global game_exit,handbrake,boost,npc1,npc2,npc3,objects,game_display,score,hearts,bonuses,bonus1,bonus2,record

    while not game_exit:
        for event in pygame.event.get():
            #print(event)

            process_keyboard(event)
            if event.type == pygame.QUIT:
                game_exit = True
                quit()
        # на этом уровне должна происходить отрисовка

        # нарисовать машинку
        # нарисовать фон

        if background.speed == background.min_speed:
            handbrake = False

        if background.speed == background.max_speed:
            boost = False

        background.draw(game_display,handbrake,boost)

        if bonus1 not in bonuses:
            bonus1 = bonus(1)
            bonuses.append(bonus1)

        if bonus2 not in bonuses:
            bonus2 = bonus(2)
            bonuses.append(bonus2)

        for i in bonuses:
            i.draw(game_display)

        if npc1 not in objects:
            npc1 = npc(1)
            objects.append(npc1)

        if npc2 not in objects:
            npc2 = npc(2)
            objects.append(npc2)

        if npc3 not in objects:
            npc3 = npc(3)
            objects.append(npc3)

        for enemy in objects:
            enemy.draw(game_display)


        car.draw(game_display)

        for heart in hearts:
            heart.draw(game_display)

        txt = font1.render('Score: {}'.format(score),False,(255,255,255))
        game_display.blit(txt,(25,25))
        txt = font1.render('Your record:{}'.format(record),False,(255,255,255))
        game_display.blit(txt,(display_w - 400,15))
        speedometer = font2.render('{}'.format(background.speed * 15),False,(20,150,150))
        game_display.blit(speedometer,(display_w-175,display_h-150))


        pygame.display.update()
        clock.tick(update_time)


background = background()
car = car()
npc1 = npc(1)
npc2 = npc(2)
npc3 = npc(3)
objects = []
bonuses = []
bonus1 = bonus(1)
bonus2 = bonus(2)
hearts = []
record = 0
with open('log.txt','r') as f:
    s = f.readlines()
    name = s[0][:-1]
    record = int(s[1])

for i in range(healpoints):
    heart1 = heart(i,True)
    hearts.append(heart1)

handbrake = False
boost = False

game_loop(60)
pygame.quit()
quit()
