import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.gridspec import GridSpec
import sys
from scipy import ndimage
from skimage.transform import resize
from skimage.segmentation import chan_vese
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



def get_condition_average(session_list, model_name, selected_pixels):

    # Create Empty Lists To Hold Variables
    group_condition_list = []

    # Iterate Through Session
    for base_directory in session_list:

        # Create Empty List To Hold Trace For Each Condition For Each Animal
        animal_condition_traces = []

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
        coefficient_matrix = np.nan_to_num(coefficient_matrix)
        number_of_conditions = len(coefficient_matrix)

        for condition_index in range(number_of_conditions):
            condition_region_trace = []
            condition_coefs = coefficient_matrix[condition_index]
            condition_coefs = np.transpose(condition_coefs)

            for timepoint_index in range(trial_length):

                # Get Timepoint Coefficients
                condition_timepoint_coefs = condition_coefs[timepoint_index]

                # Reconstruct Image
                condition_timepoint_coefs = Widefield_General_Functions.create_image_from_data(condition_timepoint_coefs, indicies, image_height, image_width)

                # Align Image
                condition_timepoint_coefs = transform_image(condition_timepoint_coefs, alignment_dictionary)

                # Get Region Pixels
                region_coefs = condition_timepoint_coefs[selected_pixels]

                # Get Region Mean
                region_mean = np.mean(region_coefs)

                # Add To List
                condition_region_trace.append(region_mean)

            animal_condition_traces.append(condition_region_trace)
        group_condition_list.append(animal_condition_traces)


    # Axis 0 = Number of Sessions
    # Axis 1 = Condition
    # Axis 2 = Time

    group_condition_list = np.array(group_condition_list)

    number_of_sessions, number_of_conditions, number_of_timepoints = np.shape(group_condition_list)

    condition_mean_traces = np.mean(group_condition_list, axis=0)
    condition_sd_traces = np.std(group_condition_list, axis=0)

    return condition_mean_traces, condition_sd_traces



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


def transform_region_mask(region_assignments, variable_dictionary):


    image_height = 600
    image_width = 608

    # Unpack Dictionary
    angle = variable_dictionary['rotation']
    x_shift = variable_dictionary['x_shift']
    y_shift = variable_dictionary['y_shift']
    x_scale = variable_dictionary['x_scale']
    y_scale = variable_dictionary['y_scale']

    transformed_image = np.zeros(np.shape(region_assignments))

    # Calculate New Height
    original_height, original_width = np.shape(transformed_image)
    new_height = int(original_height * y_scale)
    new_width = int(original_width * x_scale)

    # Get Unique Regions
    unique_regions = np.unique(region_assignments)
    for region in unique_regions:

        region_mask = np.where(region_assignments == region, 1, 0)

        # Scale
        region_mask = resize(region_mask, (new_height, new_width), preserve_range=True)

        # Rotate
        region_mask = ndimage.rotate(region_mask, angle, reshape=False, prefilter=True)

        # Insert Into Background
        mask_height, mask_width = np.shape(region_mask)
        centre_x = 200
        centre_y = 200
        background_array = np.zeros((1000, 1000))
        x_start = centre_x + x_shift
        x_stop = x_start + mask_width

        y_start = centre_y + y_shift
        y_stop = y_start + mask_height

        background_array[y_start:y_stop, x_start:x_stop] = region_mask

        # Take Chunk
        region_mask = background_array[centre_y:centre_y + image_height, centre_x:centre_x + image_width]

        # Rebinarize
        transformed_image = np.where(region_mask > 0.5, region, transformed_image)

    return transformed_image




def get_time_window(session_list):

    # Open Regression Dictionary
    regression_dictionary = np.load(os.path.join(session_list[0], "Simple_Regression", "Simple_Regression_Model.npy"), allow_pickle=True)[()]

    start_window = regression_dictionary["Start_Window"]
    stop_window = regression_dictionary["Stop_Window"]

    return start_window, stop_window


