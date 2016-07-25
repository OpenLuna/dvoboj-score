# -*- coding: utf-8 -*-
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass


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

        self.screen = pygame.display.set_mode((320, 200))
        self.screen.fill((0,0,0))
        pygame.display.update()
         
        self.font_big = pygame.font.Font(os.path.join('assets', 'OpenSans-ExtraBold.ttf'), 50)
        #self.font_big = pygame.font.Font(None , 64)
        self.value=""
        self.v=(160,160)

        #screen = self.toggle_fullscreen()
        self.text_surface = self.font_big.render('%s'%self.value, True, self.WHITE)
        self.rect = self.text_surface.get_rect(center=self.v)
        self.screen.blit(self.text_surface, self.rect)

        self.goldcrown = pygame.image.load(os.path.join('assets', 'gold.png'))
        self.goldcrown = pygame.transform.scale(self.goldcrown, (100, 100))
        self.silvercrown = pygame.image.load(os.path.join('assets', 'silver.png'))
        self.silvercrown = pygame.transform.scale(self.silvercrown, (100, 100))
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
        rect = self.text_surface.get_rect(center=self.v)
        self.screen.fill((0,0,0))
        self.screen.blit(self.text_surface, rect)
        if points["winner"]==self.person:
            self.screen.blit(self.goldcrown, (160-50,30))
        else:
            self.screen.blit(self.silvercrown, (160-50,30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        pygame.display.update()
        return True


# call main
if __name__ == '__main__':
    score = Score("sin")
    while True:
        sleep(5)
        score.update()
