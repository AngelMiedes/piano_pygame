#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame, os
from pygame.locals import *
import random

 
# Constantes

WIDTH_IMAGE_NOTA = 32
HEIGHT_IMAGE_NOTA = 200
WIDTH_IMAGE_NOTAb = 22
HEIGHT_IMAGE_NOTAb = 133
WIDTH = 1500
HEIGHT = 900
COLOR_FONDO = pygame.Color(200, 200, 200, 255)
listNotas = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
listOctavas = ('1', '2', '3', '4', '5', '6', '7')
 
# Clases
# ---------------------------------------------------------------------
class Tecla():
    def __init__(self, nota = 'C', octava = 1):
        ''' Creamos la tecla a partir de la nota y la octava'''
        self.nota = nota
        self.octava = octava

    def __eq__(self, otra_tecla):

         return self.nota == otra_tecla.nota and self.octava == otra_tecla.octava

    def setNota (self, nota):
        ''' Devolvemos la nota de la tecla'''
        self.nota = nota
        

    def setOctava (self, octava):
        ''' Devolvemos la octava de la tecla'''
        self.octava = octava
        
    
    def setRect(self, rect):
        ''' Creamos el rectangulo que contine a la tecla'''
        self.rect = rect


    def is_bemol(self):
        ''' Comprobamos si la tecla es bemol'''
        return True if self.nota.find('b') != -1 else False


    def get_sound(self):
        ''' Devolvemos la ruta del sonido de la nota'''
        return 'sounds' + os.sep + str(self.nota) + str(self.octava) + '.mp3'


    def get_image_nota(self):
        ''' Devolvemos la ruta de la imagen en el pentagrama de la nota'''
        return 'images' + os.sep + str(self.nota) + str(self.octava) + '.png'
           
        
class Teclado():

    def __init__(self, octavas = 7, x = 0, y = 0):
        '''Crea un teclado con el número de octavas indicado, en la posición izquierda (x) y arriba (y)'''
        self.octavas = octavas
        self.x = x
        self.y = y
        self.teclas = []
        

    def construir(self, screen):
        ''' Creamos la lista de teclas del teclado, las representamos en pantalla'''
        imageNota = load_image('images' + os.sep + 'tecla.png')
        imageNotaScale = pygame.transform.scale(imageNota,(WIDTH_IMAGE_NOTA,HEIGHT_IMAGE_NOTA))
        imageNotab = load_image('images' + os.sep + 'tecla_b.png')
        imageNotaScaleb = pygame.transform.scale(imageNotab,(WIDTH_IMAGE_NOTAb,HEIGHT_IMAGE_NOTAb))

        pos_x = self.x
        # Creamos los rectangulos contenedores de las teclas y sus posiciones relativas
        for oct in range(self.octavas):
            for n in listNotas:
                
                tecla = Tecla(n,oct+1)
                if not tecla.is_bemol():
                    tecla.setRect(imageNotaScale.get_rect()) 
                    tecla.rect.topleft = (pos_x, self.y)
                    pos_x += WIDTH_IMAGE_NOTA
                else:
                    tecla.setRect(imageNotaScaleb.get_rect()) 
                    # desplazamos ligeramente a la izquierda la nota Gb
                    if tecla.nota == 'Gb':
                        tecla.rect.midtop = (pos_x - 5, self.y)
                        # desplazamos ligeramente a la derecha no nota Bb
                    elif tecla.nota == 'Bb':
                        tecla.rect.midtop = (pos_x + 5, self.y)
                    else:
                        tecla.rect.midtop = (pos_x, self.y)
                    
                self.teclas.append(tecla)
        #dibujamos primero las teclas blancas
        for t in self.teclas:
            if not t.is_bemol():
                screen.blit(imageNotaScale, t.rect)
                # Dibujamos un punto para delimitar la tecla central
                if t.octava == 4 and t.nota == 'C':
                        pygame.draw.circle(screen, pygame.Color(128, 128, 128, 8), (t.rect.centerx, t.rect.bottom - 10), 5, 5)
        #dibujamos las teclas negras
        for t in self.teclas:
            if t.is_bemol():
                screen.blit(imageNotaScaleb, t.rect)
    

    def tecla_pulsada(self, posicion):
        ''' Devolvemos la tecla que ha sido pulsada'''
        tecla_pul_b = None
        tecla_pul = None
        contador = 0
        for t in self.teclas:
            # Si hemos pulsado en el rectangulo de alguna de las teclas
            if t.rect.collidepoint(posicion):
                # Puesto que los rectangolos de las teclas normales se solapan con el de las tecla bemol
                # si pulsamos sobre una tecla bemol, se reconoce la tecla bemol y la que hay detrás
                if t.is_bemol():
                    tecla_pul_b = t
                    break
                else:
                    tecla_pul = t
                contador += 1
                if contador >= 2:
                    break
        # Si hemos creado la instacia de la tecla normal y no hay instancia de la nota bemol --> se ha pulsado tecla normal
        if tecla_pul and not tecla_pul_b:
            return tecla_pul
        # Si hemos creado la instacia de la tecla bemol --> se ha pulsado tecla bemol
        elif tecla_pul_b:
            return tecla_pul_b
            
        
    def play_tecla(self, posicion):
        ''' Hacemos sonar la nota, según la tecla que ha sido pulsada'''
        pygame.mixer.music.load(self.tecla_pulsada(posicion).get_sound())
        # suena una sola vez (0)
        pygame.mixer.music.play(0)


    def mostrar_nota(self, screen, tecla, x, y):
        ''' Mostramos en pantalla la nota dentro del pentagrama'''
        # Creamos al imagen (con fondo transparente), a partir de la nota en el pentagrama que nos da la posición del ratón
        imageNota = pygame.image.load(tecla.get_image_nota()).convert_alpha()
        # Escalamos la imangen de la nota en el pentagrama
        #imageNotaScale = pygame.transform.scale(imageNota,(147,567))
        # Creamos un rectangulo de iguales dimensiones que al imagen escadala
        rect_filled = pygame.Surface(imageNota.get_size())
        # Configuramos la visualización del rectangulo con el color del fondo
        pygame.draw.rect(rect_filled, COLOR_FONDO, rect_filled.get_rect())
        # pintamos el rectangulo (BORRAR DE LA PANTALLA LA IMAGEN ANTERIOR)
        screen.blit(rect_filled, (x, y)) 
        # Pintamos la imagen de la nueva nota
        screen.blit(imageNota, (x, y))

 
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
            image.set_colorkey(color) #, RLEACCEL
        return image


