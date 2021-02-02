# - Import Libraries
import pygame, random, sys

# - Initialize pygame
pygame.init()

# - Screen Size (height and width)
WIDTH = 800
HEIGHT = 600

# - Initialize color codes
RED = (255,0,0) # - Red
BLUE = (0,0,255) # - Blue
YELLOW = (255,255,0) # - Yellow
BACKGROUND_COLOR = (0,0,0) # - Black color
bg_image = pygame.image.load("bg.jpg")


# - player size and position
player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

# - enemy size and position
enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

# - initial game speed
SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False
score = 0

clock = pygame.time.Clock()

# - set font style
myFont = pygame.font.SysFont("monospace", 35)


# - set speed based on score (increase speed with increased score)
def set_level(score, SPEED):
	if score < 20:
		SPEED = 5
	elif score < 40:
		SPEED = 8
	elif score < 60:
		SPEED = 12
	else:
		SPEED = 15
	return SPEED
	# SPEED = score/5 + 1


# - Method for randomly spawining enemies
def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

#- Method for drawing enemy shape
def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

#- Increase enemy speed when score increases
def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score

#- Check if player collides wih enemies
def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False

# - sub method for detecting collision
def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False

#- Game main loop
while not game_over:
    # - For each event in the game get event
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # - Exit if close is clicked
			sys.exit()

		if event.type == pygame.KEYDOWN: # - move player when left or right button is pressed

			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT: # - move left
				x -= player_size
			elif event.key == pygame.K_RIGHT: # - move right
				x += player_size

			player_pos = [x,y] # update player position

    # - set background image
	screen.blit(bg_image,(0,0))
    # - call method to generate enemies
	drop_enemies(enemy_list)
	# - update score
	score = update_enemy_positions(enemy_list, score)
	# -set speed of enemu generation based on score
	SPEED = set_level(score, SPEED)
    # - label "score :"
	text = "Score:" + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40)) # - Show score on screen


    #- check collision
	if collision_check(enemy_list, player_pos):
		game_over = True
		break

	draw_enemies(enemy_list)

	pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

	clock.tick(30)

	pygame.display.update()
