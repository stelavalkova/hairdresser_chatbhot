
import openai
import tkinter as tk
from tkinter import scrolledtext

# Set your OpenAI API key here
openai.api_key = "sk-your-api-key"

# Base system instruction
system_message = {
    "role": "system",
    "content": (
        "You are a professional haircare advisor. Ask users about their hair type, issues, and goals. "
        "Give friendly advice, and suggest 1-2 specific hair products when appropriate. "
        "Also respond to emotional tones if the user sounds happy, stressed, or upset."
    )
}

conversation = [system_message]

# Define simple mood detection logic (basic keyword-based)
def detect_mood(text):
    happy = ["happy", "excited", "great", "good", "awesome"]
    sad = ["sad", "upset", "depressed", "unhappy", "down"]
    angry = ["angry", "frustrated", "annoyed", "mad"]

    lower = text.lower()
    if any(word in lower for word in happy):
        return "😊 You sound happy today! Let's find great products to match your vibe!"
    elif any(word in lower for word in sad):
        return "💙 Sorry you're feeling down. Some haircare love might help!"
    elif any(word in lower for word in angry):
        return "😠 I hear your frustration! Let's fix this hair problem together."
    return None

# Chatbot logic with OpenAI API
def chat_with_bot(user_input):
    if len(user_input.strip()) < 5:
        return "Could you tell me a bit more about your hair type or issue?"

    # Add user's message
    conversation.append({"role": "user", "content": user_input})

    try:
        # Get OpenAI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        bot_reply = response['choices'][0]['message']['content']
        conversation.append({"role": "assistant", "content": bot_reply})

        # Add mood-based intro if detected
        mood_message = detect_mood(user_input)
        if mood_message:
            return mood_message + "\n\n" + bot_reply
        return bot_reply

    except openai.error.OpenAIError as e:
        return f"Error: {e}"

# ---------------- GUI Code ---------------- #

def send_message():
    user_input = input_box.get()
    if user_input.strip() == "":
        return

    chat_window.insert(tk.END, "You: " + user_input + "\n")
    input_box.delete(0, tk.END)

    response = chat_with_bot(user_input)
    chat_window.insert(tk.END, "Bot: " + response + "\n\n")
    chat_window.see(tk.END)

# Build GUI window
window = tk.Tk()
window.title("Haircare Advisor Chatbot 💬")
window.geometry("500x600")

chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=25, font=("Arial", 11))
chat_window.pack(padx=10, pady=10)

input_box = tk.Entry(window, width=60, font=("Arial", 11))
input_box.pack(padx=10, pady=(0, 5))
input_box.bind("<Return>", lambda event=None: send_message())

send_button = tk.Button(window, text="Send", command=send_message, font=("Arial", 11))
send_button.pack(pady=(0, 10))

# Start with greeting
chat_window.insert(tk.END, "Bot: Hello! I'm your personal haircare advisor \nTell me about your hair and what you want help with!\n\n")

window.mainloop()
