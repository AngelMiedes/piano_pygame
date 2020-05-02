#Necesario para las teclas presionadas
from pygame.locals import *
#Import del paquete
import pygame
import sys

#se inicializa
pygame.init()

ventana = pygame.display.set_mode((700,400))


notas = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
octavas = ['1', '2', '3', '4', '5', '6', '7']
    

i=0
j=0

#Bucle de "Juego"
while True:
    ''' Documentación relacionado con los eventos:
        https://www.pygame.org/docs/ref/event.html
    '''
    #Obtenemos todos los eventos que ocurren en este momento
    for event in pygame.event.get():
        '''
            Hasta aqui todo era exactamente igual que en el ejemplo anterior.

            En este ejemplo vamos a hacer que se modifique el color de fondo
            cuando se pulsen algunas teclas en concreto.
        '''
        #Cuando el evento es presionar una tecla...
        if event.type == pygame.KEYDOWN:
            #Obtenemos el mapping de teclas presionadas
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                #Rellenamos la ventana con un color de Pygame
                ventana.fill(pygame.Color(255, 255, 255, 255))
                print (i,j)
                print(notas[i],octavas[j])
                pygame.mixer.music.load('sounds/' + str(notas[i]) + str(octavas[j]) + '.mp3')
                pygame.mixer.music.play(0)
                
                
                if i >= len(notas)-1:
                    i = 0
                    j += 1
                else:
                    i += 1
                
                if j > len(octavas)-1: j = 0
                
            
              
            

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
               print(event)

    pygame.display.flip()



