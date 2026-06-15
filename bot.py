import os
import nltk
from nltk.corpus import wordnet
from dotenv import load_dotenv
from bale import Bot

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")


nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))

def download_nltk_data():
    try:
        nltk.data.find('corpora/wordnet')
        print("✅ WordNet already downloaded.")
    except LookupError:
        print("📥 Downloading WordNet...")
        nltk.download('wordnet', quiet=True)
        print("✅ WordNet downloaded.")

download_nltk_data()


bot = Bot(token=BOT_TOKEN)

@bot.event
async def on_message(message):

    if not message.text:
        await bot.send_message(message.chat.id, "Just send your **English word**, Don't send photo, file, etc")
        return

    if message.from_user.is_bot:
        return

    chat_id = message.chat.id
    user_text = message.text.strip().lower()


    if user_text == "/start":
        await bot.send_message(chat_id, "Welcome! Send me any English word to get its definition.")
        return


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
            for i, definition in enumerate(def_list[:], start=1):
                lines.append(f"{i}. {definition}")
            lines.append("")

    response_text = "\n".join(lines).strip()

    # 6. Send formatted response
    await bot.send_message(
        chat_id, 
        response_text, 

    )

if __name__ == '__main__':
    print("Bot is starting...")
    bot.run()
