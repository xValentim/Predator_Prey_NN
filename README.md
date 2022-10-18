# Lotka Volterra Model with Predator-Policy

We want to create a predator prey model that predator has Policy. So, in first step, we need to create a environment with gym and insert my predator in this environment. Lets create a environment!

## Create environment with Gym 

In this lotka volterra model, we will consider 3 types of elements:

1) Predator - Our objetive is to insert a policy (Neural Network) in this agent. We will represent this element with number 1 in our array. 

2) Prey - This element will assume role of food to predator. We will represent this element with number 2 in our array.

3) Empty space - We will represent this element with number 0 in our array.

For more details about our environment, check two notebooks: `predator_prey_NN_model.ipynb` and `predator_prey_NN_model_PPO.ipynb`.

