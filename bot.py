# import os
# import nltk
# from nltk.corpus import wordnet
# from dotenv import load_dotenv
# from bale import Bot

# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN not found in .env file")


# nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))

# def download_nltk_data():
#     try:
#         nltk.data.find('corpora/wordnet')
#         print("✅ WordNet already downloaded.")
#     except LookupError:
#         print("📥 Downloading WordNet...")
#         nltk.download('wordnet', quiet=True)
#         print("✅ WordNet downloaded.")

# download_nltk_data()


# bot = Bot(token=BOT_TOKEN)


# @bot.event
# async def on_message(message):
#     if not hasattr(message, "text") or not message.text:
#         return
    
#     chat_id = message.chat.id
#     user_text = message.text.strip().lower()
    
#     print(f"📩 Received: {user_text}")
    

#     if user_text == "/start":
#         await bot.send_message(
#             chat_id=chat_id,
#             text="Welcome! Please send me a word to get its definition."
#         )
#         return
    

#     try:
#         synsets = wordnet.synsets(user_text)
#     except Exception as e:
#         print(f"Error during synset lookup for '{user_text}': {e}")
#         await bot.send_message(
#             chat_id=chat_id,
#             text="An internal error occurred."
#         )
#         return
    

#     if not synsets:
#         error_msg = f"Sorry, I couldn't find a definition for '{user_text}'."
#         await bot.send_message(
#             chat_id=chat_id,
#             text=error_msg
#         )
#         return
    

#     definitions_dict = {}
#     for syn in synsets:
#         pos = syn.pos()
#         definition = syn.definition()
#         if pos not in definitions_dict:
#             definitions_dict[pos] = []
#         if definition not in definitions_dict[pos]:
#             definitions_dict[pos].append(definition)
    

#     response_text = f"📖 Word: {user_text}\n\n"
#     definitions_found = False
#     pos_map = {'n': 'Noun', 'v': 'Verb', 'a': 'Adjective', 'r': 'Adverb', 's': 'Synonym'}
    
#     for pos, def_list in definitions_dict.items():
#         if def_list:
#             definitions_found = True
#             display_pos = pos_map.get(pos, pos.upper())
            
#             response_text += f"{display_pos}:\n"
#             for i, definition in enumerate(def_list[:3]):
#                 response_text += f"{i+1}. {definition}\n"
#             response_text += "\n"
    
#     if not definitions_found:
#         await bot.send_message(
#             chat_id=chat_id,
#             text=f"Sorry, I couldn't find any definitions for '{user_text}'."
#         )
#     else:
#         await bot.send_message(
#             chat_id=chat_id,
#             text=response_text
#         )




# if __name__ == "__main__":
#     print("=" * 40)
#     print("🤖 Bot is starting...")
#     print("Send /start then type any word")
#     print("=" * 40)
#     bot.run()
import os
import nltk
from nltk.corpus import wordnet
from dotenv import load_dotenv
from bale import Bot

# تنظیمات اولیه
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not found in .env file")

# تنظیم مسیر داده‌های NLTK
nltk_path = os.path.join(os.getcwd(), 'nltk_data')
if not os.path.exists(nltk_path):
    os.makedirs(nltk_path)
nltk.data.path.append(nltk_path)

def setup_nltk():
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("📥 Downloading WordNet...")
        nltk.download('wordnet', download_dir=nltk_path, quiet=True)
        print("✅ WordNet downloaded.")

setup_nltk()

bot = Bot(token=BOT_TOKEN)

@bot.event
async def on_message(message):
    if not hasattr(message, "text") or not message.text:
        return

    chat_id = message.chat.id
    user_text = message.text.strip().lower()

    if user_text == "/start":
        await bot.send_message(chat_id, "سلام! کلمه‌ای انگلیسی بفرست تا تعریفش رو برات پیدا کنم.")
        return

    # جستجوی کلمه
    synsets = wordnet.synsets(user_text)
    
    if not synsets:
        await bot.send_message(chat_id, f"متأسفم، تعریفی برای کلمه '{user_text}' پیدا نشد.")
        return

    # گروه‌بندی و حذف تکراری‌ها
    definitions_dict = {}
    pos_map = {'n': 'اسم (Noun)', 'v': 'فعل (Verb)', 'a': 'صفت (Adjective)', 'r': 'قید (Adverb)', 's': 'صفت (Adjective Satellite)'}
    
    for syn in synsets:
        pos = syn.pos()
        definition = syn.definition()
        if pos not in definitions_dict:
            definitions_dict[pos] = set() # استفاده از set برای حذف تکرار
        definitions_dict[pos].add(definition)

    # ساخت پیام خروجی
    response = f"📖 **کلمه:** `{user_text}`\n\n"
    for pos, defs in definitions_dict.items():
        label = pos_map.get(pos, pos.upper())
        response += f"🔹 *{label}:*\n"
        for i, definition in enumerate(list(defs)[:3], 1): # حداکثر 3 تعریف برای هر نوع
            response += f"{i}. {definition}\n"
        response += "\n"

    await bot.send_message(chat_id, response, parse_mode="Markdown")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.run()