# Live Translation Project

This project utilizes the laptop camera for live feed to perform Optical Character Recognition (OCR) on detected text, translate it, and convert the translation to speech.

## Project Structure

```
live-translation-project
├── live_translation.py      # Main script for live feed and processing
├── requirements.txt         # Lists project dependencies
└── README.md                # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/HazemAbdelghafar/Live-Translation-Using-OCR.git
   cd Live-Translation-Using-OCR
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have Tesseract OCR installed on your system. Follow the installation instructions for your operating system.

## Usage Guidelines

1. Run the main script to start the live translation process:
   ```
   python live_translation.py
   ```

2. The application will access your laptop's camera, capture frames, and process them for text recognition, translation, and speech output.

## Dependencies

- OpenCV
- pytesseract
- gTTS
- pygame
- translate

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.