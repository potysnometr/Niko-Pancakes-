import pygame,os,threading
from moviepy import VideoFileClip
from PIL import Image
import pickle
import zlib
import io

def True_or_False(arg,type_method="Bool"):
    if type_method=="Int":
        if arg:
            return 0
        else:
            return 1
    elif type_method=="Bool":
        if arg:
            return False
        else:
            return True 
    elif type_method=="Reverse":
        if arg==1:
            return True
        elif arg==0:
            return False
        elif arg==True:
            return 1
        elif arg==False:
            return 0

def load_and_scale_image(image,size_w,size_h):
    sprite=pygame.image.load(image)
    return pygame.transform.scale(sprite,(size_w,size_h)).convert_alpha()

def load_and_scale_image_alpha(image,size_w,size_h,alpha):
    sprite=pygame.image.load(image)
    sprite=pygame.transform.scale(sprite,(size_w,size_h)).convert_alpha()
    sprite.set_alpha(alpha)
    return sprite

def load_and_set_volume_sound(sound,volume):
    sound=pygame.mixer.Sound(sound)
    sound.set_volume(volume)
    return sound

def rotate_offset(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)# Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def animations_load(image_path, target_list, size_w, size_h):
    contents = os.listdir(image_path)
    for filename in contents:
        full_path = os.path.join(image_path, filename)
        target_list.append(load_and_scale_image(full_path, size_w, size_h))

class Timer_Handler():
    def __init__(self,max_number):
        self.times=0
        self.max=max_number
        self.lock=threading.Lock()
    def time(self,max):
        self.max = max
        self.times += 1
        if self.times >= self.max:
            self.times = 0
            return True
        return False

class Input():
    def __init__(self, x, y, text, size, size_font, Smoothing_text, color_text, color, hover_color):
        """
            Args:
                x (int): Кординаты по оси x
                y (int): Кординаты по оси y
                text (str): Тект на кнопке
                size (list): Размер строки [100,100]
                size_font (int): Размер шрифта текста
                Smoothing_text (True or False): Сглаживание текста
                color_text ((0,0,0) or "color you chouse") Цвет текста
                color ((0,0,0) or "color you chouse") Цвет строки
                hover_color ((0,0,0) or "color you chouse") Цвет строки при наведении мышкой
        """
        self.x = x
        self.y = y
        self.click = False
        self.text = text
        self.Smoothing = Smoothing_text
        self.color_text = color_text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.sysfont.SysFont("Arial", size_font, True)
        self.text_done = self.font.render(self.text, self.Smoothing, self.color_text)
        self.Surface = pygame.Surface((size[0], size[1]))
        self.Surface.fill(self.color)
        self.Rect = self.Surface.get_rect(topleft=(self.x, self.y))
        self.rect_work=True
        self.timer_handller=Timer_Handler(100)
    
    def __call__(self, events=None,surface=None):
        self.update(events)
        self.draw(surface)
    
    def update(self, events=None):
        self.text_done = self.font.render(self.text, self.Smoothing, self.color_text)
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if self.Rect.collidepoint(mouse_pos):
            self.Surface.fill(self.hover_color)
            if mouse[0]:
                self.click = True
        else:
            self.Surface.fill(self.color)
            if mouse[0]:
                self.click = False

        if self.click == True:
            self.Surface.fill(self.hover_color)
            if events:
                for event in events:
                    if not self.text_done.width>self.Surface.width:
                        if event.type == pygame.TEXTINPUT:
                            self.text += event.text 

        if key[pygame.K_BACKSPACE]:
            if self.timer_handller.time(50):
                self.text = self.text[:-1]

    def draw(self,surface=None):
        if self.rect_work:
            self.Rect=self.Surface.get_rect(topleft=(self.x,self.y))
        else:
            self.Rect=self.Surface.get_rect(topleft=(59000,50000))
        surface.blit(self.Surface, (self.x, self.y))
        surface.blit(self.text_done, (self.x, self.y))
    def get_text(self):
        return self.text
    def change_color(self,color):
        self.color=color
    def change__text_color(self,color):
        self.color_text=color
    def rect(self,arg):
        self.rect_work=arg

