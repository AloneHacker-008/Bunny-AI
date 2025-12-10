# Bunny - Friendly Bunny AI Chatbot (Python version of your C program)
# Creator : Anup Prasad

import time
import datetime
import random
import webbrowser
import sys
import math
import ast
import operator
import os  # Added for clear command
import json  # Added for history saving/loading
from openai import OpenAI

# ---------------- API KEY LOADER ----------------

def load_api_key():
    """
    Loads API key from key.txt file.
    If key.txt is missing or empty, Bunny will stop with a friendly message.
    """
    try:
        with open("key.txt", "r") as f:
            key = f.read().strip()
            if not key:
                print("Bunny: key.txt is empty! Please paste your OpenAI API key inside key.txt")
                return None
            return key
    except FileNotFoundError:
        print("Bunny: Missing key.txt! Please create a file named 'key.txt' and paste your OpenAI API key into it.")
        return None


# Load API key
API_KEY = load_api_key()

# If key missing → stop the program
if API_KEY is None:
    import sys
    sys.exit(0)

# Initialize OpenAI client with loaded key
client = OpenAI(api_key=API_KEY)

# ---------------- RANDOM SEED ----------------
random.seed(int(time.time()))

HISTORY_FILE = "chat_history.json"
MEMORY_FILE = "memory.json"

# ---------------- Load Memory and Initialize Messages ----------------
def load_memory_and_init():
    system_prompt = """
    You are Bunny, a friendly and helpful AI chatbot created by Anup Prasad.
    Respond in a warm, engaging, and fun way, like a best friend.
    Understand and reply in the user's language (e.g., if they speak Hindi, respond in Hindi; if English, in English).
    Keep replies concise but natural. If the user asks something specific, answer accurately, but always add a friendly touch.
    Be empathetic, fun, and supportive in all interactions.
    Avoid repeating generic questions like "how are you" unless directly asked. Respond based on the user's input.
    """
    memory = ""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                memory_data = json.load(f)
                memory = memory_data.get("summary", "")
        except json.JSONDecodeError:
            memory = ""
    if memory:
        system_prompt += f"\n\nImportant memory from previous conversations: {memory}"
    return [{"role": "system", "content": system_prompt}]

# ---------------- Save History ----------------
def save_history(messages):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(messages, f)
    except Exception as e:
        print(f"Bunny: Error saving history: {e}")

# ---------------- Save Memory ----------------
def save_memory(summary):
    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump({"summary": summary}, f)
    except Exception as e:
        print(f"Bunny: Error saving memory: {e}")

# ---------------- Generate Summary ----------------
def generate_summary(messages):
    # Only summarize if there are more than 2 user messages (excluding system)
    user_messages = [msg for msg in messages if msg["role"] == "user"]
    if len(user_messages) <= 2:
        return "" 

    # No summary needed for short convos
    # Prepare messages for summary (exclude system, keep user and assistant)
    convo_messages = [msg for msg in messages if msg["role"] != "system"]
    summary_prompt = "Summarize the key points, topics discussed, user preferences, and any important information from this conversation in 2-3 sentences. Focus on what Bunny should remember for future interactions."
    convo_messages.append({"role": "user", "content": summary_prompt})
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=convo_messages,
            temperature=0.5,
            max_tokens=200,
            presence_penalty=0.0,
            frequency_penalty=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Bunny: Error generating summary: {e}")
        return ""

# ---------------- Ask AI Function ----------------
def ask_ai(question, messages):
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=1.0,
        top_p=1.0,
        max_tokens=5000,
        presence_penalty=0.6,
        frequency_penalty=0.0
    )
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    save_history(messages)
    return answer

# ---------------- Show Time ----------------
def show_time():
    now = datetime.datetime.now()
    print(f"Bunny: Current time is {now.strftime('%Y-%m-%d %H:%M:%S')} (Local time)\n")

# ---------------- Greet by time ----------------
def greet_by_time():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        print("Bunny: Good morning ! Hope your day starts great!")
    elif 12 <= hour < 17:
        print("Bunny: Good afternoon ! How's your day going?")
    elif 17 <= hour < 21:
        print("Bunny: Good evening ! Hope you had a productive day!")
    else:
        print("Bunny: Good night ! Working late, huh? Take care!")

