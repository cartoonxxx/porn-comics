import os, shutil
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

FOLDER_1  = "1-prev"   # фото с подписью = имя файла
FOLDER_AD = "2-lend"   # рекламные фото для каждого 6-го поста
FOLDER_2  = "prel"     # фото без подписи для канала 2

TARGET_1 = "https://t.me/porno_grafika"
TARGET_2 = "https://t.me/onlypornai"

AD_TEXT = ("🔥🔥🔥 MORE HOT, FREE PREMIUM CONTENT HERE (https://t.me/onlypornai) 🔥🔥🔥\n"
           "🔥🔥🔥 MORE HOT, FREE PREMIUM CONTENT HERE (https://t.me/onlypornai) 🔥🔥🔥\n"
           "🔥🔥🔥 MORE HOT, FREE PREMIUM CONTENT HERE (https://t.me/onlypornai) 🔥🔥🔥")

EXTS = (".jpg", ".jpeg", ".png", ".webp")
STATE = "state.txt"
COUNTER_DIGIT = "counter.txt"

def take_photo(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(EXTS)]
    if not files:
        return None
    src = os.path.join(folder, files[0])
    dst = os.path.join("done", folder, files[0])
    return src, dst

def read_int(path, default):
    try:
        return int(open(path).read().strip())
    except Exception:
        return default

tick = read_int(STATE, 0) + 1
open(STATE, "w").write(str(tick))

client = TelegramClient(StringSession(os.environ["TG_SESSION"]),
                        int(os.environ["API_ID"]), os.environ["API_HASH"])

with client:
    # ---------- канал 1 ----------
    if tick % 6 == 0:
        p = take_photo(FOLDER_AD)
        if p:
            src, dst = p
            client.send_file(TARGET_1, src, caption=AD_TEXT, force_document=False)
            shutil.move(src, dst)
            print("Канал 1: рекламный пост")
        else:
            client.send_message(TARGET_1, AD_TEXT)
            print("Канал 1: только текст (2-lend пуста)")
    else:
        p = take_photo(FOLDER_1)
        if p:
            src, dst = p
            caption = os.path.splitext(os.path.basename(src))[0]
            client.send_file(TARGET_1, src, caption=caption, force_document=False)
            shutil.move(src, dst)
            print(f"Канал 1: {os.path.basename(src)}")
        else:
            print("Канал 1: папка 1-prev пуста")

    # ---------- канал 2 ----------
    if tick % 6 == 0:
        counter = read_int(COUNTER_DIGIT, 0) + 1
        digit = (counter - 1) % 6 + 1
        client.send_message(TARGET_2, str(digit))
        open(COUNTER_DIGIT, "w").write(str(counter))
        print(f"Канал 2: цифра {digit}")
    else:
        p = take_photo(FOLDER_2)
        if p:
            src, dst = p
            client.send_file(TARGET_2, src, force_document=False)
            shutil.move(src, dst)
            print(f"Канал 2: {os.path.basename(src)}")
        else:
            print("Канал 2: папка prel пуста")
