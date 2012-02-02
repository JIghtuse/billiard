#!/usr/bin/python
# -*- encoding:utf-8 -*-
import random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import math, sys, random

import pygame, sys
import time

def to_pygame(p):
    return int(p.x), int(-p.y+600)
    
pygame.init()
screen = pygame.display.set_mode((1024, 600))
clock = pygame.time.Clock()
ballsprite = pygame.image.load("ball.png")
rballsprite = ballsprite.get_rect()
pointsprite = pygame.image.load("lulza.png")
rpointsprite = pointsprite.get_rect()

# pres                                                                          
screen.fill((54, 126, 121))                                                     
Font = pygame.font.SysFont('sans-serif', 46)                                    
label = Font.render("Child Billiard", True, (0,0,0))                            
screen.blit(label, (300,300))                                                   
label = Font.render("Ovcharenko", True, (0,0,0))                                
screen.blit(label, (400,400))                                                   
label = Font.render("Egorov", True, (0,0,0))                                    
screen.blit(label, (400,430))                                                   
label = Font.render("Kamenev", True, (0,0,0))                                   
screen.blit(label, (400,460))                                                   
flag = 1                                                                        
while flag == 1:                                                                
    for event in pygame.event.get():                                            
        if event.type == KEYDOWN:                                               
            flag = 0                                                            
Font = pygame.font.SysFont('sans-serif', 24) 

### Physics stuff
space = pm.Space()
space.gravity = (0.0, -900.0)

## Balls
balls = []
## Points
points = []
### walls
static_body = pm.Body()

#Координаты линий 
static_lines = [pm.Segment(static_body, (30.0, 30.0), (650.0, 30.0), 0.0)#Нижняя линия рамки
                ,pm.Segment(static_body, (30.0, 30.0), (30.0, 380.0), 0.0)#Левая боковая линия рамки
                ,pm.Segment(static_body, (650.0, 30.0), (650.0, 380.0), 0.0)#Правая бокавая линия рамки
                ,pm.Segment(static_body, (570.0, 30.0), (570.0, 380.0), 0.0)#Перегородка
                ]

barrier_static_lines = [
                         #Барьер №1, левый верхний угол, возле дуги
                         pm.Segment(static_body, (40,420),(43,397), 0)
                        ,pm.Segment(static_body, (43,397),(51,384), 0)
                        ,pm.Segment(static_body, (51,384),(70,372), 0)
                        ,pm.Segment(static_body, (70,372),(80,368), 0)
                        ,pm.Segment(static_body, (80,368),(30,355), 0)
						#Барьер №2, 
                        ,pm.Segment(static_body, (190,398),(260,384), 0)
                        ,pm.Segment(static_body, (190,398),(176,450), 0)
                        #Барьер №3
                        ,pm.Segment(static_body, (100,306),(220,297), 0)
						#Барьер №4
                        ,pm.Segment(static_body, (340,297),(320,273), 0)
                        ,pm.Segment(static_body, (320,273),(305,266), 0)
                        #Барьер №5
                        ,pm.Segment(static_body, (438,459),(452,321), 0)
                        #Барьер №6
                        ,pm.Segment(static_body, (570,298),(560,279), 0)
                        ,pm.Segment(static_body, (560,279),(542,260), 0)
                        ,pm.Segment(static_body, (542,260),(531,251), 0)
                        ,pm.Segment(static_body, (531,251),(523,247), 0)
                        ,pm.Segment(static_body, (523,247),(514,243), 0)
                        ,pm.Segment(static_body, (514,243),(500,239), 0)
                        ,pm.Segment(static_body, (500,239),(481,235), 0)
                        ,pm.Segment(static_body, (481,235),(570,229), 0)
                        #Барьер №7
                        ,pm.Segment(static_body, (400,190),(480,150), 0)
                        ,pm.Segment(static_body, (400,190),(346,123), 0)
                        ,pm.Segment(static_body, (385,170),(246,153), 0)
                        ,pm.Segment(static_body, (246,153),(346,123), 0)
                        ,pm.Segment(static_body, (346,123),(326,30), 0)
                        ,pm.Segment(static_body, (480,150),(448,30), 0)
                        #Барьер №8
                        ,pm.Segment(static_body, (116,108),(100,30), 0)
                        ,pm.Segment(static_body, (116,108),(157,99), 0)
                        ,pm.Segment(static_body, (157,99),(187,30), 0)
                        #Барьер #9
                        ,pm.Segment(static_body, (126,180),(140,177), 0)
                        ,pm.Segment(static_body, (140,177),(149,184), 0)
                        ,pm.Segment(static_body, (149,184),(133,201), 0)
                        ,pm.Segment(static_body, (133,201),(126,180), 0)
]

