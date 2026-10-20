import pandas as pd
import numpy as np

# Simplified mortality table: probability of dying within that year, by age
# (not real SOA table data)
ages = np.arange(30, 71)
qx = 0.001 + 0.0005 * (ages - 30)   # mortality rate increases with age, made-up formula

mortality = pd.DataFrame({"age": ages, "qx": qx})

sum = mortality.loc[(mortality["age"] >= 30) & (mortality["age"] <= 70), "qx"].sum()

mortality["px"] = 1 - mortality["qx"]


mortality["survival_to_age"] = mortality["px"].cumprod()


policy_length = 10

death_benefit = 100_000

term = mortality.iloc[:policy_length]

term["death_this_year"] = term["qx"] * term["survival_to_age"].shift(1, fill_value=1)

print(term)

expected_payout_per_year = term["death_this_year"] * death_benefit

total = expected_payout_per_year.sum()

print(total.round())