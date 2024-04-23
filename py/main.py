
#%% Packages
# import time
# import numpy as np
# import sys
import matplotlib.pyplot as plt
# import pandas as pd

from load_datasets import load_mg, load_mushrooms, load_phishing, load_w1a, load_a2a, load_w3a, load_a4a
from models import LogisticRegression, LinearRegression
from ml_utils import (optim_data, optim_bench, models_summary, single_diagnostic,
                      diagnostic)
from grid_search import run_solvers, run_bench, grid_search, cross_val

# %% Diabetes

data = load_a4a()

C = 0.5
# MDiab = 64
# kDiab = 200

benchDiab = run_bench(data, 0.5)
benchDiab_data = optim_bench(benchDiab)

# %% debug line search

armijo1 = LogisticRegression("SGD-Armijo", C).fit(load_w1a(), 64, 1)
# print(armijo1)

armijo2 = LogisticRegression("SGD-Armijo", C).fit(load_w1a(), 32, 1)

# %%

mslc1 = LogisticRegression("MSL-SGDM-C", C)
mslc1.fit(data, 64, 1, 0.9)
print(mslc1)

# %%

# model1 = LogisticRegression("SGDM").fit(load_a2a(), **dict(batch_size=64))
models2 = run_solvers("SGDM", C, load_w1a(), (64,))

# %% cross-validation

sgd1_cv = cross_val(LogisticRegression("SGD-Fixed"), load_w1a(), solver_options=dict(batch_size=64))

# %% Grid search

# sgdfixed_opt1, _ = grid_search_seq("SGD-Fixed", 0.5, data_diab, (64, 128), (0.1, 0.01, 0.001, 0.0001))
# print("% ----- %")
sgdfixed_opt2, _ = grid_search("SGD-Fixed", 0.5, load_phishing(), (64, 128), (0.1, 0.01, 0.001, 0.0001))

# sgdm_opt, _ = grid_search_seq("SGDM", 0.5, data_diab, (64, 128))

# armijo_opt, _ = grid_search_seq("SGD-Armijo", 0.5, data_diab, (128,), (1, 0.1, 0.01), delta_a=(0.5, 0.9))
# print("% ----- %")
# armijo_opt, _ = grid_search_par("SGD-Armijo", 0.5, data_diab, (128,), (1, 0.1, 0.01), delta_a=(0.5, 0.9))

# %% Run 3 solvers

M_grid = (64, 128)
delta_a_grid = (0.3, 0.5, 0.7)
delta_m_grid = (0.3, 0.5, 0.7)

# SGD-Fixed
sgdfixed_w1a = run_solvers("SGD-Fixed", C, data, M_grid)
# SGD-Decreasing
sgddecre_w1a = run_solvers("SGD-Decreasing", C, data, M_grid)
# SGDM
sgdm_w1a = run_solvers("SGDM", C, data, M_grid)

# SGD-Armijo
sgdarmijo_w1a = run_solvers("SGD-Armijo", C, data, M_grid, delta_a=delta_a_grid)
# MSL-SGDM-C
mslc_w1a = run_solvers("MSL-SGDM-C", C, data, M_grid, delta_a=delta_a_grid, delta_m=delta_m_grid, n_jobs=6)
# MSL-SGDM-R
mslr_w1a = run_solvers("MSL-SGDM-R", C, data, M_grid, delta_a=delta_a_grid)

# %% Adam

# adam_w1a = LogisticRegression("Adam", C)
# adam_w1a.fit(load_w1a(), 32, 0.001)

adam_opt = grid_search("Adam", C, load_w1a(), (64,), (0.01, 0.001, 0.0001))

# %% plot solvers

diagnostic([sgdfixed_w1a, sgddecre_w1a, sgdm_w1a, sgdarmijo_w1a, mslc_w1a, mslr_w1a])

single_diagnostic(mslr_w1a)

# %% Linear Regression

# data_mg = load_mg()


# linearbench1 = LinearRegression().fit(data_mg)
# linearbench2 = LinearRegression("CG").fit(data_mg)
# linearbench3 = LinearRegression("Newton-CG").fit(data_mg)

# linearmodel1 = LinearRegression("SGD-Fixed").fit(load_mg())
