import os
import pandas as pd
from tqdm import tqdm
from src import *

# Set input and output directories
input_csv = 'data/raw/track1/driving_log.csv'
output_csv = 'data/processed/track1/driving_log.csv'
output_dir = 'data/processed/track1/IMG'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Clear the output directory
clear_output_dir(output_dir)

# Load the CSV file
data = pd.read_csv(input_csv, names=["center", "left", "right", "steering_angle", "throttle", "brake", "speed"])

# Apply the clean_path function to each path column
project_folder = os.getcwd().split('/')[-2]
data['center'] = data['center'].apply(clean_path, project_folder=project_folder)
data['left'] = data['left'].apply(clean_path, project_folder=project_folder)
data['right'] = data['right'].apply(clean_path, project_folder=project_folder)
data['center'].head()

# Save the modified data back to a new CSV file
data.to_csv(output_csv, index=False, header=False)
print(f"Paths have been updated and saved to {output_csv}")

# Main processing loop
data = pd.read_csv(input_csv, names=["center", "left", "right", "steering_angle", "throttle", "brake", "speed"])
processed_data = []

for _, row in tqdm(data.iterrows(), total=len(data), desc="Processing Images"):
    processed_entries = process_and_save_images(row, output_dir)
    processed_data.extend(processed_entries)

# Save new CSV with processed data
processed_df = pd.DataFrame(processed_data, columns=["image_path", "steering_angle", "throttle", "brake", "speed"])
processed_df.to_csv(output_csv, index=False)
print(f"Processing complete. Processed data saved to {output_csv}.")