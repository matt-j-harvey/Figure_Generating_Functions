import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.gridspec import GridSpec
import sys
from scipy import ndimage
from skimage.transform import resize
sys.path.append("/home/matthew/Documents/Github_Code/Widefield_Preprocessing")
import Widefield_General_Functions

from matplotlib.pyplot import cm

def load_generous_mask(home_directory):

    # Loads the mask for a video, returns a list of which pixels are included, as well as the original image height and width
    mask = np.load(home_directory + "/Generous_Mask.npy")

    image_height = np.shape(mask)[0]
    image_width = np.shape(mask)[1]

    mask = np.where(mask>0.1, 1, 0)
    mask = mask.astype(int)
    flat_mask = np.ndarray.flatten(mask)
    indicies = np.argwhere(flat_mask)
    indicies = np.ndarray.astype(indicies, int)
    indicies = np.ndarray.flatten(indicies)

    return indicies, image_height, image_width

def transform_image(image, variable_dictionary, invert=False):

    # Unpack Dict
    angle = variable_dictionary['rotation']
    x_shift = variable_dictionary['x_shift']
    y_shift = variable_dictionary['y_shift']

    # Inverse
    if invert == True:
        angle = -1 * angle
        x_shift = -1 * x_shift
        y_shift = -1 * y_shift

    transformed_image = np.copy(image)
    transformed_image = ndimage.rotate(transformed_image, angle, reshape=False, prefilter=True)
    transformed_image = np.roll(a=transformed_image, axis=0, shift=y_shift)
    transformed_image = np.roll(a=transformed_image, axis=1, shift=x_shift)

    return transformed_image



def split_sessions_By_d_prime(session_list, intermediate_threshold, post_threshold):

    pre_learning_sessions = []
    intermediate_learning_sessions = []
    post_learning_sessions = []

    # Iterate Throug Sessions
    for session in session_list:

        # Load D Prime
        behavioural_dictionary = np.load(os.path.join(session, "Behavioural_Measures", "Performance_Dictionary.npy"), allow_pickle=True)[()]
        d_prime = behavioural_dictionary["visual_d_prime"]

        if d_prime >= post_threshold:
            post_learning_sessions.append(session)

        if d_prime < post_threshold and d_prime >= intermediate_threshold:
            intermediate_learning_sessions.append(session)

        if d_prime < intermediate_threshold:
            pre_learning_sessions.append(session)

    return pre_learning_sessions, intermediate_learning_sessions, post_learning_sessions



def get_condition_average(session_list, model_name, selected_coefficient):

    # Create Empty Lists To Hold Variables
    group_condition_1_array = []

    # Iterate Through Session
    for base_directory in session_list:

        # Create Empty Lists To Hold Variables
        session_condition_1_array = []

        # Open Regression Dictionary
        regression_dictionary = np.load(os.path.join(base_directory, "Simple_Regression", model_name + "_Regression_Model.npy"), allow_pickle=True)[()]

        # Load Mask
        indicies, image_height, image_width = load_generous_mask(base_directory)

        # Load Alignment Dictionary
        alignment_dictionary = np.load(os.path.join(base_directory, "Cluster_Alignment_Dictionary.npy"), allow_pickle=True)[()]

        # Unpack Regression Dictionary
        coefficient_matrix = regression_dictionary["Regression_Coefficients"]
        start_window = regression_dictionary["Start_Window"]
        stop_window = regression_dictionary["Stop_Window"]
        trial_length = stop_window - start_window
        condition_1_coefs = coefficient_matrix[selected_coefficient]
        condition_1_coefs = np.transpose(condition_1_coefs)
        condition_1_coefs = np.nan_to_num(condition_1_coefs)

        for timepoint_index in range(trial_length):

            # Get Timepoint Coefficients
            condition_1_timepoint_coefs = condition_1_coefs[timepoint_index]

            # Reconstruct Image
            condition_1_timepoint_coefs = Widefield_General_Functions.create_image_from_data(condition_1_timepoint_coefs, indicies, image_height, image_width)

            # Align Image
            condition_1_timepoint_coefs = transform_image(condition_1_timepoint_coefs, alignment_dictionary)

            # Smooth Image
            #condition_1_timepoint_coefs = ndimage.gaussian_filter(condition_1_timepoint_coefs, sigma=2)

            # Append To List
            session_condition_1_array.append(condition_1_timepoint_coefs)


        group_condition_1_array.append(session_condition_1_array)

    group_condition_1_array = np.mean(group_condition_1_array, axis=0)

    return group_condition_1_array


