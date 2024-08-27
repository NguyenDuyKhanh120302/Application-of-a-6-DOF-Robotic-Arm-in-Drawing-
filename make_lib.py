import os
import shutil

def get_xy_list_from_contour(contours):
    full_dataset = []
    for contour in contours:
        xy_list=[]
        for position in contour:
            [[x,y]] = position
            xy_list.append(str([x,y]))
        full_dataset.append(xy_list)
    return full_dataset

def make_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def delete_all_files(dir):
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

