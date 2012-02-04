#!/usr/bin/python
# -*- encoding:utf-8 -*-
import random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math
import sys
import time

pygame.init()
screen = pygame.display.set_mode((1024, 600))
clock = pygame.time.Clock()
Font = pygame.font.SysFont('sans-serif', 24)
ballsprite = pygame.image.load("ball.png")
rballsprite = ballsprite.get_rect()
pointsprite = pygame.image.load("lulza.png")
rpointsprite = pointsprite.get_rect()

# ball data
ball_mass = 10
ball_radius = 25
ball_elast = 0.55
# point data
point_radius = 35

### Physics stuff
space = pm.Space()
space.gravity = (0.0, -900.0)

## Balls
balls = []
## Points
points = [
    ((610, 70), 0),                                                     
    ((100, 400), 100),                                                      
    ((230, 430), -200),                                                     
    ((150, 240), -200),                                                      
    ((260, 310), -100),                                                      
    ((390, 330), -200),                                                     
    ((320, 220), 200),                                                      
    ((500, 300), 150),                                                      
    ((70, 65), 100),                                                        
    ((265, 73), -300),                                                      
    ((515, 80), 300)
]

static_body = pm.Body()
stlines = [
        # borders
        ((30.0, 30.0), (650.0, 30.0)),    # bottom
        ((30.0, 30.0), (30.0, 380.0)),    # left
        ((650.0, 30.0), (650.0, 380.0)),  # right
        ((570.0, 30.0), (570.0, 390.0)),  # center
        # barriers
        # barrier 1
        ((40, 420), (43, 397)), ((43, 397), (51, 384)),
        ((51, 384), (70, 372)), ((70, 372), (80, 368)),
        ((80, 368), (30, 355)),
		# barrier 2
        ((190, 398), (260, 384)), ((190, 398), (176, 450)),
        ((176, 450), (154, 413)), ((154, 413), (138, 405)),
        ((138, 405), (149, 368)), ((149, 368), (260, 384)),
        # barrier 3
        ((100, 306), (220, 297)), ((220, 297), (196, 277)),
        ((196, 277), (178, 271)), ((178, 271), (100, 306)),
        # barrier 4
        ((340, 297), (320, 273)), ((320, 273), (305, 266)),
        ((305, 266), (294, 278)), ((294, 278), (305, 309)),
        ((305, 309), (340, 297)),
        # barrier 5
        ((438, 439), (452, 402)), ((438, 439), (408, 381)),
        ((408, 381), (397, 375)), ((397, 375), (420, 366)),
        ((420, 366), (437, 341)), ((437, 341), (469, 371)),
        ((469, 371), (474, 388)), ((474, 388), (452, 402)),
        # barrier 6
        ((570, 298), (560, 279)), ((560, 279), (542, 260)),
        ((542, 260), (531, 251)), ((531, 251), (523, 247)),
        ((523, 247), (514, 243)), ((514, 243), (500, 239)),
        ((500, 239), (481, 235)), ((481, 235), (570, 229)),
        # barrier 7
        ((400, 190), (480, 150)), ((400, 190), (346, 123)),
        ((385, 170), (246, 153)), ((246, 153), (346, 123)),
        ((346, 123), (326, 30)),  ((480, 150), (448, 30)),
        # barrier 8
        ((116, 108), (100, 30)), ((116, 108), (157, 99)),
        ((157, 99), (187, 30)),
        # barrier 9
        ((126, 180), (140, 177)), ((140, 177), (149, 184)),
        ((149, 184), (133, 201)), ((133, 201), (126, 180)),
        # barrier 10
        ((323, 498), (313, 473)), ((313, 473), (324, 461)),
        ((324, 461), (337, 471)), ((337, 471), (348, 489)),
        ((348, 489), (323, 498))
        ]
static_lines = []
for line in stlines:
    static_lines.append(pm.Segment(static_body, line[0], line[1], 0.0))
for line in static_lines:
    line.elasticity = 0.95
space.add(static_lines)

