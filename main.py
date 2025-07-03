import speech_recognition as sr
import math
from datetime import datetime

HISTORY_FILE = 'history.txt'

def show_history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            lines = file.readlines()
            if not lines:
                print("No history found!")
            else:
                for line in reversed(lines):
                    print(line.strip())
    except FileNotFoundError:
        print("No history file exists yet.")

def clear_history():
    open(HISTORY_FILE, 'w').close()
    print('History cleared.')

def save_to_history(equation, result):
    with open(HISTORY_FILE, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"{timestamp} | {equation} = {result}\n")

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣 You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your voice.")
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
    return None

def preprocess_input(text):
    # Replace words with symbols
    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("times", "*")
    text = text.replace("multiplied by", "*")
    text = text.replace("into", "*")
    text = text.replace("divided by", "/")
    text = text.replace("over", "/")
    text = text.replace("mod", "%")
    text = text.replace("percent", "%")
    text = text.replace("power", "^")
    return text

def calculate(user_input):
    user_input = preprocess_input(user_input)

    parts = user_input.split()
    if len(parts) == 2 and parts[0] == "sqrt":
        try:
            num = float(parts[1])
            if num < 0:
                print("Error: Cannot take square root of a negative number.")
                return
            result = math.sqrt(num)
            print("Result:", result)
            save_to_history(user_input, result)
        except ValueError:
            print("Error: Invalid number for square root.")
        return

    if len(parts) != 3:
        print("Invalid input. Use format: number operator number")
        return

    try:
        num1 = float(parts[0])
        op = parts[1]
        num2 = float(parts[2])

        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 == 0:
                print("Error: Division by zero!")
                return
            result = num1 / num2
        elif op == "%":
            result = (num1 * num2) / 100
            print(f"{num2}% of {num1} is {result}")
        elif op in ("^", "**"):
            result = num1 ** num2
        else:
            print("Invalid operator. Use only + - * / % ^ sqrt")
            return

        if result == int(result):
            result = int(result)

        print("Result:", result)
        save_to_history(user_input, result)
    except ValueError:
        print("Error: Please enter valid numbers.")

def main():
    print('--- VOICE + TEXT CALCULATOR ---')
    print("Say or type: 5 + 2 | sqrt 9 | 10 percent 200 | exit | history | clear")

    while True:
        mode = input("\nType 'voice' to speak or press Enter to type: ").strip().lower()

        if mode == 'voice':
            user_input = get_voice_input()
            if not user_input:
                continue
        else:
            user_input = input(">> ").strip().lower()

        if user_input == 'exit':
            print('Goodbye!')
            break
        elif user_input == 'history':
            show_history()
        elif user_input == 'clear':
            clear_history()
        else:
            calculate(user_input)

main()
