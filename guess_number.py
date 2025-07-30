import random


import os
import subprocess
import sys

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
        # Try to use paplay with system sounds if available
        if sound_type == 'error':
            # Standard error sound on many Linux distros
            subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/dialog-error.oga"], check=False)
        elif sound_type == 'success':
            # Standard complete sound on many Linux distros
            subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"], check=False)
    else:
        pass  # No sound for other OS

def main():
    number_to_guess = random.randint(1, 20)
    attempts = 0
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 20.")
    while True:
        try:
            guess = int(input("Take a guess: "))
            attempts += 1
            if guess < 1 or guess > 20:
                print("Please enter a number between 1 and 20.")
                # Play error sound for invalid input
                play_sound('error')
                continue
            if guess < number_to_guess:
                print("Your guess is too low.")
                # Play error sound for wrong guess
                play_sound('error')
            elif guess > number_to_guess:
                print("Your guess is too high.")
                # Play error sound for wrong guess
                play_sound('error')
            else:
                print(f"Good job! You guessed my number in {attempts} attempts.")
                # Play success sound for correct guess
                play_sound('success')
                break
        except ValueError:
            print("Please enter a valid integer.")
            # Play error sound for invalid input
            play_sound('error')

if __name__ == "__main__":
    main()
