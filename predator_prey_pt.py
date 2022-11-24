from multiprocessing import allow_connection_pickling
import random
import numpy as np
import pygame
import sys
from policy_predator import *


altura = 500
largura = 500
gray = (50, 50, 50)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
background = white
ball_color = gray
fps = 200
t_max = 500000
L_sq = 10

'''
0 - empty
1 - predator
2 - prey
'''
types = [0, 1, 1]
color = [gray, red, white]
model = Policy(load=True, pos=(0, 0))
# cs = np.arange(0.18, 0.30, 0.01)
cs = [0.25, 0.35]
rhos = []


if len(sys.argv) != 3:
    print("Error Usage. You must type this form: python predator_prey.py a b c")
else:
    # a, b, c, p = sys.argv[1], sys. argv[2], sys.argv[3], sys.argv[4]
    c, p = float(sys.argv[1]), float(sys.argv[2])
    a = 0.4
    b = 1 - a - c
    pygame.init()
    relogio = pygame.time.Clock()
    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Predator Prey")
    window.fill(gray)
    for c in cs:
        rho = []
        t = 0
        particules = np.array([[random.choice(types) for i in range(0, largura, L_sq)] for j in range(0, altura, L_sq)])
        L = len(particules)
        # for k in range(1):
        #     # i, j = random.randint(0, len(particules) - 1), random.randint(0, len(particules) - 1)
        #     i, j = L // 2, L // 2
        #     model.pos = (i, j)
        #     particules[i][j] = 1
        
        # window.fill(gray)
        
        for i in range(int(L/5), int(L*4/5)):
            for j in range(int(L/5), int(L*4/5)):
                particules[i][j] = 2
                
        
        continua = True
        rhos = []
        
        b = 1 - a - c
        while continua and t < t_max:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continua = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continua = False


            
            # window.fill(background)
            i, j = random.randint(0, len(particules) - 1), random.randint(0, len(particules) - 1)
            # i, j = model.pos
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
                            continue
                            # particules[ng_index[0]][ng_index[1]] = 1
                z = random.random()
                if z < float(c):
                    continue
                    # particules[i][j] = 0
                    
                else:
                    z = random.random()
                    if z < float(p):
                        '''
                        0 - baixo
                        1 - cima
                        2 - esquerda
                        3 - direita
                        '''
                        obs = np.array(get_obs(particules, (i, j))).reshape(1, -1)
                        # action = model(obs).numpy().argmax()
                        # action = model.predict(obs.reshape(1, -1)).numpy().argmax()
                        # action = random.randint(0, 3)

                        action = model.policy.predict(obs.reshape(1, -1))[0]
                        apply_action(particules, (i, j), action, model=model)

            elif particule == 2:
                pass
                for k in range(4):
                    ng_index = adress[k]
                    ng = particules[ng_index[0]][ng_index[1]]
                    if ng == 0:
                        z = random.random()
                        if z < float(a):
                            continue
                            # particules[ng_index[0]][ng_index[1]] = 2


            for i in range(1, len(particules) - 1):
                for j in range(1, len(particules[i]) - 1):
                    pygame.draw.rect(window, color[particules[i][j]], (i * L_sq + 1, j * L_sq + 1, L_sq, L_sq))

            t += 1
            relogio.tick(fps)
            if t % 100 == 0:
                rho.append(np.sum(particules == 1) / (L * L))

            if t % 10000 == 0:
                print(t, rho[-1], c)
            pygame.display.update()

        rhos.append(rho)   
    # Save in csv file rhos results for each c with time in x axis
    for i in range(len(cs)):
        np.savetxt(f"results/rho_{cs[i]}_{a}_{b}_{c}_{p}.csv", rhos[i], delimiter=",")
    pygame.quit()
