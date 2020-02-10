# coco_annotation_tool
This repository generate coco annotations for instance segmentation.
In order to use this repository you need an image editing app such as: GIMP (free app), adobe photoshop, etc.

## Step 1: Clone or download the repository


## Step 2: Prepare your project directory
./images: Contains subdirectories for all your images (masks or RGB)

./images/cam/RGB: your RGB.png images

./images/masks_ctr: Contains super categories, simply create a folder inside ./images/masks_ctr for your all super categories

./images/masks_ctr/super_category_1: This is a subdirectory that you have created for your super category. Simply create folders for your categories inside it.

./images/masks_ctr/super_category_1/category_1: Contains masks for category_1. Each image should have only one mask that represent all the objects inside the image that belong to category_1. You can create more categories by creating more folders and place your masks inside.

./images/masks_ctr/masks: Contains your final masks. One mask per image. Each mask contains all the object. Also, it contains three diffrent json file: 
#### dataset_info.json, mask_definitions.json, coco_instances.json.

./python_project: Contains python code to generate your annotation

## Step 3: Create your masks
Use your favorite image editing tool that support transparency layers to create your masks. GIMP is free and easy to use.
Load your image to your editing tool. Create transparent layers according to the number of categories that you have in the image.

On each layer draw above your objects that belong to the same categoy assigned to this layer (make sure to use ddifferent colors for each object and categories)

Save as name_of_the_image.PNG each layer in ./images/masks_ctr/super_category_1/category_X. Make sure that the background of the mask in transparent. Keep the name of all your saved masks as the name of your original RGB image.
After you finish annotating your images go to step 4

## Step 4: Run update_mask_definitions.py
This will generate mask_definitions.json

## Step 5: Run merge_masks.py
This will generate masks in ./images/masks_ctr/masks. One mask per image. Each mask contains all the annotated objects.

## Step 5: Run create_info.py
This code is based on https://github.com/akTwelve/cocosynth. It creates dataset_info.json that contains information about your dataset i.e., licence, contributor, etc.

## Step 6: Run coco_json_utils.py
This code is written by: akTwelve https://github.com/akTwelve
https://github.com/akTwelve/cocosynth
To run this code: Go to your project directory and run the following in the terminal:
python3 ./python_project/coco_json_utils.py -md ./images/masks_ctr/masks/mask_definitions.json -di ./images/masks_ctr/masks/dataset_info.json
This will generate your coco_instances.json annotations.
