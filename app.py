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
        if not scenario_name:
            scenario_name = str(len(self.scenarios))

        if type(disabilities) is dict:
            disabilities_values = disabilities.values()
        else:
            disabilities_values = disabilities

        disabilities_values = sorted(disabilities_values, reverse=True)

        if bilateral_disabilities:
            disabilities_values.insert(
                0,
                round(
                    self.combined_rating(
                        bilateral_disabilities,
                        scenario_name=f"BilateralCombined_{scenario_name}",
                    )
                    * 1.1
                ),
            )
            # print(disabilities_values)
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

# %% try bilaterals

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
