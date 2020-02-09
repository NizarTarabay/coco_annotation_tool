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
-This code generate a mask for each image, it merges all the masks from different categories to one mask.
To make this code work properly, project directory should be as follow:
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

import os.path


prj_dir = os.getcwd()  # returns the work directory

masks_dir = os.path.join(os.path.split(prj_dir)[0], 'images/masks_ctr')  # go to the mask directory
images_dir = os.path.join(os.path.split(prj_dir)[0], 'images/cam/gsr/')  # go to the image directory

masks_spr_ctrs_path = [f.path for f in os.scandir(masks_dir)
                       if f.is_dir()]  # returns the path of super-categories

spr_ctrs = [os.path.split(dir)[1] for dir in masks_spr_ctrs_path
            if os.path.split(dir)[1] != 'masks']  # returns the super categories list

categories = []
categories_path = []
for spr_ctr in spr_ctrs:
    ctrs_path = [f.path for f in os.scandir(os.path.join(masks_dir, spr_ctr))
                 if f.is_dir() and os.path.basename(f.path) != 'no_categories']  # returns the path of categories
    categories_path.append(ctrs_path)
    ctrs = [os.path.split(dir)[1] for dir in ctrs_path
            if os.path.split(dir)[1] != 'no_categories']  # returns the super categories list
    categories.append(ctrs)

list_ctr_path = []
for list in categories_path:
    list_ctr_path = list_ctr_path + list

from PIL import Image

for file in os.listdir(images_dir):
    size_image = Image.open(os.path.join(images_dir, str(file.rsplit('.', 1)[0]) + '.png')).size
    im = Image.new('RGB', size_image, (0, 0, 0))
    if file.endswith(".png"):
        for path in list_ctr_path:
            try:
                Image1 = Image.open(os.path.join(path, str(file.rsplit('.', 1)[0]) + '.png'))
                Image1copy = Image1.copy()
                im.paste(Image1copy, (0, 0), Image1copy)
                # save the image
                save_dir = os.path.join(os.path.split(prj_dir)[0], 'images/masks_ctr/masks/')
                im.save(save_dir + str(file.rsplit('.', 1)[0]) + '.png')
                print("done")
            except:
                continue
