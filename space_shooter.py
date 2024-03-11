import pygame
from game_classes import HealthBar
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

yellow_health_bar = HealthBar(10, 10, 167, 40, 10)
red_health_bar = HealthBar(723, 10, 167, 40, 10)

pygame.display.set_caption("Retro Space Shooter")

WHITE = (225,225,225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('/Users/Arnav/Dropbox/Code/Retro Space Shooter/Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('/Users/Arnav/Dropbox/Code/Retro Space Shooter/Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('calibri', 40)
WINNER_FONT = pygame.font.SysFont('calibri', 100)

FPS = 60
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
VELOCITY = 4
BULLET_VELOCITY = 7
MAX_BULLETS = 10

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    '/Users/Arnav/Dropbox/Code/Retro Space Shooter/Assets/spaceship_yellow.png')
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    '/Users/Arnav/Dropbox/Code/Retro Space Shooter/Assets/spaceship_red.png')
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load('/Users/Arnav/Dropbox/Code/Retro Space Shooter/Assets/space.png'), (WIDTH, HEIGHT))

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WINDOW.blit(SPACE, (0,0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    yellow_health_bar.draw(WINDOW)
    red_health_bar.draw(WINDOW)

    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, BLACK)
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, BLACK)
    WINDOW.blit(yellow_health_text, (10, 10))
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))


    WINDOW.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet )

    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VELOCITY < HEIGHT - 10:
        yellow.y += VELOCITY
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VELOCITY < BORDER.x + 15:
        yellow.x += VELOCITY

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VELOCITY < HEIGHT - 10:
        red.y += VELOCITY
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VELOCITY < WIDTH + 15:
        red.x += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    winner = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(winner, (WIDTH/2 - winner.get_width()/2, HEIGHT/2 - winner.get_height()/2) )
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    yellow = pygame.Rect(150, 215, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(750, 215, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    yellow_bullets = []
    red_bullets = []
    
    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                yellow_health_bar.hp -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                red_health_bar.hp -= 1

                BULLET_HIT_SOUND.play()
        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        elif red_health <= 0:
            winner_text = "Yellow Wins!"

        if winner_text != "":
            draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    pygame.quit()

if __name__ == "__main__":
    main()