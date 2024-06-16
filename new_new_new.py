import tkinter as tk
from tkinter import messagebox
import random
import words

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.guesses = 6
        self.word = ''
        self.guessed_letters = []
        self.guess_entry = ''
        self.word_list = ['_']
        self.create_game_window()

    def create_game_window(self):
        # Create the canvas for drawing the hangman
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.grid(column=0, row=0)

        # Draw the scaffold
        self.canvas.create_line(20, 280, 120, 280)
        self.canvas.create_line(70, 280, 70, 20)
        self.canvas.create_line(70, 20, 170, 20)
        self.canvas.create_line(170, 20, 170, 50)
        #define the list of categories for the player to select from
        options_list = ["FOOD", "DANCE", "CLOTHING", "TRANSPORT", "ORGANS"]
        self.value_inside = tk.StringVar(root)
        self.value_inside.set("select")
        question_menu = tk.OptionMenu(root, self.value_inside, *options_list, command=self.start_game)
        question_menu.config(bg='IndianRed')
        question_menu.grid(row=1, column=0)

    def start_game(self, category):
        category = self.value_inside.get().lower()
        words_dict = {
            'food': words.Food,
            'dance': words.dance,
            'clothing': words.clothing,
            'transport': words.transport,
            'organs': words.organs,
            'select': "invalid"
        }
        category_words = words_dict.get(category, [])
        if not category_words:
            messagebox.showinfo("Error", "Invalid category selected.")
            return
        self.word = random.choice(category_words)
        self.screen()

    def screen(self):
        self.word_label = tk.Label(root, text=" ".join("_" for letter in self.word), bd=5, fg='darkblue', font='bold')
        self.word_label.grid(column=0, row=2)

        # Create a label for displaying the number of guesses remaining
        self.guesses_label = tk.Label(root, text="Guesses remaining: {}".format(self.guesses),fg='Maroon')
        self.guesses_label.grid(column=0, row=3)

        # Create a label for displaying the letters guessed so far
        self.guessed_label = tk.Label(root, text="Guessed letters: ")
        self.guessed_label.grid(column=0, row=4)

        # Create an entry for the user to guess a letter
        self.guess_entry = tk.Entry(root)
        self.guess_entry.config(bg='lightsalmon')
        self.guess_entry.grid(column=0, row=5)
        self.guess_entry.bind('<Return>', lambda event: self.check_guess())

    def check_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        # Check if the guess is a single letter
        if len(guess) != 1 or not guess.isalpha():
            return

        # Check if the guess has already been guessed
        if guess in self.guessed_letters:
            return

        self.guessed_letters.append(guess)
        self.guessed_label.config(text="Guessed letters: {}".format(" ".join(self.guessed_letters)))

        # Check if the guess is in the word
        if guess in self.word:
            self.word_list = list(self.word_label["text"])
            for i in range(len(self.word)):
                if self.word[i] == guess:
                    self.word_list[2 * i] = guess
            self.word_label.config(text="".join(self.word_list))

        # If the guess is not in the word, decrement the number of guesses remaining
        else:
            self.guesses -= 1
            self.guesses_label.config(text="Guesses remaining: {}".format(self.guesses))

            # Draw the hangman
            if self.guesses == 5:
                self.canvas.create_oval(140, 50, 200, 110,width=1,fill= 'indianred')
            elif self.guesses == 4:
                self.canvas.create_line(170, 110, 170, 170,width=4,fill='indianred')
            elif self.guesses == 3:
                self.canvas.create_line(170, 130, 140, 140,width=4,fill= 'indianred')
            elif self.guesses == 2:
                self.canvas.create_line(170, 130, 200, 140,width=4,fill= 'indianred')
            elif self.guesses == 1:
                self.canvas.create_line(170, 170, 140, 190,width=4,fill= 'indianred')
            elif self.guesses == 0:
                self.canvas.create_line(170, 170, 200, 190,width=4,fill= 'indianred')
                self.end_game("lose")

        # Check if the user has won
        if "_" not in self.word_list:
            self.end_game("win")

    def end_game(self, result):
        if result == "win":
            messagebox.showinfo("Hangman", "You win!")
        elif result == "lose":
            messagebox.showinfo("Hangman", "You lose! The word was '{}'".format(self.word))

        retry_button = tk.Button(root, text="Try Again", command=self.restart_game)
        retry_button.config(bg='indianred')
        retry_button.grid(column=0, row=6)

        self.guess_entry.config(state=tk.DISABLED)

    def restart_game(self):
        self.guesses = 6
        self.word = ''
        self.guessed_letters = []
        self.guess_entry.config(state=tk.NORMAL)

        # Reset the OptionMenu to its default value ("select")
        self.value_inside.set("select")

        # Destroy previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Start a new game
        self.create_game_window()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

