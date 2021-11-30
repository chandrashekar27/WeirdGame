#WEIRD GAME
#import modules
import pygame
import random
from os import path
img_dir=path.join(path.dirname(__file__),'img')
#basic settings
width = 1000
height = 600
fps = 60
# define colors
white = (255, 255, 255)
black = (0, 0, 0)
blue=(0,0,250)
#other basic variables(things to define only the first time)
r=True#player facing right or not
three=True#for third zombie
still=False#for powerups
time_passed=0#for duration of powerups
game_over=False
#define classes
class Player(pygame.sprite.Sprite):#our main player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.player_imgr0=pygame.image.load(path.join(img_dir,'game_right0.png')).convert()
        self.player_imgl0=pygame.image.load(path.join(img_dir,'game_left0.png')).convert()
        self.player_imgr1=pygame.image.load(path.join(img_dir,'game_right1.png')).convert()
        self.player_imgl1=pygame.image.load(path.join(img_dir,'game_left1.png')).convert()
        self.player_imgr2=pygame.image.load(path.join(img_dir,'game_right2.png')).convert()
        self.player_imgl2=pygame.image.load(path.join(img_dir,'game_left2.png')).convert()
        self.player_imgr3=pygame.image.load(path.join(img_dir,'game_right3.png')).convert()
        self.player_imgl3=pygame.image.load(path.join(img_dir,'game_left3.png')).convert()
        self.image=pygame.transform.scale(self.player_imgr0,(75,140))
        self.rect=self.image.get_rect()
        self.rect.center=(width/2,(height*.8)+83.5-69 )
        self.speed_x=0
        self.y_speed=0
        self.gravity=2
        self.a=0
    def update(self) :
        global z
        global b
        global p
        global r
        self.speed_x=0
        #control player moving left and right
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            if self.a%(fps/3)<fps/9:
                self.image=pygame.transform.scale(self.player_imgr1,(75,140))
            elif self.a%fps/3<(fps/9)*2:
                self.image=pygame.transform.scale(self.player_imgr2,(75,140))
            else:
                self.image=pygame.transform.scale(self.player_imgr3,(75,140))
            self.speed_x+=7
            r=True
        if keystate[pygame.K_LEFT]:
            if self.a%(fps/3)<fps/9:
                self.image=pygame.transform.scale(self.player_imgl1,(75,140))
            elif self.a%fps/3<(fps/9)*2:
                self.image=pygame.transform.scale(self.player_imgl2,(75,140))
            else:
                self.image=pygame.transform.scale(self.player_imgl3,(75,140))
            self.speed_x-=7
            r=False
        touch=pygame.sprite.spritecollide(player,p,False)
        if self.speed_x==0 or not touch :
            if r:
                self.image=pygame.transform.scale(self.player_imgr0,(75,140))
            else:
                self.image=pygame.transform.scale(self.player_imgl0,(75,140))
        #keep the player in the screen
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>width:
            self.rect.right=width
        self.rect.x+=self.speed_x
        #make the player fall if not on platform
        fall=True
        land=pygame.sprite.spritecollide(player,p,False)
        if land:
            fall=False
            self.y_speed=30#45
        if fall:
            self.y_speed-=self.gravity
            self.rect.y-=self.y_speed
        #make sure player doesnt go below the platform
        if self.rect.centery+69>(height*.8)+83.5:
            self.rect.centery=(height*.8)+83.5-69
        self.image.set_colorkey(black)
        self.a+=1
    #for player to shoot bullet
    def shoot(self):
        bul=True
        if r:
            bullet=Bulletr(self.rect.x+40,(self.rect.y)+50)
        else:
            bullet=Bulletl(self.rect.x-15,(self.rect.y)+50)
        all_sprites.add(bullet)
        b.add(bullet)
        shoot_sound.play()
    #for player to move up(jump)
    def jump(self):
        y_speed1=30#40
        self.rect.y-=y_speed1
