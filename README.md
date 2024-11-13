<div align="center">
    <h1 align="center">🚗 Self-Driving Car Project 🚗</h1>

![Demo GIF](images/run1.gif)
</div>

<br>
<br>

## Table of Contents
1. **[Introduction](#introduction)**
2. **[Prerequisites](#prerequisites)**
3. **[Data Preparation](#data-preparation)**
   - **[Manual Data Collection](#manual-data-collection)**
   - **[Download Pre-recorded Data](#download-pre-recorded-and-preprocessed-data)**
   - **[Data Preprocessing](#data-preprocessing)**
4. **[Model Architecture](#model-architecture)**
5. **[Usage](#usage)**

<br>
<br>

## Introduction

<div align="center">
    <img src="images/1.png" width="700" />
</div>

This deep learning model uses Convolutional Neural Networks (CNN) to predict steering angles and speed for the self-driving car simulation: [Udacity Self-Driving Car Simulator](https://github.com/udacity/self-driving-car-sim). The model takes input from the car's 3 cameras (left, center, and right) and makes predictions for the car's movement.

- **Car Movement**: The car can move left (←), right (→), accelerate (↑), and decelerate (↓).
- **Camera Setup**: The car is equipped with three cameras (left, center, right).

<br>
<br>

## Prerequisites

- **Operating System**: Linux or Windows (Linux preferred)
- **Python**: 3.12.7
- **Simulation App**: [Udacity Self-Driving Car Simulator](https://github.com/udacity/self-driving-car-sim)

<br>
<br>

## Data Preparation

### Manual Data Collection:
1. Open the simulator and select the **Training Mode**.

<div align="center">
    <img src="images/2.png" width="500" />
</div>

2. Click on **Record**, choose a folder to save the data, and drive the car for about **10 minutes**.
   - Driving for 10 minutes will yield around **18,000 images** (6,000 images from each camera).

### Download Pre-recorded and Preprocessed Data:
- Download **[here](https://drive.google.com/file/d/1j_R7mMiCiJPX6AzYwIgvvykyzA_wl96B/view?usp=sharing)**.

<br>

After data collection, you will have a `driving_log.csv` file, which contains information about the collected data:

| Image Path | Center Camera Image | Left Camera Image | Right Camera Image | Steering Angle | Throttle | Brake |
|------------|---------------------|-------------------|--------------------|----------------|----------|-------|

<br>
<br>

### Data Preprocessing
For Manual Data Collection Only.

Follow [**Data Preprocessing**](DataPreprocessing.md)

<br>
<br>

## Model Architecture

<div align="center">
    <img src="images/4.png" width="500" />
</div>

<br>
<br>

## Usage

### Setup Environment

- Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
```

- Install required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```
<br>

### Training Model

- Set `data_dir` in `training.py` to folder holding both preprocessed `driving_log.csv` and `IMG`. For example:
```python
data_dir = 'data/processed/track1'
```

- Run training.py:
```bash
python training.py
```

<br>

### Autonomous Run

Once the model is trained, you can use it to predict the car's movements based on the camera input in the simulator.

- First, launch the Simulator App and select Autonomous mode; at this point, the car will remain stationary.

- Next, run the following command to connect to the Simulator (without recording):
```bash
python main.py <model path>
```

Or (with recording enabled):
```bash
python main.py <model path> <image folder>
```

<br>

### Image to Video Conversion

- To convert the captured images into a video, run the following command:
```bash
python video.py <image folder> [--fps]
```
The `--fps` argument defaults to 60 if not specified.