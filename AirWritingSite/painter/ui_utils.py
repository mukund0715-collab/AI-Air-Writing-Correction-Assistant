# ui_utils.py – Modern UI for Gesture-Based Air Writing

import cv2
import numpy as np
import time
from . import config as s

# ----------------------------- BUTTON CREATION ----------------------------- #

def create_menu_buttons():
    """
    Calculates button positions dynamically based on config settings.
    """
    buttons = []
    names = ["ALPHA", "NUM", "OFF", "DEL", "COLOR", "NEXT", "EXIT"]
    actions = ["alpha", "num", "off", "del", "color", "next", "exit"]
    
    current_x = s.START_X
    
    for name, action in zip(names, actions):
        buttons.append({
            "name": name,
            "x1": current_x,
            "y1": s.START_Y,
            "x2": current_x + s.BUTTON_WIDTH,
            "y2": s.START_Y + s.BUTTON_HEIGHT,
            "action": action
        })
        current_x += s.BUTTON_WIDTH + s.BUTTON_SPACING
        
    return buttons

# ----------------------------- DRAWING HELPERS ----------------------------- #

def draw_rounded_rect(img, pt1, pt2, color, thickness, r, filled=False):
    """Custom function to draw smooth rounded rectangles"""
    x1, y1 = pt1
    x2, y2 = pt2
    
    # Top-left, Top-right, Bottom-right, Bottom-left corners
    corners = [
        ((x1 + r, y1 + r), (x1 + r, y1), (x1, y1 + r)), # TL
        ((x2 - r, y1 + r), (x2 - r, y1), (x2, y1 + r)), # TR
        ((x2 - r, y2 - r), (x2 - r, y2), (x2, y2 - r)), # BR
        ((x1 + r, y2 - r), (x1 + r, y2), (x1, y2 - r))  # BL
    ]
    
    if filled:
        # Draw main rects
        cv2.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, -1)
        cv2.rectangle(img, (x1, y1 + r), (x2, y2 - r), color, -1)
        # Draw circles at corners
        cv2.circle(img, (x1 + r, y1 + r), r, color, -1)
        cv2.circle(img, (x2 - r, y1 + r), r, color, -1)
        cv2.circle(img, (x1 + r, y2 - r), r, color, -1)
        cv2.circle(img, (x2 - r, y2 - r), r, color, -1)
    else:
        # Draw straight lines
        cv2.line(img, (x1 + r, y1), (x2 - r, y1), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x1 + r, y2), (x2 - r, y2), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x1, y1 + r), (x1, y2 - r), color, thickness, cv2.LINE_AA)
        cv2.line(img, (x2, y1 + r), (x2, y2 - r), color, thickness, cv2.LINE_AA)
        # Draw arcs
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness, cv2.LINE_AA)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness, cv2.LINE_AA)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness, cv2.LINE_AA)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness, cv2.LINE_AA)


def draw_button_modern(img, btn, active_mode, hover=False):
    """
    Draws a button with Glassmorphism style.
    Highlights the button if it matches the current 'active_mode'.
    """
    x1, y1, x2, y2 = btn["x1"], btn["y1"], btn["x2"], btn["y2"]
    radius = 10
    
    is_active = (btn["action"] == active_mode)
    
    # --- Colors ---
    if is_active:
        # Bright Highlight for active mode
        bg_color = s.NEON_GREEN if active_mode == 'alpha' else (s.NEON_BLUE if active_mode == 'num' else s.NEON_RED)
        if active_mode == 'color': bg_color = s.NEON_YELLOW
        text_color = (0, 0, 0) # Dark text on bright button
        border_thickness = -1 # Fill it
    else:
        # Standard Glass Style
        bg_color = s.GRAY_DARK
        text_color = s.UI_TEXT
        border_thickness = 2

    # Draw Button Body
    if is_active:
        draw_rounded_rect(img, (x1, y1), (x2, y2), bg_color, -1, radius, filled=True)
    else:
        # Draw simple border for inactive
        draw_rounded_rect(img, (x1, y1), (x2, y2), s.GRAY_LIGHT, 1, radius, filled=False)
    
    # Draw Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.6
    thickness = 2 if is_active else 1
    
    (w, h), _ = cv2.getTextSize(btn["name"], font, scale, thickness)
    text_x = x1 + (s.BUTTON_WIDTH - w) // 2
    text_y = y1 + (s.BUTTON_HEIGHT + h) // 2
    
    cv2.putText(img, btn["name"], (text_x, text_y), font, scale, text_color, thickness, cv2.LINE_AA)