class Platform(pygame.sprite.Sprite):#all platforms
    def __init__(self,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((w,h))
        self.image.fill(black)
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.x=-500
        self.rect.y=(height*.8)+83.5
class Bulletr(pygame.sprite.Sprite):#right moving bullets
    def __init__(self,a,b):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(path.join(img_dir,'bullet_right.png')).convert()
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.x=a
        self.rect.y=b
    #move bullet right
    def update(self):
        global bul_left
        self.rect.x+=15
        #delete bullet if it goes off the screen
        if self.rect.centerx>1150 :
            self.kill()
            bul_left-=1
class Bulletl(pygame.sprite.Sprite):#left moving bullets
    def __init__(self,a,b):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(path.join(img_dir,'bullet_left.png')).convert()
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.x=a
        self.rect.y=b
    #move bullet left
    def update(self):
        global bul_left
        self.rect.x-=15
        #delete bullet if it goes off the screen
        if self.rect.centerx<-150 :
            self.kill()
            bul_left-=1
class mob(pygame.sprite.Sprite):#all walking enemies(zombie)
    def __init__(self):
        global z
        global b
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(path.join(img_dir,'walk1l.png')).convert()
        self.rect=self.image.get_rect()
        a=random.randint(1001,1150)
        bi=random.randint(-210,-110)
        lst=[a,bi]
        self.rect.x=random.choice(lst)
        self.rect.y=(height*.8)+83.5-141                     
        self.speed=1#enemy speed
        self.count=1
        self.move=True
        self.t=-2
        self.a=0
    def update(self):
        global score
        global powup
        global time_passed
        for i in z:
            if level=='medium':
                i.speed=2
            if level=='hard':
                i.speed=1.2
            #make enemies look like they are walking
            i.a=i.count%30
            if i.move:
                #check if slow powerup is collected    
                collect= pygame.sprite.spritecollide(player,powup,True)
                time_now=pygame.time.get_ticks()
                if time_now-time_passed<3000:
                    i.speed=1
                elif collect:
                    for each in collect:    
                        if each.type=='slow':
                            time_passed=pygame.time.get_ticks()
                else:            
                    if i.rect.x-player.rect.x>0:
                        if i.a<15:
                            i.image=pygame.image.load(path.join(img_dir,'walk1l.png')).convert()
                        else:
                            i.image=pygame.image.load(path.join(img_dir,'walk2l.png')).convert()
                        i.rect.x-=i.speed
                    else:
                        if i.a<15:
                            i.image=pygame.image.load(path.join(img_dir,'walk1r.png')).convert()
                        else:
                            i.image=pygame.image.load(path.join(img_dir,'walk2r.png')).convert()
                        i.rect.x+=i.speed
                #check if bullet hit mob
                hit=pygame.sprite.spritecollide(i,b,(False,True))
                if hit and i.move:
                    score+=1
                    i.t=0
                    i.rect.y+=69
                    i.move=False
                    if i.rect.x-player.rect.x>0:
                        i.image=pygame.image.load(path.join(img_dir,'deadl.png')).convert()
                    else:
                        i.image=pygame.image.load(path.join(img_dir,'deadr.png')).convert()
                    die_sound.play()
            if i.t>-1:
                i.t+=1
                if i.t==30:
                    i.image=pygame.image.load(path.join(img_dir,'walk1l.png')).convert()
                    i.rect=i.image.get_rect()
                    #remove dead zombie and move back to start point
                    a=random.randint(1001,1150)
                    bi=random.randint(-210,-110)
                    lst=[a,bi]
                    i.rect.x=random.choice(lst)
                    i.rect.y=(height*.8)+83.5-141
                    i.move=True
                    i.t=-2
            i.count+=1
            i.image.set_colorkey(black)
class rocks(pygame.sprite.Sprite):#falling rocks
    global rok
    global b
    global p
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.a=pygame.image.load(path.join(img_dir,'rock1.png')).convert()
        self.b=pygame.image.load(path.join(img_dir,'rock2.png')).convert()
        self.c=pygame.image.load(path.join(img_dir,'rock3.png')).convert()
        self.lst=(self.a,self.b,self.c)
        self.image=random.choice(self.lst)
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(100,900)
        self.rect.y=-250
        self.speedx=random.randrange(-2,3)
        self.speedy=random.randrange(2,7)
    def update(self):
        global bul_left
        global powerup
        #moving rocks down and to the side
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        #move rocks up if it hit platform
        if self.rect.bottom>=(height*.8)+83.5:
            self.lst=(self.a,self.b,self.c)
            self.image=random.choice(self.lst)
            self.rect=self.image.get_rect()
            self.rect.x=random.randrange(100,900)
            self.rect.y=random.randrange(-150,-85)
            self.speedx=random.randrange(-2,3)
            self.speedy=random.randrange(3,7)
            #give chance for powerup every time rock hits ground
            if random.random()>0.9:
                powerup=Pow()
                all_sprites.add(powerup)
                powup.add(powerup)
        crash11=pygame.sprite.groupcollide(b,rok,True,False)
        if crash11:
            bul_left-=1
        self.image.set_colorkey(black)    
class Pow(pygame.sprite.Sprite):#all powerups
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(['bullet','slow'])
        self.image=powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(50,900)
        self.rect.y=-100
    def update(self):
        global powup
        #move it down
        self.rect.y+=3.5
        #delete if it hits the platform
        pygame.sprite.spritecollide(base_platform,powup,True)
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Wierd Game')
#set icon for game
game_icon=pygame.image.load(path.join(img_dir,'game_icon.png')).convert()
pygame.display.set_icon(game_icon)
#make dictionary to hold powerups
global powerup_images
powerup_images={}
powerup_images['bullet']=pygame.image.load(path.join(img_dir,'bullet_powerup.png')).convert()
powerup_images['slow']=pygame.image.load(path.join(img_dir,'slow_powerup.png')).convert()
#creating and adding to groups
all_sprites = pygame.sprite.Group()
b=pygame.sprite.Group()
rok=pygame.sprite.Group()
p=pygame.sprite.Group()
z=pygame.sprite.Group()
z_dead=pygame.sprite.Group()
powup=pygame.sprite.Group()
#defining other functions
font_name=pygame.font.match_font('arial')
def text(surf,text,size,x,y,color):  #function for displaying text
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.y=y
    surf.blit(text_surface,text_rect)
def bullet(num):#function for showing bullets left
    image1=pygame.image.load(path.join(img_dir,'bullet_right.png')).convert()
    image1_rect=image1.get_rect()
    image1.set_colorkey(black)
    image1_rect.y=3
    if num>0:
        image1_rect.x=3
        screen.blit(image1,image1_rect)
    if num>1:
        image1_rect.x=70
        screen.blit(image1,image1_rect)
    if num>2:
        image1_rect.x=137
        screen.blit(image1,image1_rect)
def new_game():  #function for starting a new game
    global score
    score=0#starting score
    global game_over
    game_over=False#died or not
    global bul_left
    bul_left=3#no of bullets left
    #creating and adding to groups
    global player
    player=Player()
    all_sprites.add(player)
    global base_platform
    base_platform=Platform(15000,8)
    all_sprites.add(base_platform)
    p.add(base_platform)
    #generate rocks
    global roc
    roc=[]
    for i in range(5):
        rock=rocks()
        all_sprites.add(rock)
        rok.add(rock)
        roc.append(rock)
    #generate zombies
    global zombie
    zombie=mob()
    all_sprites.add(zombie)
    z.add(zombie)
    global zombie1
    zombie1=mob()
    all_sprites.add(zombie1)
    z.add(zombie1)        
#load game sounds (and background)
shoot_sound=pygame.mixer.Sound('shoot.wav')
hit_sound=pygame.mixer.Sound('hit.wav')
die_sound=pygame.mixer.Sound('die.wav')
bg_sound=pygame.mixer.music.load('Iwan Gabovitch - Dark Ambience Loop.ogg')
pygame.mixer.music.play(loops=-1)
bg=pygame.image.load(path.join(img_dir,'bg1.png')).convert()
bg=pygame.transform.scale(bg,(width,height))
bg_rect=bg.get_rect()
#getting highscore
with open('highscore.txt','r+') as hs:
    try:
        highscore=int(hs.read())
    except:
        highscore=0

# Game loop
running = True
start=True
new_game()
while running:
    if start:
        screen.fill(white)
        screen.blit(bg,(0,0))
        text(screen,'WEIRD GAME',101,width/2,100,black)
        text(screen,'Arrow Keys To Move',50,width/2,270,white)
        text(screen,'Space To Shoot',50,width/2,330,white)
        text(screen,'Press Space To Start',60,width/2,450,blue)
        text(screen,"HighScore: %s"%(highscore),25,width/2,10,white)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                start=False
    else:
        global powerup
        if game_over==False:
            #setting difficulty and change variables
            if score<11:
                level='easy'
                me=True
            elif score<31:
                level="medium"
                ha=True
            else:
                level='hard'
            if level=='medium' and me:
                me=False
                for i in range(2):
                    rock=rocks()
                    all_sprites.add(rock)
                    rok.add(rock)
                    roc.append(rock)
            if level=='hard' and ha:
                ha=False
                for i in range(2):
                    rock=rocks()
                    all_sprites.add(rock)
                    rok.add(rock)
                    roc.append(rock)
            if level=='hard' and three:
                three=False
                zombie2=mob()
                all_sprites.add(zombie2)
                z.add(zombie2)
            land=pygame.sprite.spritecollide(player,p,False)
            # keep loop running at the right speed
            clock.tick(fps)
            print (str(clock.get_fps()))
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        player.shoot()
                    if event.key==pygame.K_UP and land:
                        player.jump()
            #end game if player hits mob or rock or bullets over
            end=pygame.sprite.collide_rect_ratio(0.7)(player,zombie)
            end_other=pygame.sprite.collide_rect_ratio(0.7)(player,zombie1)
            for i in roc:
                end1=pygame.sprite.collide_rect_ratio(0.8)(player,i)
                if end1:
                    reason='You Died'
                    die_sound.play()
                    game_over=True
            global spike        
            if end and zombie.move or end_other and zombie1.move:
                reason='You Died'
                die_sound.play()
                game_over=True
            #check if player collects powerup
            collect1= pygame.sprite.spritecollide(player,powup,True)
            for each in collect1: 
                if each.type=='bullet'and bul_left<3:
                    bul_left+=1    
            if bul_left==0:
                reason='You ran out of bullets'
                die_sound.play()
                game_over=True
            # Update
            all_sprites.update()
            # Draw / render
            screen.fill(white)
            screen.blit(bg,(0,0))
            all_sprites.draw(screen)
            score1='Score: %s'%(score)
            bullet(bul_left)
            text(screen,str(score1),30,(width/2),10,white)
        else:
            screen.blit(bg,(0,0))
            text(screen,'GAME  OVER',100,(width/2),70,black)
            text(screen,reason,50,(width/2),210,white)
            text(screen,str(score1),50,(width/2),300,white)
            text(screen,'Press Space To Play Again',55,(width/2),505,blue)
            #if a new highscore is made
            if score>highscore:
                ci=True
                text(screen,'New HighScore!',50,width/2,370,white)
                with open('highscore.txt','r+') as hs:
                    hs.write(str(score))
            else:
                text(screen,'HighScore: %s'%(highscore),55,width/2,370,white)
                ci=False
            for i in all_sprites:
                i.kill()
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                    if ci:
                        highscore=score
                        ci=False
                    new_game()    
    # after drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
quit()
#THE END