class Button():
    def __init__(self,x,y,text,size,size_font,Smoothing_text,color_text,color,hover_color,color_press,func=None,args=None):
        """
            Args:
            x (int): Кординаты по оси x
            y (int): Кординаты по оси y
            text (str): Тект на кнопке
            size (list): Размер кнопки [100,100]
            size_font (int): Размер шрифта текста
            Smoothing_text (True or False): Сглаживание текста
            color_text ((0,0,0) or "color you chouse") Цвет текста
            color ((0,0,0) or "color you chouse") Цвет кнопка
            hover_color ((0,0,0) or "color you chouse") Цвет кнопки при наведении мышкой
            color_press ((0,0,0) or "color you chouse") при нажатии
            func:указывать функцию
            args: если один аргумент то Button(...,args="Lvl1") если дохуя аргументов то Button(...,args=[List,Tuple])
        """
        self.x=x
        self.y=y
        self.func=func
        self.args=args
        self.text=str(text)
        self.Smoothing=Smoothing_text
        self.color_text=color_text
        self.color=color
        self.hover_color=hover_color
        self.press_color=color_press
        self.font = pygame.sysfont.SysFont("Arial",size_font,True)
        self.text_done=self.font.render(self.text,self.Smoothing,self.color_text)
        self.Surface=pygame.Surface((size[0],size[1]))
        self.Surface.fill(self.color)
        self.Rect=self.Surface.get_rect(topleft=(self.x,self.y))
        self.rect_work=True
    def __call__(self,surface=None):
        self.update()
        self.draw(surface)
    def update(self):
        self.text_done=self.font.render(self.text,self.Smoothing,self.color_text)
        mouse=pygame.mouse.get_just_released()
        mouse_pos=pygame.mouse.get_pos()
        
        if self.Rect.collidepoint(mouse_pos):
            self.Surface.fill(self.hover_color)
            if mouse[0]:
                self.Surface.fill(self.press_color)
                if self.func!=None:
                    if not self.args==None:
                        if isinstance(self.args, (tuple, list)):
                            self.func(*self.args) 
                        else:
                            self.func(self.args)
                    else:
                        self.func()
                self.click=False
        else:
            self.Surface.fill(self.color)

    def draw(self,surface=None):
        if self.rect_work:
            self.Rect=self.Surface.get_rect(topleft=(self.x,self.y))
        else:
            self.Rect=self.Surface.get_rect(topleft=(1000,1000))
        surface.blit(self.Surface,(self.x,self.y))
        surface.blit(self.text_done,(self.x,self.y))
    def change_text(self,text_str):
        self.text=str(text_str)
    def change_color(self,color):
        self.color=color
    def change_text_color(self,color):
        self.color_text=color
    def change_size(self,size):
        self.Surface=pygame.Surface((size[0],size[1]))
    def rect(self,arg):
        self.rect_work=arg

