from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
# path of csv for list of words
LANG_LIST = "./data/french_words.csv"
LEARN_LIST = "./data/words_to_learn.csv"
# language
LANG = "French"
current_card = {}

# data is the list of words to learn
# but if it is the first run it is the orignial list
try:
    data = pandas.read_csv(LEARN_LIST)
except FileNotFoundError:
    data = pandas.read_csv(LANG_LIST)
finally:
    to_learn = data.to_dict(orient="records")


# if word is known remove it from words to learn list
def is_known():
    to_learn.remove(current_card)
    data_to_save = pandas.DataFrame(to_learn)
    data_to_save.to_csv("data/words_to_learn.csv", index=FALSE)
    next_card()


# choose a random word
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    word_to_learn = current_card[LANG]
    # update text to the word
    canvas.itemconfig(card_title, text=LANG, fill="black")
    canvas.itemconfig(word, text=word_to_learn, fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    # wait 3 seconds then flip the card
    flip_timer = window.after(3000, func=flip_card)


# shows the translation
def flip_card():
    eg_word = current_card["English"]

    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(word, text=eg_word, fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# window config
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
# the know button
yes_image = PhotoImage(file="./images/right.png")
yes_button = Button(image=yes_image, highlightthickness=0, command=is_known)
yes_button.grid(column=1, row=1)
# the don't know button
no_image = PhotoImage(file="./images/wrong.png")
no_button = Button(image=no_image, highlightthickness=0, command=next_card)
no_button.grid(column=0, row=1)
# flashcard
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="./images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_back_img = PhotoImage(file="./images/card_back.png")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, font=("Ariel", 60, "italic"))
canvas.grid(column=0, row=0, columnspan=2)
# starts going through the cards
next_card()

window.mainloop()
