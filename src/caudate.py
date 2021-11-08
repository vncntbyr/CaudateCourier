import sys
import pygame
import random

def draw_background_continuously(background_x_pos):
    screen.blit(background, (background_x_pos, 0))
    screen.blit(background, (background_x_pos + 1920, 0))

def spawn_algae():
    random_algae_pos = random.choice(algae_height)
    bottom_algae = algae_bottom.get_rect(midtop=(700, random_algae_pos))
    top_algae = algae_bottom.get_rect(midbottom=(700, random_algae_pos - 300))
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

def display_score():
    display_score = f'Score: {str(int(score))}'
    score_surface = game_font.render(display_score, True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (288, 100))
    screen.blit(score_surface, score_rect)

def display_highscore():
    display_score = f'Highscore: {str(int(high_score))}'
    highscore_surface = game_font.render(display_score, True, (255, 255, 255))
    game_over_surface = game_highscore_font.render('Game Over', True, (255, 255, 255))
    highscore_rect = highscore_surface.get_rect(center = (288, 512))
    game_over_rect = highscore_surface.get_rect(center = (220, 400))
    screen.blit(highscore_surface, highscore_rect)
    screen.blit(game_over_surface, game_over_rect)

def update_highscore(high_score):
    if score > high_score:
        high_score = score
    return high_score    
                
pygame.init()

# general
game_active = True
score = 0
high_score = 0

clock = pygame.time.Clock()
game_font = pygame.font.Font('src/fonts/font.otf', 40)
game_highscore_font = pygame.font.Font('src/fonts/font.otf', 80)

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
player_x = 100
player_y = height / 2
falling_velocity = 0
downward_drag_acceleration = 0.5

PLAYERFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PLAYERFLAP, 1000)
player_surface = player_frames[player_frame_index]
player_rect = player_surface.get_rect(center=(player_x, player_y))

# algae entities
algae_top = pygame.image.load('src/images/algae_top.png')
algae_bottom = pygame.image.load('src/images/algae_bottom.png')
algae_list = []
SPAWNALGAE = pygame.USEREVENT

pygame.time.set_timer(SPAWNALGAE, 1200)
algae_height = [700, 750, 800]

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
            algae_list.extend(spawn_algae())
             
    # background
    draw_background_continuously(background_x_pos)
    if background_x_pos <= -1920:
        background_x_pos = 0
    
    if game_active:
        # background
        background_x_pos += background_movement_velocity    
        # player
        falling_velocity += downward_drag_acceleration
        player_rect.centery += falling_velocity
        rotated_player = rotate_player(player_surface)
        screen.blit(rotated_player, player_rect)
        game_active = check_for_collision(algae_list)
        # algae
        draw_algae(algae_list)
        # score
        score += 0.01
        high_score = update_highscore(high_score)
        display_score()
    else:
        score = 0
        display_highscore()

    pygame.display.update()
    clock.tick(60)
