import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Fist detection (left-click/drag)
def is_fist(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    return all(hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y for tip, pip in zip(finger_tips, finger_pips))

# Peace sign detection (right-click)
def is_peace_sign(hand_landmarks):
    finger_tips = [8, 12]       # index, middle
    finger_pips = [6, 10]
    other_tips = [16, 20]       # ring, pinky
    other_pips = [14, 18]
    fingers_up = all(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y for tip, pip in zip(finger_tips, finger_pips))
    fingers_down = all(hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y for tip, pip in zip(other_tips, other_pips))
    return fingers_up and fingers_down

def run_hand_tracking():
    cam = cv2.VideoCapture(0)
    max_hands = 2
    FIST_THRESHOLD_FRAMES = 3
    PEACE_THRESHOLD_FRAMES = 3

    fist_frames = [0] * max_hands
    peace_frames = [0] * max_hands
    dragging = [False] * max_hands
    drag_start_cursor = [None] * max_hands
    drag_start_hand = [None] * max_hands

    screen_w, screen_h = pyautogui.size()
    prev_x, prev_y = screen_w // 2, screen_h // 2
    smoothing = 0.2

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=max_hands,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        try:
            while cam.isOpened():
                success, image = cam.read()
                if not success or image is None:
                    continue

                image = cv2.flip(image, 1)
                frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        if results.multi_handedness and results.multi_handedness[idx].classification[0].score < 0.7:
                            continue

                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style()
                        )

                        fist = is_fist(hand_landmarks)
                        peace = is_peace_sign(hand_landmarks)
                        index_tip = hand_landmarks.landmark[8]
                        hand_x = index_tip.x
                        hand_y = index_tip.y

                        # --- Peace Sign: Right Click ---
                        if peace:
                            peace_frames[idx] += 1
                            if peace_frames[idx] >= PEACE_THRESHOLD_FRAMES:
                                pyautogui.rightClick()
                                peace_frames[idx] = 0
                        else:
                            peace_frames[idx] = 0

                        # --- Fist: Left Click & Drag ---
                        if fist:
                            fist_frames[idx] += 1
                            if fist_frames[idx] >= FIST_THRESHOLD_FRAMES:
                                if not dragging[idx]:
                                    dragging[idx] = True
                                    pyautogui.mouseDown()
                                    drag_start_cursor[idx] = (prev_x, prev_y)
                                    drag_start_hand[idx] = (hand_x, hand_y)

                                dx = (hand_x - drag_start_hand[idx][0]) * screen_w
                                dy = (hand_y - drag_start_hand[idx][1]) * screen_h
                                target_x = drag_start_cursor[idx][0] + dx
                                target_y = drag_start_cursor[idx][1] + dy

                                smooth_x = prev_x + (target_x - prev_x) * smoothing
                                smooth_y = prev_y + (target_y - prev_y) * smoothing
                                pyautogui.moveTo(smooth_x, smooth_y)
                                prev_x, prev_y = smooth_x, smooth_y
                        else:
                            fist_frames[idx] = 0
                            if dragging[idx]:
                                pyautogui.mouseUp()
                                dragging[idx] = False
                            # Normal cursor movement
                            target_x = int(hand_x * screen_w)
                            target_y = int(hand_y * screen_h)
                            smooth_x = prev_x + (target_x - prev_x) * smoothing
                            smooth_y = prev_y + (target_y - prev_y) * smoothing
                            pyautogui.moveTo(smooth_x, smooth_y)
                            prev_x, prev_y = smooth_x, smooth_y

                cv2.imshow('Hand Tracking', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            for idx in range(max_hands):
                if dragging[idx]:
                    pyautogui.mouseUp()
            cam.release()
            cv2.destroyAllWindows()

run_hand_tracking()







# Controls
# Index finger tip: Move cursor
# Fist: Click, and click and drag (release when fist is opened)
# Peace sign: Right-click 
