
Hand Gesture Recognition Program
==================================
Uses OpenCV + cvzone (HandTrackingModule) for gesture detection.
Works on Python 3.14+

Gestures recognized:
  - Open Palm
  - Fist
  - Thumbs Up
  - Victory Sign (Peace)

Requirements:
    pip install opencv-python cvzone
"""

import cv2
from cvzone.HandTrackingModule import HandDetector

# ─────────────────────────────────────────────
# Gesture recognition logic
# ─────────────────────────────────────────────
def recognize_gesture(fingers):
    """
    fingers = list of 5 values [thumb, index, middle, ring, pinky]
    1 = finger open/up, 0 = finger closed/down
    """
    thumb, index, middle, ring, pinky = fingers

    # Open Palm — all 5 fingers open
    if fingers == [1, 1, 1, 1, 1]:
        return "Open Palm ✋"

    # Fist — all fingers closed
    if fingers == [0, 0, 0, 0, 0]:
        return "Fist ✊"

    # Thumbs Up — only thumb open
    if fingers == [1, 0, 0, 0, 0]:
        return "Thumbs Up 👍"

    # Victory Sign — index and middle open only
    if fingers == [0, 1, 1, 0, 0]:
        return "Victory Sign ✌️"

    return "Unknown Gesture"


# ─────────────────────────────────────────────
# Color map for gestures
# ─────────────────────────────────────────────
COLORS = {
    "Open Palm ✋"   : (0,   200, 0  ),
    "Fist ✊"        : (0,   0,   220),
    "Thumbs Up 👍"   : (0,   165, 255),
    "Victory Sign ✌️": (255, 200, 0  ),
    "Unknown Gesture": (180, 180, 180),
    "No Hand Detected": (100, 100, 100),
}


# ─────────────────────────────────────────────
# Overlay on frame
# ─────────────────────────────────────────────
def draw_overlay(frame, gesture, hand_count):
    h, w = frame.shape[:2]
    color = COLORS.get(gesture, (255, 255, 255))

    # Dark banner at top
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 65), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Gesture label
    cv2.putText(frame, f"Gesture: {gesture}",
                (15, 42),
                cv2.FONT_HERSHEY_DUPLEX, 1.0,
                color, 2, cv2.LINE_AA)

    # Hand count
    cv2.putText(frame, f"Hands: {hand_count}",
                (15, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (200, 200, 200), 1, cv2.LINE_AA)

    # Quit hint
    cv2.putText(frame, "Press Q to quit",
                (w - 190, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (150, 150, 150), 1, cv2.LINE_AA)


# ─────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Webcam nahi mili. Camera check karo.")
        return

    # cvzone HandDetector — detectionCon = confidence threshold
    detector = HandDetector(detectionCon=0.75, maxHands=2)

    print("=" * 45)
    print("  Hand Gesture Recognition — shuru!")
    print("  Gestures:")
    print("    ✋  Open Palm   — saari ungliyan khulli")
    print("    ✊  Fist        — saari ungliyan band")
    print("    👍  Thumbs Up   — sirf angotha upar")
    print("    ✌️  Victory Sign — index + middle upar")
    print("  Q dabao band karne ke liye.")
    print("=" * 45)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)   # mirror

        # Detect hands
        hands, frame = detector.findHands(frame, draw=True)

        gesture    = "No Hand Detected"
        hand_count = len(hands) if hands else 0

        if hands:
            # Use first detected hand
            hand    = hands[0]
            fingers = detector.fingersUp(hand)  # [thumb, index, middle, ring, pinky]
            gesture = recognize_gesture(fingers)

        draw_overlay(frame, gesture, hand_count)
        cv2.imshow("Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n[INFO] Band ho raha hai — bye!")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