def transform_mask_or_atlas(image, variable_dictionary):

    image_height = 600
    image_width = 608

    # Unpack Dictionary
    angle = variable_dictionary['rotation']
    x_shift = variable_dictionary['x_shift']
    y_shift = variable_dictionary['y_shift']
    x_scale = variable_dictionary['x_scale']
    y_scale = variable_dictionary['y_scale']

    # Copy
    transformed_image = np.copy(image)

    # Scale
    original_height, original_width = np.shape(transformed_image)
    new_height = int(original_height * y_scale)
    new_width = int(original_width * x_scale)
    transformed_image = resize(transformed_image, (new_height, new_width), preserve_range=True)
    print("new image height", np.shape(transformed_image))

    # Rotate
    transformed_image = ndimage.rotate(transformed_image, angle, reshape=False, prefilter=True)

    # Insert Into Background
    mask_height, mask_width = np.shape(transformed_image)
    centre_x = 200
    centre_y = 200
    background_array = np.zeros((1000, 1000))
    x_start = centre_x + x_shift
    x_stop = x_start + mask_width

    y_start = centre_y + y_shift
    y_stop = y_start + mask_height

    background_array[y_start:y_stop, x_start:x_stop] = transformed_image

    # Take Chunk
    transformed_image = background_array[centre_y:centre_y + image_height, centre_x:centre_x + image_width]

    # Rebinarize
    transformed_image = np.where(transformed_image > 0.5, 1, 0)

    return transformed_image


def get_time_window(session_list):

    # Open Regression Dictionary
    regression_dictionary = np.load(os.path.join(session_list[0], "Simple_Regression", "Simple_Regression_Model.npy"), allow_pickle=True)[()]

    start_window = regression_dictionary["Start_Window"]
    stop_window = regression_dictionary["Stop_Window"]

    return start_window, stop_window


