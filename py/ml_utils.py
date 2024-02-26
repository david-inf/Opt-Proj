# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
# import matplotlib
# matplotlib.use("pgf")
import matplotlib.pyplot as plt
# from sklearn.metrics import accuracy_score

from models import LogisticRegression
# from solvers_utils import sigmoid

# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
#     "pgf.preamble": "\n".join([
#          r"\usepackage{lmodern}",
#          r"\usepackage[utf8]{inputenc}",
#          r"\usepackage[T1]{fontenc}",
#     ]),
# })


def run_solvers(solver, C, dataset, max_epochs, batch_size, step_size, momentum=(0, 0, 0)):
    solver1 = LogisticRegression(solver, C=C)
    solver1.fit(dataset=dataset, max_epochs=max_epochs, batch_size=batch_size,
                step_size=step_size[0], momentum=momentum[0])

    solver2 = LogisticRegression(solver, C=C)
    solver2.fit(dataset=dataset, max_epochs=max_epochs, batch_size=batch_size,
                step_size=step_size[1], momentum=momentum[1])

    solver3 = LogisticRegression(solver, C=C)
    solver3.fit(dataset=dataset, max_epochs=max_epochs, batch_size=batch_size,
                step_size=step_size[2], momentum=momentum[2])

    return [solver1, solver2, solver3]


def optim_data(models):
    # models: LogisticRegression
    models_data = pd.DataFrame(
        {
            "Solver": [model.solver for model in models],
            "C": [model.C for model in models],
            "Minibatch": [model.opt_result.minibatch_size for model in models],
            "Step-size": [model.opt_result.step_size for model in models],
            "Momentum": [model.opt_result.momentum for model in models],
            "Solution": [np.round(model.coef_, 4) for model in models],
            "Loss": [model.loss for model in models],
            "Grad norm": [model.grad for model in models],
            "Run-time": [model.opt_result.runtime for model in models],
            "Iterations": [model.opt_result.nit for model in models],
            # "Termination": [model.message for model in models],
            "Train score": [model.accuracy_train for model in models],
            "Test score": [model.accuracy_test for model in models],
            "Loss/Epochs": [model.loss_seq for model in models],
            "Time/Epochs": [model.opt_result.time_per_epoch for model in models]
        }
    )
    return models_data


def run_bench(dataset, C):
    bench1 = LogisticRegression("L-BFGS", C=C).fit(dataset=dataset)
    bench2 = LogisticRegression("Newton-CG", C=C).fit(dataset=dataset)
    bench3 = LogisticRegression("CG", C=C).fit(dataset=dataset)

    return [bench1, bench2, bench3]


def optim_bench(models):
    data = pd.DataFrame(
        {
            "Solver": [model.solver for model in models],
            "C": [model.C for model in models],
            "Minibatch": np.nan,
            "Step-size": np.nan,
            "Momentum": np.nan,
            "Solution": [np.round(model.coef_, 4) for model in models],
            "Loss": [model.loss for model in models],
            "Grad norm": [model.grad for model in models],
            "Run-time": np.nan,
            "Iterations": [model.opt_result.nit for model in models],
            # "Termination": model.message,
            "Train score": [model.accuracy_train for model in models],
            "Test score": [model.accuracy_test for model in models],
            "Loss/Epochs": np.nan,
            "Time/Epochs": np.nan
        }
    )
    return data


def models_summary(custom, bench):
    models_data = pd.concat([bench, custom], ignore_index=True)

    models_data["Distance (L-BFGS)"] = models_data["Solution"].apply(
        lambda x: np.linalg.norm(x - bench.loc[0]["Solution"]))

    models_data["Sol norm"] = models_data["Solution"].apply(
        lambda x: np.linalg.norm(x))

    return models_data.drop(columns={"Solution", "Loss/Epochs", "Time/Epochs"})


