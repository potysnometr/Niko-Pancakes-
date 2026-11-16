from scripts.pygame_additional_classes_and_functions import *
from scripts.Data_animations.Animations import *
from scripts.Entity import *
import configparser
import pygame
import os
import math
import random

run=True
config = configparser.ConfigParser()
config.read('Settings.ini')

FPS=int(config["GAME"]["fps"])
MAX_PANCAKE=int(config["GAME"]["max_pancake"])
RANDOM=int(config["GAME"]["random"])
OLD_HALF_TR=int(config["GAME"]["half_transparent_niko"])
HALF_TRANSPARENT=int(config["GAME"]["half_transparent_niko"])
MUSIC_VOLUME=float(config["GAME"]["music_volume"])
MEOW_VOLUME=float(config["GAME"]["meow_volume"])

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Niko-Pancakes")
WIDTH, HEIGHT = int(config['GAME']['width']),int(config["GAME"]['height'])
ico=pygame.image.load("icon.ico").convert_alpha()
pygame.display.set_icon(ico)
screen=pygame.display.set_mode((WIDTH, HEIGHT))
screen_width, screen_height = screen.get_size()
clock=pygame.time.Clock()
font = pygame.sysfont.SysFont("Arial", 15, True)
timer=Timer_Handler(0)
scene_type={"Main-Menu":0,"Main-Game":1}
scene=scene_type["Main-Menu"]
contents_bg = os.listdir("textures/bg")
Pancakes_list=[]
bg_images=[]
random_bg=random.randint(0,len(contents_bg)-1)
for image in contents_bg:
    if HALF_TRANSPARENT:
        bg_images.append(load_and_scale_image_alpha(f"textures/bg/{image}",WIDTH,HEIGHT,50))
    else:
        bg_images.append(load_and_scale_image(f"textures/bg/{image}",WIDTH,HEIGHT))

def convert_pos(pos):
    return int(int(pos[0])),int(HEIGHT-int(pos[1]))

def just_released(key):
    keys=pygame.key.get_just_released()
    return keys[key]

def pressed(key):
    keys=pygame.key.get_pressed()
    return keys[key]

def just_pressed(key):
    keys=pygame.key.get_just_pressed()
    return keys[key]

def mouse_just_released(key=0):
    mouse_press=pygame.mouse.get_just_released()
    return mouse_press[key]

def mouse_just_pressed(key=0):
    mouse_press=pygame.mouse.get_just_pressed()
    return mouse_press[key]

def mouse_pressed(key=0):
    mouse_press=pygame.mouse.get_pressed()
    return mouse_press[key]

def pancakes_place():
    global Pancakes_list
    Niko.pos=[10,150]
    Niko.mouse_pos_click=[10,150]
    Pancakes_list=[]
    if RANDOM:
        for pancake in range(random.randint(1,MAX_PANCAKE)):
            Pancakes_list.append(Panckes(0,0,load_and_scale_image("textures\\Pancakes\\Pancakes.png",110,70),None,None,1))
    else:
        for pancake in range(MAX_PANCAKE):
            Pancakes_list.append(Panckes(0,0,load_and_scale_image("textures\\Pancakes\\Pancakes.png",110,70),None,None,1))

meow_sound=load_and_set_volume_sound("sound/meow.mp3",MEOW_VOLUME)
music=load_and_set_volume_sound("sound/On Little Cat Feet.mp3",MUSIC_VOLUME)