def create_genotype_regression_figure(control_session_list, mutant_session_list, model_name, save_directory, selected_coefficient):


    # Get Fine Mask and Atlas Outlines
    mask_location = "/home/matthew/Documents/Allen_Atlas_Templates/Mask_Array.npy"
    atlas_outline_location = "/home/matthew/Documents/Allen_Atlas_Templates/New_Outline.npy"

    fine_mask = np.load(mask_location)
    atlas_outline = np.load(atlas_outline_location)

    mask_alignment_dictionary = np.load("/media/matthew/Expansion/Widefield_Analysis/Consensus_Clustering/Consensus_Cluster_Mask_Alignment_Dictionary.npy", allow_pickle=True)[()]
    atlas_alignment_dictionary = np.load("/media/matthew/Expansion/Widefield_Analysis/Consensus_Clustering/Consensus_Cluster_Atlas_Alignment_Dictionary.npy", allow_pickle=True)[()]

    fine_mask = transform_mask_or_atlas(fine_mask, mask_alignment_dictionary)
    atlas_outline = transform_mask_or_atlas(atlas_outline, atlas_alignment_dictionary)

    inverse_mask = np.where(fine_mask == 1, 0, 1)
    inverse_mask_pixels = np.nonzero(inverse_mask)
    atlas_outline_pixels = np.nonzero(atlas_outline)

    # Get Colourmaps
    vmin = 0
    vmax = 0.1
    diff_scale_factor = 0.5
    activity_colourmap = cm.ScalarMappable(cmap='jet')
    difference_colourmap = cm.ScalarMappable(cmap='bwr')
    activity_colourmap.set_clim(vmin=vmin, vmax=vmax)
    difference_colourmap.set_clim(vmin=-(vmax*diff_scale_factor), vmax=(vmax*diff_scale_factor))

    # Get Time Window
    timestep = 36
    start_window, stop_window = get_time_window(control_session_list)
    x_values = list(range(start_window , stop_window))
    x_values = np.multiply(x_values, timestep)

    # Split Sessions By D Prime
    intermeidate_threshold = 1
    post_threshold = 2
    control_pre_learning_sessions, control_intermediate_learning_sessions, control_post_learning_sessions = split_sessions_By_d_prime(control_session_list, intermeidate_threshold, post_threshold)
    mutant_pre_learning_sessions, mutant_intermediate_learning_sessions, mutant_post_learning_sessions = split_sessions_By_d_prime(mutant_session_list, intermeidate_threshold, post_threshold)

    # Get Learning Type Averages
    control_pre_learning = get_condition_average(control_pre_learning_sessions, model_name, selected_coefficient)
    control_intermediate_learning = get_condition_average(control_intermediate_learning_sessions, model_name, selected_coefficient)
    control_post_learning = get_condition_average(control_post_learning_sessions, model_name, selected_coefficient)

    mutant_pre_learning = get_condition_average(mutant_pre_learning_sessions, model_name, selected_coefficient)
    mutant_intermediate_learning = get_condition_average(mutant_intermediate_learning_sessions, model_name, selected_coefficient)
    mutant_post_learning = get_condition_average(mutant_post_learning_sessions, model_name, selected_coefficient)

    plt.ion()
    figure_1 = plt.figure(figsize=(75,100))
    number_of_timepoints = np.shape(control_pre_learning)[0]
    print("Number Of Timepoints")

    for timepoint_index in range(number_of_timepoints):
        print("Timepoint index", timepoint_index)

        figure_1.suptitle(str(x_values[timepoint_index]) + "ms")

        gridspec_1 = GridSpec(nrows=3, ncols=3)

        # Create Axes
        control_pre_axis = figure_1.add_subplot(gridspec_1[0, 0])
        mutant_pre_axis = figure_1.add_subplot(gridspec_1[1, 0])
        pre_diff_axis = figure_1.add_subplot(gridspec_1[2, 0])

        control_intermediate_axis = figure_1.add_subplot(gridspec_1[0, 1])
        mutant_intermediate_axis = figure_1.add_subplot(gridspec_1[1, 1])
        intermediate_diff_axis = figure_1.add_subplot(gridspec_1[2, 1])

        control_post_axis = figure_1.add_subplot(gridspec_1[0, 2])
        mutant_post_axis = figure_1.add_subplot(gridspec_1[1, 2])
        post_diff_axis = figure_1.add_subplot(gridspec_1[2, 2])
        
        # Get Difference Images
        pre_diff_image          = np.subtract(control_pre_learning[timepoint_index],            mutant_pre_learning[timepoint_index])
        intermediate_diff_image = np.subtract(control_intermediate_learning[timepoint_index],   mutant_intermediate_learning[timepoint_index])
        post_diff_image         = np.subtract(control_post_learning[timepoint_index],           mutant_post_learning[timepoint_index])


        # Create Images
        control_pre_learning_image          = activity_colourmap.to_rgba(control_pre_learning[timepoint_index])
        control_intermediate_learning_image = activity_colourmap.to_rgba(control_intermediate_learning[timepoint_index])
        control_post_learning_image         = activity_colourmap.to_rgba(control_post_learning[timepoint_index])

        mutant_pre_learning_image          = activity_colourmap.to_rgba(mutant_pre_learning[timepoint_index])
        mutant_intermediate_learning_image = activity_colourmap.to_rgba(mutant_intermediate_learning[timepoint_index])
        mutant_post_learning_image         = activity_colourmap.to_rgba(mutant_post_learning[timepoint_index])

        pre_diff_image          = difference_colourmap.to_rgba(pre_diff_image)
        intermediate_diff_image = difference_colourmap.to_rgba(intermediate_diff_image)
        post_diff_image         = difference_colourmap.to_rgba(post_diff_image)


        # Add Masks
        control_pre_learning_image[inverse_mask_pixels] = [1,1,1,1]
        control_intermediate_learning_image[inverse_mask_pixels] = [1,1,1,1]
        control_post_learning_image[inverse_mask_pixels] = [1,1,1,1]

        mutant_pre_learning_image[inverse_mask_pixels] = [1,1,1,1]
        mutant_intermediate_learning_image[inverse_mask_pixels] = [1,1,1,1]
        mutant_post_learning_image[inverse_mask_pixels] = [1,1,1,1]

        pre_diff_image[inverse_mask_pixels] = [1,1,1,1]
        intermediate_diff_image[inverse_mask_pixels] = [1,1,1,1]
        post_diff_image[inverse_mask_pixels] = [1,1,1,1]


        # Add Atlas Outlines
        control_pre_learning_image[atlas_outline_pixels] = [0,0,0,0]
        control_intermediate_learning_image[atlas_outline_pixels] = [0,0,0,0]
        control_post_learning_image[atlas_outline_pixels] = [0,0,0,0]

        mutant_pre_learning_image[atlas_outline_pixels] = [0,0,0,0]
        mutant_intermediate_learning_image[atlas_outline_pixels] = [0,0,0,0]
        mutant_post_learning_image[atlas_outline_pixels] = [0,0,0,0]

        pre_diff_image[atlas_outline_pixels] = [0,0,0,0]
        intermediate_diff_image[atlas_outline_pixels] = [0,0,0,0]
        post_diff_image[atlas_outline_pixels] = [0,0,0,0]


        # Plot These Images
        control_pre_axis.imshow(control_pre_learning_image)
        control_intermediate_axis.imshow(control_intermediate_learning_image)
        control_post_axis.imshow(control_post_learning_image)

        mutant_pre_axis.imshow(mutant_pre_learning_image)
        mutant_intermediate_axis.imshow(mutant_intermediate_learning_image)
        mutant_post_axis.imshow(mutant_post_learning_image)

        pre_diff_axis.imshow(pre_diff_image)
        intermediate_diff_axis.imshow(intermediate_diff_image)
        post_diff_axis.imshow(post_diff_image)


        # Remove Axes
        control_pre_axis.axis('off')
        mutant_pre_axis.axis('off')
        pre_diff_axis.axis('off')

        control_intermediate_axis.axis('off')
        mutant_intermediate_axis.axis('off')
        intermediate_diff_axis.axis('off')

        control_post_axis.axis('off')
        mutant_post_axis.axis('off')
        post_diff_axis.axis('off')


        plt.draw()
        plt.pause(0.1)
        plt.savefig(os.path.join(save_directory, str(timepoint_index).zfill(3)))
        plt.clf()





