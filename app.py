# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:55:09 2024

@author: david
"""
# %% imports and funcs

import pandas as pd
import numpy as np


class VaCalculator:

    def __init__(self):
        self.transition_matrix = pd.DataFrame(
            index=pd.Index(range(19, 100)),
            columns=[f"{i}" for i in range(10, 100, 10)],
        )

        for i in self.transition_matrix.index:
            ableness = 1 - i / 100
            current_disability = i / 100
            transition = np.arange(0.1, 1, 0.1)

            new_combined_rating = ableness * transition + current_disability

            self.transition_matrix.loc[i, :] = new_combined_rating

        self.transition_matrix = (
            self.transition_matrix.astype(float).round(2) * 100
        ).astype(int)

        self.scenarios = pd.DataFrame(
            columns=["Disabilities", "CombinedRating"]
        )

    def transition(self, starting_disability, next_disability):
        return self.transition_matrix.loc[
            starting_disability, f"{next_disability}"
        ]

    def combined_rating(
        self,
        disabilities: (dict, list),
        bilateral_disabilities: list = [],
        scenario_name: str = "",
    ):
        if type(disabilities) == dict:
            disabilities_names = list(disabilities.keys())
            disabilities_values = disabilities.values()
        else:
            disabilities_names = None

        disabilities_values = sorted(disabilities_values, reverse=True)

        if bilateral_disabilities:
            disabilities_values.insert(
                0, round(self.combined_rating(bilateral_disabilities) * 1.1)
            )
            print(disabilities_values)
        cumulative_rating = self.transition(
            disabilities_values[0], disabilities_values[1]
        )
        for disability in disabilities_values[2:]:
            cumulative_rating = self.transition(cumulative_rating, disability)

        self.scenarios.loc[
            scenario_name if scenario_name else len(self.scenarios)
        ] = (disabilities, cumulative_rating)

        return cumulative_rating


# %%

calc = VaCalculator()

dff = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})


# %% Current
calc.combined_rating(
    {
        "Anxiety": 50,
        "back": 20,
        "right leg": 10,
        "right ankle": 10,
        "tinitus": 10,
    },
    scenario_name="CurrentRating",
)
df = calc.scenarios.copy()
# %% Current + Sleep Apnea
combined_rating(
    {
        "Anxiety": 50,
        "back": 20,
        "right leg": 10,
        "right ankle": 10,
        "tinitus": 10,
        "Sleep Apnea": 50,
    }
)
# %% Strat 1
# Don't get sleep apnea, increase back rating. Add Migraines and Sinusitis
calc.combined_rating(
    {
        "Anxiety": 50,
        "Migraines": 50,  # Need to file
        "Sinusitis": 30,  # Need to file
        "Back": 40,
        "Tinittus": 10,
    },
    {"left leg": 20, "right leg": 20, "right foot": 10},
)
df = calc.scenarios
# %% Strat 2 - get sleep apnea, migraines, and sinusitis.
combined_rating(
    {
        "Anxiety": 50,
        "Sleep Apnea": 50,  # Need to file
        "Migraines": 50,  # Need to file
        "Sinusitis": 10,  # Need to file
        "Back": 20,
        "Tinittus": 10,
        "right leg": 10,
        "right ankle": 10,
        "rhinitis": 10,
    }
)

# %% What if 1 - only get migraines added. 90%
combined_rating(
    {
        "Anxiety": 50,
        "Migraines": 50,  # Need to file
        "Back": 20,
        "Tinittus": 10,
        "right leg": 10,
        "right ankle": 10,
    }
)

# %% What if: only get migraines added and back increased? 93!!!
# I need another 20% something to get to 100.
combined_rating(
    {
        "Anxiety": 50,
        "Migraines": 50,  # Need to file
        "Back": 40,
        # 'something': 20,
        "Tinittus": 10,
    },
    {"left leg": 20, "right leg": 20, "right foot": 10},
)

# %% What if 2 - only get sinusitis added - 80%
combined_rating(
    {
        "Anxiety": 50,
        "Sinusitis": 30,  # Need to file
        "Back": 20,
        "Tinittus": 10,
        "right leg": 10,
        "right ankle": 10,
    }
)
# %% What if 3 - Only get a back increase. 90%
combined_rating(
    {"Anxiety": 50, "OSA": 50, "Back": 40, "Sinusitis": 30, "Tinittus": 10},
    {"left leg": 20, "right leg": 20, "right foot": 10},
)

# %%