class Player(Entity):
    def __init__(self,speed,x, y, sprite, color, animations, animation_speed=1):
        super().__init__(x, y, sprite, color, animations, animation_speed)
        self.eat=False
        self.speed=speed
        self.count_speed=[0,0]
        self.min_speed=1
        self.mouse_pos=pygame.mouse.get_pos()
        self.mouse_pos_click=self.pos
        self.posx=self.pos[0]
        self.posy=self.pos[1]
        self.posxmed=0
        self.posymed=0
        self.Surface=[pygame.Surface((400,400)),pygame.Surface((250,250))]
        self.Hitboxes=[self.Surface[0].get_rect(center=self.pos),self.Surface[1].get_rect(center=self.pos)]
    def __call__(self, screen):
        self.update_rect()
        if self.animations:
            self.Niko_animation_system()
        self.draw(screen)
    def update(self):
        #pygame.draw.rect(screen,"red",self.Hitboxes[0],3)
        #pygame.draw.rect(screen,"blue",self.Hitboxes[1],3)
        self.mouse_pos=pygame.mouse.get_pos()
        self.Hitboxes=[self.Surface[0].get_rect(center=self.pos),self.Surface[1].get_rect(center=self.pos)]
        if mouse_just_released(0):
            self.mouse_pos_click=self.mouse_pos
            self.posx=self.pos[0]-self.mouse_pos_click[0]
            self.posy=self.pos[1]-self.mouse_pos_click[1]
            self.posxmed=abs(self.posx)/2.3
            self.posymed=abs(self.posy)/2.3
        if self.pos[0]!=self.posx:
            x=abs(self.pos[0]-self.mouse_pos_click[0])
            y=abs(self.pos[1]-self.mouse_pos_click[1])

            if self.count_speed[0]>=self.speed:
                self.count_speed[0]=self.speed

            if self.count_speed[1]>=self.speed:
                self.count_speed[1]=self.speed

            if self.count_speed[0]<=self.min_speed:
                self.count_speed[0]=self.min_speed

            if self.count_speed[1]<=self.min_speed:
                self.count_speed[1]=self.min_speed

            if x<=self.posxmed:
                self.count_speed[0]-=0.1
            else:
                self.count_speed[0]+=0.1

            if y<=self.posymed:
                self.count_speed[1]-=0.1
            else:
                self.count_speed[1]+=0.1

            if self.mouse_pos_click[0]>=self.pos[0] and x>=1:
                self.pos[0]+=self.count_speed[0]
            elif self.mouse_pos_click[0]<=self.pos[0] and x>=1:
                self.pos[0]-=self.count_speed[0]
            if self.mouse_pos_click[1]>=self.pos[1] and y>=1:
                self.pos[1]+=self.count_speed[1]
            elif self.mouse_pos_click[1]<=self.pos[1] and y>=1:
                self.pos[1]-=self.count_speed[1]
            if x<=3:
                x=0
            if y<=3:
                y=0

    def Niko_animation_system(self):
        pan_rect=[]
        for pancake in Pancakes_list:
            pan_rect.append(pancake.rect)

        if pan_rect:
            if self.Hitboxes[0].collidelistall(pan_rect) and not self.Hitboxes[1].collidelistall(pan_rect) and not self.rect.collidelistall(pan_rect) and not self.eat:
                self.animations_stat="eat"
                self.animation_count=0
            if self.Hitboxes[1].collidelistall(pan_rect) and not self.rect.collidelistall(pan_rect) and not self.eat:
                self.animations_stat="eat"
                self.animation_count=1
            if not self.Hitboxes[0].collidelistall(pan_rect) and not self.Hitboxes[1].collidelistall(pan_rect) and not self.rect.collidelistall(pan_rect) and not self.eat:
                self.animations_stat="Idle"
                self.animation_count=0
            if self.rect.collidelistall(pan_rect) and not self.eat:
                meow_sound.play()
                self.animations_stat="eat"
                self.animation_count=2
            if self.eat:
                if timer.time(100):
                    self.eat=False

class Panckes(Entity):
    def __init__(self, x, y, sprite, color, animations, animation_speed=1):
        super().__init__(x, y, sprite, color, animations, animation_speed)
        self.pos=[random.randint(0,WIDTH-10),random.randint(0,HEIGHT)]
    def __call__(self, screen):
        self.update_rect()
        self.draw(screen)
        self.update()
    def update(self):
        if self.rect.colliderect(Niko.rect) and not Niko.eat:
            self.pos=[random.randint(0,WIDTH-10),random.randint(0,HEIGHT)]
            Niko.eat=True

