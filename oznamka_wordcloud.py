"""Word cloud for the class oznamka (graduation announcement).

Takes the class group chat, drops filler words and profanity, boosts every
classmate's name so the names stand out and fits it all into a mask image.
"""
import argparse
import random

import numpy as np
from PIL import Image
from wordcloud import WordCloud

from common import find_message_files, load_messenger_text, load_stopwords, load_word_list

# how many times each name gets added, bigger number = bigger names
NAME_BOOST = 550


def boost_names(text, names, boost=NAME_BOOST, seed=0):
    rng = random.Random(seed)
    extra = []
    for name in names:
        for _ in range(boost):
            # pair names randomly so wordcloud doesn't glue the same pairs together
            extra += [name, rng.choice(names), rng.choice(names)]
    return text + " " + " ".join(extra)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--messages", help="facebook export folder or a message_*.json of the group chat")
    source.add_argument("--text", help="plain text file with the chat (e.g. data/database.txt)")
    parser.add_argument("--names", default="names.txt", help="one name per line (default: names.txt)")
    parser.add_argument("--mask", help="mask image, words are drawn only in the non-white area")
    parser.add_argument("--out", default="wordclouds/oznamka.png")
    parser.add_argument("--colormap", default="Wistia", help="any matplotlib colormap")
    parser.add_argument("--background", default="#0a101e")
    parser.add_argument("--max-words", type=int, default=4500)
    parser.add_argument("--scale", type=float, default=5, help="output resolution multiplier")
    parser.add_argument("--repeat", action="store_true", help="repeat words until the mask is full (good for small chats)")
    parser.add_argument("--save-text", help="also dump the cleaned chat text to this file")
    args = parser.parse_args()

    if args.messages:
        text = load_messenger_text(find_message_files(args.messages))
    else:
        with open(args.text, "r", encoding="utf-8") as f:
            text = f.read().lower()

    if args.save_text:
        with open(args.save_text, "w", encoding="utf-8") as f:
            f.write(text)

    text = boost_names(text, load_word_list(args.names))
    mask = np.array(Image.open(args.mask).convert("L")) if args.mask else None

    wordcloud = WordCloud(
        max_words=args.max_words,
        scale=args.scale,
        mask=mask,
        stopwords=load_stopwords(),
        background_color=args.background,
        collocation_threshold=75,
        min_font_size=10,
        colormap=args.colormap,
        repeat=args.repeat,
        font_step=1,
    ).generate(text)

    wordcloud.to_file(args.out)
    print("saved", args.out)


if __name__ == "__main__":
    main()