def plot_loss_epochs(ax, data):
    df = data.copy()
    df.loc[:, "labels"] = df["Solver"] + \
        "(" + df["Step-size"].astype(str) + ")"

    start = 1  # only in np.range
    end = data["Loss/Epochs"][0].shape[0] + 1

    R = data.shape[0]  # number of rows
    for i in range(R//2):
        ax.plot(np.arange(start, end), df["Loss/Epochs"][i], linestyle="dashed")

    for i in range(R//2, R):
        ax.plot(np.arange(start, end), df["Loss/Epochs"][i], linestyle="solid")

    # ax.set_xlabel("Epochs")
    ax.set_xscale("log")

    # ax.set_ylabel("Train loss")
    ax.set_yscale("log")
    # ax.set_ylim(top=np.mean(df["Loss/Epochs"][0]))

    ax.grid(True, which="both", axis="both")
    ax.legend(df["labels"], fontsize="x-small")


def diagnostic_epochs(data1, data2, data3, data4, bench):
    models = [data1, data2, data3, data4]
    E = data1["Loss/Epochs"][0].shape[0]  # number of measurement

    fig, axs = plt.subplots(2, 2, layout="constrained", sharey=True, sharex=True,
                            figsize=(6.4, 4.8))

    i = 0
    for ax in axs.flat:
        plot_loss_epochs(ax, models[i])

        # benchmark solver line
        ax.axhline(y=bench.loss, color="k", linestyle="dashed")
        ax.text(E*0.25, bench.loss*1.02, bench.solver, fontsize=8, ha="center")

        i += 1

    axs[1,0].set_xlabel("Epochs")
    axs[1,1].set_xlabel("Epochs")

    axs[0,0].set_ylabel("Train loss")
    axs[1,0].set_ylabel("Train loss")


def plot_loss_time(ax, data):
    df = data.copy()
    df.loc[:, "labels"] = df["Solver"] + \
        "(" + df["Step-size"].astype(str) + ")"

    end = data["Loss/Epochs"][0].shape[0]
    indices = np.arange(0, end, 10)

    R = data.shape[0]
    for i in range(R//2):
        ax.plot(df["Time/Epochs"][i][indices], df["Loss/Epochs"][i][indices], linestyle="dashed")

    for i in range(R//2, R):
        ax.plot(df["Time/Epochs"][i][indices], df["Loss/Epochs"][i][indices], linestyle="solid")

    # ax.set_xlabel("Time")
    # ax.set_xscale("log")

    # ax.set_ylabel("Train loss")
    ax.set_yscale("log")

    ax.grid(True, which="both", axis="both")
    ax.legend(df["labels"], fontsize="x-small")


def diagnostic_time(data1, data2, data3, data4, bench):
    models = [data1, data2, data3, data4]
    T = data1["Time/Epochs"][3][-1]

    fig, axs = plt.subplots(2, 2, layout="constrained", sharey=True, sharex=True,
                            figsize=(6.4, 4.8))

    i = 0
    for ax in axs.flat:
        plot_loss_time(ax, models[i])

        ax.axhline(y=bench.loss, color="k", linestyle="dashed")
        ax.text(T, bench.loss*1.02, bench.solver, fontsize=8, ha="right")

        i += 1

    xlabel = "Time"
    axs[1,0].set_xlabel(xlabel)
    axs[1,1].set_xlabel(xlabel)

    ylabel = "Train loss"
    axs[0,0].set_ylabel(ylabel)
    axs[1,0].set_ylabel(ylabel)



# def plot_accuracy(models, ticks):
#     solvers_dict = {}
#     solvers_dict["Train score"] = [model.accuracy_train for model in models]
#     solvers_dict["Test score"] = [model.accuracy_test for model in models]
#     x = np.arange(len(models))
#     bar_width = 0.35
#     multiplier = 0
#     fig, ax1 = plt.subplots(ncols=1, layout="constrained")
#     for score, vals in solvers_dict.items():
#         offset = bar_width * multiplier
#         rects = ax1.bar(x + offset, vals, bar_width, label=score)
#         ax1.bar_label(rects, fmt="%.3f", fontsize="small", padding=3)
#         multiplier += 1
#     ax1.set_ylabel("Accuracy")
#     ax1.set_xticks(x + bar_width / 2, ticks, rotation=90)
#     ax1.legend()
#     ax1.set_ylim([0, 1])
#     ax1.grid(True)
#     plt.show()


# def plot_runtime(models, ticks):
#     solvers_dict = {}
#     solvers_dict["Run-time"] = [model.runtime for model in models]
#     x = np.arange(len(models))
#     bar_width = 0.35
#     multiplier = 0
#     fig, ax1 = plt.subplots(ncols=1, layout="constrained")
#     for score, vals in solvers_dict.items():
#         offset = bar_width * multiplier
#         rects = ax1.bar(x + offset, vals, bar_width, label=score)
#         ax1.bar_label(rects, fmt="%.4f", padding=3)
#         multiplier += 1
#     ax1.set_ylabel("Run-time")
#     ax1.set_xticks(x, ticks, rotation=90)
#     # ax1.legend()
#     # ax1.set_ylim([0, 1])
#     ax1.grid(True)
#     plt.show()