sx = [30,50,70,90,110,130,150,170,190,210,230,250,270,290,310,330,350,
        370,390,410,430,450,470,490,510,530,550,570,590,610,630,650]

sy = [380,440,470,490,505,517,528,537,544,551,556,560,564,567,570,570,
        570,568,567,564,560,556,551,544,537,526,516,505,488,471,441,380]

frame_arc = []
for i in range(len(sx) - 1):
    frame_arc.append(pm.Segment(static_body, (sx[i], sy[i]), (sx[i + 1], sy[i + 1]), 0.0))

for line in static_lines:
    line.elasticity = 0.95

for line in barrier_static_lines:
    line.elasticity = 0.95

space.add(static_lines)
space.add(barrier_static_lines)
space.add(frame_arc) #Добавляем точки рамки, от которых будет отталкиваться шарик

def add_ball(impulse):
    mass = 10
    radius = 25
    inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
    body = pm.Body(mass, inertia)
    body.position = (610, 150)
    body.apply_impulse(Vec2d.unit() * impulse, (-100, 0))
    shape = pm.Circle(body, radius, (0,0))
    shape.elasticity = 0.55
    space.add(body, shape)
    balls.append(shape)

def add_point(x, y):
    points.append((x,y))

def draw_points(points):
    for point in points:
        rpointsprite.left, rpointsprite.top = point
        rpointsprite.top *= -1
        rpointsprite.top += 600
        rpointsprite.left = rpointsprite.left - 35
        rpointsprite.top = rpointsprite.top - 35
        screen.blit(pointsprite, rpointsprite)

def del_ball(ball):
    space.remove(ball, ball.body)
    balls.remove(ball)

def change_velocity(balls):
    for ball in balls:
        abs_velo = abs(ball.body.velocity[0]) + abs(ball.body.velocity[1])
        if abs_velo <= 10.0:
            del_ball(ball)

def draw_balls(balls):
    for ball in balls:
        rballsprite.left, rballsprite.top = to_pygame(ball.body.position)
        rballsprite.left -= 12
        rballsprite.top -= 12
        rballsprite.right -= 12
        rballsprite.bottom -= 12
        screen.blit(ballsprite, rballsprite)

def del_ball(ball):
    space.remove(ball, ball.body)
    balls.remove(ball)

def draw_lines(lines_list):
    for line in lines_list:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        pygame.draw.lines(screen, THECOLORS["black"], False, [to_pygame(pv1),to_pygame(pv2)])


def print_impulse(impulse):
    impulse_data = Font.render("Last ball impulse: {0}".format(impulse), True, (0,0,0))
    screen.blit(impulse_data, (800, 100))  

def print_scores(scores):
    scores_data = Font.render("Scores: {0}".format(scores), True, (255,0,0))
    screen.blit(scores_data, (800, 200))  

def draw_power(space_pressed):
    if space_pressed > 90:
        space_pressed = 90
    for i in range(int(space_pressed)):
        pygame.draw.rect(screen, (255,0,0), (700, 570, 100, -i))

    
def play():
    add_point(70, 65)
    add_point(265, 73)
    add_point(515, 80)
    add_point(150, 260)
    add_point(150, 400)
    add_point(230, 430)
    add_point(610, 70)
    add_point(400, 340)
    add_point(500, 300)
    add_point(290, 310)
    add_point(320, 220)
    begin_time = 0
    running = True
    last_impulse = 0
    scores = 0
    space_pressed = 0
    while running:
        screen.fill(THECOLORS["white"])
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            space_pressed += 1
        else:
            space_pressed = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:                    
                begin_time = pygame.time.get_ticks()                                
            elif event.type == KEYUP and event.key == K_SPACE:                      
                impulse = pygame.time.get_ticks() - begin_time                      
                impulse *= 10
                if impulse > 20000:
                    impulse = 20000
                last_impulse = impulse
                add_ball(impulse)

        print_impulse(last_impulse)
        print_scores(scores)
        change_velocity(balls)
        draw_power(space_pressed)
        draw_points(points)
        draw_balls(balls)
        draw_lines(static_lines)
        draw_lines(barrier_static_lines)
        
        pygame.draw.arc(screen,THECOLORS["black"],[30,30, 620,400], 0, math.pi/1.95, 2)#Левая дуга
        pygame.draw.arc(screen,THECOLORS["black"],[30,30, 620,400], math.pi/2, math.pi, 2)#Правая дуга   

        dt = 1.0/60.0
        for x in range(1):
            space.step(dt)
    
        pygame.display.flip()
        clock.tick(50)

play()