arc = [
        ((30, 380), (50, 440)), ((50, 440), (70, 470)),
        ((70, 470), (90, 490)), ((90, 490), (110, 505)),
        ((110, 505), (130, 517)), ((130, 517), (150, 528)),
        ((150, 528), (170, 537)), ((170, 537), (190, 544)),
        ((190, 544), (210, 551)), ((210, 551), (230, 556)),
        ((230, 556), (250, 560)), ((250, 560), (270, 564)),
        ((270, 564), (290, 567)), ((290, 567), (310, 570)),
        ((310, 570), (330, 570)), ((330, 570), (350, 570)),
        ((350, 570), (370, 568)), ((370, 568), (390, 567)),
        ((390, 567), (410, 564)), ((410, 564), (430, 560)),
        ((430, 560), (450, 556)), ((450, 556), (470, 551)),
        ((470, 551), (490, 544)), ((490, 544), (510, 537)),
        ((510, 537), (530, 526)), ((530, 526), (550, 516)),
        ((550, 516), (570, 505)), ((570, 505), (590, 488)),
        ((590, 488), (610, 471)), ((610, 471), (630, 441)),
        ((630, 441), (650, 380))
        ]
frame_arc = []
for line in arc:
    frame_arc.append(pm.Segment(static_body, line[0], line[1], 0.0))
space.add(frame_arc)

def show_logo():
    screen.fill(THECOLORS["white"])
    logosprite = pygame.image.load("logo3.png")
    screen.blit(logosprite, (137, 58, 0, 0))
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                flag = False

def to_pygame(p):
    return int(p.x), int(-p.y+600)

def add_ball(impulse):
    inertia = pm.moment_for_circle(ball_mass, 0, ball_radius, (0,0))
    body = pm.Body(ball_mass, inertia)
    body.position = (610, 150)
    body.apply_impulse(Vec2d.unit() * impulse, (-100, 0))
    shape = pm.Circle(body, ball_radius, (0,0))
    shape.elasticity = ball_elast
    space.add(body, shape)
    balls.append(shape)

def del_ball(ball):
    space.remove(ball, ball.body)
    balls.remove(ball)

def change_velocity():
    for ball in balls:
        abs_velo = abs(ball.body.velocity[0]) + abs(ball.body.velocity[1])

def draw_points():
    for point in points:
        x, y = point[0]
        y = 600 - y - point_radius
        x -= point_radius
        rpointsprite.left, rpointsprite.top = x, y

        label = Font.render("{0}".format(point[1]), True, (255,255,255)) 
        screen.blit(pointsprite, rpointsprite)
        screen.blit(label, (x + 20, y + 20))

def draw_balls():
    for ball in balls:
        rballsprite.left, rballsprite.top = to_pygame(ball.body.position)
        rballsprite.left -= ball_radius / 2
        rballsprite.top -= ball_radius / 2
        rballsprite.right -= ball_radius / 2
        rballsprite.bottom -= ball_radius / 2
        screen.blit(ballsprite, rballsprite)

def draw_lines(lines_list):
    for line in lines_list:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        pygame.draw.lines(screen, THECOLORS["black"], False, [to_pygame(pv1),to_pygame(pv2)])

def draw_power(space_pressed):
    if space_pressed > 90:
        space_pressed = 90
    for i in range(int(space_pressed)):
        pygame.draw.rect(screen, THECOLORS["red"], (700, 570, 100, -i))

def def_contact():
    if not balls:
        return 0
    for point in points:
        x, y = point[0]
        bx, by = balls[0].body.position
        length = math.sqrt((bx - x) * (bx - x) + (by - y) * (by - y))
        if length <= 60.0:
            return point
    return 0

def print_scores(scores):
    scores_data = Font.render("Scores: {0}".format(scores), True, (255,0,0))
    screen.blit(scores_data, (800, 200))  

def print_stat(scores, turns):
    scores_data = Font.render("Total scores: {0}".format(scores), True, (0,0,0))
    screen.blit(scores_data, (800, 140))  
    scores_data = Font.render("Turns: {0}".format(turns), True, (0,0,0))
    screen.blit(scores_data, (800, 160))  
    
def play():
    begin_time = 0
    running = True
    impulse = 0
    last_contact = 0
    scores = 0
    total_score = 0
    turns = 0
    space_pressed = 0
    while running:
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            space_pressed += 1
        else:
            space_pressed = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_q:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:                    
                begin_time = pygame.time.get_ticks()                                
            elif event.type == KEYUP and event.key == K_SPACE:                      
                impulse = 10 * (pygame.time.get_ticks() - begin_time) 
                if impulse > 20000:
                    impulse = 20000
                impulse + random.random() * 1000
                if balls:
                    del_ball(balls[0])
                total_score += scores
                turns += 1
                scores = 0
                add_ball(impulse)

        # count scores
        contact = def_contact()
        if last_contact == 0 and contact:
            scores += contact[1]

        # Drawing
        screen.fill(THECOLORS["white"])
        print_scores(scores)
        print_stat(total_score, turns)
        draw_power(space_pressed)
        draw_points()
        draw_balls()
        draw_lines(static_lines)
        pygame.draw.arc(screen,THECOLORS["black"],[30,30, 620,400], 0, math.pi/1.95, 2)
        pygame.draw.arc(screen,THECOLORS["black"],[30,30, 620,400], math.pi/2, math.pi, 2)
        pygame.display.flip()

        change_velocity()
        dt = 1.0/60.0
        for x in range(1):
            space.step(dt)
    
        clock.tick(50)
        last_contact = contact
    if balls:
        del_ball(balls[0])

