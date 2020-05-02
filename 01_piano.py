#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *

 
# Constantes

WIDTH_IMAGE_OCT = 250
HEIGHT_IMAGE_OCT = 200
WIDTH = WIDTH_IMAGE_OCT * 7 + 20
HEIGHT = 480
notas = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
octavas = ['1', '2', '3', '4', '5', '6', '7']
 
# Clases
# ---------------------------------------------------------------------
 
# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------
 
def load_image(filename, transparent=False):
        try: 
            image = pygame.image.load(filename)
        except pygame.error:
            raise SystemExit
        image = image.convert()
        
        if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
        return image
 
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Piano")
    
    images_octavas_rect = []
    images_notas1_rect = []
    
    image = load_image('images/octava_piano.png')
    octava_image = pygame.transform.scale(image,(WIDTH_IMAGE_OCT,HEIGHT_IMAGE_OCT))
    
    #kk = pygame.Rect(0,0,10,10)

    
    for i in range(len(octavas)):
        images_octavas_rect.append(octava_image.get_rect())
        images_octavas_rect[i].topleft = (10 + WIDTH_IMAGE_OCT * i, 10)#screen.get_rect().centerx
        #octava_image_rect.centery = HEIGHT/3
        screen.blit(octava_image, images_octavas_rect[i])
        
        for j in range (7):
            Rect_nota = pygame.Rect(images_octavas_rect[i].left + j * images_octavas_rect[i].w // 7, images_octavas_rect[i].top,
                                                  images_octavas_rect[i].w // 7 , images_octavas_rect[i].h)
            images_notas1_rect.append(Rect_nota)
            print(Rect_nota.topleft)
        print()
    print(WIDTH)
        
    '''print (f'top: {octava_image_rect.top}')
    print (f'left: {octava_image_rect.left}')
    print (f'bottom: {octava_image_rect.bottom}')
    print (f'right: {octava_image_rect.right}')
    print (f'topleft: {octava_image_rect.topleft}')
    print (f'bottomleft: {octava_image_rect.bottomleft}')
    print (f'topright: {octava_image_rect.topright}')
    print (f'bottomright: {octava_image_rect.bottomright}')
    print (f'midleft: {octava_image_rect.midleft}')
    print (f'midbottom: {octava_image_rect.midbottom}')
    print (f'midright: {octava_image_rect.midright}')
    print (f'center: {octava_image_rect.center}')
    print (f'centerx: {octava_image_rect.centerx}')
    print (f'centery: {octava_image_rect.centery}')
    print (f'size: {octava_image_rect.size}')
    print (f'width: {octava_image_rect.width}')
    print (f'height: {octava_image_rect.height}')
    print (f'w: {octava_image_rect.w}')
    print (f'h: {octava_image_rect.h}')'''

    
 
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
                
            if eventos.type == pygame.MOUSEBUTTONDOWN:
                
                for nota in images_notas1_rect:
                    if nota.collidepoint(pygame.mouse.get_pos()):
                       print('clicked on: ', nota.topleft)     
                    
 
        #screen.blit(background_image, (0, 0))
        pygame.display.flip()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()