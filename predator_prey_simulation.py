from multiprocessing import allow_connection_pickling
import random
import numpy as np
import pygame
import sys
from policy_predator import *

t_max = 500000

'''
0 - empty
1 - predator
2 - prey
'''
types = [0, 1, 2]
model = Policy(load=True, pos=(0, 0))
L = 25
# cs = np.arange(0.18, 0.30, 0.01)
cs = [0.25, 0.35]
rhos = []

def rho(particules):
    return len(np.where(particules == 2)[0]) / (L * L)
    


if len(sys.argv) != 6:
    print("Error Usage. You must type this form: python predator_prey.py L ci cf cstep p")
else:
    L, ci, cf, cstep, p = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    cs = np.arange(ci, cf, cstep)
    a = 0.4
    for c in cs:
        b = 1 - a - c
        rho = []
        t = 0
        
        # Fill all array with prey
        particules = np.array([[2 for i in range(L)] for j in range(L)])

        # Fill the center with predator
        particules[(L // 2) + 1][(L // 2) + 1] = 1
        
        not_finish = True

        # Density of predators
        rhos = []
        b = 1 - a - c
        while not_finish and t < t_max:
           for i in range(L):
                for j in range(L):
                    particule = particules[i][j]
                    adress = [(i, (j + 1) % len(particules)), (i, (j - 1) % len(particules)), ((i - 1) % len(particules), j), ((i + 1) % len(particules), j)]

                    right, left, up, down = particules[adress[0][0]][adress[0][1]], particules[adress[1][0]][adress[1][1]], particules[adress[2][0]][adress[2][1]], particules[adress[3][0]][adress[3][1]]

                    neighboor = [right, left, up, down]
                    
                    if particule == 1:
                        # Probability of eat prey
                        for k in range(4):
                            ng_index = adress[k]
                            ng = particules[ng_index[0]][ng_index[1]]
                            if ng == 2:
                                z = random.random()
                                if z < float(b) / 4:
                                    particules[ng_index[0]][ng_index[1]] = 1
                        z = random.random()

                        # Probability of die
                        if z < float(c):
                            particules[i][j] = 0
                        # Probability of move (in canonical basis is null)
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
                                # action = random.randint(0, 3)
                                action = model.policy.predict(obs.reshape(1, -1))[0]
                                apply_action(particules, (i, j), action, model=model)

                    # Probability of prey born
                    elif particule == 2:
                        for k in range(4):
                            ng_index = adress[k]
                            ng = particules[ng_index[0]][ng_index[1]]
                            if ng == 0:
                                z = random.random()
                                if z < float(a) / 4:
                                    particules[ng_index[0]][ng_index[1]] = 2
                    t += 1
                    