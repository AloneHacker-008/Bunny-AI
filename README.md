Bunny - Friendly AI Chatbot

Bunny is a friendly Python-based AI chatbot inspired by traditional C programs. It is designed to provide fun, interactive conversations, perform arithmetic, convert number systems, fetch time/date, access web links, and answer questions using OpenAI's GPT models. Bunny is perfect for learning AI integrations in Python while having an engaging chat companion.

Features:

Conversational AI: Chat naturally with Bunny using pre-defined responses.

OpenAI Integration: Ask questions and get AI-powered responses.

Arithmetic Operations: Add, subtract, multiply, divide multiple numbers.

Safe BODMAS Evaluation: Solve complex expressions safely.

Number System Conversion: Binary, Decimal, Octal, Hexadecimal.

Weather Lookup: Open browser to check weather in any city.

Quick Access to Websites: Google, YouTube, Instagram, Facebook, WhatsApp, Snapchat.

Random Fun Replies: Keeps conversations lively with funny and friendly messages.


Installation:

1. Clone the repository:

git clone https://github.com/AloneHacker-008/Bunny-AI.git
cd Bunny-AI


2. Create a virtual environment:

python -m venv venv

Activate the environment:

On Linux/Mac:

source venv/bin/activate

On Windows:

venv\Scripts\activate



3. Install required Python packages:

pip install -r requirements.txt


4. Set up OpenAI API key:

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here




Usage:

1. Run the chatbot:

python Bunny.py

Example Interaction:

Bunny: Hey! I'm Bunny - your AI Assistant
Bunny: Good morning! Hope your day starts great!
Type anything to chat with me (type 'bye' to exit)
For AI questions, type 'ai <question>'

You: hi
Bunny: Hey bestie! How's everything going?

You: how are you
Bunny: I'm feeling awesome today! How about you?


2. Ask AI Questions:

You: ai Who won the last football World Cup?
Bunny: Asking OpenAI...
AI: The last FIFA World Cup was won by Argentina in 2022.


3. Arithmetic Operations (multiple numbers):

You: sum 5 10 15
Bunny: Result = 30.00

You: multiply 2 3 4
Bunny: Result = 24.00


4. Evaluate Expressions (BODMAS):

You: 5 + (3 * 2)
Bunny: Result = 11.00


5. Number System Conversion:

You: convert
Bunny: 
Bunny: Number System Converter Menu
1. Binary to Decimal/Octal/Hexa
2. Decimal to Binary/Octal/Hexa
3. Octal to Decimal/Binary/Hexa
4. Hexadecimal to Decimal/Binary/Octal
Enter your choice: 1
Enter Binary: 1010
Decimal: 10
Octal: 12
Hexa: A


6. Weather Lookup:

You: weather
Bunny: Please enter your city name: New Delhi
Bunny: Fetching weather for New Delhi...

(Opens browser with weather info)


7. Open Websites:

You: open youtube
Bunny: Opening YouTube...

(Browser opens YouTube)


8. Play Music:

You: play music
Bunny: Music time! Choose:
1. YouTube
2. JioSaavn
Enter 1 or 2: 1
Bunny: Opening YouTube...


9. Motivation / Fun Chat / Greetings:

You: motivate me
Bunny: You're stronger than you think. Keep going — success is near!

You: i am sad
Bunny: Oh no — Don't worry, everything will be okay. I'm here for you


10. Exit the Chat:

You: bye
Bunny: Aww, you're leaving already? Take care, my friend!




Creator:
Anup Prasad – Python enthusiast and AI developer.
GitHub: https://github.com/AloneHacker-008
