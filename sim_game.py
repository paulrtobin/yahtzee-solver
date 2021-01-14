from scorecard import Scorecard
from collections import Counter
import itertools
import random
import numpy as np
import pickle

class Dice:
    def __init__(self):
        self.roll_num = 0
        self.dice_state = [-1, -1, -1, -1, -1]
        self.roll([1, 1, 1, 1, 1])   #roll all dice

    def roll(self, dice_to_roll):
        for die in range(5):
            if dice_to_roll[die] == 1:
                self.dice_state[die] = random.randint(1, 6)
        self.roll_num += 1

    def reset(self):
        self.roll_num = 0
        self.roll([0, 1, 2, 3, 4])

class Yahtzee_Game:
    def __init__(self):
        self.scores = Scorecard()
        self.dice = Dice()
        self.is_done = False
        #there are 252 possible combinations of dice
        #there are three roll stats: one roll, two roll, and three roll
        #there are also a number 524,288 board states
        #there are 32 ways to roll dice including not rolling
        #there are 13 scoring actions
        #need to represent states by which scores are filled and what the total in the top section is

        #total states are
        #252*3*524,288 = 396,361,728

        #total actions are
        #32+13 = 45

        self.num_states = 396361728
        self.num_actions = 45

        #actions are broken down as follows
        #0-31 are rolling actions
        self.roll_actions = np.zeros((32, 5), dtype=int)
        dice_indices = [0, 1, 2, 3, 4]
        count = 0
        for i in range(6):
            for j in itertools.combinations(dice_indices, i):
                self.roll_actions[count, j] = 1
                count += 1

        dice_nums = [1, 2, 3, 4, 5, 6]
        dice_combs = itertools.combinations_with_replacement(dice_nums, 5)
        self.dice_state_lookup = {}
        count = 0
        for index, c in enumerate(dice_combs):
            key = ''.join([str(i) for i in c])
            self.dice_state_lookup[key] = count
            count += 1



        #32-44 are scoring actions (starting with ones and going down to chance)

    def create_state_map(self):
        "this won't work because there are too many values to keep in memory"
        state_dict = {}
        roll_nums = [1, 2, 3]
        ones = [-1, 0]
        twos = [-1, 0]
        threes = [-1, 0]
        fours = [-1, 0]
        fives = [-1, 0]
        sixs = [-1] + [i for i in range(1, 64)]

        three_kind = [-1, 0]
        four_kind = [-1, 0]
        sm_straight = [-1, 0]
        lg_straight = [-1, 0]
        yahtzee = [-1, 0]
        chance = [-1, 0]

        dice_nums = [1, 2, 3, 4, 5, 6]
        count = 0
        # make a big loop and set appropriate values in class to calculate state number
        # TODO find a better way to iterate over lists of varying lengths
        for roll_num in roll_nums:
            for one_val in ones:
                for two_val in twos:
                    for three_val in threes:
                        for four_val in fours:
                            for five_val in fives:
                                for six_val in sixs:
                                    for three_kind_val in three_kind:
                                        for four_kind_val in four_kind:
                                            for sm_straight_val in sm_straight:
                                                for lg_straight_val in lg_straight:
                                                    for yahtzee_val in yahtzee:
                                                        for chance_val in chance:
                                                            for dice_comb in itertools.combinations_with_replacement(dice_nums, 5):
                                                                key = (roll_num, one_val, two_val, three_val,
                                                                       four_val, five_val, six_val, three_kind_val,
                                                                       four_kind_val, sm_straight_val, lg_straight_val,
                                                                       yahtzee_val, chance_val, dice_comb)

                                                                state_dict[key] = count
                                                                count += 1
                                                                if count % 1000000 == 0:
                                                                    print(count)

        output = open('states.pkl', 'wb')
        pickle.dump(state_dict, output)
        output.close()



    def compute_state_number(self):
        roll_number = self.dice.roll_num
        dice_state = sorted(self.dice.dice_state)
        state_num = 0
        division_level = self.num_states
        state_num += division_level/3 * (roll_number-1)
        division_level /= 3
        top_state = 0
        for entry in self.scores.scores.loc[0,'ones':'sixs']:
            if entry > 0:
                top_state += entry
        if top_state > 63:
            top_state = 63
        state_num += division_level/64 * top_state
        division_level /= 64

        ones = 0 if self.scores.scores.loc[0, 'ones'] == -1 else 1
        state_num += division_level/2 * ones
        division_level /= 2

        twos = 0 if self.scores.scores.loc[0, 'twos'] == -1 else 1
        state_num += division_level/2 * twos
        division_level /= 2

        threes = 0 if self.scores.scores.loc[0, 'threes'] == -1 else 1
        state_num += division_level/2 * threes
        division_level /= 2

        fours = 0 if self.scores.scores.loc[0, 'fours'] == -1 else 1
        state_num += division_level/2 * fours
        division_level /= 2

        fives = 0 if self.scores.scores.loc[0, 'fives'] == -1 else 1
        state_num += division_level/2 * fives
        division_level /= 2

        sixs = 0 if self.scores.scores.loc[0, 'sixs'] == -1 else 1
        state_num += division_level/2 * sixs
        division_level /= 2

        three_kind_state = 0 if self.scores.scores.loc[0, 'three_of_kind'] == -1 else 1
        state_num += division_level/2 * three_kind_state
        division_level /= 2


        four_kind_state = 0 if self.scores.scores.loc[0, 'four_of_kind'] == -1 else 1
        state_num += division_level/2 * four_kind_state
        division_level /= 2

        sm_straight = 0 if self.scores.scores.loc[0, 'small_straight'] == -1 else 1
        state_num += division_level / 2 * sm_straight
        division_level /= 2

        lg_straight = 0 if self.scores.scores.loc[0, 'large_straight'] == -1 else 1
        state_num += division_level / 2 * lg_straight
        division_level /= 2

        full_house = 0 if self.scores.scores.loc[0, 'full_house'] == -1 else 1
        state_num += division_level / 2 * full_house
        division_level /= 2

        yahtzee = 0 if self.scores.scores.loc[0, 'yahtzee'] == -1 else 1
        state_num += division_level / 2 * yahtzee
        division_level /= 2

        chance_state = 0 if self.scores.scores.loc[0, 'chance'] == -1 else 1
        state_num += division_level/2 * chance_state
        division_level /= 2

        #handled all score states and roll number states
        #now need to handle dice states
        state_num += self.dice_state_lookup[''.join([str(i) for i in dice_state])]

        return int(state_num)

    def roll(self, dice_to_roll):
        self.dice.roll(dice_to_roll)
        return self.dice.dice_state

    def get_possible_actions(self):
        #need to return valid action numbers as a list
        valid_actions = []

        if self.dice.roll_num < 3:
            valid_actions += [i for i in range(32)]

        #now need to check which columns have been filled
        open_spots = self.scores.get_open_categories() + 32
        valid_actions += list(open_spots)

        return valid_actions




    def get_valid_score(self, entry_num):
        #TODO figure out how to directly call appropriate logic without 12 if statements (list of funtions or something)
        counts = Counter(self.dice.dice_state)
        entry_num -= 32
        assert(self.scores.scores_new[entry_num] == -1)

        if entry_num == 0:
            #ones category
            return counts[1]

        elif entry_num == 1:
            #twos category
            return counts[2] * 2

        elif entry_num == 2:
            #threes category
            return counts[3] * 3

        elif entry_num == 3:
            #fours category
            return counts[4] * 4

        elif entry_num == 4:
            #fives category
            return counts[5] * 5

        elif entry_num == 5:
            #sixs category
            return counts[6] * 6

        elif entry_num == 6:
            #three of a kind
            if max(counts.values()) >= 3:
                return sum(self.dice.dice_state)
            else:
                return 0

        elif entry_num == 7:
            #four of a kind
            if max(counts.values()) >= 4:
                return sum(self.dice.dice_state)
            else:
                return 0

        elif entry_num == 8:
            #full house
            if max(counts.values()) == 3 and min(counts.values()) == 2:
                #default value for full house (25)
                return 25
            else:
                return 0

        elif entry_num == 9 or entry_num == 10:
            #small/large straight
            self.dice.dice_state.sort()
            lis_max = 0
            cur_lis = 1
            for index in range(1, 5):
                if self.dice.dice_state[index] == self.dice.dice_state[index - 1] + 1:
                    cur_lis += 1
                    if cur_lis > lis_max:
                        lis_max = cur_lis
                elif self.dice.dice_state[index] == self.dice.dice_state[index - 1]:
                    continue
                else:
                    cur_lis = 1

            if entry_num == 9 and lis_max >= 4:
                return 30
            else:
                return 0

            if entry_num == 10 and lis_max >= 5:
                return 40
            else:
                return 0


        elif entry_num == 11:
            #yahtzee
            if max(counts.values()) == 5 and self.dice.dice_state != [0, 0, 0, 0, 0]:
                return 50
            else:
                return 0

        elif entry_num == 12:
            return sum(self.dice.dice_state)

    def score(self, action):
        score = self.get_valid_score(action)
        self.scores.update_scorecard(action - 32, score)

    def take_action(self, action_number):
        if action_number < 32:
            self.dice.roll(self.roll_actions[action_number])



    def step(self, action):
        # the action is either to enter a score in a column or roll a subset of dice
        # the actions is specified as an integer from 0-45 with 0-31 being rolling actions and
        # 32 - 45 being scoring actions
        #need to return new state and the reward achieved as well as allowed next actions
        #state is defined by the dice state and the roll number
        if action >= 32:
            #scoring action
            self.score(action)
            self.dice.reset()

        else:
            self.dice.roll(self.roll_actions[action])



        #check if all scores are filled to see if the game is done
        if self.scores.is_full():
            reward = self.scores.calculate_score()
            self.is_done = True
        else:
            reward = 0

        new_state = self.compute_state_number()

        return new_state, reward

    def reset(self):
        self.scores = Scorecard()
        self.dice.reset()
        self.is_done = False




















