import json
import os
import time
import unicodedata

import pynput

from bs4 import BeautifulSoup
from pynput.keyboard import Key


def go_next(x, y, mouse):
    if mouse.position != (x, y):
        mouse.position = (x, y)
    time.sleep(.1)
    mouse.click(pynput.mouse.Button.left, 1)


def save_page(name, keyboard, sleep_time=.5):
    keyboard.press(Key.cmd.value)
    keyboard.press("s")
    keyboard.release(Key.cmd.value)
    keyboard.release("s")

    time.sleep(sleep_time)

    # name file
    name = str(name)
    for digit in name:
        keyboard.press(digit)
        keyboard.release(digit)
        time.sleep(sleep_time)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def download_exam(x, y, num_questions):
    """
    Iterates through and downloads all pages of Udemy exam as html files.

    Assummes:
        1. You are on the first page of the exam i.e. starting on Question 1
        2. 'Next' button position is hard-coded in as input params
        3. Default directory for saving files is set correctly
    """
    mouse = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()

    mouse.position = (100, 100)
    time.sleep(.1)
    mouse.click(pynput.mouse.Button.left, 1)
    time.sleep(.1)

    for i in range(1, num_questions + 1):
        time.sleep(4)
        save_page(i, keyboard)
        time.sleep(4)
        if i != num_questions:
            go_next(x, y, mouse)


def get_question_text(html):
    soup = BeautifulSoup(html, features="lxml")
    q_class = "ud-text-bold mc-quiz-question--question-prompt--2_dlz rt-scaffolding"
    question = soup.find("div", {"class": q_class}).get_text().strip()
    question = unicodedata.normalize("NFKD", question)
    c_class = "mc-quiz-question--answer--eCdL3"
    choices = []
    for choice in soup.find_all("li", {"class": c_class}):
        choices.append(unicodedata.normalize("NFKD", choice.get_text()).strip())
    
    return question, choices


def get_all_question_text(question_dir, num_questions):
    exam = {i: {"Question": "", "Choices": []} for i in range(1, num_questions + 1)}
    for i in range(1, num_questions + 1):
        fle_path = os.path.join(question_dir, f"{i}.html")
        with open(fle_path, "r") as fle:
            html = fle.read()
        question, choices = get_question_text(html)
        exam[i]["Question"] = question
        exam[i]["Choices"] = choices

    num_dupes = len(exam) - len({exam[i]["Question"] for i in range(1, len(exam) + 1)})
    if num_dupes != 0:
        print(f"{num_dupes} Duplicate Question(s)!")

    return exam


def exam_to_txt(exam_dct, txt_name):
    numberings = ["A.", "B.", "C.", "D.", "E."]
    with open(txt_name, "w") as fle:
        for i in range(1, num_questions + 1):
            fle.write(f"Question {i}\n")
            fle.write(exam_dct[i]["Question"] + "\n\n")
            for j, choice in enumerate(exam[i]["Choices"]):
                fle.write(f"{numberings[j]} {choice}\n")
            fle.write("\n\n")


if __name__ == "__main__":
    num_questions = 65
    # download_exam(1154, 728, 65)
    
    # Change me as necessary
    nth_exam = 6
    if nth_exam == 4:
        num_questions = 64
    downloaded_path = f"/Users/dstan/Desktop/Udemy/Exam_{nth_exam}"
    
    # extracts questions and answer choices as dict
    exam = get_all_question_text(downloaded_path, num_questions)

    # export dict as json file
    with open(os.path.join(downloaded_path, f"exam_{nth_exam}.json"), "w") as fle:
        json.dump(exam, fle)
    # export dict as minimally formatted txt file for reading
    exam_to_txt(exam, os.path.join(downloaded_path, f"exam_{nth_exam}.txt"))
