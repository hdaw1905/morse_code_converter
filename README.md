# Morse Code Converter

A simple Morse Code Converter application built using Python's Tkinter GUI framework. This application converts plain text into Morse code, plays the generated Morse code audio, and allows users to save both the Morse code text and audio files.

## Features

- Convert text to Morse code.
- Play Morse code audio.
- Save Morse code as text or audio files.
- Preview previously saved audio and text files.

## Requirements

To run this application, you need to have the following Python packages installed:

- `tkinter` (usually included with Python)
- `pydub`
- `playsound`
- `pygame`
- `numpy` (optional, for generating sound)

You can install the required packages using pip:

```bash
pip install pydub playsound pygame
```

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/hdaw1905/morse_code_converter.git
```

2. Run the application:
Make sure you have the necessary dependencies installed. Then, execute the script:
```bash
python morse_code_converter.py
```

## Usage
1. Enter Text: Type the text you want to convert to Morse code in the input field.
2. Convert: Click the "Convert to Morse" button to see the Morse code output.
3. Play Morse Code: Click the "Play Morse Code" button to listen to the Morse code.
4. Save Files: Use the "Save as Audio" and "Save as Text" buttons to save your Morse code.

### Code Overview
## Main Components
- Morse Code Dictionary: A dictionary that maps each letter and number to its Morse code representation.
# Functions:
- text_to_morse(text): Converts input text to Morse code.
- generate_morse_audio(morse_code): Generates audio for the given Morse code.
- play_morse(morse_code): Plays the generated Morse code audio.
- save_audio(morse_code): Saves the Morse code audio to a file.
- save_text(morse_code): Saves the Morse code text to a file.
- MorseCodeApp Class: The main GUI class that sets up the interface and handles user interactions.

## GUI Layout
- Left Panel: Displays a list of saved audio and text files.
- Right Panel: Contains input fields, buttons for actions, and displays the Morse code output.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Acknowledgments
[pydub] for audio manipulation.
[pygame] for audio playback.
[Tkinter] for creating the GUI.

## Contributing
Feel free to submit issues or pull requests for improvements or bug fixes.
