import pygame
import os
import random
import time

class ShieldPowerup:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        offset_x = int(obj.x - self.x)
        offset_y = int(obj.y - self.y)
        return self.mask.overlap(obj.mask, (offset_x, offset_y)) is not None


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.laser_img = None
        self.lasers = []
        self.cd_count = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


class Player(Ship):
    def __init__(self, x, y, img, laser_img, lives=3):
        super().__init__(x, y, lives)
        self.img = img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.img)
        self.lives = lives
        self.laser_cooldown = 0
        self.shield = None
        self.shield_active = False

    def shoot_laser(self, lasers):
        if self.laser_cooldown == 0:
            laser = Laser(
                self.x + self.get_width() // 2 - self.laser_img.get_width() // 2,
                self.y,
                self.laser_img,)
            lasers.append(laser)
            self.laser_cooldown = 30

    def cooldown_laser(self):
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

    def activate_shield(self):
        self.shield = Shield(self.x, self.y, shield_img)
        
    def check_collision_with_shield_powerup(self, powerup):
        if powerup.collision(self):
            self.activate_shield()
            return True
        return False

    def draw(self, window):
        super().draw(window)
        if self.shield:
            self.shield.draw(window)


class Asteroid(Ship):
    def __init__(self, x, y, health=30):
        super().__init__(x, y, health)
        self.x = x
        self.y = y

    def createobj(self, img1, img2, img3, img4):
        self.x = random.randint(40, 540)
        self.y = random.randint(-1000, -100)
        r = random.randint(1, 100)
        if r > 0 and r <= 25:
            self.img = img1
        elif r > 25 and r <= 50:
            self.img = img2
        elif r > 50 and r <= 75:
            self.img = img3
        else:
            self.img = img4
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, y):
        self.y += y


class Score:
    def __init__(self):
        self.score = 0
        self.highscore = 0
        self.file_path = "highscores.txt"

    def increase_score(self, points):
        self.score += points
        if self.score > self.highscore:
            self.highscore = self.score

    def reset_score(self):
        self.score = 0

    def save_score(self):
        with open(self.file_path, "a") as file:
            file.write(str(self.score) + "\n")

    def load_highscore(self):
        try:
            with open(self.file_path, "r") as file:
                scores = [int(score.strip()) for score in file.readlines()]
                if scores:
                    self.highscore = max(scores)
                else:
                    self.highscore = 0
        except FileNotFoundError:
            self.highscore = 0

    def get_highscore(self):
        return self.highscore

    def get_score(self):
        return self.score


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def move(self):
        self.y -= 5

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        offset_x = int(obj.x - self.x)
        offset_y = int(obj.y - self.y)
        return self.mask.overlap(obj.mask, (offset_x, offset_y)) is not None


