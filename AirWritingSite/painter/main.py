# main.py (FINAL CLEAN FLOW with Modern UI)

import cv2
import numpy as np
import pygame
import time
from collections import deque

from . import config as s
from . import ui_utils as ui
from . import prediction_utils as pu
from . import HandTrackingModule as htm

# ---------------------------
# GEMINI (runs AFTER camera closes)
# ---------------------------

def correct_sentence_with_gemini(sentence: str) -> str:
    try:
        import google.generativeai as genai

        genai.configure(api_key="AIzaSyBTJuVKTH1pA_XLcyiIE7z5hIFRaCLaHdk")
        model = genai.GenerativeModel("gemini-2.5-flash-lite") 

        prompt = (
            "Correct grammar and spelling. Keep meaning the same. "
            "Return ONLY corrected sentence:\n\n" + sentence
        )

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return sentence


# =====================================================
# MAIN FUNCTION
# =====================================================
def main():

    session_raw_sentences = []      
    current_sentence_words = []    

    # ---------------- OpenCV ----------------
    cap = cv2.VideoCapture(0)
    cap.set(3, s.W_WIDTH)
    cap.set(4, s.W_HEIGHT)
    imgCanvas = np.zeros((s.W_HEIGHT, s.W_WIDTH, 3), np.uint8)

    # ---------------- Pygame ----------------
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((s.W_WIDTH, s.W_HEIGHT), flags=pygame.HIDDEN)
    pygame.display.set_caption("Digit Board")

    # ---------------- Models & Utils ----------------
    AlphaMODEL, NumMODEL = pu.load_models()

    menu_buttons = ui.create_menu_buttons()
    detector = htm.handDetector(detectionCon=s.DETECTION_CONFIDENCE)

    # ---------------- State ----------------
    Words = []         
    display_word = ""
    PREDICT = "alpha" # This is now also used as the 'Active Mode' for UI

    xp = yp = 0
    x_history = deque(maxlen=s.SMOOTHING_WINDOW)
    y_history = deque(maxlen=s.SMOOTHING_WINDOW)

    number_xcord = []
    number_ycord = []

    canvas_history = [(imgCanvas.copy(), DISPLAYSURF.copy())]

    current_color_index = 0
    drawColor = s.COLOR_OPTIONS[s.COLOR_NAMES[current_color_index]]

    fist_start_time = 0
    sentence_saved_time = 0 

    # =====================================================
    # MAIN LOOP
    # =====================================================
    while True:

        SUCCESS, img = cap.read()
        if not SUCCESS:
            break

        img = cv2.flip(img, 1)

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        # ---------------------------------------------------------
        # DRAW UI (MODERNIZED)
        # We pass 'PREDICT' directly so the UI knows which button to highlight
        # ---------------------------------------------------------
        ui.draw_ui(
            img,
            menu_buttons,
            PREDICT, # Passes 'alpha', 'num', or 'off'
            s.COLOR_NAMES[current_color_index],
            drawColor
        )

        # ---------------------------------------------------------
        # SHOW “Sentence Saved!” TOAST
        # ---------------------------------------------------------
        if sentence_saved_time != 0:
            sentence_saved_time = ui.draw_toast_message(img, "Sentence Saved!", sentence_saved_time)

        # ---------------------------------------------------------
        # HAND LOGIC
        # ---------------------------------------------------------
        if len(lmList) > 0:

            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            fingers = detector.fingersUp()

            # =====================================================
            # MENU SELECTION
            # =====================================================
            if fingers[1] and fingers[2]:
                fist_start_time = 0
                xp = yp = 0
                x_history.clear()
                y_history.clear()

                action = ui.check_button_click(x1, y1, menu_buttons)

                if action:
                    if action == "alpha":
                        PREDICT = "alpha"
                    elif action == "num":
                        PREDICT = "num"
                    elif action == "off":
                        PREDICT = "off"
                        Words = []
                        display_word = ""
                    elif action == "color":
                        current_color_index = (current_color_index + 1) % len(s.COLOR_OPTIONS)
                        drawColor = s.COLOR_OPTIONS[s.COLOR_NAMES[current_color_index]]
                    elif action == "del":
                        if len(canvas_history) > 1:
                            if Words: Words.pop()
                            canvas_history.pop()
                            last = canvas_history[-1]
                            imgCanvas = last[0].copy()
                            DISPLAYSURF.blit(last[1], (0, 0))
                        display_word = "".join(Words)
                    elif action == "next":
                        if Words:
                            raw = "".join(Words).strip().lower()
                            if raw:
                                
                                current_sentence_words.append(raw)

                        if current_sentence_words:
                            raw_sentence = " ".join(current_sentence_words).strip()
                            if not raw_sentence.endswith("."): raw_sentence += "."
                            session_raw_sentences.append(raw_sentence)
                            print("RAW SENTENCE:", raw_sentence)

                        Words = []
                        display_word = ""
                        number_xcord = []
                        number_ycord = []
                        current_sentence_words = []
                        sentence_saved_time = time.time()

                    elif action == "exit":
                        break

                # Prediction Logic
                if len(number_xcord) > 0 and PREDICT != "off":
                    if drawColor != s.COLOR_OPTIONS['ERASER']: # Use Config Key
                        model = AlphaMODEL if PREDICT == "alpha" else NumMODEL
                        labels = s.AlphaLABELS if PREDICT == "alpha" else s.NumLABELS
                        new_label, bbox = pu.make_prediction(DISPLAYSURF, model, labels, number_xcord, number_ycord)

                        if new_label:
                            Words.append(new_label)
                            display_word = "".join(Words)
                            r1, r2, r3, r4 = bbox
                            cv2.rectangle(imgCanvas, (r1, r2), (r3, r4), s.NEON_GREEN, 2) # Modern Border
                            canvas_history.append((imgCanvas.copy(), DISPLAYSURF.copy()))

                    number_xcord = []
                    number_ycord = []
                    pygame.draw.rect(DISPLAYSURF, (0,0,0), (0, 0, s.W_WIDTH, s.W_HEIGHT))

                # Cursor - Neon Circle instead of blocky rect
                cv2.circle(img, (x1, y1), 10, drawColor, -1, cv2.LINE_AA)
                cv2.circle(img, (x1, y1), 15, (255,255,255), 2, cv2.LINE_AA)

            # =====================================================
            # DRAWING MODE
            # =====================================================
            elif fingers[1] and not fingers[2]:
                fist_start_time = 0
                if y1 < s.HEADER_HEIGHT:
                    xp = yp = 0
                    x_history.clear()
                    y_history.clear()
                    continue

                x_history.append(x1)
                y_history.append(y1)
                sx = int(np.mean(x_history))
                sy = int(np.mean(y_history))
                number_xcord.append(sx)
                number_ycord.append(sy)

                cv2.circle(img, (sx, sy), 10, drawColor, cv2.FILLED) # Small tip

                if xp == 0 and yp == 0: xp, yp = sx, sy

                # Use Eraser or Brush
                is_eraser = (drawColor == s.COLOR_OPTIONS['ERASER'])
                thickness = s.ERASER_THICKNESS if is_eraser else s.BRUSH_THICKNESS

                cv2.line(img, (xp, yp), (sx, sy), drawColor, thickness, cv2.LINE_AA)
                cv2.line(imgCanvas, (xp, yp), (sx, sy), drawColor, thickness, cv2.LINE_AA)

                if not is_eraser:
                    pygame.draw.line(DISPLAYSURF, s.WHITE, (xp, yp), (sx, sy), s.BRUSH_THICKNESS)

                xp, yp = sx, sy

            # =====================================================
            # CONFIRM WORD (Thumb)
            # =====================================================
            elif fingers[0] == 1 and not any(fingers[1:]):
                if Words:
                    raw = "".join(Words).strip().lower()
                    if raw:

                        current_sentence_words.append(raw)
                Words = []
                display_word = ""
                number_xcord = []
                number_ycord = []
                time.sleep(0.25)

            # =====================================================
            # CLEAR CANVAS (Fist)
            # =====================================================
            elif all(f == 0 for f in fingers):
                now = time.time()
                if fist_start_time == 0: fist_start_time = now
                
                # Draw Circular Progress for Clear
                elapsed = now - fist_start_time
                if elapsed > 0.2:
                    percentage = min(elapsed / s.FIST_DURATION, 1.0)
                    # Draw progress circle
                    center = (x1, y1) if x1 else (s.W_WIDTH//2, s.W_HEIGHT//2)
                    radius = 40
                    # Background circle
                    cv2.circle(img, center, radius, (50,50,50), 4, cv2.LINE_AA)
                    # Progress arc
                    end_angle = int(360 * percentage)
                    cv2.ellipse(img, center, (radius, radius), 0, 0, end_angle, s.NEON_RED, 4, cv2.LINE_AA)
                    cv2.putText(img, "CLEARING...", (center[0]-50, center[1]-50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, s.NEON_RED, 2)

                if elapsed >= s.FIST_DURATION:
                    imgCanvas.fill(0)
                    pygame.draw.rect(DISPLAYSURF, (0,0,0), (0, 0, s.W_WIDTH, s.W_HEIGHT))
                    Words = []
                    display_word = ""
                    canvas_history = [(imgCanvas.copy(), DISPLAYSURF.copy())]
                    fist_start_time = 0
                    time.sleep(0.3)
            else:
                fist_start_time = 0
                xp = yp = 0
                x_history.clear()
                y_history.clear()

        # ---------------------------------------------------------
        # BOTTOM BAR (Live Word)
        # ---------------------------------------------------------
        # Semi-transparent bottom bar
        overlay = img.copy()
        cv2.rectangle(overlay, (0, s.W_HEIGHT - 80), (s.W_WIDTH, s.W_HEIGHT), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)

        if display_word:
            cv2.putText(img, display_word, (50, s.W_HEIGHT - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, s.NEON_GREEN, 3, cv2.LINE_AA)
        else:
            # Placeholder text
            cv2.putText(img, "Write something...", (50, s.W_HEIGHT - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, s.UI_TEXT_MUTED, 2, cv2.LINE_AA)

        # Merge canvas
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        pygame.display.update()
        cv2.imshow("Digit Board (Cyberpunk Edition)", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    
    # ... (Django/Gemini Logic Remains Same) ...
    if session_raw_sentences:
        import os, django, sys
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AirWritingSite.settings')
        django.setup()
        from . import document_utils
        
        final_corrected = []
        for raw in session_raw_sentences:
            corrected = correct_sentence_with_gemini(raw)
            final_corrected.append(corrected)

        document_utils.save_session_sentences(final_corrected)
        print("\nSession saved.\n")

if __name__ == "__main__":
    main()