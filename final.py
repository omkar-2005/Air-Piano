import cv2
import threading
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector
import tkinter as tk
from tkinter import ttk

# 🎹 Initialize Pygame MIDI
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)  # 0 = Acoustic Grand Piano

# 🎐 Initialize Hand Detector
cap = cv2.VideoCapture(0)  # 1 because I am using the phone as a webcam. If you have a laptop camera, use 0.
detector = HandDetector(detectionCon=0.8)

# 🎼 Chords Mapping for Scales
scales = {
    "GP": {
        "left": {
            "thumb": [67, 71, 74],    # G Major (G, B, D)
            "index": [64, 67, 71],  # E Minor (E, G, B)
            "middle": [60, 64, 67],   # C Major (C, E, G)
            "pinky": [62, 66, 69]   # D Major (D, F#, A)
        },
        "right": {
            "thumb": [67, 71, 74],    # G Major (G, B, D)
            "index": [64, 67, 71],  # E Minor (E, G, B)
            "middle": [60, 64, 67],   # C Major (C, E, G)
            "pinky": [62, 66, 69]   # D Major (D, F#, A)
        }
    },
    "C": {
        "left": {
            "thumb": [60, 64, 67],   # C Major (C, E, G)
            "index": [62, 65, 69],   # D Minor (D, F, A)
            "middle": [64, 67, 71],  # E Minor (E, G, B)
            "ring": [65, 69, 72],    # F Major (F, A, C)
            "pinky": [67, 71, 74]    # G Major (G, B, D)
        },
        "right": {
            "thumb": [60, 64, 67],   # C Major (C, E, G)
            "index": [62, 65, 69],   # D Minor (D, F, A)
            "middle": [64, 67, 71],  # E Minor (E, G, B)
            "ring": [65, 69, 72],    # F Major (F, A, C)
            "pinky": [67, 71, 74]    # G Major (G, B, D)
        }
    },
    "D": {
        "left": {
            "thumb": [62, 66, 69],   # D Major (D, F#, A)
            "index": [64, 67, 71],   # E Minor (E, G, B)
            "middle": [66, 69, 73],  # F# Minor (F#, A, C#)
            "ring": [67, 71, 74],    # G Major (G, B, D)
            "pinky": [69, 73, 76]    # A Major (A, C#, E)
        },
        "right": {
            "thumb": [62, 66, 69],   # D Major (D, F#, A)
            "index": [64, 67, 71],   # E Minor (E, G, B)
            "middle": [66, 69, 73],  # F# Minor (F#, A, C#)
            "ring": [67, 71, 74],    # G Major (G, B, D)
            "pinky": [69, 73, 76]    # A Major (A, C#, E)
        }
    },
    "E": {
        "left": {
            "thumb": [64, 68, 71],   # E Major (E, G#, B)
            "index": [66, 69, 73],   # F# Minor (F#, A, C#)
            "middle": [68, 71, 75],  # G# Minor (G#, B, D#)
            "ring": [69, 73, 76],    # A Major (A, C#, E)
            "pinky": [71, 74, 78]    # B Major (B, D#, F#)
        },
        "right": {
            "thumb": [64, 68, 71],   # E Major (E, G#, B)
            "index": [66, 69, 73],   # F# Minor (F#, A, C#)
            "middle": [68, 71, 75],  # G# Minor (G#, B, D#)
            "ring": [69, 73, 76],    # A Major (A, C#, E)
            "pinky": [71, 74, 78]    # B Major (B, D#, F#)
        }
    },
    "F": {
        "left": {
            "thumb": [65, 69, 72],   # F Major (F, A, C)
            "index": [67, 71, 74],   # G Minor (G, B, D)
            "middle": [69, 72, 76],  # A Minor (A, C, E)
            "ring": [70, 74, 77],    # A# Major (A#, D, F)
            "pinky": [72, 76, 79]    # B Major (B, D#, F#)
        },
        "right": {
            "thumb": [65, 69, 72],   # F Major (F, A, C)
            "index": [67, 71, 74],   # G Minor (G, B, D)
            "middle": [69, 72, 76],  # A Minor (A, C, E)
            "ring": [70, 74, 77],    # A# Major (A#, D, F)
            "pinky": [72, 76, 79]    # B Major (B, D#, F#)
        }
    },
    "G": {
        "left": {
            "thumb": [67, 71, 74],   # G Major (G, B, D)
            "index": [69, 73, 76],   # A Minor (A, C, E)
            "middle": [71, 74, 78],  # B Minor (B, D, F#)
            "ring": [72, 76, 79],    # C Major (C, E, G)
            "pinky": [74, 77, 81]    # D Major (D, F#, A)
        },
        "right": {
            "thumb": [67, 71, 74],   # G Major (G, B, D)
            "index": [69, 73, 76],   # A Minor (A, C, E)
            "middle": [71, 74, 78],  # B Minor (B, D, F#)
            "ring": [72, 76, 79],    # C Major (C, E, G)
            "pinky": [74, 77, 81]    # D Major (D, F#, A)
        }
    },
    "Am": {
        "left": {
            "thumb": [57, 60, 64],   # A Minor (A, C, E)
            "index": [60, 64, 67],   # C Major (C, E, G)
            "middle": [62, 65, 69],  # D Minor (D, F, A)
            "ring": [64, 68, 71],    # E Minor (E, G, B)
            "pinky": [65, 69, 72]    # F Major (F, A, C)
        },
        "right": {
            "thumb": [57, 60, 64],   # A Minor (A, C, E)
            "index": [60, 64, 67],   # C Major (C, E, G)
            "middle": [62, 65, 69],  # D Minor (D, F, A)
            "ring": [64, 68, 71],    # E Minor (E, G, B)
            "pinky": [65, 69, 73]    # F Major (F, A, C)
        }
    },
}

