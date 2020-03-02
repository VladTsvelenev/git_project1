# -*- coding: utf-8 -*-
import pygame, random, os
from random import choice
import copy
import sys
pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()  
SPEED = 5
FPS = 300
A = [(9, 9)]
B = [] * 400
z = False
DIRECTION = 0

def load_image(name, colorkey=(255, 255, 255)):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image 

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
    player_image = load_image('snakehead.png')
    tile_width = tile_height = 0   
    player = None
    pygame.display.flip()
    xsm = 0
    ysm = 0
    running = True    
    #!!!!!!!!!!!!!!!!!!!!!!!!!
    intro_text = []
    fon = pygame.transform.scale(load_image('fon.png'), (1000, 1000))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)       
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                xkoord = pos[0]
                ykoord = pos[1]
                if ykoord > 360 and ykoord < 460: 
                    if xkoord > 350 and xkoord < 660:
                        return 'mapeasy.txt'                    
                elif ykoord > 500 and ykoord < 620: 
                    if xkoord > 270 and xkoord < 760:
                        return 'mapmedium.txt'                 
                elif ykoord > 660 and ykoord < 750: 
                    if xkoord > 350 and xkoord < 680:
                        return 'maphard.txt'              
        pygame.display.flip()
        clock.tick(FPS) 

def lose_screen():
    global A
    intro_text = ["Score:" + str(len(A) - 1)]
    fon = pygame.transform.scale(load_image('losescreen.png'), (1000, 1000))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 150)
    text_coord = 700
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 330
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)     
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Thanks for playing")
                terminate()       
        pygame.display.flip()
        clock.tick(FPS)

def win_screen():
    fon = pygame.transform.scale(load_image('winscreen.png'), (1000, 1000))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50      
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Thanks for playing")
                terminate()            
        pygame.display.flip()
        clock.tick(FPS)
        
def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
  
    max_width = max(map(len, level_map))
  
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))    

tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('snakehead.png')

tile_width = tile_height = 50 

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group):
        super().__init__(group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(group)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
    
    def transfer(self, dx, dy):
        global running
        self.rect = self.rect.move(dx, dy)
        self.pos_x += dx//50
        self.pos_y += dy//50
        if pygame.sprite.spritecollideany(self, walls):
            self.rect = self.rect.move(-dx, -dy)
            self.pos_x -= dx//50
            self.pos_y -= dy//50
            lose_screen()

    
    def coords(self):
        return (self.pos_x, self.pos_y)
    
    def turn(self, DIRECTION):
        if DIRECTION == 1:
            self.image = load_image('snakeheadup.png')
        elif DIRECTION == 2:
            self.image = load_image('snakeheadright.png')     
        elif DIRECTION == 3:
            self.image = load_image('snakeheaddown.png')
        elif DIRECTION == 4:
            self.image = load_image('snakeheadleft.png') 
             
class Apple(pygame.sprite.Sprite):
    def __init__(self, FILE, *group):
        super().__init__(group)
        global A
        q = True 
        if FILE == 'mapeasy.txt':
            self.B = load_level('mapeasy.txt')
        elif FILE == 'mapmedium.txt':
            self.B = load_level('mapmedium.txt')
        elif FILE == 'maphard.txt':
            self.B = load_level('maphard.txt')
        self.X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        while q:
            x = choice(self.X)
            y = choice(self.X)
            if (x, y) not in A and self.B[y][x] != "#":
                q = False
        self.pos_x = x
        self.pos_y = y
        self.image = load_image('apple.png')
        self.rect = self.image.get_rect().move(tile_width * self.pos_x, tile_height * self.pos_y)    
        
    def coords(self):
        return (self.pos_x, self.pos_y)
    
    def teleport(self):
        q = True
        while q:
            x = choice(self.X)
            y = choice(self.X)
            if (x, y) not in A and self.B[y][x] != "#":
                q = False
        self.pos_x = x
        self.pos_y = y
        self.rect = self.image.get_rect().move(tile_width * self.pos_x, tile_height * self.pos_y)
        
        


player = None


all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':
                Tile('wall', x, y , tiles_group, walls, all_sprites)
            elif level[y][x] == '@':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_player = Player(x, y, player_group, all_sprites)           
    return new_player, x, y
FILE = start_screen()
player, level_x, level_y = generate_level(load_level(FILE))
pygame.display.flip()
xsm = 0
ysm = 0
food = None
food = Apple(FILE, all_sprites, tiles_group) 
body = load_image('snakebody.png')
running = True
tiles_group.draw(screen)
while running:
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and DIRECTION != 4:
                xsm = 50
                ysm = 0 
                DIRECTION = 2
                player.turn(DIRECTION)
            if event.key == pygame.K_LEFT  and DIRECTION != 2:
                xsm = -50
                ysm = 0
                DIRECTION = 4
                player.turn(DIRECTION)
            if event.key == pygame.K_DOWN  and DIRECTION != 1:
                xsm = 0
                ysm = 50
                DIRECTION = 3
                player.turn(DIRECTION)
            if event.key == pygame.K_UP  and DIRECTION != 3:
                xsm = 0
                ysm = -50
                DIRECTION = 1
                player.turn(DIRECTION)
    A[0] =  player.coords()   
    if player.coords() == food.coords():
        food.teleport()
        A += [(0, 0)]
        z = True
    if FILE == 'mapeasy.txt':  
        if len(A) == 324:
            win_screen()
    elif FILE == 'mapmedium.txt':
        if len(A) == 294:
            win_screen()
    elif FILE == 'maphard.txt':
        if len(A) == 256:
            win_screen()
    for i in range(1, len(A)):
        A[i] = B[i - 1] 
    player.transfer(xsm, ysm)          
    if player.coords() in A[1:]:
        lose_screen()
    tiles_group.draw(screen) 
    player_group.draw(screen)
    for i in range(0, len(A)):
        screen.blit(body, (tile_width * A[i][0],  tile_height * A[i][1]))
    pygame.display.flip()
    if len(A) > 162:
        SPEED = 14
    elif len(A) > 81:
        SPEED = 12
    elif len(A) > 40:
        SPEED = 10
    elif len(A) > 20:
        SPEED = 8 
    elif len(A) > 10:
        SPEED = 6
    clock.tick(SPEED)
    B = copy.deepcopy(A)
    z = False
    
pygame.quit()
