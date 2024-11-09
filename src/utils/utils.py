import os
import cv2
from glob import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img

def clear_output_dir(output_dir):
    for file in glob(os.path.join(output_dir, 'IMG/*')):
        os.remove(file)
    for file in glob(os.path.join(output_dir, '*')):
        if os.path.isfile(file):
            os.remove(file)
            
def load_image(path):
    image = cv2.imread(path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def preprocess_image(image):
    image = image[60:140, :, :]  # Crop top and bottom
    return cv2.resize(image, (200, 66), interpolation=cv2.INTER_AREA)

def augment_image(image, steering_angle):
    images, angles = [image], [steering_angle]
    
    # Horizontal flip
    flipped_image = cv2.flip(image, 1)
    images.append(flipped_image)
    angles.append(-steering_angle)
    
    # Brightness adjustment
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hsv_image[:, :, 2] = hsv_image[:, :, 2] * (0.2 + np.random.uniform())
    bright_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
    images.append(bright_image)
    angles.append(steering_angle)
    
    # Translation
    trans_x = np.random.randint(-20, 20)
    trans_y = np.random.randint(-10, 10)
    trans_matrix = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
    translated_image = cv2.warpAffine(image, trans_matrix, (image.shape[1], image.shape[0]))
    images.append(translated_image)
    angles.append(steering_angle + trans_x * 0.002)
    
    return images, angles

def process_and_save_images(row, output_dir):
    camera_paths = [row['center'], row['left'], row['right']]
    angles = [row['steering_angle'], row['steering_angle'] + 0.2, row['steering_angle'] - 0.2]
    throttle, brake, speed = row['throttle'], row['brake'], row['speed']
    
    processed_entries = []
    
    for path, angle in zip(camera_paths, angles):
        image = load_image(path)
        if image is not None:
            image = preprocess_image(image)
            augmented_images, augmented_angles = augment_image(image, angle)
            
            for idx, (aug_img, aug_angle) in enumerate(zip(augmented_images, augmented_angles)):
                filename = f"{os.path.basename(path).split('.')[0]}_aug_{idx}.jpg"
                save_path = os.path.join(output_dir, filename)
                cv2.imwrite(save_path, cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))
                
                processed_entries.append([save_path, aug_angle, throttle, brake, speed])
    
    return processed_entries

def clean_path(path, project_folder):
    start_index = path.find(project_folder)
    return path[start_index+len(project_folder):] if start_index != -1 else path

