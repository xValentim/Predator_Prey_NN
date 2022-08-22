import random
import numpy as np
import pygame
import sys


altura = 500
largura = 500
gray = (50, 50, 50)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
background = white
ball_color = gray
fps = 60

'''
0 - empty
1 - predator
2 - prey
'''
types = [0, 1, 2]
color = [gray, red, white]
if len(sys.argv) != 4:
    print("Error Usage. You must type this form: python predator_prey.py a b c")
else:
    a, b, c = sys.argv[1], sys. argv[2], sys.argv[3]
    t = 0
    particules = [[random.choice(types) for i in range(0, largura, 5)] for j in range(0, altura, 5)]
    print(len(particules))
    pygame.init()
    relogio = pygame.time.Clock()
    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Predator Prey")
    window.fill(gray)
    continua = True
    while continua:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continua = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continua = False


        
        window.fill(background)

        for i in range(1, len(particules) - 1):
            for j in range(1, len(particules[i]) - 1):
                particule = particules[i][j]
                adress = [(i, (j + 1) % largura), (i, (j - 1) % largura), ((i - 1) % altura, j), ((i + 1) % altura, j)]
                right, left, up, down = particules[adress[0][0]][adress[0][1]], particules[adress[1][0]][adress[1][1]], particules[adress[2][0]][adress[2][1]], particules[adress[3][0]][adress[3][1]]
                neighboor = [right, left, up, down]
                
                if particule == 1:
                    for k in range(4):
                        ng_index = adress[k]
                        ng = particules[ng_index[0]][ng_index[1]]
                        if ng == 2:
                            z = random.random()
                            if z < float(b):
                                particules[ng_index[0]][ng_index[1]] = 1
                    z = random.random()
                    if z < float(c):
                        particules[i][j] = 0
                elif particule == 2:
                    for k in range(4):
                        ng_index = adress[k]
                        ng = particules[ng_index[0]][ng_index[1]]
                        if ng == 0:
                            z = random.random()
                            if z < float(a):
                                particules[ng_index[0]][ng_index[1]] = 2
                    
                    


                pygame.draw.rect(window, color[particules[i][j]], (i * 5 + 1, j * 5 + 1, 5, 5))

        t += 1
        relogio.tick(fps)
        pygame.display.update()
    pygame.quit()