# 🎵 Function to Play a Chord
def play_chord(chord_notes):
    for note in chord_notes:
        player.note_on(note, 127)  # Start playing

# 🎵 Function to Stop a Chord After a Delay
def stop_chord_after_delay(chord_notes):
    time.sleep(SUSTAIN_TIME)  # Sustain for specified time
    for note in chord_notes:
        player.note_off(note, 127)  # Stop playing

# 🎶 Chord Mapping for the Selected Scale
selected_scale = "C"  # Default Scale is C

chords = scales[selected_scale]

# Sustain Time (in seconds) after the finger is lowered
SUSTAIN_TIME = 1.0

# Time threshold for debouncing in seconds (e.g., 0.2s)
DEBOUNCE_DELAY = 0.2

# Dictionary to store the last time finger state was updated
last_state_change_time = {hand: {finger: time.time() for finger in chords[hand]} for hand in chords}

# Track Previous States to Stop Chords
prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

# GUI for controlling the video processing
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hand Gesture MIDI Player")
        self.geometry("300x300")
        
        # Start button
        self.start_button = tk.Button(self, text="Start", command=self.start_video_processing)
        self.start_button.pack(pady=20)

        # Stop button
        self.stop_button = tk.Button(self, text="Stop", state=tk.DISABLED, command=self.stop_video_processing)
        self.stop_button.pack(pady=20)

        # Scale selection drop-down list
        self.scale_label = tk.Label(self, text="Select Scale")
        self.scale_label.pack(pady=10)

        self.scale_dropdown = ttk.Combobox(self, values=["GP","C", "D","E","F","G","Am"], state="readonly")
        self.scale_dropdown.set(selected_scale)  # Default value set to "C"
        self.scale_dropdown.pack(pady=10)

    def start_video_processing(self):
        global selected_scale, chords
        selected_scale = self.scale_dropdown.get()  # Get selected scale from drop-down
        chords = scales[selected_scale]  # Update chords based on selected scale
        
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.processing_thread = threading.Thread(target=self.run_video_processing)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def stop_video_processing(self):
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.should_stop = True

    def run_video_processing(self):
        self.should_stop = False
        while not self.should_stop:
            success, img = cap.read()
            if not success:
                print("❌ Camera not capturing frames")
                continue

            hands, img = detector.findHands(img, draw=True)

            if hands:
                for hand in hands:
                    hand_type = "left" if hand["type"] == "Left" else "right"
                    fingers = detector.fingersUp(hand)
                    finger_names = ["thumb", "index", "middle", "ring", "pinky"]

                    for i, finger in enumerate(finger_names):
                        if finger in chords[hand_type]:  # Only check assigned chords
                            if fingers[i] == 1 and prev_states[hand_type][finger] == 0:
                                play_chord(chords[hand_type][finger])  # Play chord
                            elif fingers[i] == 0 and prev_states[hand_type][finger] == 1:
                                threading.Thread(target=stop_chord_after_delay, args=(chords[hand_type][finger],), daemon=True).start()
                            prev_states[hand_type][finger] = fingers[i]  # Update state
            else:
                # If no hands detected, stop all chords after delay
                for hand in chords:
                    for finger in chords[hand]:
                        threading.Thread(target=stop_chord_after_delay, args=(chords[hand][finger],), daemon=True).start()
                prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

            cv2.imshow(f"Hand Tracking MIDI Chords - {selected_scale} Scale", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = Application()
    app.mainloop()

pygame.midi.quit()
