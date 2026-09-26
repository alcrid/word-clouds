import glob
import json
import os

import unidecode as uni

HERE = os.path.dirname(os.path.abspath(__file__))


# facebook exports save text in the wrong encoding so we have to fix it
# and we also strip the accents so "však" and "vsak" count as the same word
def fix_encoding(s):
    try:
        s = s.encode("iso-8859-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return uni.unidecode(s)


# finds every message_*.json in a facebook export
# accepts the export root, the messages/inbox folder or a single json file
def find_message_files(path):
    if os.path.isfile(path):
        return [path]
    return sorted(glob.glob(os.path.join(path, "**", "message_*.json"), recursive=True))


# returns all message text from the given json files as one lowercase string
def load_messenger_text(paths):
    words = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for message in data.get("messages", []):
            if "content" in message:
                words.append(fix_encoding(message["content"]).lower())
    return " ".join(words)


# one word per line, lines starting with # are comments
def load_word_list(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def load_stopwords(path=None):
    return set(load_word_list(path or os.path.join(HERE, "stopwords_sk.txt")))
