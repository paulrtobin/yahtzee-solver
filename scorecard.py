import pandas as pd
import math

class Scorecard():
    def __init__(self):
        #each entry in self.scores is a tuple (score, default)
        #where score is the current entry where score is the current score (-1 means no entry yet)
        #default is the predetermined score for the category if it exists
        board_info = {
            'ones': (-1, None),
            'twos': (-1, None),
            'threes': (-1, None),
            'fours': (-1, None),
            'fives': (-1, None),
            'sixs': (-1, None),

            'three_of_kind': (-1, None),
            'four_of_kind': (-1, None),
            'full_house': (-1, 25),
            'small_straight': (-1, 30),
            'large_straight': (-1, 40),
            'yahtzee': (-1, 50),
            'chance': (-1, None)
        }

        self.scores = pd.DataFrame(data=board_info)
        self.is_done = False

    def update_scorecard(self, category, score=None):

        if not math.isnan(self.scores.loc[1, category]):
            self.scores.loc[0, category] = self.scores.loc[1, category]
        else:
            self.scores.loc[0, category] = score

    def get_score(self, category):
        return self.scores.loc[0, category]

    def is_full(self):
        if self.scores.loc[0].value_counts()[-1] == 0:
            return True
        else:
            return False


    def calculate_score(self):
        return self.scores.loc[0].sum()








