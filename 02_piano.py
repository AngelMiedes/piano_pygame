#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *

 
# Constantes

WIDTH_IMAGE_NOTA = 32
HEIGHT_IMAGE_NOTA = 200
WIDTH_IMAGE_NOTAb = 22
HEIGHT_IMAGE_NOTAb = 133
WIDTH = 1500
HEIGHT = 480
listNotas = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
listOctavas = ('1', '2', '3', '4', '5', '6', '7')
 
# Clases
# ---------------------------------------------------------------------
class Tecla():
    def __init__(self, nota = 'C', octava = 1):
        self.nota = nota
        self.octava = octava
        self.sonido = 'sounds/' + self.nota + str(self.octava) + '.mp3'


    def setNota (self, nota):
        self.nota = nota
        

    def setOctava (self, octava):
        self.octava = octava
        
    
    def setRect(self, rect):
        self.rect = rect


    def is_bemol(self):
        return True if self.nota.find('b') != -1 else False
        
        
class Teclado():

    def __init__(self, octavas = 7, x = 0, y = 0):
        self.octavas = octavas
        self.x = x
        self.y = y
        self.teclas = []
        

    def construir(self, screen):
        imageNota = load_image('images/tecla.png')
        imageNotaScale = pygame.transform.scale(imageNota,(WIDTH_IMAGE_NOTA,HEIGHT_IMAGE_NOTA))
        imageNotab = load_image('images/tecla_b.png')
        imageNotaScaleb = pygame.transform.scale(imageNotab,(WIDTH_IMAGE_NOTAb,HEIGHT_IMAGE_NOTAb))

        pos_x = self.x
        
        for oct in range(self.octavas):
            
            for n in listNotas:
                
                tecla = Tecla(n,oct+1)
                
                if not tecla.is_bemol():
                    tecla.setRect(imageNotaScale.get_rect()) 
                    tecla.rect.topleft = (pos_x, self.y)
                    
                    pos_x += WIDTH_IMAGE_NOTA
                else:
                    tecla.setRect(imageNotaScaleb.get_rect()) 
                    tecla.rect.midtop = (pos_x, self.y)
                    
                self.teclas.append(tecla)
        #dibujamos primero las teclas blancas
        for t in self.teclas:
            if not t.is_bemol():
                screen.blit(imageNotaScale, t.rect)
        #dibujamos las teclas negras
        for t in self.teclas:
            if t.is_bemol():
                screen.blit(imageNotaScaleb, t.rect)
 
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
    
    
    teclado = Teclado(5,10,10)
    screen = pygame.display.set_mode((teclado.octavas * WIDTH_IMAGE_NOTA * 7 + teclado.x * 2, HEIGHT))
    pygame.display.set_caption("Pygame Piano")

    teclado.construir(screen)
      
 
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
                
            if eventos.type == pygame.MOUSEBUTTONDOWN:
                tecla_pul_b = None
                tecla_pul = None
                for t in teclado.teclas:
                    if t.rect.collidepoint(pygame.mouse.get_pos()):
                        if t.is_bemol():
                            tecla_pul_b = t
                        else:
                            tecla_pul = t
                # Las teclas normales se solapan en la imagen con las teclas bemol
                if tecla_pul and not tecla_pul_b:
                    pygame.mixer.music.load('sounds/' + str(tecla_pul.nota) + str(tecla_pul.octava) + '.mp3')
                    pygame.mixer.music.play(0)
                    del(tecla_pul)
                if tecla_pul_b:
                    pygame.mixer.music.load('sounds/' + str(tecla_pul_b.nota) + str(tecla_pul_b.octava) + '.mp3')
                    pygame.mixer.music.play(0)
                    del(tecla_pul_b)
                     
                    
 
        #screen.blit(background_image, (0, 0))
        pygame.display.flip()
    # finaliza Pygame
    pygame.quit()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()