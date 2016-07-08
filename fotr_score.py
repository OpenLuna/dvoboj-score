# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
from time import sleep
import requests
import json
#Colours
class Score():
    def __init__(self, person):
        self.WHITE = (255,255,255)
        self.person = person
        pygame.init()

        self.screen = pygame.display.set_mode((800, 480))
        self.screen.fill((0,0,0))
        pygame.display.update()         
        self.font_big = pygame.font.Font(os.path.join('assets', 'OpenSans-ExtraBold.ttf'), 140)
        #self.font_big = pygame.font.Font(None , 64)
        self.value=""
        self.v=(400,120)

        screen = self.toggle_fullscreen()
        self.text_surface = self.font_big.render('%s'%self.value, True, self.WHITE)
        self.text_surface = pygame.transform.rotate(self.text_surface, 180)
	self.rect = self.text_surface.get_rect(center=self.v)
        self.screen.blit(self.text_surface, self.rect)

        self.goldcrown = pygame.image.load(os.path.join('assets', 'gold.png'))
        self.goldcrown = pygame.transform.scale(self.goldcrown, (200, 200))
        self.silvercrown = pygame.image.load(os.path.join('assets', 'silver.png'))
        self.silvercrown = pygame.transform.scale(self.silvercrown, (200, 200))
        self.goldcrown = pygame.transform.rotate(self.goldcrown, 180)
	self.silvercrown = pygame.transform.rotate(self.silvercrown, 180)
	pygame.mouse.set_visible(False)
        pygame.display.update()

        self.update()
            

    def toggle_fullscreen(self):
        self.screen = pygame.display.get_surface()
        tmp = self.screen.convert()
        caption = pygame.display.get_caption()
        #cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
        
        w,h = self.screen.get_width(),self.screen.get_height()
        flags = self.screen.get_flags()
        bits = self.screen.get_bitsize()
        
        pygame.display.quit()
        pygame.display.init()
        
        self.screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
        self.screen.blit(tmp,(0,0))
        pygame.display.set_caption(*caption)
     
        pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
     
        #pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007

    def update(self):
        try:
            
            points = json.loads(requests.get("http://dvoboj.si/api/getPoints/").text)
            self.value=points[self.person]
            print "update points"
        except:
            print "request fail"
            return True
        self.text_surface = self.font_big.render('%s'%self.value, True, self.WHITE)
	self.text_surface = pygame.transform.rotate(self.text_surface, 180)
        rect = self.text_surface.get_rect(center=self.v)
        self.screen.fill((0,0,0))
        self.screen.blit(self.text_surface, rect)
        if points["winner"]==self.person:
            self.screen.blit(self.goldcrown, (300,230))
        else:
            self.screen.blit(self.silvercrown, (300,230))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
	pygame.display.flip()
        #pygame.display.update()
        return True


# call main
if __name__ == '__main__':
    score = Score("sin")
    while True:
        sleep(5)
        score.update()
