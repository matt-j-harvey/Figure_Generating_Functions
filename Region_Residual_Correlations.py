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



def transform_clusters(clusters, variable_dictionary, invert=False):

    # Unpack Dict
    angle = variable_dictionary['rotation']
    x_shift = variable_dictionary['x_shift']
    y_shift = variable_dictionary['y_shift']

    # Invert
    if invert == True:
        angle = -1 * angle
        x_shift = -1 * x_shift
        y_shift = -1 * y_shift

    transformed_clusters = np.zeros(np.shape(clusters))

    unique_clusters = list(np.unique(clusters))
    for cluster in unique_clusters:
        cluster_mask = np.where(clusters == cluster, 1, 0)
        cluster_mask = ndimage.rotate(cluster_mask, angle, reshape=False, prefilter=True)
        cluster_mask = np.roll(a=cluster_mask, axis=0, shift=y_shift)
        cluster_mask = np.roll(a=cluster_mask, axis=1, shift=x_shift)
        cluster_indicies = np.nonzero(cluster_mask)
        transformed_clusters[cluster_indicies] = cluster

    return transformed_clusters


def reshape_coefficients(coefficients, indicies, height, width):

    reshaped_coefficients = []
    for timepoint in coefficients:
        reshaped_timepoint = Widefield_General_Functions.create_image_from_data(timepoint, indicies, height, width)
        reshaped_coefficients.append(reshaped_timepoint)

    reshaped_coefficients = np.array(reshaped_coefficients)
    reshaped_coefficients = np.nan_to_num(reshaped_coefficients)

    return reshaped_coefficients



def get_condition_average_correlation(session_list, clusters):

    # Create Empty Lists To Hold Variables
    group_condition_1_array = []
    group_condition_2_array = []

    selected_regions = [56, 2]


    # Iterate Through Session
    for base_directory in session_list:

        # Load Cluster Alignment Dictioanry
        alignment_dictionary = np.load(os.path.join(base_directory, "Cluster_Alignment_Dictionary.npy"), allow_pickle=True)[()]

        # Align Clusters
        aligned_clusters = transform_clusters(clusters, alignment_dictionary, invert=True)

        # Get Selected indicies
        selected_region_indicies = []
        for region in selected_regions:
            region = np.where(aligned_clusters == region, 1, 0)
            region_indicies = np.nonzero(region)
            for index in region_indicies:
                selected_region_indicies.append(index)

        # Create Empty Lists To Hold Variables
        session_condition_1_array = []
        session_condition_2_array = []

        # Open Regression Dictionary
        regression_dictionary = np.load(os.path.join(base_directory, "Simple_Regression", "Simple_Regression_Model.npy"), allow_pickle=True)[()]

        # Load Mask
        indicies, image_height, image_width = load_generous_mask(base_directory)

        # Load Alignment Dictionary
        alignment_dictionary = np.load(os.path.join(base_directory, "Cluster_Alignment_Dictionary.npy"), allow_pickle=True)[()]

        # Unpack Regression Dictionary
        partial_determination_matrix = regression_dictionary["Coefficients_of_Partial_Determination"]
        start_window = regression_dictionary["Start_Window"]
        stop_window = regression_dictionary["Stop_Window"]
        trial_length = stop_window - start_window

        condition_1_coefs = partial_determination_matrix[0:trial_length]
        condition_2_coefs = partial_determination_matrix[trial_length:2*trial_length]

        condition_1_coefs = reshape_coefficients(condition_1_coefs, indicies, image_height, image_width)
        condition_2_coefs = reshape_coefficients(condition_2_coefs, indicies, image_height, image_width)

        # Reshape Coefficients


        # Get Region Average Trace
        print("Condition 1 coefs", np.shape(condition_1_coefs))
        selected_region_trace = condition_1_coefs[:, selected_region_indicies]
        print("Selected Region Trace", np.shape(selected_region_trace))

        selected_region_trace = np.mean(selected_region_trace, axis=1)

        for timepoint_index in range(trial_length):

            # Get Timepoint Coefficients
            condition_1_timepoint_coefs = condition_1_coefs[timepoint_index]
            condition_2_timepoint_coefs = condition_2_coefs[timepoint_index]

            # Reconstruct Image
            condition_1_timepoint_coefs = Widefield_General_Functions.create_image_from_data(condition_1_timepoint_coefs, indicies, image_height, image_width)
            condition_2_timepoint_coefs = Widefield_General_Functions.create_image_from_data(condition_2_timepoint_coefs, indicies, image_height, image_width)

            # Align Image
            condition_1_timepoint_coefs = transform_image(condition_1_timepoint_coefs, alignment_dictionary)
            condition_2_timepoint_coefs = transform_image(condition_2_timepoint_coefs, alignment_dictionary)

            # Get

            # Smooth Image
            #condition_1_timepoint_coefs = ndimage.gaussian_filter(condition_1_timepoint_coefs, sigma=2)
            #condition_2_timepoint_coefs = ndimage.gaussian_filter(condition_2_timepoint_coefs, sigma=2)

            # Append To List
            session_condition_1_array.append(condition_1_timepoint_coefs)
            session_condition_2_array.append(condition_2_timepoint_coefs)

        group_condition_1_array.append(session_condition_1_array)
        group_condition_2_array.append(session_condition_2_array)

    group_condition_1_array = np.mean(group_condition_1_array, axis=0)
    group_condition_2_array = np.mean(group_condition_2_array, axis=0)

    return group_condition_1_array, group_condition_2_array


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