# Markov chain
iterate = 100000
trmatrix = [
    [0,   0.2, 0.2, 0,   0.2, 0.2, 0,   0.2, 0,   0,   0], 
    [0,   0,   0,   0,   1.0, 0,   0,   0,   0,   0,   0], 
    [0,   0.1, 0.3, 0,   0.3, 0.3, 0,   0,   0,   0,   0], 
    [0,   0,   0,   0.1, 0,   0,   0.3, 0,   0.3, 0.3, 0], 
    [0,   0,   0,   0.2, 0,   0.2, 0.2, 0,   0.2, 0.2, 0], 
    [0,   0,   0,   0,   0.1, 0,   0.3, 0.3, 0,   0,   0.3], 
    [0,   0,   0,   0.1, 0,   0,   0,   0,   0.4, 0.4, 0.1], 
    [0,   0,   0,   0,   0,   0,   0.6, 0,   0,   0,   0.4], 
    [0,   0,   0,   0,   0,   0,   0,   0,   1.0, 0,   0], 
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   1.0, 0], 
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1.0]
]

s1 = [
    [0,   0.2, 0.4, 0.4, 0.6, 0.8, 0,   1.0, 0,   0,   0], 
    [0,   0,   0,   0,   1.0, 1.0, 1.0, 1.0, 0,   0,   0], 
    [0,   0.1, 0.4, 0.4, 0.7, 1.0, 0,   0,   0,   0,   0], 
    [0,   0,   0,   0.1, 0.1, 0.1, 0.4, 0.4, 0.7, 1.0, 1.0], 
    [0,   0,   0,   0.2, 0.2, 0.4, 0.6, 0.6, 0.8, 1.0, 0], 
    [0,   0,   0,   0,   0.1, 0.1, 0.4, 0.7, 0.7, 0.7, 1.0], 
    [0,   0,   0,   0.1, 0.1, 0.1, 0.1, 0.1, 0.5, 0.9, 1.0], 
    [0,   0,   0,   0,   0,   0,   0.6, 0.6, 0.6, 0.6, 1.0], 
    [0,   0,   0,   0,   0,   0,   0,   0,   1.0, 1.0, 1.0], 
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   1.0, 1.0], 
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1.0] 
]

def return_state(slist, rndm):
    for i in range(11):
        if slist[i] >= rndm:
            return i

def draw_in_state(state, score):
    screen.fill(THECOLORS["white"])
    draw_points()
    draw_lines(static_lines)
    pygame.draw.arc(screen,THECOLORS["black"],[30,30, 620,400], 0, math.pi/1.95, 2)
    pygame.draw.arc(screen,THECOLORS["black"],[30,30, 620,400], math.pi/2, math.pi, 2)
    x, y = points[state][0]
    y = 600 - y
    rballsprite.left, rballsprite.top = x, y
    rballsprite.left -= ball_radius
    rballsprite.top -= ball_radius
    screen.blit(ballsprite, rballsprite)
    print_scores(score)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                running = False
    
def step(test, total_score, turns):
    state = 0
    score = 0
    run = 1
    last_state = state
    llast_state = state
    while (run):
        state = return_state(s1[state], random.random())
        score += points[state][1]
        if not test:
            draw_in_state(state, score)
            print_stat(total_score, turns)
            pygame.display.flip()
        if llast_state == last_state and last_state == state:
            run = 0
        llast_state = last_state
        last_state = state
    return score

def mark(iterate):
    total_score = 0
    turns = 0
    draw_in_state(0, 0)
    print_stat(0, 0)
    pygame.display.flip()
    for i in range(iterate):
        total_score += step(False, total_score, turns)
        turns += 1
    print("Total score: {0}; turns: {1}".format(total_score, turns))

def markov():
    totalscore = 0.0
    sq = 0.0
    for i in range(iterate):
        tmp = step(True, totalscore, sq)
        totalscore += tmp
        sq += tmp * tmp
    average = totalscore / iterate
    variance = sq / iterate - average * average
    print("Total score: {0}".format(totalscore))
    print("Average: {0}".format(totalscore / iterate))
    print("Variance: {0}".format(variance))
