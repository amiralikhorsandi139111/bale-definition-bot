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
    if not hasattr(message, "text") or not message.text:
        return
    
    chat_id = message.chat.id
    user_text = message.text.strip().lower()
    
    print(f"📩 Received: {user_text}")
    

    if user_text == "/start":
        await bot.send_message(
            chat_id=chat_id,
            text="Welcome! Please send me a word to get its definition."
        )
        return
    

    try:
        synsets = wordnet.synsets(user_text)
    except Exception as e:
        print(f"Error during synset lookup for '{user_text}': {e}")
        await bot.send_message(
            chat_id=chat_id,
            text="An internal error occurred."
        )
        return
    

    if not synsets:
        error_msg = f"Sorry, I couldn't find a definition for '{user_text}'."
        await bot.send_message(
            chat_id=chat_id,
            text=error_msg
        )
        return
    

    definitions_dict = {}
    for syn in synsets:
        pos = syn.pos()
        definition = syn.definition()
        if pos not in definitions_dict:
            definitions_dict[pos] = []
        if definition not in definitions_dict[pos]:
            definitions_dict[pos].append(definition)
    

    response_text = f"📖 Word: {user_text}\n\n"
    definitions_found = False
    pos_map = {'n': 'Noun', 'v': 'Verb', 'a': 'Adjective', 'r': 'Adverb', 's': 'Adjective Satellite'}

    for pos, def_list in definitions_dict.items():
        if def_list:
            definitions_found = True
            display_pos = pos_map.get(pos, pos.upper()).replace(" ", "")
            
            response_text += f"{display_pos}:\n"
            for i, definition in enumerate(def_list[:]):
                response_text += f"{i+1}. {definition}\n"
            response_text += "\n"
    
    if not definitions_found:
        await bot.send_message(
            chat_id=chat_id,
            text=f"Sorry, I couldn't find any definitions for '{user_text}'."
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=response_text
        )




if __name__ == "__main__":
    print("=" * 40)
    print("🤖 Bot is starting...")
    print("Send /start then type any word")
    print("=" * 40)
    bot.run()
# import os
# import nltk
# from nltk.corpus import wordnet
# from dotenv import load_dotenv
# from bale import Bot

# # Load environment variables
# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# if not BOT_TOKEN:
#     raise ValueError("❌ BOT_TOKEN not found in .env file")

# # Setup NLTK data path
# nltk_path = os.path.join(os.getcwd(), "nltk_data")
# os.makedirs(nltk_path, exist_ok=True)
# nltk.data.path.append(nltk_path)

# def setup_nltk():
#     """Downloads WordNet data if not already present."""
#     try:
#         nltk.data.find('corpora/wordnet')
#         print("✅ WordNet already downloaded.")
#     except LookupError:
#         print("📥 Downloading WordNet...")
#         # Ensure quiet=True for cleaner output during download
#         nltk.download('wordnet', download_dir=nltk_path, quiet=True)
#         print("✅ WordNet downloaded.")

# setup_nltk()

# bot = Bot(token=BOT_TOKEN)

# @bot.event
# async def on_message(message):
#     """Handles incoming messages from users."""
#     # Ignore messages without text content or empty messages
#     if not hasattr(message, "text") or not message.text:
#         return

#     chat_id = message.chat.id
#     user_text = message.text.strip().lower()

#     # Handle the /start command
#     if user_text == "/start":
#         await bot.send_message(
#             chat_id=chat_id,
#             text="Welcome! Please send me an English word to get its definitions."
#         )
#         return

#     # Fetch synsets from WordNet
#     try:
#         synsets = wordnet.synsets(user_text)
#     except Exception as e:
#         print(f"Error during synset lookup for '{user_text}': {e}")
#         await bot.send_message(chat_id=chat_id, text="An internal error occurred while processing your request.")
#         return

#     # If no synsets are found, inform the user
#     if not synsets:
#         await bot.send_message(
#             chat_id=chat_id,
#             text=f"Sorry, I couldn't find any definitions for the word '{user_text}'."
#         )
#         return

#     # Process definitions and group them by part of speech
#     definitions_dict = {}
#     # Mapping for displaying parts of speech in a user-friendly way
#     pos_map = {
#         'n': 'Noun',
#         'v': 'Verb',
#         'a': 'Adjective',
#         'r': 'Adverb',
#         's': 'Adjective Satellite'
#     }

#     for syn in synsets:
#         pos = syn.pos()
#         definition = syn.definition()
#         if pos not in definitions_dict:
#             definitions_dict[pos] = []
#         # Add definition only if it's not already listed for this part of speech
#         if definition not in definitions_dict[pos]:
#             definitions_dict[pos].append(definition)

#     # Construct the response message
#     response_text = f"📖 Word: `{user_text}`\n\n"

#     # Iterate through collected definitions and format the output
#     for pos, def_list in definitions_dict.items():
#         display_pos = pos_map.get(pos, pos.upper()) # Use mapped name or uppercase if not found
#         response_text += f"🔹 *{display_pos}:*\n"
#         for i, definition in enumerate(def_list, 1):
#             response_text += f"{i}. {definition}\n"
#         response_text += "\n"

#     # Send the final response to the user
#     await bot.send_message(chat_id=chat_id, text=response_text, parse_mode="Markdown")

# if __name__ == "__main__":
#     print("=" * 40)
#     print("🤖 Bot is starting...")
#     print("Send /start then type any English word.")
#     print("=" * 40)
#     bot.run()