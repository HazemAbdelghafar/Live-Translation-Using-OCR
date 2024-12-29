# Live OCR Project

This project utilizes the laptop camera for live feed to perform Optical Character Recognition (OCR) on detected text, translate it, and convert the translation to speech.

## Project Structure

```
live-ocr-project
├── src
│   ├── live_ocr.py          # Main script for live feed and processing
│   ├── camera_feed.py       # Handles camera feed and image capture
│   ├── ocr.py               # Functions for Optical Character Recognition
│   ├── translation.py        # Functions for translating extracted text
│   └── text_to_speech.py    # Functions for converting text to speech
├── requirements.txt          # Lists project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd live-ocr-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have Tesseract OCR installed on your system. Follow the installation instructions for your operating system.

## Usage Guidelines

1. Run the main script to start the live OCR process:
   ```
   python src/live_ocr.py
   ```

2. The application will access your laptop's camera, capture frames, and process them for text recognition, translation, and speech output.

## Dependencies

- OpenCV
- pytesseract
- gTTS
- Translation library (e.g., googletrans)

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.