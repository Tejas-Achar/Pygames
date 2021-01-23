import pygame
from pygame.locals import *

pygame.init()
#-----Freeze Frame Rate ----------(Lesson 2)
clock = pygame.time.Clock()
fps = 60


#------------Screen Configuration-------------------
screen_width = 1000
screen_height= 700
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Odessey") #------------Title of the screen

#------------Flag to check if the game is running------------------
run = True


#-------------Load Images-------------------

background_image = pygame.image.load("spacebg.png")

#-------------Draw Grid for reference --------------------
def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

#------------Define Game Variables----------

tile_size = 50
game_over = 1

#------------Player Class-------------------
class Player():
    def __init__(self,x,y):
        img = pygame.image.load("tom.png")
        self.image = pygame.transform.scale(img,(40,80))
        self.dead_image = pygame.image.load("ghost.png")
        self.win_image = pygame.image.load("Rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumped = False
        self.vel_y = 0
    def update(self, game_over):
      dx = 0
      dy = 0
      if game_over == 1:
        #-get keybard inputs to move player
        key = pygame.key.get_pressed()
        if key[K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[K_SPACE] == False:
            self.jumped = False

        if key[K_LEFT]:
            dx -= 5
        if key[K_RIGHT]:
            dx += 5
        #-set graviy
        self.vel_y +=1
        if self.vel_y>10:
            self.vel_y=10
        dy += self.vel_y
        #-Check for Collision
        for tile in world.tile_list:
            #-check collision x axis
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #-check collision y axis
            if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                #check if below the ground (jumping)
                if self.vel_y<0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground (falling)
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        #-Check for collisions with enimies
        if pygame.sprite.spritecollide(self, lava_group, False):
            game_over = 0
            print("Game Over!!")
        if pygame.sprite.spritecollide(self, finish_group, False):
            game_over = 2
            print("You win!!")

      elif game_over==0:
          self.image = self.dead_image
          self.rect.y -= 5
      elif game_over == 2:
          self.image = self.win_image
          self.rect.y -= 5
      #-Update player coordinates
      self.rect.x += dx
      self.rect.y += dy



      #-draw player
      screen.blit(self.image,self.rect)

      #-Showplayer collider
      # pygame.draw.rect(screen,(255,255,255),self.rect,0)
      return game_over

#------------World Class--------------------
class World():
    def __init__(self,data):
        self.tile_list = []

        #load images------------------
        platform_image = pygame.image.load("platform.png")
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(platform_image,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    lava = Enemy(col_count*tile_size,row_count*tile_size)
                    lava_group.add(lava)

                if tile == 3:
                    Rocket = EndGame(col_count*tile_size,row_count*tile_size)
                    finish_group.add(Rocket)

                col_count +=1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 0)

#----------------Enemy class------------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("lava.png")
        self.image = pygame.transform.scale(img,(tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#----------------End game portal class--------------------------
class EndGame(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("Rocket.png")
        self.image = pygame.transform.scale(img,(tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
change the values within the matrix/list of lists to change the world
1 = bricks
2 = lava
3 = End game portal
"""
world_data = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,0,1,2,2,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,1,1,1,1,1,2,1,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,2,2,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

]

#----Initialize game objects-----------
lava_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
player = Player(200,screen_height-110)
world = World(world_data)


while run:
    clock.tick(fps)
    screen.blit(background_image,(0,0))

    #-draw_grid() #un comment to see the grid view of the screen
    world.draw()
    lava_group.draw(screen)
    finish_group.draw(screen)

    #-monitoring events happening in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    game_over= player.update(game_over)
    pygame.display.update()


