#!/usr/bin/env python3

import sys
import pygame
import random
import time
import math
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

print(os.path.dirname(sys.argv[0]))

pygame.init()
pygame.display.set_caption("Incest Machine")
pygame.mouse.set_visible(False)
screen_size = pygame.display.Info()
try:
    font = pygame.font.Font(resource_path("Pixelmania.ttf"), 16)
except:
    font = pygame.font.Font(os.path.join(os.path.dirname(sys.argv[0]), "Pixelmania.ttf"), 16)
white = (255,255,255)
blue  = (0,0,255)
red   = (255,0,0)

# 4 Pairs of adams end eves
start_creatures = 4

max_creatures = (math.floor(screen_size.current_w / 32) * math.floor(screen_size.current_h / 32)) / 10

screen = pygame.display.set_mode([screen_size.current_w, screen_size.current_h], pygame.FULLSCREEN)

tick = pygame.time.Clock()
tick_rate = 600

creatures = []
games =      0 # Number of games
count_m =    0 # Males
count_f =    0 # Females
wins_m =     0 # Males win
wins_f =     0 # Females win
lastwinner = 3 # 0 = Males, 1 = Females, 2 = Draw, 3 = First run

# New creature
def newCreature(sex):
    creature = [
        random.randint(0, (math.floor(screen_size.current_w / 32)) - 1) * 32,
        random.randint(0, (math.floor(screen_size.current_h / 32)) - 1) * 32,
        sex
    ]
    global count_m
    global count_f
    if sex == 0: count_m = count_m + 1
    if sex == 1: count_f = count_f + 1

    creatures.append(creature)

# Adam and Eve
for x in range(0, start_creatures):
    newCreature(0)
    newCreature(1)

running = True

while running:

    # Blank screen
    screen.fill((0, 0, 0))

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()

    for creature in creatures:
        # Movement
        x = creature[0]
        y = creature[1]
        
        direction = random.randint(0, 7)
        if direction == 0 and x < screen_size.current_w - 32:   x = x + 32
        if direction == 1 and y < screen_size.current_h - 32:   y = y + 32
        if direction == 2 and x > 0:                            x = x - 32
        if direction == 3 and y > 0:                            y = y - 32

        # Draw
        if creature[2] == 0: color = red
        if creature[2] == 1: color = blue
        pygame.draw.rect(screen, color, (x, y, 32, 32))

        # Update creature
        creature[0] = x
        creature[1] = y

    # Fixed text
    row1 = font.render('MALES', False, red)
    row2 = font.render('FEMALES', False, blue)
    row3 = font.render('GAMES', False, white)
    row4 = font.render('LAST WINNER', False, white)
    row5 = font.render('WINS BY MALES', False, red)
    row6 = font.render('WINS BY FEMALES', False, blue)
    screen.blit(row1, (10, 10))
    screen.blit(row2, (10, 40))
    screen.blit(row3, (10, 70))
    screen.blit(row4, (10, 100))
    screen.blit(row5, (10, 130))
    screen.blit(row6, (10, 160))

    # Text
    row1 = font.render(str(count_m), False, red)
    row2 = font.render(str(count_f), False, blue)
    row3 = font.render(str(games), False, white)
    if lastwinner == 0: row4 = font.render('MALES', False, red)
    if lastwinner == 1: row4 = font.render('FEMALES', False, blue)
    if lastwinner == 2: row4 = font.render('DRAW', False, white)
    if lastwinner == 3: row4 = font.render('', False, white)
    row5 = font.render(str(wins_m), False, red)
    row6 = font.render(str(wins_f), False, blue)
    screen.blit(row1, (400, 10))
    screen.blit(row2, (400, 40))
    screen.blit(row3, (400, 70))
    screen.blit(row4, (400, 100))
    screen.blit(row5, (400, 130))
    screen.blit(row6, (400, 160))
    
    # Update screen
    pygame.display.update()
    tick.tick(tick_rate)

    # Check for collisions
    for male in creatures:
        if male[2] == 0:
            for female in creatures:
                if female[2] == 1:
                    if male[0] == female[0] and male[1] == female[1]:
                        newCreature(random.randint(0, 1))

    # Restart
    if len(creatures) >= max_creatures:
        if count_m > count_f:
            lastwinner = 0
            wins_m = wins_m + 1
        elif count_f > count_m:
            lastwinner = 1
            wins_f = wins_f + 1
        else:
            lastwinner = 2
        count_m = 0
        count_f = 0
        games = games + 1
        creatures = []
        for x in range(0, start_creatures):
            newCreature(0)
            newCreature(1)