class Video():
    def __init__(self, videopath, name_video, fpsvideo, width, height, Surface, animation_speed, loop):
        self.videopath = videopath
        self.name_video = name_video
        self.fps = fpsvideo
        self.width = width
        self.height = height
        self.Surface = Surface
        self.animation_speed = animation_speed
        self.loop = loop
        self.count = 0
        self.timer = 0
        
        self.frames = [] 
        self.loaded = False
        self.loading = False
        self.total_frames = 0

        self.load_text=f"Загружено {len(self.frames)}/{self.total_frames} кадров"
        self.cache_path = f"{self.videopath}/cache_{self.name_video}_{fpsvideo}_{width}_{height}.jpg_cache"
        #self.cache_path = f"{self.videopath}/cache_{self.name_video}_{fpsvideo}_{width}_{height}.pkl"
    
    def load(self):
        if os.path.exists(self.cache_path):
            print("Загрузка из кэша")
            self.load_from_cache_threaded()
        else:
            print("Загрузка видео...")
            self.load_video_threaded()
    
    def load_video(self):
        video = VideoFileClip(self.videopath + self.name_video)
        
        frames_data = []
        total_frames = 0
        
        print("Конвертирую кадры в JPEG...")
        for frame in video.iter_frames(fps=self.fps, dtype="uint8"):
            # Конвертируем numpy array в PIL Image
            img = Image.fromarray(frame)
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            
            # Сохраняем как JPEG с сжатием
            buffer = io.BytesIO()
            # quality=75 - хороший баланс качество/размер
            img.save(buffer, format='JPEG', quality=75, optimize=True, progressive=True)
            frames_data.append(buffer.getvalue())
            
            total_frames += 1
            if total_frames % 30 == 0:
                print(f"Обработано {total_frames} кадров")
        
        #сжимаем с помощью zlib
        print("Сжимаю и сохраняю кэш...")
        with open(self.cache_path, 'wb') as f:
            compressed_data = zlib.compress(pickle.dumps(frames_data), level=9)
            f.write(compressed_data)
        
        # Загружаем в память
        self._load_frames_from_data(frames_data)
        self.loaded = True
        
        size_mb = os.path.getsize(self.cache_path) / (1024 * 1024)
        print(f"Сохранено {total_frames} кадров, размер кэша: {size_mb:.2f} МБ")
        print(f"Загружено {len(self.frames)} кадров")
    
    def load_from_cache(self):
        """Загружает из JPEG кэша ПОСТЕПЕННО"""
        print("Распаковываю JPEG кэш...")
        with open(self.cache_path, 'rb') as f:
            compressed_data = f.read()
            jpeg_data = pickle.loads(zlib.decompress(compressed_data))
        
        self.total_frames = len(jpeg_data)
        print(f"Всего кадров в кэше: {self.total_frames}")
        
        # Загружаем ПОСТЕПЕННО (по 5 кадров за раз)
        self._load_frames_gradually(jpeg_data)
    
    def _load_frames_gradually(self, jpeg_data):
        """Загружает JPEG кадры постепенно, чтобы не лагать"""
        batch_size = 5  # Загружаем по 5 кадров за раз
        
        def load_batch():
            for i in range(0, len(jpeg_data), batch_size):
                batch = jpeg_data[i:i+batch_size]
                for jpeg_bytes in batch:
                    # Декодируем JPEG в pygame поверхность
                    img = Image.open(io.BytesIO(jpeg_bytes))
                    img_str = img.tobytes()
                    mode = 'RGBA' if img.mode == 'RGBA' else 'RGB'
                    surf = pygame.image.fromstring(img_str, img.size, mode).convert_alpha()
                    self.frames.append(surf)
                    
                    self.load_text = f"Загружено {len(self.frames)}/{self.total_frames} кадров"
                    print(self.load_text)
                
                progress = len(self.frames) / self.total_frames * 100
                if int(progress) % 10 == 0:
                    print(f"Прогресс: {int(progress)}%")
                
                # Маленькая пауза, чтобы не лагать
                pygame.time.wait(10)
            
            self.loaded = True
            print(f"Загрузка завершена! {len(self.frames)} кадров")
        
        # Запускаем загрузку в отдельном потоке
        thread = threading.Thread(target=load_batch, daemon=True)
        thread.start()
    
    def _load_frames_from_data(self, jpeg_data):
        """Быстрая загрузка всех кадров из JPEG данных"""
        print("Декодирую JPEG в поверхности...")
        for jpeg_bytes in jpeg_data:
            img = Image.open(io.BytesIO(jpeg_bytes))
            img_str = img.tobytes()
            mode = 'RGBA' if img.mode == 'RGBA' else 'RGB'
            surf = pygame.image.fromstring(img_str, img.size, mode).convert_alpha()
            self.frames.append(surf)
        
        self.total_frames = len(self.frames)
        print(f"Сконвертировано {len(self.frames)} кадров")
    
    def load_from_cache_threaded(self):
        """Запускает загрузку из кэша в фоне"""
        thread = threading.Thread(target=self.load_from_cache, daemon=True)
        thread.start()
    
    def load_video_threaded(self):
        thread = threading.Thread(target=self.load_video, daemon=True)
        thread.start()
    
    def play(self):
        if self.loaded:
            self.timer+=self.animation_speed
            if self.timer>=2.2:
                self.timer=0
                self.count+=1
            if self.count>=len(self.frames)-1:
                if self.loop:
                    self.count=0
                elif not self.loop:
                    self.count=len(self.frames)-1
            if not self.count>=len(self.frames)-1:
                self.Surface.blit(self.frames[self.count],(0,0))
    
    def change_loop(self, loop):
        self.loop = loop