from sim_game import Yahtzee_Game
from random import sample

env = Yahtzee_Game()

for step in range(1000):
    while env.is_done == False:
        possible_actions = env.get_possible_actions()
        action = sample(possible_actions, 1)[0]
        new_state, reward = env.step(action)
    print('game done')
    print(env.scores.calculate_score())
    env.reset()

