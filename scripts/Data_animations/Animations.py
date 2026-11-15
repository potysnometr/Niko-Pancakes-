import pygame,os

pygame.init()

screen=pygame.display.set_mode((1, 1))
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("game")

class Animation_Data():
    def __init__(self,image_path,size_w,size_h):
        self.image_path=image_path
        self.animations_list=[]
        self.status_animation={}
        self.status_animation_base=""
        self.size_w=size_w
        self.size_h=size_h
        for index,image in enumerate(self.image_path):
            self.animations_list.append([])
            animations_load(image,self.animations_list[index],self.size_w,self.size_h)
    def Set_status(self,animation_status,animation_base_status):
        self.status_animation=animation_status
        self.status_animation_base=animation_base_status

def load_and_scale_image(image,size_w,size_h):
    sprite=pygame.image.load(image).convert_alpha()
    return pygame.transform.scale(sprite,(size_w,size_h)).convert_alpha()

def animations_load(image_path, target_list, size_w, size_h):
    contents = os.listdir(image_path)
    for filename in contents:
        full_path = os.path.join(image_path, filename)
        target_list.append(load_and_scale_image(full_path, size_w, size_h))

Niko_animation=Animation_Data(["textures/Niko/idle","textures/Niko/idle_other","textures/Niko/shoked","textures/Niko/eat"],130,130)
Niko_animation.Set_status({"Idle":Niko_animation.animations_list[0],"Idle_other":Niko_animation.animations_list[1]
                           ,"shoked":Niko_animation.animations_list[2],"eat":Niko_animation.animations_list[3]},"Idle")