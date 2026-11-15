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
        for pancake in Panckes_list:
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

Panckes_list=[]
for pancake in range(random.randint(1,MAX_PANCAKE)):
    Panckes_list.append(Panckes(0,0,load_and_scale_image("textures\\Pancakes\\Pancakes.png",110,70),None,None,1))
Niko=Player(5,0,150,load_and_scale_image("textures\\Niko\\idle\\Niko0.png",130,130),None,Niko_animation,0.05)
window_focus_lost=False
while run:
    if music:
        music.play(1000)
    music=False
    screen.fill("white")
    for event in pygame.event.get():
        if event.type==pygame.WINDOWFOCUSLOST:
            window_focus_lost=True
        elif event.type==pygame.WINDOWFOCUSGAINED:
            window_focus_lost=False
        if event.type==pygame.WINDOWRESIZED:
            screen_width, screen_height = screen.get_size()
        if event.type==pygame.QUIT:
            run = False

    for pancake in Panckes_list:
        #pancake.draw_rect(screen)
        pancake(screen)
        
    Niko(screen)
    #Niko.draw_rect(screen)
    Niko.update()

    pygame.display.update()
    clock.tick(FPS)