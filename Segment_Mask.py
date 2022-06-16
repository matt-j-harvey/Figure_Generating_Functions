import numpy as np
import matplotlib.pyplot as plt
from skimage import data, filters, color, morphology
from skimage.segmentation import flood, flood_fill
from skimage.morphology import remove_small_objects
from scipy import ndimage as ndi



"""
def segment_outlines(outline_image):

    image_height, image_width = np.shape(outline_image)

    region_list = []
    for y in range(0, image_height, 4):
        for x in range(0, image_width, 4):
            print(x, y)
            new_flood_mask = flood(outline_image, seed_point=(y, x))

            already_segmented = False
            for item in region_list:
                if np.array_equal(new_flood_mask, item):
                    already_segmented = True

            if already_segmented == False:
                region_list.append(new_flood_mask)

                plt.imshow(new_flood_mask)
                plt.show()
"""

def segment_outlines(outline_image):

    outline_image = ndi.binary_fill_holes(outline_image)
    outline_image = remove_small_objects(outline_image, min_size=200)

    plt.title("small objects removed")
    plt.imshow(outline_image)
    plt.show()

    image_height, image_width = np.shape(outline_image)
    selected_regions = []
    region_list = []
    region_count = 2
    plt.ion()
    for y in range(0, image_height, 10):
        for x in range(0, image_width, 10):

            print(x, y)
            new_flood_mask = flood(outline_image, seed_point=(y, x))

            already_segmented = False
            for item in region_list:
                if np.array_equal(new_flood_mask, item):
                    already_segmented = True

            if already_segmented == False:
                region_list.append(new_flood_mask)

                labeled_region_mask = np.where(new_flood_mask == 1, region_count, 0)
                selected_regions.append(labeled_region_mask)
                region_count += 1
                plt.clf()
                plt.imshow(np.max(np.array(selected_regions), axis=0))
                plt.draw()
                plt.pause(0.1)

    segmented_regions = np.max(np.array(selected_regions), axis=0)
    np.save("/home/matthew/Documents/Allen_Atlas_Templates/New_Outline_Regions.npy", segmented_regions)




# Get Fine Mask and Atlas Outlines
atlas_outline_location = "/home/matthew/Documents/Allen_Atlas_Templates/New_Outline.npy"
atlas_outline = np.load(atlas_outline_location)

# Dilate
atlas_outline = ndi.morphology.binary_dilation(atlas_outline)

plt.imshow(atlas_outline)
atlas_outline = np.where(atlas_outline > 0.9, 1, 0)
segment_outlines(atlas_outline)