class Main_Menu():
    def __init__(self):
        self.scene_type={"Main":0,"Settings":1}
        self.scene=self.scene_type["Main"]

        self.Button_Play=Button(10,10,"Play",[100,50],30,True,"black","white","gray12","black",lambda arg="Main-Game":self.Change_Scene(arg))
        self.Button_Exit=Button(10,150,"Quit",[100,50],30,True,"black","white","gray12","black",lambda: self.Exit())

        self.Button_Settings=Button(10,80,"Settings",[100,50],25,True,"black","white","gray12","black",lambda arg="Settings":self.Change_Scene_Menu(arg))
        self.Button_Back_to_Main=Button(10,80,"Back",[100,50],30,True,"black","white","gray12","black",lambda arg="Main":self.Change_Scene_Menu(arg))
        self.Button_change_setting_Random_pancake=Button(10,10,"Random pancakes",[100,50],20,True,"black","white","gray12","black",self.change_settings,"Random")
        self.Button_change_setting_half_transparent_niko=Button(120,10,"half_transparent_niko",[100,50],18,True,"black","white","gray12","black",self.change_settings,"half_transparent_niko")
        self.Button_change_setting_MAX_PANCAKE_PLUS=Button(495,10,">",[100,50],50,True,"black","white","gray12","black",self.change_settings,"Max_pancake_plus")
        self.Button_change_setting_TEXT_MAX_PANCAKE=Button(350,10,f"Max_Pancakes:{MAX_PANCAKE}",[100,50],18,True,"black","white","white","white",None,None)
        self.Button_change_setting_MAX_PANCAKE_MINUS=Button(320,10,"<",[35,50],50,True,"black","white","gray12","black",self.change_settings,"Max_pancake_minus")

    def __call__(self):
        self.Update()
    def Update(self):
        if self.scene==self.scene_type["Main"]:
            self.Button_Play(screen)
            self.Button_Settings(screen)
            self.Button_Exit(screen)
        elif self.scene==self.scene_type["Settings"]:
            self.Button_Back_to_Main(screen)

            self.Button_change_setting_Random_pancake(screen)
            self.Button_change_setting_Random_pancake.change_text(f"Random\n{str(True_or_False(RANDOM,'Reverse'))}")
            
            self.Button_change_setting_half_transparent_niko(screen)
            self.Button_change_setting_half_transparent_niko.change_text(f"Half_transparent_niko\n{str(True_or_False(HALF_TRANSPARENT,'Reverse'))}")
            self.Button_change_setting_half_transparent_niko.change_size([self.Button_change_setting_half_transparent_niko.text_done.width,50])
            
            self.Button_change_setting_MAX_PANCAKE_PLUS(screen)
            self.Button_change_setting_MAX_PANCAKE_PLUS.change_size([self.Button_change_setting_MAX_PANCAKE_PLUS.text_done.width,50])
            self.Button_change_setting_MAX_PANCAKE_PLUS.x=self.Button_change_setting_TEXT_MAX_PANCAKE.text_done.get_rect()[2]+351
            self.Button_change_setting_TEXT_MAX_PANCAKE(screen)
            self.Button_change_setting_TEXT_MAX_PANCAKE.change_size([self.Button_change_setting_TEXT_MAX_PANCAKE.text_done.width,50])
            self.Button_change_setting_TEXT_MAX_PANCAKE.change_text(f"Max_Pancakes:{MAX_PANCAKE}")
            self.Button_change_setting_MAX_PANCAKE_MINUS(screen)
            self.Button_change_setting_MAX_PANCAKE_MINUS.change_size([self.Button_change_setting_MAX_PANCAKE_MINUS.text_done.width,50])

    def Change_Scene(self,arg):
        global scene
        if arg in scene_type:
            if arg=="Main-Game":
                pancakes_place()
            scene=scene_type[arg]
        else:
            print("Неправильный аргумент")
    def Change_Scene_Menu(self,arg):
        if arg in self.scene_type:
            self.scene=self.scene_type[arg]
        else:
            print("Неправильный аргумент")
    def change_settings(self,arg):
        global MAX_PANCAKE,RANDOM,HALF_TRANSPARENT
        self.config = configparser.ConfigParser()
        self.config.read('Settings.ini')
        if arg=="Max_pancake_plus":
            MAX_PANCAKE=MAX_PANCAKE+1
            self.config.set("GAME","max_pancake",str(MAX_PANCAKE))
            with open('Settings.ini', 'w') as configfile:
                self.config.write(configfile)

        elif arg=="Max_pancake_minus":
            if MAX_PANCAKE<=1:
                return
            MAX_PANCAKE=MAX_PANCAKE-1
            self.config.set("GAME","max_pancake",str(MAX_PANCAKE))
            with open('Settings.ini', 'w') as configfile:
                self.config.write(configfile)

        elif arg=="Random":
            RANDOM=True_or_False(RANDOM,"Int")
            self.config.set("GAME","random",str(RANDOM))
            with open('Settings.ini', 'w') as configfile:
                self.config.write(configfile)

        elif arg=="half_transparent_niko":
            HALF_TRANSPARENT=True_or_False(HALF_TRANSPARENT,"Int")
            self.config.set("GAME","half_transparent_niko",str(HALF_TRANSPARENT))
            with open('Settings.ini', 'w') as configfile:
                self.config.write(configfile)
                
    def Exit(self):
        global run
        run=False

