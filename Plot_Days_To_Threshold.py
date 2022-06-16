import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn




def plot_days_to_learn(control_dict, mutant_dict):

    # Get Mice
    control_mice = control_dict.keys()
    mutant_mice = mutant_dict.keys()

    # Get Performance Lists
    days_to_learn_list = []
    genotype_list = []

    for mouse in control_mice:
        mouse_days_to_learn = control_dict[mouse]
        days_to_learn_list.append(mouse_days_to_learn)
        genotype_list.append("Wildtype")

    for mouse in mutant_mice:
        mouse_days_to_learn = mutant_dict[mouse]
        days_to_learn_list.append(mouse_days_to_learn)
        genotype_list.append("Homozygous")

    # Combine_Into Dataframe
    dataframe = pd.DataFrame()
    dataframe["Days_To_Learn"] = days_to_learn_list
    dataframe["Genotype"] = genotype_list

    axis = seaborn.swarmplot(y="Days_To_Learn", x="Genotype", data=dataframe)
    axis.set_ylim(0, 30)
    plt.show()


mutants = {
    "NRXN71.2A":21,
    "NXAK4.1A":28,
    "NXAK16.1B":28,
    "NXAK10.1A": 15,
    "NXAK24.1C":18,
    "NXAK20.1B":23,
}

controls = {
    "NRXN78.1A":9,
    "NRXN78.1D":13,
    "NXAK4.1B":19,
    "NXAK7.1B":24,
    "NXAK14.1A":11,
    "NXAK22.1A":16,
}

plot_days_to_learn(controls, mutants)

# p = 0.0214
