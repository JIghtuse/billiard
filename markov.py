#!/usr/bin/python

from random import *
import pygame

states = [
        (70, 100),
        (160, 300),
        (95, 215),
        (50, 310),
        (5, 420),
        (95, 420),
        (190, 420),
        #(100, 100),
        #(100, 100),
        #(100, 100)
        ]

def return_state(s1, state):
    for string in s1:
        for elem in string:
            if elem >= state:
                return string.index(elem)

def rand_gen(state):
    return random() * 10

def markov():
    trmatrix = [
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] 
        ]

    s1 = [
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
         ]

    state = 0
    for i in range(100):
        for j in range(5):
            state = return_state(s1, random())
            print("{0}: {1}".format(j, state))

def print_states(screen):
    font = pygame.font.SysFont('sans-serif', 46)
    for st in states:
        state = font.render("state", True, (0,0,0))
        screen.blit(state, st)


def form():
    pygame.init()
    pygame.display.set_caption("Billiard")
    screen = pygame.display.set_mode((640, 480))
    ball = pygame.image.load("bal1.png")
    glass = pygame.image.load("Untitled.png")
    screen.fill((125, 255, 125))
    screen.blit(glass, (0, 0))
    screen.blit(ball, (285, 430))
    imw, imh = 256, 256
    
    print_states(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

form()
