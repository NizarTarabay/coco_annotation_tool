"""
MIT License

Copyright (c) 2019 Adam Kelly

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
"""
Run create_info.py before running coco_json_utils.py
this code create information for your data
"""

from datetime import datetime
from pathlib import Path
import os
import json

# A convenience wizard for automatically creating dataset info
# The user can always modify the resulting .json manually if needed

prj_dir = os.getcwd()  # returns the current work directory
should_continue = input('Would you like to create dataset info json? (y/n) ').lower()
if should_continue != 'y' and should_continue != 'yes':
    print('No problem. You can always create the json manually.')
    quit()

print('Note: you can always modify the json manually if you need to update this.')
info = dict()
info['description'] = input('Description: ')
info['url'] = input('URL: ')
info['version'] = input('Version: ')
info['contributor'] = input('Contributor: ')
now = datetime.now()
info['year'] = now.year
info['date_created'] = f'{now.month:0{2}}/{now.day:0{2}}/{now.year}'

image_license = dict()
image_license['id'] = 0

should_add_license = input('Add an image license? (y/n) ').lower()
if should_add_license != 'y' and should_add_license != 'yes':
    image_license['url'] = ''
    image_license['name'] = 'None'
else:
    image_license['name'] = input('License name: ')
    image_license['url'] = input('License URL: ')

dataset_info = dict()
dataset_info['info'] = info
dataset_info['license'] = image_license

# Write the JSON output file
output_file_path = Path(os.path.join(os.path.split(prj_dir)[0],
                                     'images/masks_ctr/masks/info')) / 'dataset_info.json'
with open(output_file_path, 'w+') as json_file:
    json_file.write(json.dumps(dataset_info))

print('Successfully created {output_file_path}', output_file_path)
