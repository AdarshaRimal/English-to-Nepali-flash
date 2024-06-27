from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/data.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")  # list contains dictionaries here


def next_cards():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="english")
    canvas.itemconfig(card_word, text=current_card["english"])
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="नेपाली")
    canvas.itemconfig(card_word, text=current_card["nepali"])
    canvas.itemconfig(card_background, image=back_image)


def is_known():
    to_learn.remove(current_card)
    current_data = pandas.DataFrame(to_learn)
    current_data.to_csv("./data/words_to_learn.csv", index=False)

    next_cards()


window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
card_front_image = PhotoImage(file="./images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_image)
back_image = PhotoImage(file="./images/card_back.png")

card_title = canvas.create_text(400, 150, text="title", font=("ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("ariel", 40, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="./images/wrong.png")
right_image = PhotoImage(file="./images/right.png")

wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_cards)
wrong_button.grid(row=1, column=0)
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_cards()

window.mainloop()
