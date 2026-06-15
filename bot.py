import os
import nltk
from nltk.corpus import wordnet
from dotenv import load_dotenv
from bale import Bot

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")

# Setup NLTK data path
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)
nltk.data.path.append(nltk_data_path)

def download_nltk_data():
    try:
        nltk.data.find('corpora/wordnet')
        print("WordNet already downloaded.")
    except LookupError:
        print("Downloading WordNet...")
        nltk.download('wordnet', download_dir=nltk_data_path)
        print("WordNet downloaded.")

download_nltk_data()

bot = Bot(token=BOT_TOKEN)

@bot.event
async def on_message(message):
    try:
        # Handle non-text messages
        if not message.text:
            print(f"Received non-text message from chat_id={message.chat.id}")
            await bot.send_message(message.chat.id, "I can only process text messages. Please send me an English word.")
            return

        user_text = message.text.strip().lower()
        chat_id = message.chat.id
        print(f"Received text: {user_text}")

        if user_text == "/start":
            await bot.send_message(chat_id, "Welcome! Please send me a word to get its definition.")
            return

        # Search WordNet
        synsets = wordnet.synsets(user_text)
        if not synsets:
            await bot.send_message(chat_id, f"Sorry, I couldn't find a definition for '{user_text}'.")
            return

        # Grouping definitions
        definitions_dict = {}
        pos_map = {"n": "Noun", "v": "Verb", "a": "Adjective", "r": "Adverb", "s": "Adjective Satellite"}
        
        for syn in synsets:
            pos = syn.pos()
            label = pos_map.get(pos, "Other")
            if label not in definitions_dict:
                definitions_dict[label] = []
            definitions_dict[label].append(syn.definition())

        # Build response
        response_text = f"📖 Word: {user_text}\n\n"
        for pos, defs in definitions_dict.items():
            response_text += f"[{pos}]:\n"
            for i, definition in enumerate(defs[:3], 1): # Limit to 3 per POS
                response_text += f"{i}. {definition}\n"
            response_text += "\n"

        # Safe sending with 400 error protection
        final_msg = response_text.strip()
        if len(final_msg) > 4000:
            final_msg = final_msg[:3990] + "\n\n... (Message truncated)"

        if final_msg:
            try:
                await bot.send_message(chat_id=chat_id, text=final_msg)
            except Exception as e:
                print(f"Failed to send message to {chat_id}: {e}")
                
    except Exception as e:
        print(f"Unexpected error: {e}")
        try:
            await bot.send_message(message.chat.id, "An internal error occurred.")
        except:
            pass

if __name__ == "__main__":
    print("Bot is starting...")
    print("Send /start, then type any word.")
    bot.run()