"""



"""


control_session_list = [
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_04_Discrimination_Imaging",
    #"/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_06_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_08_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_10_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_12_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_14_Discrimination_Imaging",
    "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_22_Discrimination_Imaging",

    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_15_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_17_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_19_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_21_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NRXN78.1A/2020_11_24_Discrimination_Imaging",

    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_09_25_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_09_29_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_01_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_03_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_05_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_07_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK22.1A/2021_10_08_Discrimination_Imaging",

]


mutant_session_list = [
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_08_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_10_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_12_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_14_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_18_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_23_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_25_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_02_27_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_03_01_Discrimination_Imaging",
    #r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_03_03_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK4.1A/2021_03_05_Discrimination_Imaging",

    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_09_28_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_09_30_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_09_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_11_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_13_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_15_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_17_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK20.1B/2021_10_19_Discrimination_Imaging",

    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_04_30_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_02_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_04_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_06_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_08_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_10_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_12_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_14_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_16_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_18_Discrimination_Imaging",
    r"/media/matthew/Seagate Expansion Drive1/Processed_Widefield_Data/NXAK16.1B/2021_05_20_Discrimination_Imaging",

]



save_directory = "/media/matthew/Expansion/Widefield_Analysis/Discrimination_Analysis/Average_Coefs/Genotype_Comparison"
save_directory = "/media/matthew/Expansion/Widefield_Analysis/Discrimination_Analysis/Average_Coefs/Genotype_Comparison_Vis_2"
model_name = "All_Vis_1_All_Vis_2"
selected_coefficient = 1
create_genotype_regression_figure(control_session_list, mutant_session_list, model_name, save_directory, selected_coefficient)