def menu():
    global scene
    scene=scene_type["Main-Menu"]

Back_to_menu=Button(WIDTH-110,HEIGHT-60,"Back",[100,50],40,True,"black","gray12","gray","black",menu,None)
Niko=Player(5,10,150,load_and_scale_image("textures\\Niko\\idle\\Niko0.png",130,130),None,Niko_animation,0.05)
Main_menu=Main_Menu()
window_focus_lost=False
pancakes_place()
while run:
    if OLD_HALF_TR!=HALF_TRANSPARENT:
        bg_images=[]
        print(HALF_TRANSPARENT,OLD_HALF_TR)
        for image in contents_bg:
            if HALF_TRANSPARENT:
                print("HALF")
                bg_images.append(load_and_scale_image_alpha(f"textures/bg/{image}",WIDTH,HEIGHT,50))
            else:
                print("NORMAL")
                bg_images.append(load_and_scale_image(f"textures/bg/{image}",WIDTH,HEIGHT))
        OLD_HALF_TR=HALF_TRANSPARENT
        print(HALF_TRANSPARENT,OLD_HALF_TR)
    if music:
        music.play(1000)
    music=False
    for event in pygame.event.get():
        if event.type==pygame.WINDOWFOCUSLOST:
            window_focus_lost=True
        elif event.type==pygame.WINDOWFOCUSGAINED:
            window_focus_lost=False
        if event.type==pygame.WINDOWRESIZED:
            screen_width, screen_height = screen.get_size()
        if event.type==pygame.QUIT:
            run = False

    if scene==scene_type["Main-Game"]:
        if not HALF_TRANSPARENT:
            screen.blit(bg_images[random_bg])
        Back_to_menu(screen)
        for pancake in Pancakes_list:
            #pancake.draw_rect(screen)
            pancake(screen)

        Niko(screen)
        #Niko.draw_rect(screen)
        Niko.update()

        if HALF_TRANSPARENT:
            screen.blit(bg_images[random_bg])
    elif scene==scene_type["Main-Menu"]:
        screen.blit(bg_images[random_bg])
        #screen.fill("gray")
        Main_menu()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()