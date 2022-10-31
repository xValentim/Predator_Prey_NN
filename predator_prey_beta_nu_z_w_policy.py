# from multiprocessing import allow_connection_pickling
import random
import numpy as np
from policy_predator import *
# import pygame
# import sys
# # from policy_predator import *

t_max = 90000

'''
0 - empty
1 - predator
2 - prey
'''
types = [0, 1, 2]
model = Policy(load=True, pos=(0, 0))
cc = 0.26
rhos = []



def number_of_predators(particules):
    return len(np.where(particules == 1)[0])

def rho(particules):
    return len(np.where(particules == 1)[0]) / (len(particules) * len(particules))


# L, Li, Lf, Lstep, p = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])

L = 200
a = 0.4
b = 1 - a - cc
p = 0

all_pos = [(i, j) for i in range(L) for j in range(L)]

times = np.arange(0, t_max, 100)
# Density of predators
rhos = []
nb_copies = 50
for nb in range(nb_copies):
    # Fill all array with prey
    particules = np.array([[2 for i in range(L)] for j in range(L)])

    predators_init = 0
    while predators_init < (L**2) // 2:
        i, j = random.randint(0, len(particules) - 1), random.randint(0, len(particules) - 1)
        if particules[i][j] == 2:
            particules[i][j] = 1
            predators_init += 1
    curr_rho = []
    for t in range(0, t_max, 100):
        # random.shuffle(all_pos)
        
        for iter in range(L * L):
            i, j = random.randint(0, L - 1), random.randint(0, L - 1)
            particule = particules[i][j]
            adress = [(i, (j + 1) % len(particules)), (i, (j - 1) % len(particules)), ((i - 1) % len(particules), j), ((i + 1) % len(particules), j)]

            right, left, up, down = particules[adress[0][0]][adress[0][1]], particules[adress[1][0]][adress[1][1]], particules[adress[2][0]][adress[2][1]], particules[adress[3][0]][adress[3][1]]

            neighboor = [right, left, up, down]
            
            if particule == 1:
                z = random.random()
                # Probability of die
                if z < float(cc):
                    particules[i][j] = 0
                else:
                    obs = np.array(get_obs(particules, (i, j))).reshape(1, -1)
                    # print(get_obs(particules, (i, j)), 'before')
                    # print(particules[i][j], 'my predator before')
                    # print(neighboor, 'neighboor before')

                    # print(obs)
                    action = model.policy.predict(obs.reshape(1, -1))[0]
                    # print(action, 'action')
                    # print(action, 'action')
                    particules = apply_action(particules, (i, j), action, model=model)
                    # print(particules[i][j], 'my predator after')
                    # right, left, up, down = particules[adress[0][0]][adress[0][1]], particules[adress[1][0]][adress[1][1]], particules[adress[2][0]][adress[2][1]], particules[adress[3][0]][adress[3][1]]
                    # neighboor = [right, left, up, down]
                    # print(neighboor, 'neighboor after')
                    # print(particules[i][j], )
                    # print(get_obs(particules, (i, j)), 'after')
                    
                # Probability of move (in canonical basis is null)
                # else:
                #     z = random.random()
                #     if z < float(p):
                #         '''
                #         0 - direita
                #         1 - esquerda
                #         2 - cima
                #         3 - baixo
                #         '''
                #         # obs = np.array(get_obs(particules, (i, j))).reshape(1, -1)
                #         # action = random.randint(0, 3)
                #         # action = model.policy.predict(obs.reshape(1, -1))[0]
                #         # apply_action(particules, (i, j), action, model=model)

            # Probability of predator born
            # If is prey, try to insert predator 
            elif particule == 2:
                vpd = 0
                for k in range(4):
                    ng_index = adress[k]
                    ng = particules[ng_index[0]][ng_index[1]]
                    if ng == 1:
                        vpd += 1
                z = random.random()
                if z < (float(b) / 4) * vpd:
                    particules[i][j] = 1
            
            # Probability of prey born
            # If is empty, try to insert prey
            elif particule == 0:
                vp = 0
                for k in range(4):
                    ng_index = adress[k]
                    ng = particules[ng_index[0]][ng_index[1]]
                    if ng == 2:
                        vp += 1
                z = random.random()
                if z < (float(a) / 4) * vp:
                    particules[i][j] = 2



        if number_of_predators(particules) == 0:
            # introduce a new predator
            particules[(L // 2) + 1][(L // 2) + 1] = 1

        curr_rho.append(rho(particules))
        print(t, curr_rho[-1])

    content = 'time,rho\n'
    for i in range(min(len(times), len(curr_rho))):
        content += str(times[i]) + ',' + str(curr_rho[i]) + '\n'

    with open(f'data_w_policy_cc/results_{nb}_w_policy_c{int(cc*100)}_{L}.csv', 'w') as f:
        f.write(content)
    
    print(f'{nb} - {rho(particules)}')
    rhos.append(curr_rho)

rhos = np.array(rhos)
rhos = np.mean(rhos, axis=0)

# save in csv file the results
content = ''
for i in range(min(len(times), len(rhos))):
    content += str(times[i]) + ',' + str(rhos[i]) + '\n'

with open(f'data_w_policy_cc/results_w_policy_{int(cc*100)}_{L}.csv', 'w') as f:
    f.write(content)





        
            