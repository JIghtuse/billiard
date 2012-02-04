#!/usr/bin/python

from ball import *

def show_menu():
    sprites = []
    menu_items = ["chain", "physics", "testing", "exit"]
    coords = [(405, 100), (429, 150), (473, 200), (486, 250)]
    widths = [213, 166, 77, 51]
    for i in range(4):
        sprite = pygame.image.load(menu_items[i] + ".png")
        sprites.append(sprite)

    flag = True
    while flag:
        screen.fill(THECOLORS["white"])
        for i in range(4):
            x, y = coords[i]
            screen.blit(sprites[i], (x, y, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coord = event.pos
                if (coord[0] >= 405 and coord[0] <= 405 + 213 and coord[1] >= 100 and coord[1] <= 123):
                    mark(5)
                elif (coord[0] >= 429 and coord[0] <= 429 + 166 and coord[1] >= 150 and coord[1] <= 173):
                    play()
                elif (coord[0] >= 473 and coord[0] <= 473 + 213 and coord[1] >= 200 and coord[1] <= 223):
                    markov()
                elif (coord[0] >= 486 and coord[0] <= 486 + 213 and coord[1] >= 250 and coord[1] <= 273):
                    flag = False
        pygame.display.flip()
#show_logo()
show_menu()
