import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

def calculate_area(image, bboxes):
    area_image_mm = 7854
    h, w, c = image.shape
    area_image = h * w
    
    area_list = []
    for x, y, w, h in bboxes:
        area_bbox = w * h
        area_list.append((area_bbox / area_image) * area_image_mm)
        
    return sum(area_list)

def count_vibrio(im_arr, mask, color):
    
    height_img, width_img, _ = im_arr.shape

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bboxes = []
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        is_within = (x-(height_img//2))**2 + (y-(width_img//2))**2 < (((height_img-500)/2)**2)
        
        if(100 <= area <= 15000) & is_within:
            # im_arr_draw = cv2.rectangle(im_arr_draw, (x, y), (x + w, y + h),  (0, 255, 0), 5)
            bboxes.append([x,y,w,h])

    total_area = calculate_area(im_arr, bboxes)
    return {'color': color, 'total_colony': len(bboxes), 'total_size': total_area}

def predict(im_arr):

    kernel = np.ones((5, 5), "uint8")

    hsvFrame = cv2.cvtColor(im_arr, cv2.COLOR_RGB2HSV)

    yellow_lower = np.array([25, 100, 20], np.uint8)
    yellow_upper = np.array([35, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    green_lower = np.array([40, 100, 20], np.uint8)
    green_upper = np.array([65, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([255, 255, 30], np.uint8)
    black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)

    # For yellow color
    yellow_mask = cv2.dilate(yellow_mask, kernel)
    res_yellow = cv2.bitwise_and(hsvFrame, hsvFrame, mask = yellow_mask)

    # For green color
    green_mask = cv2.dilate(green_mask, kernel)
    res_green = cv2.bitwise_and(hsvFrame, hsvFrame, mask = green_mask)

    # For black color
    black_mask = cv2.dilate(black_mask, kernel)
    res_black = cv2.bitwise_and(hsvFrame, hsvFrame, mask = black_mask)

    mask_dict = {
        'yellow': yellow_mask,
        'green': green_mask,
        'black': black_mask
    }

    im_arr_draw = im_arr.copy()

    result = []
    for color, mask in mask_dict.items():
        data = count_vibrio(im_arr_draw, mask, color)
        result.append(data)

    return result