import pygame, sys, random

# - reset ball position to center method/function
def ball_restart():
    global ball_speed_y
    ball.center = (screen_width/2,screen_height/2)
    ball_speed_y *= random.choice((1,-1))

# - initialize pygame
pygame.init()
clock = pygame.time.Clock()

# - screen width and height
screen_width = 1280
screen_height = 700

# - flag variable to check whether game is running or not : true = game running & false = game has stopped
run = True

# - Start screen with window caption "Ping Pong!"
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Ping pong!")

# - Game Objects
ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15, 30,30)
player = pygame.Rect(screen_width - 20, screen_height/2-70,10,140)
opponent = pygame.Rect(10, screen_height/2-70,10,140)

# - Game object controls
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7 # this variable decides the difficulty of the game, higher the number more difficult the game.

# - Game colors
bg_color = pygame.Color("grey12")
object_color = (255,255, 255)

# - game main loop
while run:
    # - get all events in game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # - move player up and down 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # - Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # - Ball boundaries
    if ball.top <=0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()

    # - Ball collisions with player and opponent...If collision is true. change horizontal ball direction.
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # - Player threshold... to make the player stay within the screen
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
    player.y += player_speed
    
    # - logic for opponant AI
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    # - Opponant threshold... to make opponent stay within the screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

    # - Draw game objects on screen
    screen.fill(bg_color)
    pygame.draw.rect(screen, object_color, player)
    pygame.draw.rect(screen,object_color, opponent)
    pygame.draw.ellipse(screen, object_color, ball)
    pygame.draw.aaline(screen, object_color, (screen_width/2, 0),(screen_width/2, screen_height))
    pygame.display.flip()

    #- Set refresh rate of screen
    clock.tick(60)
