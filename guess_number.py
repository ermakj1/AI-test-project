import random

import os
import subprocess

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
                subprocess.run(["afplay", "/System/Library/Sounds/Funk.aiff"], check=False)
                continue
            if guess < number_to_guess:
                print("Your guess is too low.")
                # Play error sound for wrong guess
                subprocess.run(["afplay", "/System/Library/Sounds/Funk.aiff"], check=False)
            elif guess > number_to_guess:
                print("Your guess is too high.")
                # Play error sound for wrong guess
                subprocess.run(["afplay", "/System/Library/Sounds/Funk.aiff"], check=False)
            else:
                print(f"Good job! You guessed my number in {attempts} attempts.")
                # Play success sound for correct guess
                subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], check=False)
                break
        except ValueError:
            print("Please enter a valid integer.")
            # Play error sound for invalid input
            subprocess.run(["afplay", "/System/Library/Sounds/Funk.aiff"], check=False)

if __name__ == "__main__":
    main()
