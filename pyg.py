import pygame
import sys
import utili

pygame.mixer.init()
laser_sound = pygame.mixer.Sound("D:/SEMESTER 1/programming comp102/pythonProject2/shoot.mp3")
pygame.mixer.music.load("D:/SEMESTER 1/programming comp102/pythonProject2/sound.mp3")
collision_sound = pygame.mixer.Sound("D:/SEMESTER 1/programming comp102/pythonProject2/jump.mp3")
pygame.mixer.music.play()
pygame.init()
font_path = r"D:/SEMESTER 1/programming comp102/pythonProject2/ARCADECLASSIC.ttf"
width = 600
height = 700
wind = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroid Junction")
background = pygame.transform.scale(pygame.image.load("background.jpg"), (width, height))
player = pygame.image.load("Player.png")
met1 = pygame.image.load("met.png")
met2 = pygame.image.load("met3.png")
met3 = pygame.image.load("met2.png")
met4 = pygame.image.load("met4.png")
enemy = pygame.image.load("enemy.png")
elaser = pygame.image.load('enemy.png')
shield_img = pygame.image.load("shield.png")
laserimg = pygame.image.load("playerlaser.png")
gun = pygame.image.load("gun.png")
barrier = pygame.image.load("barrier.png")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)
pygame.display.set_icon(icon)
pygame.display.set_icon(icon)


def detect_collision(player, enemies):
    for asteroid in enemies:
        if player.mask.overlap(asteroid.mask, (asteroid.x - player.x, asteroid.y - player.y)):
            player.lives -= 1  # Decrement player's health by 1
            enemies.remove(asteroid)
            collision_sound.play()


def main_menu(high_score):
    font_path = r"D:/SEMESTER 1/programming comp102/pythonProject2/ARCADECLASSIC.ttf"
    menu_font = pygame.font.Font(font_path, 25)
    title_label = menu_font.render("Asteroid Junction", 1, (204, 204, 255))
    start_label = menu_font.render("WELCOME! Press 'Enter' to Start", 1, (255, 255, 255))
    high_score_label = menu_font.render("Press 'H' to View High Score", 1, (255, 255, 255))
    exit_label = menu_font.render("Press 'esc' to exit", 1, (255, 255, 255))
    menu_running = True
    while menu_running:
        wind.blit(background, (0, 0))
        title_x = width // 2 - title_label.get_width() // 2
        title_y = height // 2 - title_label.get_height() - 50
        start_x = width // 2 - start_label.get_width() // 2
        start_y = height // 2 - start_label.get_height() // 2
        high_score_x = width // 2 - high_score_label.get_width() // 2
        high_score_y = height // 2 - high_score_label.get_height() // 2 + 50
        exit_x = width // 2 - exit_label.get_width() // 2
        exit_y = height // 2 - exit_label.get_height() // 2 + 100

        wind.blit(title_label, (title_x, title_y))
        wind.blit(start_label, (start_x, start_y))
        wind.blit(high_score_label, (high_score_x, high_score_y))
        wind.blit(exit_label, (exit_x, exit_y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Start the game
                elif event.key == pygame.K_h:
                    high_score_text = menu_font.render(f"High Score: {high_score}", 1, (255, 255, 255))
                    wind.blit(high_score_text, (width // 2 - high_score_text.get_width() // 2, 550))
                    pygame.display.update()
                    pygame.time.delay(3000)  # Display high score for 3 seconds
                    main_menu(high_score)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    FPS = 60
    clock = pygame.time.Clock()
    play = utili.Player(250, 700, player, laserimg)
    font_path = r"D:/SEMESTER 1/programming comp102/pythonProject2/ARCADECLASSIC.ttf"
    main_font = pygame.font.Font(font_path, 20)

    enemies = []
    lasers = []

    bg_y = 0
    bg_y2 = -height

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False

    score = utili.Score()
    score.load_highscore()
    highscore = score.get_highscore()

    def redraw(player, lasers):
        wind.blit(background, (0, bg_y))
        wind.blit(background, (0, bg_y2))
        life = main_font.render(f"Lives: {player.lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score.get_score()}", 1, (255, 255, 255))

        if lost:
            wind.fill((0, 0, 0))
            wind.blit(background, (0, 0))
            lost_label = main_font.render(f"YOU LOST! | GAME OVER | SCORE: {score.get_score()}", 1, (0, 255, 255))
            wind.blit(lost_label, (width / 2 - lost_label.get_width() / 2, 400))
        player.draw(wind)
        for laser in lasers:
            laser.draw(wind)
        for enm in enemies:
            enm.draw(wind)
        wind.blit(life, (10, 10))
        wind.blit(score_label, (width - score_label.get_width() - 10, 10))
        pygame.display.update()

    while True:
        r = True
        lost = False
        lostcount = 0
        pause = False
        start_game = False

        main_menu(highscore)

        while r:
            clock.tick(FPS)

            if play.lives == 0:
                lost = True

            if lost:
                play.lives=0
                if lostcount >= FPS * 2:
                    r = False
                else:
                    lostcount += 1
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                r = False
                                start_game = True  # Set the flag to start the game
                                break
            if not r:
                # Reset game state and variables
                play.lives = 3
                score.reset_score()
                enemies.clear()
                lasers.clear()
                break
            if start_game:
                # Game initialization
                pygame.mixer.music.play()  # Start background music
                play = utili.Player(250, 700, player, laserimg)
                enemies = []
                lasers = []
                bg_y = 0
                bg_y2 = -height
            if len(enemies) < 12:
                for i in range(1):
                    ast = utili.Asteroid(0, -100 * i)
                    ast.createobj(met1, met2, met3, met4)
                    enemies.append(ast)

            for i in enemies:
                i.move(1)
                if i.y > 800:
                    enemies.remove(i)

            for i in enemies:
                i.move(1)
                if i.y > 800:
                    enemies.remove(i)

            bg_y += 1
            bg_y2 += 1
            if bg_y > height:
                bg_y = -height

            if bg_y2 > height:
                bg_y2 = -height

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    r = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        up_pressed = True
                    elif event.key == pygame.K_DOWN:
                        down_pressed = True
                    elif event.key == pygame.K_LEFT:
                        left_pressed = True
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = True
                    elif event.key == pygame.K_SPACE:
                        play.shoot_laser(lasers)
                        laser_sound.play()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        up_pressed = False
                    elif event.key == pygame.K_DOWN:
                        down_pressed = False
                    elif event.key == pygame.K_LEFT:
                        left_pressed = False
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = False

            if up_pressed and play.y > 0:
                play.y -= 3
            if down_pressed and play.y < 700:
                play.y += 3
            if left_pressed and play.x > 0:
                play.x -= 3
            if right_pressed and play.x < 550:
                play.x += 3

            if play.y > height:
                play.y = 700

            play.cooldown_laser()

            for laser in lasers[:]:
                laser.move()
                if laser.y < 0:
                    lasers.remove(laser)
                else:
                    for enemy in enemies:
                        if laser.collision(enemy):
                            enemies.remove(enemy)
                            lasers.remove(laser)
                            score.increase_score(15)
                            break

            detect_collision(play, enemies)

            redraw(play, lasers)
        score.save_score()
        score.reset_score()


main()
