# MIT License

# Copyright (c) 2020 NizarTarabay

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
-This code is a prerequisite to build the coco_format data set.
-This code extract colors from png images that represent masks.
-You can run this code without merging the masks together (merge_masks.py)
-To make this code work properly, project directory should be as follow:
Make sure to follow the same hierarchy.
project directory:
{
images
       {cam
            {RGB  # for rgb images
                 {...*.png
       {masks_ctr
                 {masks
                        {dataset_info.json  # Run create_info.py
                        {mask_definitions.json  # Run update_mask_definitions.py
                        {coco_instances.json  # Run coco_json_utils.py
                        {...*.png  # Masks automatically merged together from all the categories (run merge_masks.py)
                 {super_category_1
                                  {category_1
                                             {...*.png  # Masks from super_category_1 category_1
                                  {category_2
                                             {...*.png  # Masks from super_category_1 category_2
                                       :
                                  {category_n
                                             {...*.png  # Masks from super_category_1 category_n
                 {super_category_2
                                  {category_1
                                            {...*.png  # Masks from super_category_2 category_1
                                  {category_2
                                            {...*.png  # Masks from super_category_2 category_2
                                       :
                                  {category_n
                                            {...*.png  # Masks from super_category_2 category_n
                          :
                 {super_category_n
                                  {category_1
                                            {...*.png  # Masks from super_category_3 category_1
                                  {category_2
                                            {...*.png  # Masks from super_category_3 category_2
                                       :
                                  {category_n
                                            {...*.png  # Masks from super_category_3 category_n
python_project
             {merge_masks.py,
             {update_mask_definitions.py
             {coco_json_utils.py

NB: All the masks that correspond to the same image should have the same name as their image,
saved as png with alpha channel (transparency channel RGBA) enabled.
"""

import json
import os.path
from PIL import Image


prj_dir = os.getcwd()  # returns the current work directory

masks_dir = os.path.join(os.path.split(prj_dir)[0], 'images/masks_ctr')  # got to the mask directory
images_dir = os.path.join(os.path.split(prj_dir)[0], 'images/cam/rgb/')  # got to the mask directory

masks_spr_ctrs_path = [f.path for f in os.scandir(masks_dir)
                       if f.is_dir()]  # returns the path of super-categories

spr_ctrs = [os.path.split(dir)[1] for dir in masks_spr_ctrs_path
            if os.path.split(dir)[1] != 'masks']  # returns the super categories list

#######################################################################
# extract the super categories from the directory that the author made#
# and populate the super categories dict accordingly                  #
# following the mask definition format                                #
#######################################################################

categories = {}
for spr_ctr in spr_ctrs:
    ctr_path = [f.path for f in os.scandir(os.path.join(masks_dir, spr_ctr))
                if f.is_dir()]  # returns the path of categories
    ctrs = [os.path.split(dir)[1] for dir in ctr_path
            if os.path.split(dir)[1] != 'no_categories']  # returns the categories list
    categories[spr_ctr] = ctrs

######################################################################
#                 populate mask_definition dictionary                #
######################################################################
mask_definitions = {'masks': {}, 'super_categories': categories}

# Define the images and the masks' names keys
for file in os.listdir(images_dir):
    if file.endswith(".png"):
        mask_definitions['masks'][ str(file)] = {'mask': str(file.rsplit('.', 1)[0]) + '.png',
                                                            'color_categories': {}}  # mask files should end in .png


for spr_ctr in spr_ctrs:  # iterates in the super categories folders
    ctrs = categories[spr_ctr]
    for ctr in ctrs:  # iterates in the categories folders inside the super categories folder
        masks = [f.path for f in os.scandir(os.path.join(masks_dir, spr_ctr + '/' + ctr))
                 if f.is_dir()]  # returns the path of categories
        for file in os.listdir(
                os.path.join(masks_dir, spr_ctr + '/' + ctr)):  # iterates inside the categories masks images
            if file.endswith(".png"):
                img = Image.open(os.path.join(os.path.join(masks_dir, spr_ctr + '/' + ctr), file))
                his_color = img.convert('RGB').getcolors()

                for i in range(0, len(his_color) - 1):  # iterates inside each mask to return the colors
                    color = str(his_color[i][1])
                    mask_definitions['masks'][str(file.rsplit('.', 1)[0]) + '.png'] \
                                    ['color_categories'][color] = {'category': ctr,
                                                       'super_category': spr_ctr}  # populate the entire dictionary


######################################################################
#                 save mask_definitions json file                    #
######################################################################
with open(os.path.join(os.path.split(prj_dir)[0],
                       'images/masks_ctr/masks/mask_definitions.json'),
          'w') as fp:
    json.dump(mask_definitions, fp, indent=4)