def quantify_regression_coefficients(condition_1_session_list, condition_2_session_list, model_name, save_directory):

    # Get Fine Mask and Atlas Outlines
    mask_location = "/home/matthew/Documents/Allen_Atlas_Templates/Mask_Array.npy"
    atlas_outline_location = "/home/matthew/Documents/Allen_Atlas_Templates/New_Outline.npy"
    atlas_regions_location = "/home/matthew/Documents/Allen_Atlas_Templates/New_Outline_Regions.npy"

    fine_mask = np.load(mask_location)
    atlas_outline = np.load(atlas_outline_location)
    atlas_regions = np.load(atlas_regions_location)

    mask_alignment_dictionary = np.load("/media/matthew/Expansion/Widefield_Analysis/Consensus_Clustering/Consensus_Cluster_Mask_Alignment_Dictionary.npy", allow_pickle=True)[()]
    atlas_alignment_dictionary = np.load("/media/matthew/Expansion/Widefield_Analysis/Consensus_Clustering/Consensus_Cluster_Atlas_Alignment_Dictionary.npy", allow_pickle=True)[()]

    fine_mask = transform_mask_or_atlas(fine_mask, mask_alignment_dictionary)
    atlas_outline = transform_mask_or_atlas(atlas_outline, atlas_alignment_dictionary)
    atlas_regions = transform_region_mask(atlas_regions, atlas_alignment_dictionary)

    plt.imshow(atlas_outline)
    plt.show()

    plt.imshow(atlas_regions)
    plt.show()

    # Get Time Window
    timestep = 36
    start_window, stop_window = get_time_window(condition_1_session_list)
    x_values = list(range(start_window , stop_window))
    x_values = np.multiply(x_values, timestep)

    # Get Regions Of Selected pixes
    selected_regions = [4,6]
    #selected_regions = [34, 38]
    selected_regions_mask = np.zeros(np.shape(atlas_regions))
    for region in selected_regions:
        selected_regions_mask = np.where(atlas_regions == region, 1, selected_regions_mask)

    selected_pixels = np.nonzero(selected_regions_mask)
    plt.imshow(selected_regions_mask)
    plt.show()

    # Get Learning Type Averages
    group_1_condition_mean_traces, group_1_condition_sd_traces = get_condition_average(condition_1_session_list, model_name, selected_pixels)
    group_2_condition_mean_traces, group_2_condition_sd_traces = get_condition_average(condition_2_session_list, model_name, selected_pixels)

    number_of_conditions = np.shape(group_2_condition_sd_traces)[1]

    for condition_index in range(number_of_conditions):

        group_1_mean_trace = group_1_condition_mean_traces[condition_index]
        group_1_std_trace = group_1_condition_sd_traces[condition_index]

        group_2_mean_trace = group_2_condition_mean_traces[condition_index]
        group_2_std_trace = group_2_condition_sd_traces[condition_index]

        group_1_std_upper_bound = np.add(group_1_mean_trace, group_1_std_trace)
        group_1_std_lower_bound = np.subtract(group_1_mean_trace, group_1_std_trace)

        group_2_std_upper_bound = np.add(group_2_mean_trace, group_2_std_trace)
        group_2_std_lower_bound = np.subtract(group_2_mean_trace, group_2_std_trace)

        plt.plot(x_values, group_1_mean_trace, c='b')
        plt.plot(x_values, group_2_mean_trace, color='orange')

        plt.fill_between(x=x_values, y1=group_1_std_upper_bound, y2=group_1_std_lower_bound, alpha=0.2, color='b')
        plt.fill_between(x=x_values, y1=group_2_std_upper_bound, y2=group_2_std_lower_bound, alpha=0.2, color='orange')

        plt.show()



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
]


#save_directory = "/media/matthew/Expansion/Widefield_Analysis/Discrimination_Analysis/Average_Coefs/Controls"
save_directory = None
model_name = "All_Vis_1_All_Vis_2"
quantify_regression_coefficients(control_session_list[0:3], mutant_session_list[0:3], model_name, save_directory)
