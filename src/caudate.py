import sys
import pygame
import random

def draw_background_continuously(background_x_pos):
    screen.blit(background, (background_x_pos, 0))
    screen.blit(background, (background_x_pos + 1920, 0))

def create_algae():
    random_algae_pos = random.choice(algae_height)
    bottom_algae = algae_bottom.get_rect(midtop=(500, random_algae_pos))
    top_algae = algae_bottom.get_rect(midbottom=(500, random_algae_pos - 300))
    return bottom_algae, top_algae


def move_algae(algaes):
    for algae in algaes:
        algae.centerx -= 5
    return algaes

def draw_algae(algaes):
    algaes = move_algae(algaes)
    for algae in algaes:
        if algae.bottom >= 1024:
            screen.blit(algae_bottom, algae)
        else:
            flipped_algae = pygame.transform.flip(algae_bottom, False, True)    
            screen.blit(flipped_algae, algae)
        
def check_for_collision(algaes):
    for algae in algaes:
        if(player_rect.colliderect(algae)):
            return False
    if player_rect.top <= -100 or player_rect.bottom >= 900:
         return False
    return True    

def reset_map():
    algae_list.clear()
    player_rect.center = (100,512)
    
def rotate_player(player):
    new_player = pygame.transform.rotozoom(player, falling_velocity * 1.5, 1)  
    return new_player  

def player_animation():
    new_player = player_frames[player_frame_index]
    new_player_rect = new_player.get_rect(center = (100, player_rect.centery))
    return new_player, new_player_rect
pygame.init()

# background
background = pygame.image.load('src/images/background.png')
background_x_pos = 0
background_movement_velocity = -2
size = width, height = 576, 1024

screen = pygame.display.set_mode(size)
screen.blit(background, (0, 0))

# player
player_idle = pygame.image.load('src/images/normal.png')
player_jump = pygame.image.load('src/images/jump.png')
player_frames = [player_idle, player_jump]
player_frame_index = 0
player_x = width / 2
player_y = height / 2
falling_velocity = 0
downward_drag_acceleration = 0.5

PLAYERFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PLAYERFLAP, 1000)
player_surface = player_frames[player_frame_index]
player_rect = player_surface.get_rect(center=(player_x, player_y))

# pipe entities
algae_top = pygame.image.load('src/images/algae_top.png')
algae_bottom = pygame.image.load('src/images/algae_bottom.png')
algae_list = []
SPAWNALGAE = pygame.USEREVENT

# general
game_active = True

pygame.time.set_timer(SPAWNALGAE, 1200)
algae_height = [700, 750, 800]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                falling_velocity = -10
                screen.blit(player_jump, (player_x, player_y))
                if player_frame_index < 1:
                   player_frame_index += 1
                else:
                    player_frame_index = 0 
               
                player_surface, player_rect = player_animation()  
                
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                reset_map()   
        if event.type == SPAWNALGAE:
            algae_list.extend(create_algae())
             
    # background
    background_x_pos += background_movement_velocity
    draw_background_continuously(background_x_pos)
    if background_x_pos <= -1920:
        background_x_pos = 0
    
    if game_active:    
        # player
        falling_velocity += downward_drag_acceleration
        player_rect.centery += falling_velocity
        rotated_player = rotate_player(player_surface)
        screen.blit(rotated_player, player_rect)
        game_active = check_for_collision(algae_list)
        # algae
        draw_algae(algae_list)


    pygame.display.update()
    clock.tick(60)
