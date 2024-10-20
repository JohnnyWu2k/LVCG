import tkinter as tk
from tkinter import messagebox
import requests
import random
import os

# Check and read the score
def read_score():
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    else:
        return 0

# Save the score
def save_score(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

# Initialize the score
score = read_score()

# Datamuse API to fetch words starting with a letter
def get_words_starting_with(letter):
    url = f"https://api.datamuse.com/words?sp={letter}*&max=100"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            words = [word['word'] for word in data]
            return words if words else None
        else:
            return None
    except Exception as e:
        print(f"Error fetching words: {e}")
        return None

# Free Dictionary API to get word details and examples
def get_word_with_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                word_data = data[0]  # Word data from the response
                word = word_data['word']
                
                # Retrieve the part of speech and example sentence
                meanings = word_data.get('meanings', [])
                if meanings:
                    definitions = meanings[0].get('definitions', [])
                    if definitions and 'example' in definitions[0]:
                        example_sentence = definitions[0]['example']
                        return word, example_sentence
                    else:
                        return word, None
                else:
                    return word, None
            else:
                return word, None
        else:
            print(f"Error fetching word details for {word}: {response.status_code}")
            return word, None
    except Exception as e:
        print(f"Error fetching word details: {e}")
        return word, None

# Generate word options and example sentence
def generate_question(letter):
    words = get_words_starting_with(letter)

    if not words:
        messagebox.showerror("Error", "No words found for this letter. Please try another.")
        return

    # Attempt to find a word with an example
    correct_word, example_sentence = None, None
    while correct_word is None:
        potential_word = random.choice(words)
        correct_word, example_sentence = get_word_with_details(potential_word)

        # If no example is found, remove the word and try again
        if example_sentence is None or correct_word not in example_sentence:
            words.remove(potential_word)
            correct_word, example_sentence = None, None

        # Exit if the list is empty
        if not words:
            messagebox.showerror("Error", "Unable to find a word with an example. Try another letter.")
            return

    if correct_word in example_sentence:
        sentence_with_blank = example_sentence.replace(correct_word, "_____")

        # Pick two incorrect options
        wrong_choices = random.sample([w for w in words if w != correct_word], 2)

        # Combine correct answer and incorrect options
        choices = wrong_choices + [correct_word]
        random.shuffle(choices)

        # Display the question
        show_question(sentence_with_blank, choices, correct_word)

# Display the fill-in-the-blank question
def show_question(sentence, choices, correct_word):
    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()

    # Display the question label
    question_label = tk.Label(root, text=sentence, wraplength=400, font=("Helvetica", 14))
    question_label.pack(pady=20)

    # Display answer buttons
    for i, choice in enumerate(choices):
        button = tk.Button(root, text=choice, font=("Helvetica", 12), width=20,
                           bg="#3498db", fg="white",
                           command=lambda c=choice: check_answer(c, correct_word))
        button.pack(pady=5)

# Check if the answer is correct
def check_answer(selected_word, correct_word):
    global score
    if selected_word == correct_word:
        messagebox.showinfo("Result", "Correct! Well done!")
        score += 1
    else:
        messagebox.showerror("Result", f"Incorrect. The correct answer was {correct_word}.")
    save_score(score)
    reset_game()

# Reset the game and display letter options
def reset_game():
    for widget in root.winfo_children():
        widget.destroy()
    create_letter_buttons()

# Create letter buttons
def create_letter_buttons():
    instruction_label = tk.Label(root, text=f"Select a letter to start the game (Current Score: {score}):", font=("Helvetica", 14))
    instruction_label.pack(pady=20)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        button = tk.Button(frame, text=letter, font=("Helvetica", 12), width=5,
                           bg="#2ecc71", fg="white",
                           command=lambda l=letter: generate_question(l))
        button.grid(row=(ord(letter) - 65) // 6, column=(ord(letter) - 65) % 6, padx=5, pady=5)

# Set up the main window
root = tk.Tk()
root.title("Letter Selection Fill-in-the-Blank Game")
root.geometry("600x450")
root.configure(bg="#ecf0f1")

# Initialize the game
create_letter_buttons()

# Run the main loop
root.mainloop()
