import cv2
import pytesseract
import pygame as pg
from gtts import gTTS
from io import BytesIO
from translate import Translator as tr

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class CameraFeed:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.roi = None
        self.frame = None

    def start(self):
        if not self.cap.isOpened():
            self.cap.open(0)

    def get_frame(self):
        ret, self.frame = self.cap.read()
        if not ret:
            return None
        return self.frame

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()

def perform_ocr(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"An error occurred during OCR: {e}"

def translate_text(text, dest_lang):
    try:
        translator = tr(to_lang=dest_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"An error occurred during translation: {e}"

def text_to_speech(text, dest_lang):
    try:
        tts = gTTS(text=text, lang=dest_lang, slow=False)
        bytes = BytesIO()
        tts.write_to_fp(bytes)
        bytes.seek(0)
        return bytes
    except Exception as e:
        return f"An error occurred during text-to-speech: {e}"

def play_audio(bytes):
    try:
        pg.init()
        pg.mixer.music.load(bytes)
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():
            pg.time.Clock().tick(10)
        pg.quit()
    except Exception as e:
        return f"An error occurred during audio playback: {e}"

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, camera_feed, dest_lang

    if event == cv2.EVENT_LBUTTONDOWN:
        button_index = check_button_click(x, y)
        if button_index is not None:
            languages = ['en', 'ar', 'fr', 'es', 'de', 'zh']
            if 0 <= button_index < len(languages):
                dest_lang = languages[button_index]
                print(f"Destination language changed to: {dest_lang}")
        else:
            drawing = True
            ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            frame = camera_feed.frame.copy()
            cv2.rectangle(frame, (ix, iy), (x, y), (0, 255, 0), 2)
            draw_buttons(frame)
            cv2.imshow('Camera Feed', frame)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        frame = camera_feed.frame.copy()
        cv2.rectangle(frame, (ix, iy), (x, y), (0, 255, 0), 2)
        draw_buttons(frame)
        cv2.imshow('Camera Feed', frame)
        camera_feed.roi = (ix, iy, x, y)

def draw_buttons(frame):
    languages = ['en', 'ar', 'fr', 'es', 'de', 'zh']
    lang_names = ['English', 'Arabic', 'French', 'Spanish', 'Deutsch', 'Chinese']
    button_height = 40
    button_width = 120
    button_spacing = 20
    for i, lang in enumerate(languages):
        y = i * (button_height + button_spacing)
        cv2.rectangle(frame, (10, y), (10 + button_width, y + button_height), (0, 0, 0), -1)
        text_size = cv2.getTextSize(lang_names[i], cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_x = 10 + (button_width - text_size[0]) // 2
        text_y = y + (button_height + text_size[1]) // 2
        cv2.putText(frame, lang_names[i], (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def check_button_click(x, y):
    button_height = 40
    button_width = 120
    button_spacing = 20
    if x < 10 + button_width:
        index = y // (button_height + button_spacing)
        if index < len(['en', 'ar', 'fr', 'es', 'de', 'zh']):
            return index
    return None

def main():
    global camera_feed, ix, iy, drawing, dest_lang
    camera_feed = CameraFeed()
    camera_feed.start()
    dest_lang = 'en'
    drawing = False
    ix, iy = -1, -1

    cv2.namedWindow('Camera Feed')
    cv2.setMouseCallback('Camera Feed', draw_rectangle)

    try:
        while True:
            frame = camera_feed.get_frame()
            if frame is not None:
                draw_buttons(frame)
                cv2.imshow('Camera Feed', frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

                if camera_feed.roi:
                    x1, y1, x2, y2 = camera_feed.roi
                    # Ensure ROI is within image boundaries and does not overlap with button area
                    x1, y1 = max(140, x1), max(0, y1)
                    x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
                    if x1 < x2 and y1 < y2:
                        roi_frame = frame[y1:y2, x1:x2]
                        text = perform_ocr(roi_frame)
                        if text:
                            print("Detected text:", text)
                            translated_text = translate_text(text, dest_lang=dest_lang)
                            print("Translated text:", translated_text)
                            audio_bytes = text_to_speech(translated_text, dest_lang=dest_lang)
                            if isinstance(audio_bytes, BytesIO):
                                play_audio(audio_bytes)
                            else:
                                print(audio_bytes)  # Print error message if text-to-speech failed
                    camera_feed.roi = None  # Reset ROI after processing

                if cv2.getWindowProperty('Camera Feed', cv2.WND_PROP_VISIBLE) < 1:
                    break
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        camera_feed.stop()

if __name__ == "__main__":
    main()