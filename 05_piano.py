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
WIDTH = 1600 
HEIGHT = 900
TIEMPO_FALLO = 10000 # ms
COLOR_FONDO = pygame.Color(200, 200, 200, 255)
listNotas = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
listOctavas = (1, 2, 3, 4, 5, 6, 7)
 
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
        if self.is_bemol():
            ran = random.choice(['', 's'])
            dir = 'images' + os.sep + str(self.nota) + str(self.octava) + ran + '.png'
        else:
            dir = 'images' + os.sep + str(self.nota) + str(self.octava) + '.png'

        return dir
           
        
class Teclado():

    def __init__(self, octavas, x = 0, y = 0):
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
        for oct in listOctavas:
            for n in listNotas:
                
                tecla = Tecla(n,oct)
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

                if oct in self.octavas:    
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


def texto(screen, texto, posx, posy, color=(255, 255, 255), color_fondo=COLOR_FONDO):
    
    fuente = pygame.font.Font('images/DroidSans.ttf', 20)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.x = posx
    salida_rect.y = posy
    rect_filled = pygame.Surface((salida_rect.w,salida_rect.h))
    pygame.draw.rect(rect_filled, color_fondo, rect_filled.get_rect()) 
    screen.blit(rect_filled, (posx, posy))
    screen.blit(salida, salida_rect)

def borrar_barra_info(screen, posx, posy, width, height, color=COLOR_FONDO):
    rect_filled = pygame.Surface((width, height))
    pygame.draw.rect(rect_filled, color, rect_filled.get_rect()) 
    screen.blit(rect_filled, (posx, posy))

def actualiza_info(screen, mensaje, puntuacion, posx = 10, posy = HEIGHT - 40, width = WIDTH, height= 40, color_text=(0, 0, 0), color_ftext=COLOR_FONDO):
    borrar_barra_info(screen, posx, posy, width, height, color=COLOR_FONDO)
    texto(screen, mensaje, posx, posy, color_text, color_ftext)
    texto(screen, f'Puntuación: {puntuacion}', posx + 1400, posy, color_text, COLOR_FONDO)

 
# ---------------------------------------------------------------------
 
def main():
    
    # Creamos teclado
    octavas = [4]
    teclado = Teclado(octavas,10,10)
    # Creamos la pantalla del programa cuyo tamaño depende del número de octavas del teclado
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(COLOR_FONDO)
    pygame.display.set_caption("Pygame Piano")
    # Construimos y dibujamos el teclado en la pantalla
    
    puntuacion = 0
    construir0, construir1, construir2, construir3 = False, False, False, False
    cont_time_fallo = 0
    time_msg = 0
    clock = pygame.time.Clock()

    # Construimos el teclado con solo una octava, según la puntuación iremos sumbiendo el nº, mostramos la nota a adivinar
    teclado = Teclado([4],10,10)
    screen.fill(COLOR_FONDO)
    teclado.construir(screen)
    tecla_random = Tecla(random.choice(listNotas), int(random.choice(teclado.octavas)))
    teclado.mostrar_nota(screen, tecla_random, 10, HEIGHT_IMAGE_NOTA + teclado.x)
    construir0 = True
    
    while True:
        # Construimos el teclado con 3 octavas
        if puntuacion >= 10 and  not construir1:
            del(teclado)
            teclado = Teclado([3,4,5],10,10)
            screen.fill(COLOR_FONDO)
            teclado.construir(screen)
            tecla_random = Tecla(random.choice(listNotas), int(random.choice(teclado.octavas)))
            teclado.mostrar_nota(screen, tecla_random, 10, HEIGHT_IMAGE_NOTA + teclado.x)
            if construir0:
                actualiza_info(screen,'Bravo, subes de nivel!!!', puntuacion, color_ftext=(0, 255, 0)) 
            construir1 = True
        # Construimos el teclado con 5 octavas
        if puntuacion >= 50  and  not construir2:
            del(teclado)
            teclado = Teclado([2,3,4,5,6],10,10)
            screen.fill(COLOR_FONDO)
            teclado.construir(screen)
            tecla_random = Tecla(random.choice(listNotas), int(random.choice(teclado.octavas)))
            teclado.mostrar_nota(screen, tecla_random, 10, HEIGHT_IMAGE_NOTA + teclado.x)
            if construir1:
                actualiza_info(screen,'Bravo, subes de nivel!!!', puntuacion, color_ftext=(0, 255, 0)) 
            construir2 = True
        # Construimos el teclado con 7 octavas
        if puntuacion >= 100 and  not construir3:
            del(teclado)
            teclado = Teclado([1,2,3,4,5,6,7],10,10)
            screen.fill(COLOR_FONDO)
            teclado.construir(screen)
            tecla_random = Tecla(random.choice(listNotas), int(random.choice(teclado.octavas)))
            teclado.mostrar_nota(screen, tecla_random, 10, HEIGHT_IMAGE_NOTA + teclado.x)
            if construir2:
                actualiza_info(screen,'Bravo, subes de nivel!!!', puntuacion, color_ftext=(0, 255, 0))
            construir3 = True
        
        
        dt = clock.tick_busy_loop(20)
        cont_time_fallo += dt
        time_msg += dt
        
        if cont_time_fallo >= TIEMPO_FALLO:
            puntuacion -= 1
            actualiza_info(screen,f' Han Pasado {TIEMPO_FALLO // 1000} seg. Un punto negativo!!!', puntuacion, color_ftext=(255, 0, 0)) 
            cont_time_fallo = 0
            time_msg = 0
        if time_msg >= 3000:
            time_msg = 0
            actualiza_info(screen,'', puntuacion, color_ftext= COLOR_FONDO)

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
                    #teclado.mostrar_nota(screen, teclado.tecla_pulsada(pygame.mouse.get_pos()), (WIDTH + teclado.x) // 2, HEIGHT_IMAGE_NOTA + teclado.x)
                    if tecla_random == teclado.tecla_pulsada(pygame.mouse.get_pos()):
                        addPunt = abs(tecla_random.octava - 4) + 1
                        puntuacion += addPunt
                        actualiza_info(screen, f' Enhorabuena. {addPunt} puntos más!!!!!', puntuacion, color_ftext=(0, 255, 0)) 
                        time_msg = 0
                        cont_time_fallo = 0
                        tecla_random = Tecla(random.choice(listNotas), int(random.choice(teclado.octavas)))
                        teclado.mostrar_nota(screen, tecla_random, 10, HEIGHT_IMAGE_NOTA + teclado.x)
                        
                    else:
                        puntuacion -= 1
                        actualiza_info(screen,' Error. Un punto negativo!!!!!', puntuacion, color_ftext=(255, 0, 0)) 
                        time_msg = 0
                        

                except AttributeError:
                
                    pass
            
      
        pygame.display.flip()
    # finaliza Pygame
    pygame.quit()
    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()