import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats


def get_group_mean(mouse_meta_list):

    # Get Group Means
    mean_scores = []
    score_sems = []
    condition = True

    count = 0
    while condition == True:
        day_scores = []
        for mouse in mouse_meta_list:
            if len(mouse) > count:
                mouse_day_score = mouse[count]
                day_scores.append(mouse_day_score)

        if len(day_scores) >= 4:
            mean_scores.append(np.mean(day_scores))
            score_sems.append(stats.sem(day_scores))
        else:
            condition = False
        count += 1

    return mean_scores, score_sems


mutant_mouse_list = [

    #Mutants
    # 72.1A - Slow Learner
    [r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_13_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_14_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_15_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_17_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_18_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_19_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_20_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_21_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_22_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_23_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_24_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_25_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_26_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_27_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_28_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_29_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_11_30_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_12_01_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_12_02_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN71.2A/2020_12_03_Discrimination_Imaging"],


    #4.1A Slow Learner
    [r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_03_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_05_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_07_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_08_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_09_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_10_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_11_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_12_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_13_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_14_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_15_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_17_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_18_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_19_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_20_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_21_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_22_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_23_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_24_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_25_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_26_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_27_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_02_28_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1A/2021_03_01_Discrimination_Imaging"],

    #10.1A Fast learner
    [r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_04_30_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_01_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_05_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_07_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_08_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_09_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_10_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_11_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_12_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_13_Discrimination_Behaviour",
    r"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK10.1A/2021_05_14_Discrimination_Imaging",
    ],

    # 16.1B Slow Learner
    [
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_04_30_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_01_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_02_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_03_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_07_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_08_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_09_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_10_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_11_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_12_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_13_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_17_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_18_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_19_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_20_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_22_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_23_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_24_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_25_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_26_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK16.1B/2021_05_27_Discrimination_Behaviour",
    ],

    #24.1C Fast Learner
    [
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_20_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_22_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_23_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_24_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_25_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_26_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_27_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_28_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_29_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_09_30_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_01_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_02_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_03_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK24.1C/2021_10_08_Discrimination_Imaging",
    ],

    # 20.1B Slow Leaner
    [
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_09_28_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_09_29_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_09_30_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_01_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_02_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_03_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_07_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_08_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_09_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_10_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_11_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_12_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_13_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_14_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_16_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK20.1B/2021_10_20_Discrimination_Behaviour",
    ],
    ]


control_mice_list = [ # Control Mice

    #78.1A - Fast Learner
    ["/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_21_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1A/2020_11_22_Discrimination_Behaviour",],

    # 78.1D - Fast learner
    ["/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_16_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_21_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_22_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_23_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_24_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_25_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NRXN78.1D/2020_11_26_Discrimination_Behaviour"],

    #4.1B
    ["/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_04_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_05_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_06_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_07_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_08_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_09_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_10_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_11_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_12_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_13_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_14_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_15_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_19_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK4.1B/2021_02_22_Discrimination_Imaging"],


    #14.1A FSt learner
    ["/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_04_29_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_04_30_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_01_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_02_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_03_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_04_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_05_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_06_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_07_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_08_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK14.1A/2021_05_09_Discrimination_Imaging"],

    # 22.1A
    ["/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_25_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_26_Discrimination_Behaviour",
    #"/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_27_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_28_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_29_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_09_30_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_01_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_02_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_03_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_04_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_05_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_06_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_07_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_08_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK22.1A/2021_10_09_Discrimination_Behaviour"],

    #7.1B Slow learner
    ["/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_01_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_02_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_03_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_04_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_05_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_06_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_07_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_08_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_09_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_10_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_11_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_12_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_13_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_14_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_15_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_16_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_17_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_18_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_19_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_20_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_21_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_22_Discrimination_Imaging",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_23_Discrimination_Behaviour",
    "/media/matthew/Seagate Expansion Drive2/Learning_Behaviour_Data/NXAK7.1B/2021_02_24_Discrimination_Imaging"],

]


control_mouse_meta_list = []
mutant_mouse_meta_list = []

for mouse in control_mice_list:
    mouse_d_prime_list = []
    for session in mouse:

        # Load Performance Dictionary
        performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        hits = performance_dictionary["visual_hits.npy"]
        misses = performance_dictionary["visual_misses.npy"]
        vis_1_percentage_correct = (float(hits) / (hits + misses)) * 100
        mouse_d_prime_list.append(vis_1_percentage_correct)

    control_mouse_meta_list.append(mouse_d_prime_list)
    plt.plot(mouse_d_prime_list, c='b')



for mouse in mutant_mouse_list:
    mouse_d_prime_list = []
    for session in mouse:

        # Load Performance Dictionary
        performance_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        hits = performance_dictionary["visual_hits.npy"]
        misses = performance_dictionary["visual_misses.npy"]
        print("Hits", hits)
        print("Misses", misses)
        vis_1_percentage_correct = (float(hits) / (hits + misses)) * 100
        print("vis 1 perfentage correct", vis_1_percentage_correct)
        mouse_d_prime_list.append(vis_1_percentage_correct)

    mutant_mouse_meta_list.append(mouse_d_prime_list)
    plt.plot(mouse_d_prime_list, c='g')
plt.show()



plt.title("Rewarded Grating Performance")
control_group_mean, control_sems = get_group_mean(control_mouse_meta_list)
mutant_group_mean, mutant_sems = get_group_mean(mutant_mouse_meta_list)

plt.plot(control_group_mean, c='b', label="Wildtype")
plt.plot(mutant_group_mean, c='g', label="Homozygous")

control_upper_bound = np.add(control_group_mean, control_sems)
control_lower_bound = np.subtract(control_group_mean, control_sems)

mutant_upper_bound = np.add(mutant_group_mean, mutant_sems)
mutant_lower_bound = np.subtract(mutant_group_mean, mutant_sems)

print(control_sems)
mutant_x_values = list(range(len(mutant_group_mean)))
control_x_values = list(range(len(control_group_mean)))
plt.fill_between(x=control_x_values, y1=control_lower_bound, y2=control_upper_bound, color='b', alpha=0.2)
plt.fill_between(x=mutant_x_values, y1=mutant_lower_bound, y2=mutant_upper_bound, color='g', alpha=0.2)

plt.ylim([0, 100])
plt.legend()
plt.xlabel("Sesion")
plt.ylabel("d prime")
plt.show()

