# prediction_utils.py
# This file handles model loading and prediction logic.

import numpy as np
import cv2
import pygame
from tensorflow.keras.models import load_model
from . import config as s # Import constants from config.py
import os # <-- IMPORT THE OS MODULE

# --- THIS IS THE CRITICAL FIX ---
# Get the absolute path to the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths to the model files
ALPHA_MODEL_PATH = os.path.join(CURRENT_DIR, s.MODEL_ALPHA_PATH)
NUM_MODEL_PATH = os.path.join(CURRENT_DIR, s.MODEL_NUM_PATH)
# -----------------------------


def load_models():
    """Loads and returns the alphabet and number recognition models."""
    try:
        # Load models using the new absolute paths
        AlphaMODEL = load_model(ALPHA_MODEL_PATH)
        NumMODEL = load_model(NUM_MODEL_PATH)
        print("Models loaded successfully.")
        return AlphaMODEL, NumMODEL
    except Exception as e:
        print(f"Error loading models: {e}")
        # This new print statement will show you the *exact* path it's trying to load
        print(f"Attempted to load from: {ALPHA_MODEL_PATH}") 
        return None, None

def make_prediction(surf, model, labels, x_coords, y_coords):
    """
    Processes the drawn coordinates, crops from the Pygame surface,
    and returns a prediction and the bounding box.
    """
    
    # 1. Create Bounding Box
    rect_min_x = max(min(x_coords) - s.BOUNDRYINC, 0)
    rect_max_x = min(max(x_coords) + s.BOUNDRYINC, s.W_WIDTH)
    rect_min_y = max(min(y_coords) - s.BOUNDRYINC, s.HEADER_HEIGHT) # Ensure box is below header
    rect_max_y = min(max(y_coords) + s.BOUNDRYINC, s.W_HEIGHT)
    
    box_width = rect_max_x - rect_min_x
    box_height = rect_max_y - rect_min_y

    # 2. Check if drawing is too small (e.g., a dot)
    if box_width < s.MIN_BOX_SIZE or box_height < s.MIN_BOX_SIZE:
        print("Drawing too small, skipping.")
        return None, (0,0,0,0) # Return no label and no box
        
    # 3. Get image array from Pygame surface
    try:
        img_arr = np.array(pygame.PixelArray(surf))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
    except Exception as e:
        print(f"Error creating pixel array: {e}")
        return None, (0,0,0,0)

    # 4. Preprocess the image for the model
    if img_arr.size > 0:
        image = cv2.resize(img_arr, (28, 28))
        image = np.pad(image, (10, 10), 'constant', constant_values=0)
        image = cv2.resize(image, (28, 28)) / 255.0
        
        # 5. Make prediction
        prediction = model.predict(image.reshape(1, 28, 28, 1))
        label = str(labels[np.argmax(prediction)])
        
        bounding_box = (rect_min_x, rect_min_y, rect_max_x, rect_max_y)
        
        return label, bounding_box
    
    return None, (0,0,0,0)