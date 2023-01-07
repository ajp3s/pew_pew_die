import os.path
import pygame

pygame.font.init()
pygame.mixer.init()

# Loading sounds and adjusting volume.
left_laser_sound = pygame.mixer.Sound(os.path.join("Assets", "laser_gun_sound_left.wav"))
right_laser_sound = pygame.mixer.Sound(os.path.join("Assets", "laser_gun_sound_right.mp3"))
right_laser_sound.set_volume(0.1)
background_music = pygame.mixer.Sound(os.path.join("Assets", "general_battle.mp3"))
background_music.set_volume(0.3)

# Setting the game name.
pygame.display.set_caption("Pew,pew,die!")

# Storing ships measurements in a variable to use them later.
ships_width, ships_height = 110, 110

# And window measurements in constants.
WIDTH, HEIGHT = 1600, 920

# Creating border in the middle of the screen.
BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

# Defining window size.
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Loading and resizing the background image to fit the window.
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Outer-Space.jpg")), (WIDTH, HEIGHT))

# Creating user events for when the ships take a hit.
left_hit = pygame.USEREVENT + 1
right_hit = pygame.USEREVENT + 2

FPS = 60
projectile_speed = 12
ships_speed = 8

# Playing some music in the background,so we don't feel stupid while playing a 2D game.
background_music.play(-1)

# Loading, resizing and rotating the ships images.
LEFT_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "white_spaceship.png"))

LEFT_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(LEFT_SPACESHIP_IMAGE, (ships_width, ships_height)), -90)

RIGHT_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship.png"))

RIGHT_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RIGHT_SPACESHIP_IMAGE, (ships_width, ships_height)), 90)

# Choosing font.
FONT = pygame.font.SysFont("Fixedsys Regular", 80)


# Defining functions for player movement controls while making sure they don't go out of bounds.
def right_ship_controls(keys_pushed, right):
    if keys_pushed[pygame.K_DOWN] and right.y + ships_speed < HEIGHT - ships_height:
        right.y += ships_speed
    if keys_pushed[pygame.K_UP] and right.y + ships_speed > 11:
        right.y -= ships_speed
    if keys_pushed[pygame.K_LEFT] and right.x + ships_speed > BORDER.x + 20:
        right.x -= ships_speed
    if keys_pushed[pygame.K_RIGHT] and right.x - ships_speed < WIDTH - ships_width - 15:
        right.x += ships_speed


def left_ship_controls(keys_pushed, left):
    if keys_pushed[pygame.K_s] and left.y + ships_speed < HEIGHT - ships_height:
        left.y += ships_speed
    if keys_pushed[pygame.K_w] and left.y - ships_speed > -5:
        left.y -= ships_speed
    if keys_pushed[pygame.K_a] and left.x - ships_speed > 0:
        left.x -= ships_speed
    if keys_pushed[pygame.K_d] and left.x + ships_speed + ships_width < BORDER.x + 1:
        left.x += ships_speed


# Checking if any of projectiles hit something or left the screen and if they do - remove them from the respective list.
def shooting_func(left_projectiles, right_projectiles, left, right):
    for projectile in left_projectiles:
        projectile.x += projectile_speed
        if right.colliderect(projectile):
            pygame.event.post(pygame.event.Event(left_hit))
            left_projectiles.remove(projectile)
        elif projectile.x > WIDTH:
            left_projectiles.remove(projectile)

    for projectile in right_projectiles:
        projectile.x -= projectile_speed
        if left.colliderect(projectile):
            pygame.event.post(pygame.event.Event(right_hit))
            right_projectiles.remove(projectile)
        elif projectile.x < 0:
            right_projectiles.remove(projectile)


def draw_win(left, right, left_projectiles, right_projectiles, left_armor, right_armor):
    # Drawing the background image and the border.
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDER)

    # Drawing the armor points labels.
    left_armor_text = FONT.render("Bright Side: " + str(left_armor), True, (255, 255, 255))
    right_armor_text = FONT.render("Dark Side: " + str(right_armor), True, (255, 255, 255))
    WINDOW.blit(right_armor_text, (WIDTH - right_armor_text.get_width() - 20, 20))
    WINDOW.blit(left_armor_text, (20, 20))

    # Drawing the ships.
    WINDOW.blit(LEFT_SPACESHIP, (left.x, left.y))
    WINDOW.blit(RIGHT_SPACESHIP, (right.x, right.y))

    # Drawing projectiles.
    for projectile in left_projectiles:
        pygame.draw.rect(WINDOW, (110, 13, 129), projectile)

    for projectile in right_projectiles:
        pygame.draw.rect(WINDOW, (110, 13, 129), projectile)
    pygame.display.update()


# Drawing the winner's phrase in the selected color.
def endgame_draw(string, string1, string2, color):
    winner_text = FONT.render(string, True, color)
    winner_text1 = FONT.render(string1, True, color)
    winner_text2 = FONT.render(string2, True, color)
    WINDOW.blit(winner_text, (400, 300))
    WINDOW.blit(winner_text1, (400, 400))
    WINDOW.blit(winner_text2, (400, 500))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    # Defining starting positions and size of the ships.
    left = pygame.Rect(150, 400, ships_width, ships_height)
    right = pygame.Rect(1350, 400, ships_width, ships_height)

    # Gun clips.
    right_projectiles = []
    left_projectiles = []

    # Starting armor points.
    left_armor = 10
    right_armor = 10

    # Creating Clock object to limit the max FPS
    clock = pygame.time.Clock()
    executing = True
    while executing:
        # Limiting the max FPS
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executing = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Defining starting point and size of the projectiles.
                left_projectile = pygame.Rect(left.x + left.width - 10, left.y + ships_height // 2, 20, 5)
                right_projectile = pygame.Rect(right.x, right.y + ships_height // 2, 20, 5)

                # Defining shooting controls,limiting the maximum projectiles count and adding a sound to it.
                if event.key == pygame.K_LCTRL and len(left_projectiles) < 3:
                    left_projectiles.append(left_projectile)
                    left_laser_sound.play()

                if event.key == pygame.K_RCTRL and len(right_projectiles) < 3:
                    right_projectiles.append(right_projectile)
                    right_laser_sound.play()

            if event.type == left_hit:
                right_armor -= 1

            if event.type == right_hit:
                left_armor -= 1

        endgame_string = ""
        endgame_string1 = ""
        endgame_string2 = ""

        # Finding out who won and picking their endgame phrase.
        if left_armor <= 0:
            endgame_string = "Dark side clouds everything..."
            endgame_string1 = "impossible to see the future is..."
            endgame_string2 = "-Yoda."
            color = (74, 0, 17)

        if right_armor <= 0:
            endgame_string = "No matter how dark the night..."
            endgame_string1 = "Morning always comes..."
            endgame_string2 = "And our journey begins anew..."
            color = (240, 190, 99)

        if endgame_string != "":
            # Calling the endgame_draw function to draw the chosen phrase on the screen.
            endgame_draw(endgame_string, endgame_string1, endgame_string2, color)
            break

        shooting_func(left_projectiles, right_projectiles, left, right)
        keys_pushed = pygame.key.get_pressed()
        left_ship_controls(keys_pushed, left)
        right_ship_controls(keys_pushed, right)
        draw_win(left, right, left_projectiles, right_projectiles, left_armor, right_armor)

    main()


# So the game can be executed from this file only.
if __name__ == "__main__":
    main()
