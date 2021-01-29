import pygame,random

pygame.init()

Clock = pygame.time.Clock()
run = True
screenWidth = 500
screenHeight = 750

# - Game images
Background_Image = pygame.image.load("background.png")
Bird = pygame.image.load("bird.png")
BirdRect = Bird.get_rect()
OtherBird = pygame.image.load("bird.png")
OtherBirdRect = OtherBird.get_rect()

# - Bird position
Bird_x = 50
Bird_y = 300
Bird_y_Change = 0

# - Other birds
OtherBirdWidth = 70
OtherBirdHeight = 70
OtherBird_X_Change = -4
OtherBird_X = 500
OtherBird_Y = random.randint(150,650)

screen = pygame.display.set_mode((screenWidth,screenHeight))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Bird_y_Change = -6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                Bird_y_Change = 8
    # Bird logic-------------------------
    screen.blit(Background_Image,(0,0))
    Bird_y += Bird_y_Change

    # If bird touches thrones above and below the screen-------------------
    if Bird_y <= 0:
        Bird_y = 350
    if Bird_y >= 570:
        Bird_y = 350
    screen.blit(Bird,(Bird_x,Bird_y))

    # Oponent logic ----------------------
    OtherBird_X += OtherBird_X_Change
    if OtherBird_X <= -10:
        OtherBird_X = 500
        OtherBird_Y = random.randint(100,650)
    screen.blit(OtherBird,((OtherBird_X,OtherBird_Y)))

    pygame.display.flip()
    Clock.tick(60)