def transform_atlas_regions(atlas_regions, transformation_dictionary):

    transformed_atlas = np.zeros(np.shape(atlas_regions))

    unique_regions = np.unique(atlas_regions)

    for region in unique_regions:
        region_mask = np.where(atlas_regions == region, 1, 0)
        transformed_mask = transform_image(region_mask, transformation_dictionary)
        transformed_mask = np.where(transformed_mask > 0.5, 1, 0)
        transformed_region_pixels = np.nonzero(transformed_mask)
        transformed_atlas[transformed_region_pixels] = region

    return transformed_atlas



def create_correlation_figure(session_list, save_directory):

    number_of_sessions = len(session_list)

    # Get Fine Mask and Atlas Outlines
    mask_location = "/home/matthew/Documents/Allen_Atlas_Templates/Mask_Array.npy"
    atlas_outline_location = "/home/matthew/Documents/Allen_Atlas_Templates/New_Outline.npy"
    final_consensus_clusters = np.load("/media/matthew/Expansion/Widefield_Analysis/Consensus_Clustering/Final_Consensus_Clusters.npy")

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
    vmax = 0.005
    activity_colourmap = cm.ScalarMappable(cmap='viridis')
    difference_colourmap = cm.ScalarMappable(cmap='bwr')
    activity_colourmap.set_clim(vmin=vmin, vmax=vmax)
    difference_colourmap.set_clim(vmin=-vmax, vmax=vmax)

    # Split Sessions By D Prime
    intermeidate_threshold = 1
    post_threshold = 2
    pre_learning_sessions, intermediate_learning_sessions, post_learning_sessions = split_sessions_By_d_prime(session_list, intermeidate_threshold, post_threshold)
    print("Pre Learning Sessions", pre_learning_sessions)
    print("Intermediate Learning Sessions", intermediate_learning_sessions)
    print("Post Learning Sessions", post_learning_sessions)

    # Get Learning Type Averages
    pre_learning_vis_1, pre_learning_vis_2 = get_condition_average_correlation(pre_learning_sessions, final_consensus_clusters)
    #intermediate_learning_vis_1, intermediate_learning_vis_2 = get_condition_average_correlation(intermediate_learning_sessions)
    #post_learning_vis_1, post_learning_vis_2 = get_condition_average_correlation(post_learning_sessions)

    plt.ion()
    figure_1 = plt.figure()
    number_of_timepoints = np.shape(pre_learning_vis_1)[0]
    print("Number Of Timepoints")

    for timepoint_index in range(number_of_timepoints):
        print("Timepoint index")

        gridspec_1 = GridSpec(nrows=3, ncols=3)

        # Create Axes
        pre_vis_1_axis = figure_1.add_subplot(gridspec_1[0, 0])
        pre_vis_2_axis = figure_1.add_subplot(gridspec_1[1, 0])
        pre_diff_axis = figure_1.add_subplot(gridspec_1[2, 0])

        intermediate_vis_1_axis = figure_1.add_subplot(gridspec_1[0, 1])
        intermediate_vis_2_axis = figure_1.add_subplot(gridspec_1[1, 1])
        intermediate_diff_axis = figure_1.add_subplot(gridspec_1[2, 1])

        post_vis_1_axis = figure_1.add_subplot(gridspec_1[0, 2])
        post_vis_2_axis = figure_1.add_subplot(gridspec_1[1, 2])
        post_diff_axis = figure_1.add_subplot(gridspec_1[2, 2])


        # Get Difference Images
        pre_diff_image = np.subtract(pre_learning_vis_1[timepoint_index], pre_learning_vis_2[timepoint_index])
        intermediate_diff_image = np.subtract(intermediate_learning_vis_1[timepoint_index], intermediate_learning_vis_2[timepoint_index])
        post_diff_image = np.subtract(post_learning_vis_1[timepoint_index], post_learning_vis_2[timepoint_index])


        # Create Images
        pre_learning_vis_1_image          = activity_colourmap.to_rgba(pre_learning_vis_1[timepoint_index])
        intermediate_learning_vis_1_image = activity_colourmap.to_rgba(intermediate_learning_vis_1[timepoint_index])
        post_learning_vis_1_image         = activity_colourmap.to_rgba(post_learning_vis_1[timepoint_index])

        pre_learning_vis_2_image          = activity_colourmap.to_rgba(pre_learning_vis_2[timepoint_index])
        intermediate_learning_vis_2_image = activity_colourmap.to_rgba(intermediate_learning_vis_2[timepoint_index])
        post_learning_vis_2_image         = activity_colourmap.to_rgba(post_learning_vis_2[timepoint_index])

        pre_diff_image          = difference_colourmap.to_rgba(pre_diff_image)
        intermediate_diff_image = difference_colourmap.to_rgba(intermediate_diff_image)
        post_diff_image         = difference_colourmap.to_rgba(post_diff_image)


        # Add Masks
        pre_learning_vis_1_image[inverse_mask_pixels] = [1,1,1,1]
        intermediate_learning_vis_1_image[inverse_mask_pixels] = [1,1,1,1]
        post_learning_vis_1_image[inverse_mask_pixels] = [1,1,1,1]

        pre_learning_vis_2_image[inverse_mask_pixels] = [1,1,1,1]
        intermediate_learning_vis_2_image[inverse_mask_pixels] = [1,1,1,1]
        post_learning_vis_2_image[inverse_mask_pixels] = [1,1,1,1]

        pre_diff_image[inverse_mask_pixels] = [1,1,1,1]
        intermediate_diff_image[inverse_mask_pixels] = [1,1,1,1]
        post_diff_image[inverse_mask_pixels] = [1,1,1,1]


        # Add Atlas Outlines
        pre_learning_vis_1_image[atlas_outline_pixels] = [0,0,0,0]
        intermediate_learning_vis_1_image[atlas_outline_pixels] = [0,0,0,0]
        post_learning_vis_1_image[atlas_outline_pixels] = [0,0,0,0]

        pre_learning_vis_2_image[atlas_outline_pixels] = [0,0,0,0]
        intermediate_learning_vis_2_image[atlas_outline_pixels] = [0,0,0,0]
        post_learning_vis_2_image[atlas_outline_pixels] = [0,0,0,0]

        pre_diff_image[atlas_outline_pixels] = [0,0,0,0]
        intermediate_diff_image[atlas_outline_pixels] = [0,0,0,0]
        post_diff_image[atlas_outline_pixels] = [0,0,0,0]


        # Plot These Images
        pre_vis_1_axis.imshow(pre_learning_vis_1_image)
        pre_vis_2_axis.imshow(pre_learning_vis_2_image)
        pre_diff_axis.imshow(pre_diff_image)

        intermediate_vis_1_axis.imshow(intermediate_learning_vis_1_image)
        intermediate_vis_2_axis.imshow(intermediate_learning_vis_2_image)
        intermediate_diff_axis.imshow(intermediate_diff_image)

        post_vis_1_axis.imshow(post_learning_vis_1_image)
        post_vis_2_axis.imshow(post_learning_vis_2_image)
        post_diff_axis.imshow(post_diff_image)



        # Remove Axes

        # Create Axes
        pre_vis_1_axis.axis('off')
        pre_vis_2_axis.axis('off')
        pre_diff_axis.axis('off')

        intermediate_vis_1_axis.axis('off')
        intermediate_vis_2_axis.axis('off')
        intermediate_diff_axis.axis('off')

        post_vis_1_axis.axis('off')
        post_vis_2_axis.axis('off')
        post_diff_axis.axis('off')

        plt.draw()
        plt.pause(0.1)
        plt.savefig(os.path.join(save_directory, str(timepoint_index).zfill(3)))
        plt.clf()



session_list = [
     "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_04_Discrimination_Imaging",
     "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_06_Discrimination_Imaging",
     "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_08_Discrimination_Imaging",
     "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_10_Discrimination_Imaging",
     "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_12_Discrimination_Imaging",
     "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_14_Discrimination_Imaging",
     "/media/matthew/Expansion/Widefield_Analysis/NXAK4.1B/2021_02_22_Discrimination_Imaging"]

save_directory = "/media/matthew/Expansion/Widefield_Analysis/Discrimination_Analysis/Average_CPDs"

create_correlation_figure(session_list, save_directory)
