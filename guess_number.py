
import random
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def play_sound(sound_type):
    if sys.platform.startswith('win'):
        import winsound
        if sound_type == 'error':
            winsound.MessageBeep(winsound.MB_ICONHAND)
        elif sound_type == 'success':
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    elif sys.platform == 'darwin':
        if sound_type == 'error':
            subprocess.run(["afplay", "/System/Library/Sounds/Funk.aiff"], check=False)
        elif sound_type == 'success':
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], check=False)
    elif sys.platform.startswith('linux'):
        if sound_type == 'error':
            subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/dialog-error.oga"], check=False)
        elif sound_type == 'success':
            subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"], check=False)
    else:
        pass

class GuessingGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Number Guessing Game")
        master.resizable(False, False)

        self.number_to_guess = random.randint(1, 20)
        self.attempts = 0

        self.label = tk.Label(master, text="I'm thinking of a number between 1 and 20.")
        self.label.pack(pady=10)

        self.entry = tk.Entry(master)
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', self.check_guess)

        self.guess_button = tk.Button(master, text="Guess", command=self.check_guess)
        self.guess_button.pack(pady=5)

        self.message_label = tk.Label(master, text="")
        self.message_label.pack(pady=10)

        self.reset_button = tk.Button(master, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(pady=5)

    def check_guess(self, event=None):
        guess_str = self.entry.get()
        try:
            guess = int(guess_str)
            self.attempts += 1
            if guess < 1 or guess > 20:
                self.message_label.config(text="Please enter a number between 1 and 20.", fg="red")
                play_sound('error')
                return
            if guess < self.number_to_guess:
                self.message_label.config(text=f"Your guess ({guess}) is too low.", fg="blue")
                play_sound('error')
            elif guess > self.number_to_guess:
                self.message_label.config(text=f"Your guess ({guess}) is too high.", fg="blue")
                play_sound('error')
            else:
                self.message_label.config(text=f"Good job! You guessed my number in {self.attempts} attempts.", fg="green")
                play_sound('success')
                self.reset_game()
        except ValueError:
            self.message_label.config(text="Please enter a valid integer.", fg="red")
            play_sound('error')
        finally:
            self.entry.delete(0, tk.END)

    def reset_game(self):
        self.number_to_guess = random.randint(1, 20)
        self.attempts = 0
        self.message_label.config(text="Game reset! I'm thinking of a new number.", fg="black")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGameGUI(root)
    root.mainloop()