def texto(screen, texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font('images/DroidSans.ttf', 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.x = posx
    salida_rect.y = posy
    screen.blit(salida, salida_rect)
    #return salida, salida_rect

def borrar_texto(screen, posx, posy, color=(255, 255, 255)):
    rect_filled = pygame.Surface((500, 25))
    pygame.draw.rect(rect_filled, color, rect_filled.get_rect()) 
    screen.blit(rect_filled, (posx, posy))
 
# ---------------------------------------------------------------------
 
def main():
    
    # Creamos teclado
    teclado = Teclado(7,10,10)
    # Creamos la pantalla del programa cuyo tamaño depende del número de octavas del teclado
    screen = pygame.display.set_mode((teclado.octavas * WIDTH_IMAGE_NOTA * 7 + teclado.x * 2, HEIGHT))
    screen.fill(COLOR_FONDO)
    pygame.display.set_caption("Pygame Piano")
    # Construimos y dibujamos el teclado en la pantalla
    teclado.construir(screen)
    tecla_random = Tecla(random.choice(listNotas), int(random.choice(listOctavas)))
    teclado.mostrar_nota(screen, tecla_random, 10, HEIGHT_IMAGE_NOTA + teclado.x)
    puntuacion = 0
    
    
    while True:
        # Espera eventos
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
            # Evento pulsación del ratón    
            if eventos.type == pygame.MOUSEBUTTONDOWN:
                
                try:
                    # Hacemos sonar la tecla pulsada según la posición del ratón
                    teclado.play_tecla(pygame.mouse.get_pos())
                    # Mostramos la nota en el pentagrama asociada a la tecla pulsada
                    #teclado.mostrar_nota(screen, teclado.tecla_pulsada(pygame.mouse.get_pos()), (teclado.octavas * WIDTH_IMAGE_NOTA * 7 + teclado.x) // 2,
                    #                    HEIGHT_IMAGE_NOTA + teclado.x)
                    if tecla_random == teclado.tecla_pulsada(pygame.mouse.get_pos()):
                        puntuacion += abs(teclado.tecla_pulsada(pygame.mouse.get_pos()).octava - 4) + 1
                        borrar_texto(screen, 10, HEIGHT - 40, color=(0, 255, 0))
                        texto(screen, f'Acierto!!!!!     Puntuación: {puntuacion}', 10, HEIGHT - 40, color=(0, 0, 0))
                        tecla_random = Tecla(random.choice(listNotas), int(random.choice(listOctavas)))
                        teclado.mostrar_nota(screen, tecla_random, 10, HEIGHT_IMAGE_NOTA + teclado.x)
                        
                    else:
                        puntuacion -= 1
                        borrar_texto(screen, 10, HEIGHT - 40, color=(255, 0, 0))
                        texto(screen, f'Error!!!!!     Puntuación: {puntuacion}', 10, HEIGHT - 40, color=(0, 0, 0))
                        

                except AttributeError:
                
                    pass
            
      
        pygame.display.flip()
    # finaliza Pygame
    pygame.quit()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()