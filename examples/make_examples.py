"""Builds the demo images in this folder from made-up data.

No real chats are used: it writes a fake facebook export (with the same broken
encoding facebook uses) and a "4.SA" mask, then runs both scripts on them.

    python examples/make_examples.py
"""
import json
import os
import random
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# made-up chat vocabulary with rough frequencies
CHAT_WORDS = {
    "zajtra": 90, "neviem": 85, "sak": 80, "teraz": 70, "bude": 65, "nic": 60,
    "xd": 60, "ok": 55, "dobre": 50, "potom": 45, "ideme": 40, "treba": 40,
    "pisomka": 38, "matika": 35, "ucitel": 30, "ulohy": 30, "prestavka": 28,
    "edupage": 26, "rozvrh": 25, "obed": 24, "jedalen": 22, "telocvik": 22,
    "fyzika": 20, "projekt": 20, "prezentacia": 18, "lmao": 18, "okej": 18,
    "vsetko": 16, "niekto": 16, "poznamky": 15, "suplovanie": 14, "vylet": 14,
    "maturita": 14, "stuzkova": 13, "hodina": 12, "trieda": 12, "skola": 12,
    "cvicenie": 10, "domaca": 10, "odovzdat": 10, "termin": 9, "prosim": 9,
    "dakujem": 9, "chemia": 8, "dejepis": 8, "anglictina": 8, "kniznica": 6,
}

FAKE_NAMES = os.path.join(ROOT, "names.example.txt")


def fake_sentences(n, rng):
    words, weights = zip(*CHAT_WORDS.items())
    return [" ".join(rng.choices(words, weights, k=rng.randint(3, 9))) for _ in range(n)]


def write_fake_export(folder, rng):
    inbox = os.path.join(folder, "messages", "inbox")
    for chat in ("trieda_4sa", "projekt_team"):
        os.makedirs(os.path.join(inbox, chat))
        messages = [
            # facebook stores utf-8 text decoded as latin-1, recreate that here
            {"sender_name": "Demo", "content": s.encode("utf-8").decode("latin-1")}
            for s in fake_sentences(1500, rng) + ["však už je piatok", "čo máme zajtra"] * 40
        ]
        with open(os.path.join(inbox, chat, "message_1.json"), "w", encoding="utf-8") as f:
            json.dump({"messages": messages}, f)


def find_bold_font():
    for path in (
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
    ):
        if os.path.exists(path):
            return path
    return None


# black "4.SA" on white, wordcloud fills only the black part
def write_class_mask(path, text="4.SA"):
    img = Image.new("L", (1600, 700), 255)
    draw = ImageDraw.Draw(img)
    font_path = find_bold_font()
    font = ImageFont.truetype(font_path, 560) if font_path else ImageFont.load_default()
    box = draw.textbbox((0, 0), text, font=font)
    x = (img.width - (box[2] - box[0])) // 2 - box[0]
    y = (img.height - (box[3] - box[1])) // 2 - box[1]
    draw.text((x, y), text, fill=0, font=font)
    img.save(path)


def run(*args):
    print("$ python", " ".join(args))
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main():
    rng = random.Random(4)
    with tempfile.TemporaryDirectory() as tmp:
        write_fake_export(tmp, rng)
        mask = os.path.join(tmp, "4sa_mask.png")
        write_class_mask(mask)
        out = lambda name: os.path.join(HERE, name)

        run("messenger_wordcloud.py", tmp, "--out", out("messenger.png"))
        run("messenger_wordcloud.py", tmp, "--out", out("messenger_light.png"),
            "--background", "white", "--colormap", "plasma")
        run("oznamka_wordcloud.py", "--messages", tmp, "--names", FAKE_NAMES,
            "--mask", mask, "--scale", "1.5", "--max-words", "1500", "--repeat", "--out", out("oznamka_4sa.png"))
        run("oznamka_wordcloud.py", "--messages", tmp, "--names", FAKE_NAMES,
            "--mask", mask, "--scale", "1.5", "--max-words", "1500", "--repeat", "--colormap", "cool",
            "--background", "black", "--out", out("oznamka_4sa_cool.png"))


if __name__ == "__main__":
    main()
