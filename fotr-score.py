# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
from time import sleep
import requests
#Colours
 
def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)
 
    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
 
    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
    return screen

WHITE = (255,255,255)
 
pygame.init()

screen = pygame.display.set_mode((320, 240))
screen.fill((0,0,0))
pygame.display.update()
 
font_big = pygame.font.Font("/usr/share/fonts/OpenSans-ExtraBold.ttf", 50)
value=""
v=(160,120)

screen = toggle_fullscreen()
text_surface = font_big.render('%s'%value, True, WHITE)
rect = text_surface.get_rect(center=v)
screen.blit(text_surface, rect)
 
pygame.display.update()

while True:
	print "loop"
	try:
		value = requests.get("http://dvoboj.si/api/getOcesPoints/").text
	except:
		print "request fail"
	print value
	text_surface = font_big.render('Fotr:   %s'%value, True, WHITE)
	rect = text_surface.get_rect(center=v)
	screen.fill((0,0,0))
	screen.blit(text_surface, rect)
	pygame.display.update()
	sleep(5)
