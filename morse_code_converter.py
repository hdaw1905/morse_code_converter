import tkinter as tk
from tkinter import messagebox
from pydub import AudioSegment
from pydub.generators import Sine
import os
import time
from playsound import playsound
import pygame

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': ' / '
}

# Convert text to Morse code
def text_to_morse(text):
    text = text.upper()
    return ' '.join(MORSE_CODE_DICT[char] for char in text if char in MORSE_CODE_DICT)

# Generate Morse code audio
def generate_morse_audio(morse_code):
    dot = Sine(700).to_audio_segment(duration=150)  # Dot sound
    dash = Sine(700).to_audio_segment(duration=400)  # Dash sound
    silence = AudioSegment.silent(duration=100)  # Space between symbols
    word_gap = AudioSegment.silent(duration=700)  # Space between words

    audio_sequence = AudioSegment.silent(duration=0)
    for symbol in morse_code:
        if symbol == '.':
            audio_sequence += dot + silence
        elif symbol == '-':
            audio_sequence += dash + silence
        elif symbol == '/':
            audio_sequence += word_gap
        else:
            audio_sequence += silence

    return audio_sequence

def play_morse(morse_code):
    timestamp = int(time.time())
    temp_file = f"temp_morse_{timestamp}.mp3"
    audio = generate_morse_audio(morse_code)
    audio.export(temp_file, format="mp3")

    try:
        pygame.mixer.init()  # Initialize the mixer module
        pygame.mixer.music.load(temp_file)  # Load the generated MP3 file
        pygame.mixer.music.play()  # Play the music

        while pygame.mixer.music.get_busy():  # Wait until the music finishes
            pygame.time.Clock().tick(10)

        # After the music finishes, delete the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except Exception as e:
        print(f"Error playing sound: {e}")
    finally:
        # Ensure the file is deleted if it's still there after playing
        if os.path.exists(temp_file):
            os.remove(temp_file)

def save_audio(morse_code):
    timestamp = int(time.time())
    filename = f"morse_code_{timestamp}.mp3"  # Add timestamp for uniqueness
    audio = generate_morse_audio(morse_code)
    audio.export(filename, format="mp3")  # Save the audio file with a unique name

    # Print the full path of the saved file
    full_path = os.path.abspath(filename)
    print(f"Audio saved as {full_path}")

    return filename

def save_text(morse_code):
    timestamp = int(time.time())
    filename = f"morse_code_{timestamp}.txt"  # Add timestamp for uniqueness
    with open(filename, "w") as file:
        file.write(morse_code)
    print(f"Text file saved as {filename}")
    return filename

# GUI Application using Tkinter
class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Converter")

        # Frame for the Left Tab and Main Area
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Panel for file list
        self.left_panel = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Listbox for displaying files
        self.file_listbox = tk.Listbox(self.left_panel, width=30, height=20)
        self.file_listbox.pack(pady=10)

        # Load files into the Listbox
        self.load_files()

        # Bind the Listbox selection event to open and preview the file
        self.file_listbox.bind("<ButtonRelease-1>", self.preview_file)

        # Right Panel for Morse Code App
        self.right_panel = tk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title Label
        self.title_label = tk.Label(self.right_panel, text="Morse Code Converter", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Text Input Label
        self.text_label = tk.Label(self.right_panel, text="Enter text to convert to Morse code:")
        self.text_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Text Input Field
        self.text_entry = tk.Entry(self.right_panel, width=40)
        self.text_entry.grid(row=1, column=1, padx=10, pady=5)

        # Convert Button
        self.convert_button = tk.Button(self.right_panel, text="Convert to Morse", command=self.convert_to_morse)
        self.convert_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Morse Code Output Label
        self.morse_label = tk.Label(self.right_panel, text="Morse Code:")
        self.morse_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Morse Code Output Text
        self.morse_output = tk.Label(self.right_panel, text="", width=40, height=4, relief="solid", anchor="w", justify="left")
        self.morse_output.grid(row=3, column=1, padx=10, pady=5)

        # Buttons for actions
        self.play_button = tk.Button(self.right_panel, text="Play Morse Code", command=self.play_morse_code, state=tk.DISABLED)
        self.play_button.grid(row=4, column=0, pady=10)

        self.save_audio_button = tk.Button(self.right_panel, text="Save as Audio", command=self.save_audio_file, state=tk.DISABLED)
        self.save_audio_button.grid(row=4, column=1, pady=10)

        self.save_text_button = tk.Button(self.right_panel, text="Save as Text", command=self.save_text_file, state=tk.DISABLED)
        self.save_text_button.grid(row=5, column=0, columnspan=2, pady=10)

    def load_files(self):
        # Load all .txt and .mp3 files from the current directory into the listbox
        files = [f for f in os.listdir() if f.endswith('.txt') or f.endswith('.mp3')]
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def preview_file(self, event):
        # Get the selected file
        selected_file = self.file_listbox.get(self.file_listbox.curselection())

        if selected_file.endswith('.txt'):
            # Display the content of the text file
            with open(selected_file, 'r') as file:
                content = file.read()
                self.morse_output.config(text=content)
        elif selected_file.endswith('.mp3'):
            # Play the sound of the audio file
            playsound(selected_file)

    def convert_to_morse(self):
        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        morse_code = text_to_morse(text)
        self.morse_output.config(text=morse_code)
        self.play_button.config(state=tk.NORMAL)
        self.save_audio_button.config(state=tk.NORMAL)
        self.save_text_button.config(state=tk.NORMAL)

    def play_morse_code(self):
        morse_code = self.morse_output.cget("text")
        if morse_code:
            play_morse(morse_code)

    def save_audio_file(self):
        morse_code = self.morse_output.cget("text")
        if morse_code:
            filename = save_audio(morse_code)
            messagebox.showinfo("Success", f"Audio saved as {filename}")

    def save_text_file(self):
        morse_code = self.morse_output.cget("text")
        if morse_code:
            filename = save_text(morse_code)
            messagebox.showinfo("Success", f"Text file saved as {filename}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeApp(root)
    root.mainloop()