# ----------------------------- MAIN UI DRAW ----------------------------- #

def draw_ui(img, buttons, active_mode, current_color_name, drawColor):
    """
    Draws the complete overlay UI.
    active_mode: 'alpha', 'num', 'off', etc. used to highlight buttons.
    """
    
    # 1. Create a separate overlay layer for transparency
    overlay = img.copy()
    
    # 2. Draw Header Background (Dark Strip)
    cv2.rectangle(overlay, (0, 0), (s.W_WIDTH, s.HEADER_HEIGHT), s.UI_BG_OVERLAY, -1)
    
    # 3. Draw Buttons on Overlay
    for btn in buttons:
        draw_button_modern(overlay, btn, active_mode)
        
    # 4. Apply Overlay (Blend with original image)
    alpha = 0.8 # Opacity of the header
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    
    # 5. Draw Status Info (Bottom of Header)
    # Color Indicator
    cv2.putText(img, "Ink:", (20, s.HEADER_HEIGHT + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, s.UI_TEXT, 1, cv2.LINE_AA)
    
    # Color Preview Circle with Border
    cx, cy = 80, s.HEADER_HEIGHT + 25
    cv2.circle(img, (cx, cy), 18, (255, 255, 255), 2, cv2.LINE_AA) # White ring
    cv2.circle(img, (cx, cy), 15, drawColor, -1, cv2.LINE_AA)      # Color fill

    # Mode Text
    status_text = f"MODE: {active_mode.upper()}"
    status_color = s.NEON_GREEN if active_mode == 'alpha' else (s.NEON_BLUE if active_mode == 'num' else s.NEON_RED)
    cv2.putText(img, status_text, (130, s.HEADER_HEIGHT + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2, cv2.LINE_AA)

# ----------------------------- NOTIFICATIONS ----------------------------- #

def draw_toast_message(img, text, opacity_start_time):
    """
    Draws a pop-up notification card.
    """
    elapsed = time.time() - opacity_start_time
    if elapsed > 2.0: return 0 # Time out
    
    # Dimensions
    h, w, _ = img.shape
    box_w, box_h = 400, 80
    x1 = (w - box_w) // 2
    y1 = h - 150 # Near bottom, above text area
    
    overlay = img.copy()
    
    # Draw Card background
    draw_rounded_rect(overlay, (x1, y1), (x1+box_w, y1+box_h), (50, 50, 50), -1, 15, filled=True)
    
    # Blend for transparency
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
    
    # Draw Border
    draw_rounded_rect(img, (x1, y1), (x1+box_w, y1+box_h), s.NEON_GREEN, 2, 15, filled=False)
    
    # Draw Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_scale = 0.9
    (tw, th), _ = cv2.getTextSize(text, font, text_scale, 2)
    tx = x1 + (box_w - tw) // 2
    ty = y1 + (box_h + th) // 2
    
    cv2.putText(img, text, (tx, ty), font, text_scale, (255, 255, 255), 2, cv2.LINE_AA)
    
    return opacity_start_time


# ----------------------------- DEBOUNCE ----------------------------- #

_last_click_time = 0
CLICK_DELAY = 0.5

def is_debounced():
    global _last_click_time
    now = time.time()
    if now - _last_click_time > CLICK_DELAY:
        _last_click_time = now
        return True
    return False

def check_button_click(x, y, buttons):
    if not is_debounced():
        return None

    for btn in buttons:
        if btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]:
            return btn["action"]

    return None