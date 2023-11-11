from video_processing import find_person, calculate_intersection_percent
import os
import numpy as np
import cv2

camera_folder = "D:/dataset/valid_cameras"
danger_zone_folder = "D:/dataset/valid_danger_zones"

data = [['camera_name', 'filename', 'in_danger_zone', 'percent']]
cameras = os.listdir(camera_folder)
for camera in cameras:
    masks = [file for file in os.listdir(f"{danger_zone_folder}") if file.startswith(f"danger_{camera}")]
    images = [img for img in os.listdir(f'{camera_folder}/{camera}') if img.lower().endswith(".jpg")] + \
             [img for img in os.listdir(f'{camera_folder}/{camera}') if img.lower().endswith(".png")]
    intersections = []
    for image in images:
        print(f"{camera}/{image}")
        img = cv2.imread(f'{camera_folder}/{camera}/{image}')
        rectangles = find_person(img)
        for mask in masks:
            for rectangle in rectangles:
                with open(f'{danger_zone_folder}/{mask}', "r") as f:
                    mask_list = []
                    temp = f.readlines()
                    for elem in temp:
                        f_s = elem.replace(',', '')
                        f_s = f_s.replace(']', '')
                        f_s = f_s.replace('[', '')
                        mask_list.append(
                            tuple(map(int, f_s.split()))
                        )
                intersection_percent = calculate_intersection_percent(rectangle, mask_list)
                intersections.append(intersection_percent)
        final_intersection = 0
        if len(intersections) > 0:
            final_intersection = max(intersections)
        if final_intersection > 15:
            status = True
        else:
            status = False

        data.append(
            [
                camera,
                image,
                status,
                final_intersection / 100
            ]
        )

np.savetxt("result.csv",
           data,
           delimiter=", ",
           fmt='% s')
