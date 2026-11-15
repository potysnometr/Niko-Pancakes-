import pygame,math
from scripts.pygame_additional_classes_and_functions import rotate_offset

class Entity():
    def __init__(self,x,y,sprite,color,animations,animation_speed=1):
        self.pos=[x,y]
        self.Sprite=sprite
        self.rect=self.Sprite.get_rect(center=self.pos)
        self.color=color
        self.animations=animations
        if animations:
            self.animation_timer=0
            self.animation_count=0
            self.animation_loop=True
            self.animations_stat=self.animations.status_animation_base
            self.animation_status_old=self.animations.status_animation_base
            self.animation_speed=animation_speed
        if not self.color==None:
            self.Sprite.fill(self.color)
    def __call__(self,screen):
        self.update_rect()
        if self.animations:
            self.basic_animation_system()
        self.draw(screen)
    def update_rect(self):
        self.rect=self.Sprite.get_rect(center=self.pos)
    def basic_animation_system(self):
        self.animation_timer+=self.animation_speed
        if self.animation_timer>=2.2:
            self.animation_count+=1
            self.animation_timer=0
        if self.animation_count>=len(self.animations.status_animation[self.animations_stat]):
            self.animation_count=0
            if not self.animation_loop:
                self.stat_animation=self.animations.status_animation_base
        if not self.animation_status_old==self.animations_stat:
            self.animation_count=0
            self.animation_status_old=self.animations_stat
    def draw(self,Surface):
        if self.animations:
            Surface.blit(self.animations.status_animation[self.animations_stat][self.animation_count],self.rect)
        else:#print(self.animations.status_animation[self.animations_stat][self.animation_count])
            Surface.blit(self.Sprite,self.rect)
    def draw_rect(self,Surface):
        pygame.draw.rect(Surface,"red",self.rect,3)
        
class Entity_Rotate():
    def __init__(self,x,y,sprite,color,Target_Rotate,Target_var,Rotate_Offset=pygame.Vector2(0,0),animations=None,animation_speed=1):
        self.pos=[x,y]
        self.Sprite=sprite
        self.Sprite_rotate=sprite
        self.color=color
        self.Angle=0
        self.angle_rad=0
        self.Rotate_Offset=Rotate_Offset
        self.Target_Rotate=Target_Rotate
        self.Target_Var=Target_var
        self.rect=self.Sprite_rotate.get_rect(center=self.pos)
        self.animations=animations
        if animations:
            self.animation_timer=0
            self.animation_count=0
            self.animation_loop=True
            self.animations_stat=self.animations.status_animation_base
            self.animation_status_old=self.animations.status_animation_base
            self.animation_speed=animation_speed
        if not self.color==None:
            self.sprite.fill(self.color)
    def __call__(self,screen):
        self.draw(screen)
        if self.animations:
            self.basic_animation_system()
        if self.Target_Rotate:
            self.Rotate()
    def basic_animation_system(self):
        self.animation_timer+=self.animation_speed
        if self.animation_timer>=2.2:
            self.animation_count+=1
            self.animation_timer=0
        if self.animation_count>=len(self.animations.status_animation[self.animations_stat]):
            self.animation_count=0
            if not self.animation_loop:
                self.stat_animation=self.animations.status_animation_base
        if not self.animation_status_old==self.animations_stat:
            self.animation_count=0
    def Rotate(self):
        if self.Target_Rotate:
            dx = self.Target_Rotate.pos_shape[0] - self.pos[0]
            dy = self.Target_Rotate.pos_shape[1] - self.pos[1]
            self.angle_rad = math.atan2(dy, dx)
            self.Angle = math.degrees(self.angle_rad)
            self.Sprite_rotate,self.rect=rotate_offset(self.Sprite,self.Angle,self.pos,self.Rotate_Offset)
        else:
            self.Sprite_rotate,self.rect=rotate_offset(self.Sprite,self.Angle,self.pos,self.Rotate_Offset)
    def draw(self,Surface):
        Surface.blit(self.Sprite_rotate,self.rect)
    def draw_rect(self,Surface):
        pygame.draw.rect(Surface,"red",self.rect,3)