import os
import nltk
from nltk.corpus import wordnet
from bale import Bot, Update

# Configuration
BOT_TOKEN = "YOUR_BALE_BOT_TOKEN_HERE"
bot = Bot(token=BOT_TOKEN)

# Setup NLTK data path
nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))

def download_nltk_data():
    try:
        nltk.data.find('corpora/wordnet')
        print("WordNet corpus already downloaded.")
    except LookupError:
        print("WordNet corpus not found. Downloading...")
        nltk.download('wordnet', quiet=True)
        print("WordNet corpus downloaded successfully.")

download_nltk_data()

@bot.event
async def on_message(message):
    # 1. Ignore messages that are not text
    if not message.text:
        return

    # 2. Prevent the bot from processing its own messages
    # (Check if the sender is the bot itself)
    if message.from_user.is_bot:
        return

    chat_id = message.chat.id
    user_text = message.text.strip().lower()

    # 3. Simple Command Handler
    if user_text == "/start":
        await bot.send_message(chat_id, "Welcome! Send me any English word to get its definition.")
        return

    # 4. Search WordNet
    try:
        synsets = wordnet.synsets(user_text)
    except Exception as e:
        print(f"Error: {e}")
        return

    if not synsets:
        await bot.send_message(chat_id, f"Sorry, I couldn't find a definition for '{user_text}'.")
        return

    # 5. Format Definitions (Following your requested structure)
    definitions_dict = {}
    for syn in synsets:
        pos = syn.pos()
        definition = syn.definition()
        if pos not in definitions_dict:
            definitions_dict[pos] = []
        if definition not in definitions_dict[pos]:
            definitions_dict[pos].append(definition)

    pos_map = {
        'n': 'Noun',
        'v': 'Verb',
        'a': 'Adjective',
        'r': 'Adverb',
        's': 'Adjective Satellite'
    }

    # Build the message lines
    lines = [f"📖 *Word:* {user_text}", ""]
    
    for pos, def_list in definitions_dict.items():
        if def_list:
            display_pos = pos_map.get(pos, pos.upper())
            lines.append(f"*{display_pos}:*")
            for i, definition in enumerate(def_list[:3], start=1):
                lines.append(f"{i}. {definition}")
            lines.append("")

    response_text = "\n".join(lines).strip()

    # 6. Send formatted response
    await bot.send_message(
        chat_id, 
        response_text, 
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    print("Bot is starting...")
    bot.run()