# ---------------- Arithmetic for many numbers ----------------
def arithmetic_many(user_input):
    parts = user_input.split()
    if len(parts) < 3:
        print("Bunny: Please enter operation followed by at least two numbers (e.g. 'sum 1 2 3').")
        return
    cmd = parts[0]
    try:
        nums = [float(x) for x in parts[1:]]
    except ValueError:
        print("Bunny: Couldn't parse numbers. Make sure to enter numeric values.")
        return
    result = nums[0]
    for n in nums[1:]:
        if cmd in ("sum", "add", "jod"):
            result += n
        elif cmd in ("sub", "subtract", "ghata"):
            result -= n
        elif cmd in ("mul", "multiply", "guna"):
            result *= n
        elif cmd in ("div", "divide", "bhag"):
            if n == 0:
                print("Bunny: Division by zero!")
                return
            result /= n
        else:
            print("Bunny: Unknown command. Use sum/add/sub/mul/div.")
            return
    print(f"Bunny: Result = {result:.2f}")

# ---------------- Safe BODMAS evaluator using ast ----------------
_allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
}

def _eval_ast(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type in _allowed_operators:
            try:
                return _allowed_operators[op_type](left, right)
            except ZeroDivisionError:
                raise ZeroDivisionError
        else:
            raise ValueError("Unsupported operator")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type in _allowed_operators:
            return _allowed_operators[op_type](operand)
        else:
            raise ValueError("Unsupported unary operator")
    elif isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    else:
        raise ValueError("Unsupported expression")

def evaluate_bodmas(expr_str):
    expr = expr_str.strip()
    try:
        parsed = ast.parse(expr, mode='eval')
        result = _eval_ast(parsed)
        print(f"Bunny: Result = {float(result):.2f}")
    except ZeroDivisionError:
        print("Bunny: Division by zero!")
    except Exception:
        print("Bunny: Could not evaluate expression. Only arithmetic allowed.")

# ---------------- Number System Converter ----------------
def number_system_conversion():
    try:
        print("\nBunny: Number System Converter Menu")
        print("1. Binary to Decimal/Octal/Hexa")
        print("2. Decimal to Binary/Octal/Hexa")
        print("3. Octal to Decimal/Binary/Hexa")
        print("4. Hexadecimal to Decimal/Binary/Octal")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            b = input("Enter Binary: ").strip()
            dec = int(b, 2)
            print(f"Decimal: {dec}\nOctal: {oct(dec)[2:]}\nHexa: {hex(dec)[2:].upper()}\n")
        elif choice == "2":
            d = int(input("Enter Decimal: ").strip())
            print("Binary:", bin(d)[2:])
            print("Octal:", oct(d)[2:])
            print("Hexa:", hex(d)[2:].upper())
        elif choice == "3":
            o = input("Enter Octal: ").strip()
            dec = int(o, 8)
            print(f"Decimal: {dec}\nHexa: {hex(dec)[2:].upper()}\nBinary: {bin(dec)[2:]}\n")
        elif choice == "4":
            h = input("Enter Hexa: ").strip()
            dec = int(h, 16)
            print(f"Decimal: {dec}\nOctal: {oct(dec)[2:]}\nBinary: {bin(dec)[2:]}\n")
        else:
            print("Bunny: Invalid choice!")
    except ValueError:
        print("Bunny: Invalid number for that base!")

# ---------------- Helper: open URL ----------------
def open_url(url):
    try:
        webbrowser.open_new_tab(url)
    except Exception as e:
        print("Bunny: Couldn't open browser:", e)

# ---------------- Main Chat Loop ----------------
def main():
    messages = load_memory_and_init()
    print("\nBunny: Hey! I'm Bunny - your AI Assistant")
    greet_by_time()
    print("Type anything to chat with me (type 'bye' to exit)")
    print("For AI questions, type 'ai <question>'")
    print()

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            # On exit, generate summary, save memory, but keep history
            summary = generate_summary(messages)
            if summary:
                save_memory(summary)
            # Removed: if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE)
            print("\nBunny: Bye! Take care.")
            sys.exit(0)

        user_input = user_input.strip()
        if user_input == "":
            continue
        lower = user_input.lower()

        if lower == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue

        if lower.startswith("ai "):
            question = user_input[3:].strip()
            print("Bunny: Asking OpenAI...")
            answer = ask_ai(question, messages)
            print(f"Bunny: {answer}")
            print()
            continue

        # Check if any word in input is "bye" or "exit"
        words = lower.split()
        if "bye" in words or "exit" in words:
            # On bye, generate summary, save memory, but keep history
            summary = generate_summary(messages)
            if summary:
                save_memory(summary)
            # Removed: if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE)
            print("Bunny: Aww, you're leaving already? Take care, my friend!")
            sys.exit(0)

        # Removed hardcoded responses for name, thanks, love, creator, greetings, motivation to let AI handle full context

        # Made time condition stricter: only exact match
        if lower == "time" or lower == "date" or lower == "samay" or lower == "tarikh":
            show_time()
            continue

        if lower == "convert" or lower == "number system" or lower == "convert karo":
            number_system_conversion()
            continue

        if any(lower.startswith(k) for k in ["sum ", "add ", "sub ", "subtract ", "mul ", "multiply ", "div ", "divide ", "jod ", "ghata ", "guna ", "bhag "]):
            arithmetic_many(lower)
            continue

        if any(ch in lower for ch in "+-*/()"):
            expr_chars = set("0123456789.+-*/() ")
            if all((c in expr_chars) for c in lower):
                evaluate_bodmas(lower)
                continue

        if lower.startswith("lyrics") or lower.startswith("gaana lyrics") or lower.startswith("song lyrics"):
            song = input("Bunny: Which song's lyrics do you want? ").strip()
            question = f"Provide the lyrics for the song '{song}'. If possible, include the artist or source."
            answer = ask_ai(question, messages)
            print(f"Bunny: {answer}")
            print()
            continue

        if lower.startswith("weather") or lower.startswith("mausam"):
            location = input("Bunny: Please enter your city name: ").strip()
            url = f"https://www.google.com/search?q=weather+in+{location.replace(' ', '+')}"
            print(f"Bunny: Fetching weather for {location}...")
            open_url(url)
            continue

        if lower == "open google" or lower == "google kholo":
            print("Bunny: Opening Google...")
            open_url("https://www.google.com")
            continue

        if lower == "open youtube" or lower == "youtube kholo":
            print("Bunny: Opening YouTube...")
            open_url("https://www.youtube.com")
            continue

        if lower.startswith("play music") or lower.startswith("song") or lower.startswith("music") or lower.startswith("gaana"):
            print("Bunny: Music time! Choose:")
            print("1. YouTube")
            print("2. JioSaavn")
            choice = input("Enter 1 or 2: ").strip()
            if choice == "1":
                print("Bunny: Opening YouTube…")
                open_url("https://youtu.be/h7rpAUGwQ0g?si=Xa-k46q8b8og_A-F")
            elif choice == "2":
                print("Bunny: Opening JioSaavn…")
                open_url("https://www.jiosaavn.com")
            else:
                print("Bunny: Invalid choice!")
            continue

        if lower == "open instagram" or lower == "instagram kholo":
            print("Bunny: Opening Instagram...")
            open_url("https://www.instagram.com")
            continue

        if lower == "open snapchat" or lower == "snapchat kholo":
            print("Bunny: Opening Snapchat...")
            open_url("https://www.snapchat.com")
            continue

        if lower == "open facebook" or lower == "facebook kholo":
            print("Bunny: Opening Facebook...")
            open_url("https://www.facebook.com")
            continue

        if lower == "open whatsapp" or lower == "whatsapp kholo":
            print("Bunny: Opening WhatsApp Web...")
            open_url("https://web.whatsapp.com")
            continue

        # For any unmatched input, use AI to respond directly without thinking pause
        answer = ask_ai(user_input, messages)
        print(f"Bunny: {answer}")
        print()

if __name__ == "__main__":
    main()
