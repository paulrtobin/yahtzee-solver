import unittest
import itertools
import numpy as np
from sim_game import Yahtzee_Game


class TestEnv(unittest.TestCase):

    def test_state_calculator(self, skip_percentage=0.999999):
        state_numbers = []
        env = Yahtzee_Game()
        # manually set all combinations of board state, dice state, and roll num and compute state number
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
                                                            for dice_comb in itertools.combinations_with_replacement(
                                                                    dice_nums, 5):
                                                                if np.random.random() < skip_percentage:
                                                                    continue
                                                                env.dice.roll_num = roll_num
                                                                env.dice.dice_state = dice_comb
                                                                env.scores.scores.loc[0, 'ones'] = one_val
                                                                env.scores.scores.loc[0, 'twos'] = two_val
                                                                env.scores.scores.loc[0, 'threes'] = three_val
                                                                env.scores.scores.loc[0, 'fours'] = four_val
                                                                env.scores.scores.loc[0, 'fives'] = five_val
                                                                env.scores.scores.loc[0, 'sixs'] = six_val
                                                                env.scores.scores.loc[0,
                                                                                      'three_of_kind'] = three_kind_val
                                                                env.scores.scores.loc[0, 'four_of_kind'] = four_kind_val
                                                                env.scores.scores.loc[0,
                                                                                      'small_straight'] = sm_straight_val
                                                                env.scores.scores.loc[0,
                                                                                      'large_straight'] = lg_straight_val
                                                                env.scores.scores.loc[0, 'yahtzee'] = yahtzee_val
                                                                env.scores.scores.loc[0, 'chance'] = chance_val

                                                                state_num = env.compute_state_number()
                                                                state_numbers.append(state_num)

        state_numbers = np.array(state_numbers)
        total_states = state_numbers.shape[0]
        unique_states = np.unique(state_numbers).shape[0]

        self.assertEqual(total_states, unique_states)


if __name__ == '__main__':
    unittest.main()
