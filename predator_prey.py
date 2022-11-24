from multiprocessing import allow_connection_pickling
import random
import numpy as np
import pygame
import sys
from policy_predator import *
import time

altura = 500
largura = 500
gray = (50, 50, 50)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
background = white
ball_color = gray
fps = 50
L_sq = 5

'''
0 - empty
1 - predator
2 - prey
'''

'''
To run this code, you must type this form: python predator_prey.py a b c

a = prey birth rate
b = predator birth rate
c = predator death rate
p = jump probability


This code is a predator prey model with a predator that uses a policy to move.

The prey is born in a random position and the predator is born in the center of the grid.

In this context, we initialize just one predator in the center of the grid. 

If you want to see example of simulation that predator to hunt multiples prey and validate the policy, just set: 
a = 0
b = 1
c = 0
p = 1

In other other words, type in terminal:

$ python predator_prey.py 0 1 0 1

'''


types = [0, 0, 2]
color = [gray, red, white]
model = Policy(load=True, pos=(0, 0))

if len(sys.argv) != 5:
    print("Error Usage. You must type this form: python predator_prey.py a b c")
else:
    a, b, c, p = sys.argv[1], sys. argv[2], sys.argv[3], sys.argv[4]
    t = 0
    particules = np.array([[random.choice(types) for i in range(0, largura, L_sq)] for j in range(0, altura, L_sq)])
    print(len(particules))
    L = len(particules)
    for k in range(1):
        # i, j = random.randint(0, len(particules) - 1), random.randint(0, len(particules) - 1)
        i, j = L // 2, L // 2
        model.pos = (i, j)
        particules[i][j] = 1
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
        # i, j = random.randint(0, len(particules) - 1), random.randint(0, len(particules) - 1)
        i, j = model.pos
        particule = particules[i][j]
        adress = [(i, (j + 1) % len(particules)), (i, (j - 1) % len(particules)), ((i - 1) % len(particules), j), ((i + 1) % len(particules), j)]
        right, left, up, down = particules[adress[0][0]][adress[0][1]], particules[adress[1][0]][adress[1][1]], particules[adress[2][0]][adress[2][1]], particules[adress[3][0]][adress[3][1]]
        neighboor = [right, left, up, down]
        
        if particule == 1:
            for k in range(4):
                ng_index = adress[k]
                ng = particules[ng_index[0]][ng_index[1]]
                if ng == 2:
                    z = random.random()
                    if z < float(b):
                        particules[ng_index[0]][ng_index[1]] = 0
            z = random.random()
            if z < float(c):
                particules[i][j] = 0
            else:
                z = random.random()
                if z < float(p):
                    '''
                    0 - baixo
                    1 - cima
                    2 - esquerda
                    3 - direita
                    '''
                    # Get obs and reshape this
                    obs = np.array(get_obs(particules, (i, j))).reshape(1, -1)

                    # To run with random walk actions in predator
                    # action = random.randint(0, 3)

                    # Action with pre-trained policy in my local machine
                    action = model.policy.predict(obs.reshape(1, -1))[0]

                    # time.sleep(0.5)
                    apply_action(particules, (i, j), action, model=model)

        elif particule == 2:
            for k in range(4):
                ng_index = adress[k]
                ng = particules[ng_index[0]][ng_index[1]]
                if ng == 0:
                    z = random.random()
                    if z < float(a):
                        particules[ng_index[0]][ng_index[1]] = 2


        for i in range(1, len(particules) - 1):
            for j in range(1, len(particules[i]) - 1):
                pygame.draw.rect(window, color[particules[i][j]], (i * L_sq + 1, j * L_sq + 1, L_sq, L_sq))


        print(t)
        
        t += 1
        relogio.tick(fps)
        pygame.display.update()
    pygame.quit()
